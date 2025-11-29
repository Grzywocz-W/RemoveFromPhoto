import numpy as np
from PIL import Image
import cv2 as cv
from scipy import ndimage

def analyze_mask_complexity(mask):

    mask_np = np.array(mask)
    total_pixels = mask_np.size
    mask_pixels = np.sum(mask_np > 0)
    
    if mask_pixels == 0:
        return None
    
    #Powierzchnia względna
    area_ratio = mask_pixels / total_pixels
    
    #Liczba oddzielnych regionów
    labeled, num_holes = ndimage.label(mask_np > 0)
    
    #Oblicz obwód
    kernel = np.ones((3, 3), np.uint8)
    eroded = cv.erode(mask_np, kernel, iterations=1)
    perimeter = np.sum((mask_np > 0) & (eroded == 0))
    perimeter_ratio = perimeter / mask_pixels if mask_pixels > 0 else 0
    
    #Rozmiary dziur
    hole_sizes = []
    for i in range(1, num_holes + 1):
        hole_size = np.sum(labeled == i)
        hole_sizes.append(hole_size)
    
    avg_hole_size = np.mean(hole_sizes) if hole_sizes else 0
    max_hole_size = max(hole_sizes) if hole_sizes else 0
    
    #Czy dotyka krawędzi
    h, w = mask_np.shape
    edges = np.concatenate([
        mask_np[0, :],
        mask_np[-1, :],
        mask_np[:, 0],
        mask_np[:, -1]
    ])
    is_edge_touching = np.any(edges > 0)
    
    return {
        'area_ratio': area_ratio,
        'holes_count': num_holes,
        'perimeter_ratio': perimeter_ratio,
        'avg_hole_size': avg_hole_size,
        'max_hole_size': max_hole_size,
        'is_edge_touching': is_edge_touching,
        'total_mask_pixels': mask_pixels
    }


def select_best_inpainting_method(mask):
    metrics = analyze_mask_complexity(mask)
    
    if metrics is None:
        return 'neighbor'
    
    area = metrics['area_ratio']
    holes = metrics['holes_count']
    perimeter = metrics['perimeter_ratio']
    max_size = metrics['max_hole_size']
    edge_touch = metrics['is_edge_touching']
    
    
    #1.Bardzo małe obszary
    if area < 0.01:
        return 'neighbor'
    
    #2.Duże, złożone obszary
    if area > 0.15:
        return 'criminisi'
    
    #3.Wiele małych dziur
    if holes > 5 and max_size < 1000:
        return 'neighbor'
    
    #4.Skomplikowany kształt
    #Criminisi lepiej radzi sobie z teksturami
    if perimeter > 0.3:
        return 'criminisi'
    
    #5.Średnie obszary z prostym kształtem
    if 0.01 <= area <= 0.15 and perimeter <= 0.3:
        return 'telea'
    
    #6.Dotyka krawędzi
    if edge_touch and area < 0.1:
        return 'telea'
    
    #Telea wygląda nalepiej
    return 'telea'


def auto_inpaint(img, mask, neighbor_func=None, telea_func=None, criminisi_func=None):

    method = select_best_inpainting_method(mask)
    ###DEBUGGING####
    print(f"Auto-wybór metody: {method.upper()}")
    
    if method == 'neighbor':
        if neighbor_func:
            return neighbor_func(img.copy(), mask)
        from helpers import neighbor_inpaint
        return neighbor_inpaint(img.copy(), mask)
    elif method == 'telea':
        if telea_func:
            return telea_func(img.copy(), mask)
        from helpers import telea_inpaint
        return telea_inpaint(img.copy(), mask)
    elif method == 'criminisi':
        if criminisi_func:
            return criminisi_func(img.copy(), mask)
        from criminisi import criminisi_inpaint
        return criminisi_inpaint(img.copy(), mask)
    
    return img.copy()


def auto_inpaint_with_info(img, mask):
    metrics = analyze_mask_complexity(mask)
    method = select_best_inpainting_method(mask)
    
    
    result = auto_inpaint(img, mask)
    return result, method, metrics
