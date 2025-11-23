import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import pyqtSlot, QEvent

#===IMPORTY Z INNYCH PLIKÓW===#
import helpers
import settings
from shortcuts import SHORTCUTS
from mouse import mousePressEvent, mouseMoveEvent, mouseReleaseEvent, enterEvent_logic, leaveEvent_logic
from ui import setup_ui, RoundedButton

class LassoEraser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Usuwanie obiektów – Lasso / Pędzel")
        self.resize(1100, 750)
        # Flagi połączenie z SD
        self.sd_connected = False
        self.sd_client = None
        self.image = None
        self.mask = None
        self.history = []
        self.scale_factor = 1.0
        self.drawing = False
        self.points = []
        self.lasso_lines = []
        #===Pędzel===#
        #=== ===#
        self.last_brush_pos = None
        self.brush_update_counter = 0

        #Miejsce na integracje z SD API->
        #zrobiłem osobny plik sd.py
        
        self.setup_ui()
        self.setup_shortcuts()

    def setup_ui(self):
        setup_ui(self)  #Funkcja z pliku ui.py

    def setup_shortcuts(self):
        for key, method_name in SHORTCUTS.items():
            action = QAction(self)
            action.setShortcut(QKeySequence(key))
            action.triggered.connect(getattr(self, method_name))
            self.addAction(action)

    def eventFilter(self, source, event):
        if source == self.view.viewport():
            if event.type() == QEvent.MouseButtonPress:
                mousePressEvent(self, event)  #Funkcja z pliku mouse
                return True
            elif event.type() == QEvent.MouseMove:
                mouseMoveEvent(self, event)
                return True
            elif event.type() == QEvent.MouseButtonRelease:
                mouseReleaseEvent(self, event)
                return True
        return super().eventFilter(source, event)
    def enterEvent(self, event):
        enterEvent_logic(self, event) #===Delagat logiki===#
        super().enterEvent(event)
    def leaveEvent(self, event):
        leaveEvent_logic(self, event)
        super().leaveEvent(event)


    @pyqtSlot()
    def set_lasso(self):
        self.tool_combo.setCurrentIndex(0)
        self.on_tool_changed()

    @pyqtSlot()
    def set_brush(self):
        self.tool_combo.setCurrentIndex(1)
        self.on_tool_changed()

    def draw_image(self):
        helpers.draw_image(self)
    def update_brush_mask(self, x, y, update_display=False):
        helpers.update_brush_mask(self, x, y, update_display)
    def update_brush_display(self):
        helpers.update_brush_display(self)

    def on_brush_size_changed(self, value):
        helpers.on_brush_size_changed(self, value)
    def update_scale(self, val):
        helpers.update_scale(self, val)
    def on_tool_changed(self, index=None):
        helpers.on_tool_changed(self, index)


    # Settings
    def open_settings(self):
        settings.open_settings(self)
    def save_settings(self):
        settings.open_settings(self)


    def open_image(self):
        helpers.open_image(self)
    def save_image(self):
        helpers.save_image(self)

    def erase_selection(self):
        helpers.erase_selection(self)
    def _local_inpaint_and_update(self):
        helpers._local_inpaint_and_update(self)

    def undo(self):
        helpers.undo(self)
    def reset_selection(self):
        helpers.reset_selection(self)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LassoEraser()
    window.show()
    sys.exit(app.exec_())
