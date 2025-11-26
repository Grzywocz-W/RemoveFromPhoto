import io
import base64
from datetime import datetime
from PIL import Image, ImageDraw
import numpy as np
import cv2 as cv
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush, QImage, QPainter, QCursor
from PyQt5.QtCore import Qt
from criminisi import criminisi_inpaint

#===stałe===#
COLORS = {
    "status_idle": "#FFFF00",
    "status_done": "#00AA00",
    "status_processing": "#FF4500",
    "brush_cursor": "#00AA00",
    "toolbar_gradient_start": "#000000",
    "toolbar_gradient_end": "#FFD700"
}

#===Funckje pomocnicze===#
def pil_to_base64(img_pil, fmt="PNG"):
    buf = io.BytesIO()
    img_pil.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def bytes_to_pil_image(data: bytes, mode: str = "RGB"):
    """Konwertuje surowe bajty obrazu (np. pliki PNG/JPEG) na obiekt PIL.Image.

    Zwraca obiekt PIL.Image w żądanym trybie (domyślnie RGB).
    """
    if data is None:
        raise ValueError("No data provided")
    img = Image.open(io.BytesIO(data)).convert(mode)
    return img


def bytes_to_mask_image(data: bytes):
    """Konwertuje surowe bajty na maskę w skali szarości (tryb 'L')."""
    if data is None:
        raise ValueError("No mask data provided")
    img = Image.open(io.BytesIO(data)).convert("L")
    return img

def base64_to_pil(b64str):
    data = base64.b64decode(b64str)
    return Image.open(io.BytesIO(data)).convert("RGB")

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def pil_to_qimage(pil_img):
    if pil_img.mode == "RGB":
        data = pil_img.tobytes("raw", "RGB")
        qimg = QImage(data, pil_img.width, pil_img.height, pil_img.width * 3, QImage.Format_RGB888)
    elif pil_img.mode == "RGBA":
        data = pil_img.tobytes("raw", "RGBA")
        qimg = QImage(data, pil_img.width, pil_img.height, pil_img.width * 4, QImage.Format_RGBA8888)
    else:
        pil_img = pil_img.convert("RGBA")
        data = pil_img.tobytes("raw", "RGBA")
        qimg = QImage(data, pil_img.width, pil_img.height, pil_img.width * 4, QImage.Format_RGBA8888)
    return qimg

def draw_image(self):
    if not self.image:
        return
    size = (int(self.image.width * self.scale_factor), int(self.image.height * self.scale_factor))
    img = self.image.copy().resize(size, Image.Resampling.LANCZOS)
    if self.mask:
        m = self.mask.resize(size, Image.Resampling.NEAREST)
        overlay = Image.new("RGBA", size, (0, 0, 0, 0))
        mask_np = np.array(m)
        overlay_np = np.array(overlay)
        overlay_np[mask_np > 0] = [255, 0, 0, 70]
        overlay = Image.fromarray(overlay_np)
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    qimg = pil_to_qimage(img)
    pixmap = QPixmap.fromImage(qimg)
    self.pixmap_item.setPixmap(pixmap)
    self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
    for line in self.lasso_lines:
        self.scene.removeItem(line)
    self.lasso_lines.clear()

def create_brush_cursor(self):
    size = self.brush_slider.value()
    cursor_size = max(size + 4, 16)
    pixmap = QPixmap(cursor_size, cursor_size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    pen = QPen(QColor(COLORS["brush_cursor"]), 2)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)
    center = cursor_size // 2
    radius = size // 2
    painter.drawEllipse(center - radius, center - radius, size, size)
    painter.setPen(QPen(QColor(COLORS["brush_cursor"]), 1))
    cross_size = 3
    painter.drawLine(center - cross_size, center, center + cross_size, center)
    painter.drawLine(center, center - cross_size, center, center + cross_size)
    painter.end()
    return QCursor(pixmap, center, center)

def update_brush_mask(self, x, y, update_display=False):
    r = self.brush_slider.value() // 2
    draw = ImageDraw.Draw(self.mask)
    if not self.last_brush_pos:
        draw.ellipse((x-r, y-r, x+r, y+r), fill=255)
        self.last_brush_pos = (x, y)
        if update_display:
            update_brush_display(self)
        return
    prev_x, prev_y = self.last_brush_pos
    dx = x - prev_x
    dy = y - prev_y
    distance = (dx**2 + dy**2)**0.5
    if distance < 1:
        draw.ellipse((x-r, y-r, x+r, y+r), fill=255)
    else:
        steps = max(int(distance), 1)
        for i in range(steps + 1):
            t = i / steps
            ix = prev_x + dx * t
            iy = prev_y + dy * t
            draw.ellipse((ix-r, iy-r, ix+r, iy+r), fill=255)
    self.last_brush_pos = (x, y)
    if update_display:
        update_brush_display(self)

