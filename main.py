import io
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QSlider, QLabel,
    QFileDialog, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QAction, QPushButton, QWidget, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QKeySequence, QImage
from PyQt5.QtCore import Qt
from PIL import Image
import sys
import numpy as np


# --- Stałe ---
SHORTCUTS = {
    "Ctrl+O": "open_image",
    "Ctrl+S": "save_image",
    "Ctrl+R": "reset_selection",
    "Ctrl+Z": "undo"
}

COLORS = {
    "status_idle": "#FFFF00",
    "toolbar_gradient_start": "#000000",
    "toolbar_gradient_end": "#FFD700"
}


# --- Helpery ---
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def pil_to_qimage(pil_img):
    """Konwersja PIL Image do QImage"""
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
    """Zaokrąglony przycisk z gradientem i animacjami"""
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
        self.setWindowTitle("Usuwanie obiektów – Lasso Eraser")
        self.resize(1100, 750)

        # Zmienne stanu
        self.image = None
        self.mask = None
        self.history = []
        self.scale_factor = 1.0

        self.setup_ui()
        self.setup_shortcuts()

    def setup_ui(self):
        """Konfiguracja interfejsu użytkownika"""
        # Toolbar z gradientem
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

        # Przyciski akcji
        actions = [
            ("Otwórz", self.open_image),
            ("Zapisz", self.save_image),
            ("Reset", self.reset_selection),
            ("Cofnij", self.undo)
        ]
        
        for text, func in actions:
            btn = RoundedButton(text)
            btn.clicked.connect(func)
            toolbar.addWidget(btn)

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

        # Status indicator
        self.status_label = QLabel()
        self.status_label.setFixedSize(20, 20)
        self.status_label.setStyleSheet(f"background: {COLORS['status_idle']}; border-radius: 10px;")
        toolbar.addWidget(self.status_label)

        # Canvas - obszar rysowania
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setDragMode(QGraphicsView.NoDrag)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setCentralWidget(self.view)

        # Pixmap item do wyświetlania obrazu
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

    def setup_shortcuts(self):
        """Konfiguracja skrótów klawiszowych"""
        for key, method_name in SHORTCUTS.items():
            action = QAction(self)
            action.setShortcut(QKeySequence(key))
            action.triggered.connect(getattr(self, method_name))
            self.addAction(action)

    def draw_image(self):
        """Rysuje obraz na canvas z uwzględnieniem skali"""
        if not self.image:
            return
        
        # Skalowanie obrazu
        size = (int(self.image.width * self.scale_factor), 
                int(self.image.height * self.scale_factor))
        img = self.image.copy().resize(size, Image.Resampling.LANCZOS)

        # Opcjonalnie: nałożenie maski (jeśli istnieje)
        if self.mask:
            m = self.mask.resize(size, Image.Resampling.NEAREST)
            overlay = Image.new("RGBA", size, (0, 0, 0, 0))
            mask_np = np.array(m)
            overlay_np = np.array(overlay)
            # Czerwone półprzezroczyste zaznaczenie
            overlay_np[mask_np > 0] = [255, 0, 0, 70]
            overlay = Image.fromarray(overlay_np)
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

        # Konwersja do QPixmap i wyświetlenie
        qimg = pil_to_qimage(img)
        pixmap = QPixmap.fromImage(qimg)
        self.pixmap_item.setPixmap(pixmap)
        self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())

    def update_scale(self, val):
        """Aktualizacja skali wyświetlania obrazu"""
        self.scale_factor = val / 100
        self.scale_value_label.setText(str(val))
        self.draw_image()

    def open_image(self):
        """Wczytanie obrazu z pliku (punkt 31-33)"""
        path, _ = QFileDialog.getOpenFileName(
            self, 
            "Otwórz obraz", 
            "", 
            "Obrazy (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if path:
            try:
                # Wczytanie obrazu
                img = Image.open(path).convert("RGB")
                
                # Walidacja rozmiaru
                if img.width == 0 or img.height == 0:
                    raise ValueError("Obraz ma nieprawidłowy rozmiar")
                
                # Ostrzeżenie dla dużych obrazów
                if img.width > 4096 or img.height > 4096:
                    QMessageBox.warning(
                        self, 
                        "Uwaga", 
                        f"Obraz bardzo duży: {img.width}x{img.height}"
                    )
                
                # Zapisanie obrazu i utworzenie pustej maski
                self.image = img
                self.mask = Image.new("L", self.image.size, 0)
                self.history.clear()
                
                # Wyświetlenie obrazu
                self.draw_image()
                
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "Błąd", 
                    f"Nie można otworzyć obrazu:\n{str(e)}"
                )

    def save_image(self):
        """Zapisanie obrazu do pliku (punkt 34-35)"""
        if not self.image:
            QMessageBox.warning(self, "Błąd", "Brak obrazu do zapisania.")
            return
        
        # Domyślna nazwa z timestampem
        default_name = f"wynik_{get_timestamp()}.png"
        
        path, _ = QFileDialog.getSaveFileName(
            self, 
            "Zapisz obraz", 
            default_name, 
            "PNG (*.png);;JPG (*.jpg)"
        )
        
        if path:
            try:
                self.image.save(path)
                QMessageBox.information(self, "Zapisano", f"Zapisano: {path}")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie można zapisać obrazu:\n{str(e)}")

    def reset_selection(self):
        """Resetowanie zaznaczenia maski (punkt 36)"""
        if self.image:
            self.mask = Image.new("L", self.image.size, 0)
            self.draw_image()
        else:
            QMessageBox.warning(self, "Błąd", "Brak obrazu.")

    def undo(self):
        """Cofnięcie ostatniej operacji (punkt 38)"""
        if self.history:
            self.image, self.mask = self.history.pop()
            self.draw_image()
        else:
            QMessageBox.information(self, "Info", "Brak operacji do cofnięcia.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LassoEraser()
    window.show()
    sys.exit(app.exec_())
