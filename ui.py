from PyQt5.QtWidgets import (
    QToolBar, QSlider, QLabel, QScrollArea, QDialog, QFormLayout, QLineEdit,
    QCheckBox, QComboBox, QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QGraphicsLineItem, QAction, QButtonGroup, QRadioButton, QWidget, QApplication
)
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush, QKeySequence, QImage, QPainter, QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
import helpers
from file_configurator import LangKeys

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
                border-radius: 15px;
                padding: 10px 24px;
                font: bold 12pt "Segoe UI";
                min-width: 90px;
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
    toolbar.setMovable(False)#nie chcemy aby ruszać nim
    lang = getattr(self, 'lang_data', None) #jezyk

    #### PODSTAWOWE
##    toolbar.setStyleSheet(f"""
##        QToolBar {{
##            background: qlineargradient(
##                x1:0, y1:0, x2:0, y2:1,
##                stop:0 {helpers.COLORS['toolbar_gradient_start']},
##                stop:1 {helpers.COLORS['toolbar_gradient_end']}
##            );
##            spacing: 15px;
##            padding: 10px;
##        }}
##    """)

            #CHROME
##    toolbar.setStyleSheet("""
##        QToolBar {
##            background: qlineargradient(
##                x1:0, y1:0, x2:1, y2:0,
##                stop:0 #1a1a2e,
##                stop:0.5 #16213e,
##                stop:1 #0f3460
##            );
##            border-bottom: 2px solid qlineargradient(
##                x1:0, y1:0, x2:1, y2:0,
##                stop:0 #e94560,
##                stop:0.5 #f39c12,
##                stop:1 #00d4ff
##            );
##            spacing: 15px;
##            padding: 10px;
##        }
##    """)

    toolbar.setStyleSheet("""
        QToolBar {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #2c3e50,
                stop:0.5 #34495e,
                stop:1 #2c3e50
            );
            border: 1px solid #1a252f;
            border-top: 1px solid #4a5f7f;
            spacing: 15px;
            padding: 10px;
        }
    """)
    #self.addToolBar(toolbar)
    self.addToolBar(Qt.LeftToolBarArea, toolbar)
    label_style = "color: white; font-size: 12pt; font-weight: bold;"
    self.tool_label = QLabel("Narzędzie:") 
    self.tool_label.setStyleSheet(label_style)
    toolbar.addWidget(self.tool_label)


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
            padding: 8px 12px;
            min-width: 110px;
            min-height: 25px;
            font-weight: bold;
            border-radius: 8px;
            font: 11pt;
        }
        QComboBox::drop-down {
            border: 0;
            width: 30px;
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
    self.fill_label = QLabel("Wypełnienie:")
    self.fill_label.setStyleSheet(label_style)
    toolbar.addWidget(self.fill_label)
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
            padding: 8px 12px;
            min-width: 110px;
            min-height: 25px;
            font-weight: bold;
            border-radius: 8px;
            font: 11pt;
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

##    actions = [
##        ("Otwórz", self.open_image),
##        ("Usuń i wypełnij", self.erase_selection),
##        ("Zapisz", self.save_image),
##        ("Reset", self.reset_selection),
##        ("Cofnij", self.undo),
##        ("Ustawienia", self.open_settings)
##    ]
##    for text, func in actions:
##        btn = RoundedButton(text)
##        btn.clicked.connect(func)
##        toolbar.addWidget(btn)



    # Przycisk Otwórz (Ctrl+O)
    self.btn_open = RoundedButton("Otwórz")
    text_open = lang[LangKeys.BTN_OPEN].strip() if lang else "Otwórz"
    self.btn_open.setToolTip(f"Ctrl+O)")
    self.btn_open.clicked.connect(self.open_image)
    toolbar.addWidget(self.btn_open)

    # Przycisk Usuń i wypełnij (Ctrl+E)
    self.btn_erase = RoundedButton("Usuń i wypełnij")
    text_erase = lang[LangKeys.BTN_ERASE].strip() if lang else "Usuń i wypełnij"
    self.btn_erase.setToolTip(f"(Ctrl+E)")
    self.btn_erase.clicked.connect(self.erase_selection)
    toolbar.addWidget(self.btn_erase)

    # Przycisk Zapisz (Ctrl+S)
    self.btn_save = RoundedButton("Zapisz")
    text_save = lang[LangKeys.BTN_SAVE].strip() if lang else "Zapisz"
    self.btn_save.setToolTip(f"Ctrl+S)")
    self.btn_save.clicked.connect(self.save_image)
    toolbar.addWidget(self.btn_save)

    # Przycisk Reset (Ctrl+R)
    self.btn_reset = RoundedButton("Reset")
    text_reset = lang[LangKeys.BTN_RESET].strip() if lang else "Reset"
    self.btn_reset.setToolTip(f"(Ctrl+R)")
    self.btn_reset.clicked.connect(self.reset_selection)
    toolbar.addWidget(self.btn_reset)

    # Przycisk Cofnij (Ctrl+Z)
    self.btn_undo = RoundedButton("Cofnij")
    text_undo = lang[LangKeys.BTN_UNDO].strip() if lang else "Cofnij"
    self.btn_undo.setToolTip(f"(Ctrl+Z)")
    self.btn_undo.clicked.connect(self.undo)
    toolbar.addWidget(self.btn_undo)

    # Przycisk Ustawienia (brak skrótu w shortcuts.py, dodajemy sam opis)
    self.btn_settings = RoundedButton("Ustawienia")
    text_settings = lang[LangKeys.BTN_SETTINGS].strip() if lang else "Ustawienia"
    self.btn_settings.setToolTip('⚙️')
    self.btn_settings.clicked.connect(self.open_settings)
    toolbar.addWidget(self.btn_settings)





##    #===SUWAK PĘDZLNA===#
##    brush_container = QWidget()
##    #Zamieńcie jak chcecie
##    #brush_layout = QHBoxLayout(brush_container)
##    brush_layout = QVBoxLayout(brush_container)
##    brush_layout.setContentsMargins(0, 0, 0, 0)
##    self.brush_label = QLabel("Pędzel")
##    self.brush_label.setStyleSheet("color: white;")
##    brush_layout.addWidget(self.brush_label)
##    self.brush_value_label = QLabel("10")
##    self.brush_value_label.setStyleSheet("color: white; min-width: 30px;")
##    brush_layout.addWidget(self.brush_value_label)
##    #self.brush_slider = QSlider(Qt.Horizontal)
##    self.brush_slider = QSlider(Qt.Vertical)
##    self.brush_slider.setRange(3, 100)
##    self.brush_slider.setValue(10)
##    self.brush_slider.setMinimumHeight(128)
##    self.brush_slider.valueChanged.connect(self.on_brush_size_changed)
##    brush_layout.addWidget(self.brush_slider)
##    toolbar.addWidget(brush_container)
##
##    #===SUWAK ROZMIARU===#
##    scale_container = QWidget()
##    #scale_layout = QHBoxLayout(scale_container)
##    scale_layout = QVBoxLayout(scale_container)
##    scale_layout.setContentsMargins(0, 0, 0, 0)
##    self.scale_label = QLabel("Skala (%)")
##    self.scale_label.setStyleSheet("color: white;")
##    scale_layout.addWidget(self.scale_label)
##    self.scale_value_label = QLabel("100")
##    self.scale_value_label.setStyleSheet("color: white; min-width: 40px;")
##    scale_layout.addWidget(self.scale_value_label)
##    self.scale_slider = QSlider(Qt.Vertical)
##    self.scale_slider.setRange(10, 200)
##    self.scale_slider.setValue(100)
##    self.scale_slider.setMinimumHeight(128)
##    self.scale_slider.valueChanged.connect(self.update_scale)
##    scale_layout.addWidget(self.scale_slider)
##    toolbar.addWidget(scale_container)

        
    #====KONTENER NA SUWAKI =====#

    sliders_container = QWidget()
    
    sliders_layout = QHBoxLayout(sliders_container)
    sliders_layout.setContentsMargins(0, 5, 0, 5)
    sliders_layout.setSpacing(10)

    #==== PĘDZEL ===###
    brush_widget = QWidget()
    brush_layout = QVBoxLayout(brush_widget)
    brush_layout.setContentsMargins(0, 0, 0, 0)
    brush_layout.setAlignment(Qt.AlignCenter)


    
    self.brush_label = QLabel(lang[LangKeys.LBL_BRUSH_NAME].strip() if lang else "Pędzel")
    self.brush_label.setStyleSheet(label_style)
    self.brush_label.setAlignment(Qt.AlignCenter)
    brush_layout.addWidget(self.brush_label)

    self.brush_value_label = QLabel("10")
    self.brush_value_label.setStyleSheet(label_style)
    self.brush_value_label.setAlignment(Qt.AlignCenter)
    brush_layout.addWidget(self.brush_value_label)

##    self.brush_slider = QSlider(Qt.Vertical)
##    self.brush_slider.setRange(3, 100)
##    self.brush_slider.setValue(10)
##    self.brush_slider.setMinimumHeight(130)
##    self.brush_slider.valueChanged.connect(self.on_brush_size_changed)
    self.brush_slider = QSlider(Qt.Vertical)
    self.brush_slider.setRange(3, 100)
    self.brush_slider.setValue(10)
    self.brush_slider.setMinimumHeight(130)
    self.brush_slider.setStyleSheet("""
        QSlider::groove:vertical {
            background: #2d2d2d;
            width: 8px;
            border-radius: 4px;
        }
        QSlider::sub-page:vertical {
            background: transparent;
            width: 8px;
            border-radius: 4px;
        }
        QSlider::add-page:vertical {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea,
                stop:1 #764ba2
            );
            width: 8px;
            border-radius: 4px;
        }
        QSlider::handle:vertical {
            background: white;
            border: 2px solid #667eea;
            width: 18px;
            height: 18px;
            margin: 0 -5px;
            border-radius: 9px;
        }
        QSlider::handle:vertical:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #7b93f7,
                stop:1 #8a5cb8
            );
            border: 2px solid white;
        }
    """)
    self.brush_slider.valueChanged.connect(self.on_brush_size_changed)
    brush_layout.addWidget(self.brush_slider)

    sliders_layout.addWidget(brush_widget)

    #==== SKALA
    scale_widget = QWidget()
    scale_layout = QVBoxLayout(scale_widget)
    scale_layout.setContentsMargins(0, 0, 0, 0)
    scale_layout.setAlignment(Qt.AlignCenter)

    self.scale_label = QLabel(lang[LangKeys.LBL_SCALE_NAME].strip() if lang else "Skala %")
    self.scale_label.setStyleSheet(label_style)
    self.scale_label.setAlignment(Qt.AlignCenter)
    scale_layout.addWidget(self.scale_label)

    self.scale_value_label = QLabel("100%")
    self.scale_value_label.setStyleSheet(label_style)
    self.scale_value_label.setAlignment(Qt.AlignCenter)
    scale_layout.addWidget(self.scale_value_label)

##    self.scale_slider = QSlider(Qt.Vertical)
##    self.scale_slider.setRange(10, 200)
##    self.scale_slider.setValue(100)
##    self.scale_slider.setMinimumHeight(130)
##    self.scale_slider.valueChanged.connect(self.update_scale)

    self.scale_slider = QSlider(Qt.Vertical)
    self.scale_slider.setRange(10, 200)
    self.scale_slider.setValue(100)
    self.scale_slider.setMinimumHeight(130)
    self.scale_slider.setStyleSheet("""
        QSlider::groove:vertical {
            background: #2d2d2d;
            width: 8px;
            border-radius: 4px;
        }
        QSlider::sub-page:vertical {
            background: transparent;
            width: 8px;
            border-radius: 4px;
        }
        QSlider::add-page:vertical {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea,
                stop:1 #764ba2
            );
            width: 8px;
            border-radius: 4px;
        }
        QSlider::handle:vertical {
            background: white;
            border: 2px solid #667eea;
            width: 18px;
            height: 18px;
            margin: 0 -5px;
            border-radius: 9px;
        }
        QSlider::handle:vertical:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #7b93f7,
                stop:1 #8a5cb8
            );
            border: 2px solid white;
        }
    """)
    self.scale_slider.valueChanged.connect(self.update_scale)
    scale_layout.addWidget(self.scale_slider)

    sliders_layout.addWidget(scale_widget)

    toolbar.addWidget(sliders_container)
    

    #===STATUS===#
    self.status_label = QLabel()
    self.status_label.setFixedSize(30, 30)
    self.status_label.setStyleSheet(f"background: {helpers.COLORS['status_idle']}; border-radius: 15px;")
    toolbar.addWidget(self.status_label)

    #===INFORMACJA O STATUSIE===#
    self.status_message = QLabel("")
    self.status_message.setStyleSheet("color: white; font-weight: bold;")
    toolbar.addWidget(self.status_message)




    #===CANVA===#
    #=== POTESTUJCIE NA WIĘKSZYCH OBRAZKACH NP. 16K===#
    self.scene = QGraphicsScene()
    #SIATKA
##    checkerboard = QBrush(QColor(30, 30, 30))
##    self.scene.setBackgroundBrush(checkerboard)

    self.view = QGraphicsView(self.scene)
    #OPCJA 1

##    QGraphicsView {
##        background-color: #1e1e1e;
##        border: none;
##    }
    self.view.setStyleSheet("""
        QGraphicsView {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #0f0c29,
                stop:0.5 #302b63,
                stop:1 #24243e
            );
            border: none;
        }
        QScrollBar:vertical {
            background: #2d2d2d;
            width: 14px;
            border: none;
        }
        QScrollBar::handle:vertical {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #5568d3,
                stop:1 #764ba2
            );
            border-radius: 7px;
            min-height: 30px;
        }
        QScrollBar::handle:vertical:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea,
                stop:1 #8a5cb8
            );
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar:horizontal {
            background: #2d2d2d;
            height: 14px;
            border: none;
        }
        QScrollBar::handle:horizontal {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #5568d3,
                stop:1 #764ba2
            );
            border-radius: 7px;
            min-width: 30px;
        }
        QScrollBar::handle:horizontal:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #667eea,
                stop:1 #8a5cb8
            );
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
    """)
    self.view.setDragMode(QGraphicsView.NoDrag)
    self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.setCentralWidget(self.view)
    self.pixmap_item = QGraphicsPixmapItem()
    self.scene.addItem(self.pixmap_item)
    self.view.viewport().installEventFilter(self)