def update_brush_display(self):
    if not self.image or not self.mask:
        return
    size = (int(self.image.width * self.scale_factor), int(self.image.height * self.scale_factor))
    img = self.image.copy().resize(size, Image.Resampling.LANCZOS)
    m = self.mask.resize(size, Image.Resampling.NEAREST)
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    mask_np = np.array(m)
    overlay_np = np.array(overlay)
    overlay_np[mask_np > 0] = [255, 0, 0, 70]
    overlay = Image.fromarray(overlay_np)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    qimg = pil_to_qimage(img)
    pixmap = QPixmap.fromImage(qimg)
    self.pixmap_item.setPixmap(pixmap)

def on_brush_size_changed(self, value):
    self.brush_value_label.setText(str(value))
    if self.tool_combo.currentData() == 1 and self.image:
        self.view.viewport().setCursor(create_brush_cursor(self))
        
def update_scale(self, val):
    self.scale_factor = val / 100
    self.scale_value_label.setText(str(val))
    draw_image(self)
    
def on_tool_changed(self, index=None):
    if self.image:
        if self.tool_combo.currentData() == 1:
            self.view.viewport().setCursor(create_brush_cursor(self))
        else:
            self.view.viewport().setCursor(Qt.CrossCursor)
            
def open_image(self):
    from PyQt5.QtWidgets import QFileDialog, QMessageBox
    from PIL import Image
    path, _ = QFileDialog.getOpenFileName(self, "Otwórz obraz", "", "Obrazy (*.png *.jpg *.jpeg *.bmp)")
    if path:
        try:
            img = Image.open(path).convert("RGB")
            if img.width == 0 or img.height == 0:
                raise ValueError("Obraz ma nieprawidłowy rozmiar")
            if img.width > 4096 or img.height > 4096:
                QMessageBox.warning(self, "Uwaga", f"Obraz bardzo duży: {img.width}x{img.height}")
            self.image = img
            self.mask = Image.new("L", self.image.size, 0)
            self.history.clear()
            draw_image(self)
            # reset status
            try:
                self.status_label.setStyleSheet(f"background: {COLORS['status_idle']}; border-radius: 10px;")
                self.status_message.setText("")
            except Exception:
                pass
            if self.tool_combo.currentData() == 1:
                self.view.viewport().setCursor(create_brush_cursor(self))
            else:
                self.view.viewport().setCursor(Qt.CrossCursor)
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie można otworzyć obrazu:\n{str(e)}")


def set_image_from_bytes(self, data: bytes):
    """Ustawia obraz aplikacji z surowych bajtów obrazu.

    Jest to programowy odpowiednik funkcji open_image() (bez okna dialogowego).
    """
    try:
        img = bytes_to_pil_image(data, mode="RGB")
        if img.width == 0 or img.height == 0:
            raise ValueError("Obraz ma nieprawidłowy rozmiar")
        if img.width > 4096 or img.height > 4096:
            # ciche ostrzeżenie — zachowaj minimalne zachowanie UI przy użyciu programowym
            pass
        self.image = img
        self.mask = Image.new("L", self.image.size, 0)
        self.history.clear()
        draw_image(self)
        if self.tool_combo.currentData() == 1:
            self.view.viewport().setCursor(create_brush_cursor(self))
        else:
            self.view.viewport().setCursor(Qt.CrossCursor)
    except Exception as e:

        raise


def set_mask_from_bytes(self, data: bytes):
    """Ustaw aktywną maskę z surowych bajtów. Maska powinna mieć rozmiar pasujący do obrazu."""
    if not self.image:
        raise ValueError("Set image first before applying a mask")
    try:
        m = bytes_to_mask_image(data)
        if m.size != self.image.size:
            # spróbuj przeskalować (nearest)
            m = m.resize(self.image.size, Image.Resampling.NEAREST)
        self.mask = m
        draw_image(self)
    except Exception:
        raise


def set_image_and_mask_from_bytes(self, image_bytes: bytes, mask_bytes: bytes):
    """Funkcja pomocnicza: ustawia jednocześnie obraz i maskę z dostarczonych bajtów."""
    set_image_from_bytes(self, image_bytes)
    set_mask_from_bytes(self, mask_bytes)
            
