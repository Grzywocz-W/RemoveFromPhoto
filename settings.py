import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGroupBox, QFormLayout, QScrollArea, QLineEdit, QLabel, QWidget, QHBoxLayout, QComboBox, QSlider, QPushButton
from PyQt5.QtCore import Qt

def open_settings(self):
    dialog = QDialog(self)
    dialog.setWindowTitle("Ustawienia SD + ControlNet")
    dialog.resize(680, 750)
    # --- CIEMNY MOTYW ---
    dialog.setStyleSheet("""
        QDialog {
            background-color: #1e1e1e;
            color: white;
            padding: 0;
            margin: 0;
        }
        QScrollArea {
            background-color: #1e1e1e;
            border: none;
        }
        QScrollArea > QWidget {
            background-color: #1e1e1e;
            margin: 0;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #444;
            border-radius: 6px;
            margin: 0;
            padding-top: 10px;
            background-color: #2d2d2d;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 8px;
            color: #FFD700;
            font-size: 14pt;
        }
        QFormLayout {
            margin: 5px;
            spacing: 5px;
        }
        QLineEdit, QComboBox {
            background-color: #333;
            color: white;
            border: 1px solid #555;
            padding: 4px;
            border-radius: 4px;
        }
        QCheckBox, QRadioButton {
            color: white;
        }
        QLabel {
            color: white;
        }
        QSlider::groove:horizontal {
            border: 1px solid #444;
            height: 8px;
            background: #333;
            margin: 2px 0;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #FFD700;
            border: 1px solid #AAA;
            width: 16px;
            margin: -4px 0;
            border-radius: 8px;
        }
    """)
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    widget = QGroupBox("Ustawienia SD")
    form = QFormLayout(widget)
    form.setContentsMargins(10, 10, 10, 10)
    self.prompt_edit = QLineEdit(getattr(self, 'saved_prompt', "usuń obiekt i wypełnij tłem naturalnie"))
    form.addRow("Prompt:", self.prompt_edit)
    self.neg_edit = QLineEdit(getattr(self, 'saved_negative_prompt', "niska jakość, rozmycie, artefakty"))
    form.addRow("Negative Prompt:", self.neg_edit)
    # ==============================
    # Parametry Stable Diffusion
    # ==============================
    sd_group = QGroupBox("Parametry Stable Diffusion")
    sd_layout = QVBoxLayout()
    # --- Kroki ---
    steps_container = QWidget()
    steps_layout = QHBoxLayout(steps_container)
    steps_layout.setContentsMargins(0, 0, 0, 0)
    steps_label = QLabel("Kroki")
    steps_layout.addWidget(steps_label)
    self.steps_value = QLabel(str(getattr(self, 'saved_steps', 25)))
    self.steps_value.setStyleSheet("min-width: 30px; color: white;")
    steps_layout.addWidget(self.steps_value)
    self.steps_slider = QSlider(Qt.Horizontal)
    self.steps_slider.setRange(5, 150)
    self.steps_slider.setValue(getattr(self, 'saved_steps', 25))
    self.steps_slider.valueChanged.connect(lambda v: self.steps_value.setText(str(v)))
    steps_layout.addWidget(self.steps_slider)
    sd_layout.addWidget(steps_container)
    # --- Denoising Strength ---
    denoise_container = QWidget()
    denoise_layout = QHBoxLayout(denoise_container)
    denoise_layout.setContentsMargins(0, 0, 0, 0)
    denoise_label = QLabel("Denoising")
    denoise_layout.addWidget(denoise_label)
    self.denoise_value = QLabel(f"{getattr(self, 'saved_denoising', 0.7):.2f}")
    self.denoise_value.setStyleSheet("min-width: 40px; color: white;")
    denoise_layout.addWidget(self.denoise_value)
    self.denoise_slider = QSlider(Qt.Horizontal)
    self.denoise_slider.setRange(0, 100)
    self.denoise_slider.setValue(int(getattr(self, 'saved_denoising', 0.7) * 100))
    self.denoise_slider.valueChanged.connect(lambda v: self.denoise_value.setText(f"{v/100:.2f}"))
    denoise_layout.addWidget(self.denoise_slider)
    sd_layout.addWidget(denoise_container)
    # --- CFG Scale ---
    cfg_container = QWidget()
    cfg_layout = QHBoxLayout(cfg_container)
    cfg_layout.setContentsMargins(0, 0, 0, 0)
    cfg_label = QLabel("CFG Scale")
    cfg_layout.addWidget(cfg_label)
    self.cfg_value = QLabel(f"{getattr(self, 'saved_cfg_scale', 7.0):.1f}")
    self.cfg_value.setStyleSheet("min-width: 40px; color: white;")
    cfg_layout.addWidget(self.cfg_value)
    self.cfg_slider = QSlider(Qt.Horizontal)
    self.cfg_slider.setRange(10, 300)
    self.cfg_slider.setValue(int(getattr(self, 'saved_cfg_scale', 7.0) * 10))
    self.cfg_slider.valueChanged.connect(lambda v: self.cfg_value.setText(f"{v/10:.1f}"))
    cfg_layout.addWidget(self.cfg_slider)
    sd_layout.addWidget(cfg_container)
    sd_group.setLayout(sd_layout)
    form.addRow(sd_group)
    # Modele i Preprocesory
    model_group = QGroupBox("Modele i Preprocesory")
    model_layout = QVBoxLayout()
    self.model_combo = QComboBox()
    if hasattr(self, 'sd_client') and self.sd_client is not None and hasattr(self, 'saved_models'):
        for m in self.saved_models:
            self.model_combo.addItem(m)
    else:
        self.model_combo.addItem("Brak połączenia z SD")

    model_layout.addWidget(QLabel("Model SD:"))
    model_layout.addWidget(self.model_combo)
    self.prep_combo = QComboBox()
    # Wypelnia liste preprocesorów z saved_controlnets,
    # jak nie znajdzie, to komunikat 'Brak ControlNet'.
    if hasattr(self, 'saved_controlnets') and self.saved_controlnets:
        for p in self.saved_controlnets:
            self.prep_combo.addItem(p)
        self.prep_combo.setCurrentText(getattr(self, 'saved_preprocessor', self.saved_controlnets[0]))
    else:
        self.prep_combo.addItem("Brak ControlNet")
        self.prep_combo.setCurrentText(getattr(self, 'saved_preprocessor', "Brak ControlNet"))
    model_layout.addWidget(QLabel("Preprocessor:"))
    model_layout.addWidget(self.prep_combo)
    model_group.setLayout(model_layout)
    form.addRow(model_group)
    # Połączenie z SD
    connect_group = QGroupBox("Połączenie z SD")
    connect_layout = QVBoxLayout()
    self.sd_url_edit = QLineEdit(getattr(self, 'saved_sd_url', "http://127.0.0.1:7860"))
    connect_layout.addWidget(QLabel("Adres SD API:"))
    connect_layout.addWidget(self.sd_url_edit)
    connect_btn = QPushButton("Połącz z SD")
    def _connect():
        import sd
        url = self.sd_url_edit.text().strip() or None
        self.status_message = getattr(self, 'status_message', None)
        res = sd.connect_sd(window=self, url=url, timeout=4)
        from PyQt5.QtWidgets import QMessageBox
        if res.get('ok'):
            QMessageBox.information(self, "Połączono", f"Znaleziono {len(res.get('models', []))} modeli.")
        else:
            QMessageBox.warning(self, "Błąd połączenia", f"Nie można połączyć z SD:\n{res.get('error')}")
    connect_btn.clicked.connect(_connect)
    connect_layout.addWidget(connect_btn)
    connect_group.setLayout(connect_layout)
    form.addRow(connect_group)
    # Finalizacja
    scroll.setWidget(widget)
    layout.addWidget(scroll)
    btn_layout = QHBoxLayout()
    save_btn = QPushButton("Zapisz ustawienia")
    save_btn.clicked.connect(lambda: save_settings(self, dialog))
    btn_layout.addWidget(save_btn)
    layout.addLayout(btn_layout)
    dialog.setLayout(layout)
    dialog.exec_()

def save_settings(self, dialog):
    try:
        #place holder, potem zamieńcie
        self.saved_steps = self.steps_slider.value()
        self.saved_denoising = self.denoise_slider.value() / 100
        self.saved_cfg_scale = self.cfg_slider.value() / 10
        self.saved_model = self.model_combo.currentText()
        self.saved_preprocessor = self.prep_combo.currentText()
        self.saved_sd_url = self.sd_url_edit.text().strip()
        self.saved_prompt = self.prompt_edit.text().strip()
        self.saved_negative_prompt = self.neg_edit.text().strip()
        print("Ustawienia zapisane!")  # Dla debug
        dialog.accept()
    except Exception as e:
        print(f"Błąd zapisywania: {e}")  # Dla debug
