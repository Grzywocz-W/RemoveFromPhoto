from PyQt5.QtWidgets import (
    QToolBar, QSlider, QLabel, QScrollArea, QDialog, QFormLayout, QLineEdit,
    QCheckBox, QComboBox, QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QGraphicsLineItem, QAction, QButtonGroup, QRadioButton, QWidget, QApplication
)
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush, QKeySequence, QImage, QPainter, QCursor
from PyQt5.QtCore import Qt
import helpers

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
       
def setup_ui(self):
    toolbar = QToolBar()
    toolbar.setStyleSheet(f"""
        QToolBar {{
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {helpers.COLORS['toolbar_gradient_start']},
                stop:1 {helpers.COLORS['toolbar_gradient_end']}
            );
            spacing: 8px;
            padding: 4px;
        }}
    """)
    self.addToolBar(toolbar)
    #===LABEL===#
    tool_label = QLabel("Narzędzie:")
    tool_label.setStyleSheet("color: white;")
    toolbar.addWidget(tool_label)
    #===COMBOBOX Z WYBOREM===#
    self.tool_combo = QComboBox()
    self.tool_combo.addItem("Lasso", 0)
    self.tool_combo.addItem("Pędzel", 1)
    self.tool_combo.setCurrentIndex(1)
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
    #===WYPEŁNIENIE===#
    fill_label = QLabel("Wypełnienie:")
    fill_label.setStyleSheet("color: white;")
    toolbar.addWidget(fill_label)
    #===RODZAJE WYPEŁNIENIA===#
    self.fill_combo = QComboBox()
    self.fill_combo.addItem("Sąsiedztwo", 0)
    self.fill_combo.addItem("Puste", 1)
    self.fill_combo.addItem("SD + ControlNet", 2)
    self.fill_combo.addItem("Criminisi", 3)
    self.fill_combo.addItem("Telea", 4)
    self.fill_combo.addItem("Auto", 5) 
    self.fill_combo.setCurrentIndex(0)
    self.fill_combo.setStyleSheet("""
        QComboBox {
            color: white;
            background-color: #333333;
            border: 1px solid #555555;
            padding: 4px 8px;
            min-width: 120px;
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
    toolbar.addWidget(self.fill_combo)
    toolbar.addSeparator()
    #===BUTTONY ===#
    actions = [
        ("Otwórz", self.open_image),
        ("Usuń i wypełnij", self.erase_selection),
        ("Zapisz", self.save_image),
        ("Reset", self.reset_selection),
        ("Cofnij", self.undo),
        ("Ustawienia", self.open_settings)
    ]
    for text, func in actions:
        btn = RoundedButton(text)
        btn.clicked.connect(func)
        toolbar.addWidget(btn)
    #===SUWAK PĘDZLNA===#
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
    self.brush_slider.setRange(3, 100)
    self.brush_slider.setValue(10)
    self.brush_slider.valueChanged.connect(self.on_brush_size_changed)
    brush_layout.addWidget(self.brush_slider)
    toolbar.addWidget(brush_container)
    #===SUWAK ROZMIARU===#
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
    #===STATUS===#
    self.status_label = QLabel()
    self.status_label.setFixedSize(20, 20)
    self.status_label.setStyleSheet(f"background: {helpers.COLORS['status_idle']}; border-radius: 10px;")
    toolbar.addWidget(self.status_label)
    #===INFORMACJA O STATUSIE===#
    self.status_message = QLabel("")
    self.status_message.setStyleSheet("color: white; font-weight: bold;")
    toolbar.addWidget(self.status_message)
    #===CANVA===#
    #=== POTESTUJCIE NA WIĘKSZYCH OBRAZKACH NP. 16K===#
    self.scene = QGraphicsScene()
    self.view = QGraphicsView(self.scene)
    self.view.setDragMode(QGraphicsView.NoDrag)
    self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.setCentralWidget(self.view)
    self.pixmap_item = QGraphicsPixmapItem()
    self.scene.addItem(self.pixmap_item)
    self.view.viewport().installEventFilter(self)