def save_image(self):
    from PyQt5.QtWidgets import QFileDialog, QMessageBox
    if not self.image:
        QMessageBox.warning(self, "Błąd", "Brak obrazu do zapisania.")
        return
    default_name = f"wynik_{get_timestamp()}.png" if self.saved_save_with_timestamp else "wynik.png"
    path, _ = QFileDialog.getSaveFileName(self, "Zapisz obraz", default_name, "PNG (*.png);;JPG (*.jpg)")
    if path:
        self.image.save(path)
        QMessageBox.information(self, "Zapisano", f"Zapisano: {path}")
        
def erase_selection(self):
    from PyQt5.QtWidgets import QMessageBox, QApplication
    if not self.image:
        QMessageBox.warning(self, "Błąd", "Wczytaj obraz najpierw.")
        return
    if not self.mask or not any(px > 0 for px in self.mask.getdata()):
        QMessageBox.warning(self, "Błąd", "Zaznacz obszar do usunięcia.")
        return
    
    #===DODANIE DO HISTORII===#
    self.history.append((self.image.copy(), self.mask.copy()))
    
    #===ZMIANA STATUSU PRZETWARZANIA===#
    self.status_label.setStyleSheet(f"background: {COLORS['status_processing']}; border-radius: 10px;")
    self.status_message.setText("⏳ Przetwarzanie...")
    QApplication.processEvents()
    
    #===LOGIKA INPAINTNGU===#
    if self.fill_combo.currentData() == 2:  # SD + ControlNet
        if self.sd_connected:
            import sd
            sd.sd_inpaint_with_controlnet(self)
        else:
            QMessageBox.warning(self, "Info", "Najpierw połącz się z SD (Ustawienia -> Połącz z SD)")
            self.status_label.setStyleSheet(f"background: {COLORS['status_idle']}; border-radius: 10px;")
            self.status_message.setText("Gotowy")
            return
    else:
        _local_inpaint_and_update(self)
    
    #===ZMIANA STATUSU===#
    self.status_label.setStyleSheet(f"background: {COLORS['status_done']}; border-radius: 10px;")
    self.status_message.setText("✓ Gotowy")
    
def _local_inpaint_and_update(self):
    id_ = self.fill_combo.currentData() 
    if id_ == 0:
        filled = neighbor_inpaint(self.image.copy(), self.mask)
    elif id_ == 1:
        filled = empty_inpaint(self.image.copy(), self.mask)
    elif id_ == 3:
        filled = criminisi_inpaint(self.image.copy(), self.mask)
    elif id_ == 4:
        filled = telea_inpaint(self.image.copy(), self.mask)
    else:
        filled = self.image.copy() #=== TZW. FALLBACK===#
    self.image = filled
    self.mask = Image.new("L", self.image.size, 0)
    draw_image(self)
    
def neighbor_inpaint(img, mask):
    pixels = img.load()
    mask_pixels = mask.load()
    w, h = img.size
    for _ in range(80):
        changed = False
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if mask_pixels[x, y] == 255:
                    n = [pixels[nx, ny] for nx, ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if mask_pixels[nx, ny] == 0]
                    if n:
                        avg = tuple(sum(p[i] for p in n)//len(n) for i in range(3))
                        pixels[x, y] = avg
                        mask_pixels[x, y] = 0
                        changed = True
        if not changed: break
    return img

def empty_inpaint(img, mask):
    px = img.load()
    mp = mask.load()
    for y in range(img.height):
        for x in range(img.width):
            if mp[x, y] == 255:
                px[x, y] = (255, 255, 255)
    return img

def telea_inpaint(img, mask):
    img_np = np.array(img)
    mask_np = np.array(mask)
    filled_np = cv.inpaint(img_np, mask_np, 3, cv.INPAINT_TELEA)
    return Image.fromarray(filled_np)

def undo(self):
    #Cofanie
    from PyQt5.QtWidgets import QMessageBox
    if self.history:
        self.image, self.mask = self.history.pop()
        draw_image(self)
        # reset statusu
        try:
            self.status_label.setStyleSheet(f"background: {COLORS['status_idle']}; border-radius: 10px;")
            self.status_message.setText("")
        except Exception:
            pass
    else:
        QMessageBox.information(self, "Info", "Brak operacji do cofnięcia.")
        
def reset_selection(self):
    from PyQt5.QtWidgets import QMessageBox
    if self.image:
        self.mask = Image.new("L", self.image.size, 0)
        draw_image(self)
        # reset status
        try:
            self.status_label.setStyleSheet(f"background: {COLORS['status_idle']}; border-radius: 10px;")
            self.status_message.setText("")
        except Exception:
            pass
    else:
        QMessageBox.warning(self, "Błąd", "Brak obrazu.")
