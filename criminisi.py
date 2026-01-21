import numpy as np
import cv2 as cv
from PIL import Image

def gets_normals(front_mask):
    gx = cv.Sobel(front_mask.astype(np.float32), cv.CV_32F, 1, 0)
    gy = cv.Sobel(front_mask.astype(np.float32), cv.CV_32F, 0, 1)
    normal = np.sqrt(gx**2 + gy**2) + 1e-6
    return gx / normal, gy / normal

def find_best_ssd(img, mask, target_px, radius):
    h, w, _ = img.shape
    px, py = target_px
    
    y1, y2 = max(0, py - radius), min(h, py + radius + 1)
    x1, x2 = max(0, px - radius), min(w, px + radius + 1)
    
    patch_target = img[y1:y2, x1:x2].astype(np.float32)
    patch_mask = (1 - mask[y1:y2, x1:x2]).astype(np.float32)
    
    if np.sum(patch_mask) == 0:
        return (px, py)

    res = cv.matchTemplate(img.astype(np.float32), patch_target, cv.TM_SQDIFF, mask=patch_mask)
    
    #Blokada wybierania tego samego miejsca
    res_h, res_w = res.shape
    safe_r = radius + 1
    
    ry_start = max(0, (py - radius) - safe_r)
    ry_end = min(res_h, (py - radius) + safe_r + 1)
    rx_start = max(0, (px - radius) - safe_r)
    rx_end = min(res_w, (px - radius) + safe_r + 1)
    
    #Ignoruje obszar obok dziury
    if ry_start < ry_end and rx_start < rx_end:
        res[ry_start:ry_end, rx_start:rx_end] = np.inf

    min_val, _, min_loc, _ = cv.minMaxLoc(res)
    
    best_x, best_y = min_loc
    new_y = py - y1
    new_x = px - x1
    
    return (best_x + new_x, best_y + new_y)

def update_image_and_confidence(img, mask, confidence, target_px, source_px, radius, c_val):
    h, w, _ = img.shape
    px, py = target_px
    sx, sy = source_px
    
    ty1, ty2 = max(0, py - radius), min(h, py + radius + 1)
    tx1, tx2 = max(0, px - radius), min(w, px + radius + 1)
    
    h_patch = ty2 - ty1
    w_patch = tx2 - tx1

    offset_y = ty1 - py
    offset_x = tx1 - px
    
    sy1 = sy + offset_y
    sx1 = sx + offset_x
    sy2 = sy1 + h_patch
    sx2 = sx1 + w_patch
    
    if sy1 < 0 or sx1 < 0 or sy2 > h or sx2 > w:
        return 

    target_mask_patch = mask[ty1:ty2, tx1:tx2]
    to_update = target_mask_patch > 0
    
    if not np.any(to_update):
        return

    img_crop = img[ty1:ty2, tx1:tx2]
    src_crop = img[sy1:sy2, sx1:sx2]
    
    img_crop[to_update] = src_crop[to_update]
    conf_crop = confidence[ty1:ty2, tx1:tx2]
    conf_crop[to_update] = c_val
    mask_crop = mask[ty1:ty2, tx1:tx2]
    mask_crop[to_update] = 0

def criminisi_inpaint(img, mask, patch_radius=4):

    img = np.array(img).astype(np.float32)
    mask = np.array(mask)
    if mask.ndim == 3: mask = mask[:,:,0]
    

    mask = (mask > 127).astype(np.uint8)

    confidence = (1 - mask).astype(np.float32)
    
    h, w, c = img.shape
    max_iters = h * w
    
    for i in range(max_iters):
        conturs, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        if not conturs:
            break
        
        front_pixels = np.vstack(conturs).squeeze()
        if front_pixels.ndim == 1: front_pixels = front_pixels[np.newaxis, :]
        
        nx, ny = gets_normals(mask)
        
        priorities = []
        c_terms = []
        
        gray = cv.cvtColor(img.astype(np.uint8), cv.COLOR_RGB2GRAY).astype(np.float32)
        grad_x = cv.Sobel(gray, cv.CV_32F, 1, 0)
        grad_y = cv.Sobel(gray, cv.CV_32F, 0, 1)
        
        for px, py in front_pixels:
            y1, y2 = max(0, py - patch_radius), min(h, py + patch_radius + 1)
            x1, x2 = max(0, px - patch_radius), min(w, px + patch_radius + 1)
            
            patch_conf = confidence[y1:y2, x1:x2]
            
            area = (y2-y1)*(x2-x1)
            if area == 0: 
                C_term = 0
            else:
                C_term = np.sum(patch_conf) / area

            safe_px = min(w-1, max(0, px))
            safe_py = min(h-1, max(0, py))
            
            vec_iso = np.array([-grad_y[safe_py, safe_px], grad_x[safe_py, safe_px]])
            vec_norm = np.array([nx[safe_py, safe_px], ny[safe_py, safe_px]])
            
            D_term = np.abs(np.dot(vec_iso, vec_norm)) / 255.0
            
            priorities.append(C_term * D_term)
            c_terms.append(C_term)
            
        if not priorities: break 
        
        best_idx = np.argmax(priorities)
        target_point = front_pixels[best_idx]
        px, py = target_point
        best_c = c_terms[best_idx]
        
        best_patch_coords = find_best_ssd(img, mask, (px, py), patch_radius)
        update_image_and_confidence(img, mask, confidence, (px, py), best_patch_coords, patch_radius, best_c)
        
    return Image.fromarray(img.astype(np.uint8))
