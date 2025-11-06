import base64
import io
import requests
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QSlider, QLabel, QScrollArea, QDialog, QFormLayout, QLineEdit,
    QCheckBox, QComboBox, QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QGraphicsLineItem, QAction, QButtonGroup, QRadioButton, QWidget
)
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush, QKeySequence, QImage, QPainter, QCursor
from PyQt5.QtCore import Qt, pyqtSlot
from PIL import Image, ImageDraw
import sys
import numpy as np

# --- Stałe ---
SHORTCUTS = {
    "Ctrl+O": "open_image",
    "Ctrl+E": "erase_selection",
    "Ctrl+S": "save_image",
    "Ctrl+R": "reset_selection",
    "Ctrl+Z": "undo",
    "Ctrl+L": "set_lasso",
    "Ctrl+B": "set_brush"
}

COLORS = {
    "status_idle": "#FFFF00",
    "status_processing": "#FF4500",
    "brush_cursor": "#00AA00",
    "toolbar_gradient_start": "#000000",
    "toolbar_gradient_end": "#FFD700"
}


# --- Helpery ---
def pil_to_base64(img_pil, fmt="PNG"):
    buf = io.BytesIO()
    img_pil.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


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


class RoundedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, 
                    stop:1 #764ba2
                );
                color: white;
                border-radius: 12px;
                padding: 6px 16px;
                font: bold 10pt "Segoe UI";
                min-width: 70px;
                border: none;
            }
            QPushButton:hover { 
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7b93f7, 
                    stop:1 #8a5cb8
                );
            }
            QPushButton:pressed { 
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5568d3, 
                    stop:1 #643a8e
                );
            }
        """)


class LassoEraser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Usuwanie obiektów – Lasso / Pędzel")
        self.resize(1100, 750)

        self.image = None
        self.mask = None
        self.history = []
        self.scale_factor = 1.0
        self.drawing = False
        self.points = []
        self.lasso_lines = []

        # Pędzel
        self.last_brush_pos = None
        self.brush_update_counter = 0

        self.setup_ui()
        self.setup_shortcuts()

    def setup_ui(self):
        toolbar = QToolBar()
        toolbar.setStyleSheet(f"""
            QToolBar {{ 
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS['toolbar_gradient_start']}, 
                    stop:1 {COLORS['toolbar_gradient_end']}
                );
                spacing: 8px;
                padding: 4px;
            }}
        """)
        self.addToolBar(toolbar)

        # Narzędzie label
        tool_label = QLabel("Narzędzie:")
        tool_label.setStyleSheet("color: white;")
        toolbar.addWidget(tool_label)

        # Narzędzie: ComboBox z wyborem
        self.tool_combo = QComboBox()
        self.tool_combo.addItem("Lasso", 0)
        self.tool_combo.addItem("Pędzel", 1)
        self.tool_combo.setCurrentIndex(0)
        self.tool_combo.setStyleSheet("""
            QComboBox {
                color: white;
                background-color: #333333;
                border: 1px solid #555555;
                padding: 4px 8px;
                min-width: 90px;
                font-weight: bold;
                border-radius: 6px;
            }
            QComboBox::drop-down {
                border: 0;
                width: 20px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
            }
            QComboBox QAbstractItemView {
                background-color: #444444;
                color: white;
                selection-background-color: #5CA9FF;
                border: 1px solid #555555;
            }
        """)
        self.tool_combo.currentIndexChanged.connect(self.on_tool_changed)
        toolbar.addWidget(self.tool_combo)

        toolbar.addSeparator()

        # Przyciski
        actions = [
            ("Otwórz", self.open_image),
            ("Usuń i wypełnij", self.erase_selection),
            ("Zapisz", self.save_image),
            ("Reset", self.reset_selection),
            ("Cofnij", self.undo)
        ]
        for text, func in actions:
            btn = RoundedButton(text)
            btn.clicked.connect(func)
            toolbar.addWidget(btn)

        # --- Suwak pędzla + wartość ---
        brush_container = QWidget()
        brush_layout = QHBoxLayout(brush_container)
        brush_layout.setContentsMargins(0, 0, 0, 0)

        self.brush_label = QLabel("Pędzel")
        self.brush_label.setStyleSheet("color: white;")
        brush_layout.addWidget(self.brush_label)

        self.brush_value_label = QLabel("10")
        self.brush_value_label.setStyleSheet("color: white; min-width: 30px;")
        brush_layout.addWidget(self.brush_value_label)

        self.brush_slider = QSlider(Qt.Horizontal)
        self.brush_slider.setRange(3, 50)
        self.brush_slider.setValue(10)
        self.brush_slider.valueChanged.connect(self.on_brush_size_changed)
        brush_layout.addWidget(self.brush_slider)

        toolbar.addWidget(brush_container)

        toolbar.addSeparator()

        # --- Suwak skali + wartość ---
        scale_container = QWidget()
        scale_layout = QHBoxLayout(scale_container)
        scale_layout.setContentsMargins(0, 0, 0, 0)

        self.scale_label = QLabel("Skala (%)")
        self.scale_label.setStyleSheet("color: white;")
        scale_layout.addWidget(self.scale_label)

        self.scale_value_label = QLabel("100")
        self.scale_value_label.setStyleSheet("color: white; min-width: 40px;")
        scale_layout.addWidget(self.scale_value_label)

        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setRange(10, 200)
        self.scale_slider.setValue(100)
        self.scale_slider.valueChanged.connect(self.update_scale)
        scale_layout.addWidget(self.scale_slider)

        toolbar.addWidget(scale_container)

        # Status
        self.status_label = QLabel()
        self.status_label.setFixedSize(20, 20)
        self.status_label.setStyleSheet(f"background: {COLORS['status_idle']}; border-radius: 10px;")
        toolbar.addWidget(self.status_label)

        # Canvas
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setDragMode(QGraphicsView.NoDrag)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setCentralWidget(self.view)

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        self.view.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if source == self.view.viewport():
            if event.type() == event.MouseButtonPress:
                self.mousePressEvent(event)
                return True
            elif event.type() == event.MouseMove:
                self.mouseMoveEvent(event)
                return True
            elif event.type() == event.MouseButtonRelease:
                self.mouseReleaseEvent(event)
                return True
        return super().eventFilter(source, event)

    def setup_shortcuts(self):
        for key, method_name in SHORTCUTS.items():
            action = QAction(self)
            action.setShortcut(QKeySequence(key))
            action.triggered.connect(getattr(self, method_name))
            self.addAction(action)

    @pyqtSlot()
    def set_lasso(self):
        self.tool_combo.setCurrentIndex(0)
        self.on_tool_changed()

    @pyqtSlot()
    def set_brush(self):
        self.tool_combo.setCurrentIndex(1)
        self.on_tool_changed()

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

    def update_brush_mask(self, x, y, update_display=False):
        r = self.brush_slider.value() // 2
        draw = ImageDraw.Draw(self.mask)
        if not self.last_brush_pos:
            draw.ellipse((x - r, y - r, x + r, y + r), fill=255)
            self.last_brush_pos = (x, y)
            if update_display:
                self.update_brush_display()
            return
        prev_x, prev_y = self.last_brush_pos
        dx = x - prev_x
        dy = y - prev_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < 1:
            draw.ellipse((x - r, y - r, x + r, y + r), fill=255)
        else:
            steps = max(int(distance), 1)
            for i in range(steps + 1):
                t = i / steps
                ix = prev_x + dx * t
                iy = prev_y + dy * t
                draw.ellipse((ix - r, iy - r, ix + r, iy + r), fill=255)
        self.last_brush_pos = (x, y)
        if update_display:
            self.update_brush_display()

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

    def mousePressEvent(self, event):
        if not self.image: return
        pos = self.view.mapToScene(event.pos())
        x, y = pos.x() / self.scale_factor, pos.y() / self.scale_factor
        self.drawing = True
        self.points = [(x, y)]
        self.last_brush_pos = None
        self.brush_update_counter = 0
        if self.tool_combo.currentData() == 1:
            self.update_brush_mask(x, y, update_display=True)

    def mouseMoveEvent(self, event):
        pos = self.view.mapToScene(event.pos())
        if not self.drawing or not self.image:
            return
        x, y = pos.x() / self.scale_factor, pos.y() / self.scale_factor
        if self.tool_combo.currentData() == 0:  # Lasso
            if len(self.points) > 1:
                prev = self.points[-1]
                line = self.scene.addLine(
                    prev[0] * self.scale_factor, prev[1] * self.scale_factor,
                    x * self.scale_factor, y * self.scale_factor,
                    QPen(QColor("red"), 2)
                )
                self.lasso_lines.append(line)
            self.points.append((x, y))
        else:  # Pędzel
            self.brush_update_counter += 1
            self.update_brush_mask(x, y, update_display=(self.brush_update_counter % 3 == 0))

    def mouseReleaseEvent(self, event):
        if not self.image: return
        self.drawing = False
        if self.tool_combo.currentData() == 0 and len(self.points) > 2:
            draw = ImageDraw.Draw(self.mask)
            draw.polygon(self.points, fill=255)
        elif self.tool_combo.currentData() == 1:
            pos = self.view.mapToScene(event.pos())
            x, y = pos.x() / self.scale_factor, pos.y() / self.scale_factor
            self.update_brush_mask(x, y, update_display=False)
            self.last_brush_pos = None
        self.draw_image()

    def enterEvent(self, event):
        if self.tool_combo.currentData() == 1 and self.image:
            self.view.viewport().setCursor(self.create_brush_cursor())
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.view.viewport().setCursor(Qt.ArrowCursor)
        super().leaveEvent(event)

    def on_brush_size_changed(self, value):
        self.brush_value_label.setText(str(value))
        if self.tool_combo.currentData() == 1 and self.image:
            self.view.viewport().setCursor(self.create_brush_cursor())

    def update_scale(self, val):
        self.scale_factor = val / 100
        self.scale_value_label.setText(str(val))
        self.draw_image()

    def on_tool_changed(self, index=None):
        if self.image:
            if self.tool_combo.currentData() == 1:
                self.view.viewport().setCursor(self.create_brush_cursor())
            else:
                self.view.viewport().setCursor(Qt.CrossCursor)

    def open_image(self):
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
                self.draw_image()
                if self.tool_combo.currentData() == 1:
                    self.view.viewport().setCursor(self.create_brush_cursor())
                else:
                    self.view.viewport().setCursor(Qt.CrossCursor)
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie można otworzyć obrazu:\n{str(e)}")

    def save_image(self):
        if not self.image:
            QMessageBox.warning(self, "Błąd", "Brak obrazu do zapisania.")
            return
        default_name = f"wynik_{get_timestamp()}.png"
        path, _ = QFileDialog.getSaveFileName(self, "Zapisz obraz", default_name, "PNG (*.png);;JPG (*.jpg)")
        if path:
            self.image.save(path)
            QMessageBox.information(self, "Zapisano", f"Zapisano: {path}")

    def erase_selection(self):
        """Usuń zaznaczony obszar i wypełnij (punkt 71-72)"""
        if not self.image:
            QMessageBox.warning(self, "Błąd", "Wczytaj obraz najpierw.")
            return

        if not self.mask or not any(px > 0 for px in self.mask.getdata()):
            QMessageBox.warning(self, "Błąd", "Zaznacz obszar do usunięcia.")
            return

        # Dodaj do historii
        self.history.append((self.image.copy(), self.mask.copy()))

        # Zmień status na przetwarzanie
        self.status_label.setStyleSheet(f"background: {COLORS['status_processing']}; border-radius: 10px;")
        QApplication.processEvents()

        # Tutaj w przyszłości będzie logika wypełniania
        # Na razie tylko informacja
        QMessageBox.information(self, "Info",
                                "Funkcja usuwania i wypełniania zostanie zaimplementowana w kolejnych krokach.")

        # Przywróć status
        self.status_label.setStyleSheet(f"background: {COLORS['status_idle']}; border-radius: 10px;")

    def undo(self):
        if self.history:
            self.image, self.mask = self.history.pop()
            self.draw_image()
        else:
            QMessageBox.information(self, "Info", "Brak operacji do cofnięcia.")

    def reset_selection(self):
        if self.image:
            self.mask = Image.new("L", self.image.size, 0)
            self.draw_image()
        else:
            QMessageBox.warning(self, "Błąd", "Brak obrazu.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LassoEraser()
    window.show()
    sys.exit(app.exec_())
