import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QGroupBox, QFormLayout, 
    QScrollArea, QLineEdit, QLabel, QWidget, QHBoxLayout, QComboBox, 
    QSlider, QPushButton, QCheckBox, QButtonGroup, QRadioButton, QMessageBox)
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
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #667eea,
                stop:1 #764ba2
            );
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: bold;
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
    
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    widget = QGroupBox("Ustawienia SD")
    form = QFormLayout(widget)
    form.setContentsMargins(10, 10, 10, 10)
    
    #Prompt i Negative Prompt
    self.prompt_edit = QLineEdit(getattr(self, 'saved_prompt', "usuń obiekt i wypełnij tłem naturalnie"))
    form.addRow("Prompt:", self.prompt_edit)
    self.neg_edit = QLineEdit(getattr(self, 'saved_negative_prompt', "niska jakość, rozmycie, artefakty"))
    form.addRow("Negative Prompt:", self.neg_edit)
    

    #------Parametry Stable Diffusion----#

    sd_group = QGroupBox("Parametry Stable Diffusion")
    sd_layout = QVBoxLayout()
    
    # --- Kroki ---#
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
    
    # --- Denoising Strength ---#
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
    
    # --- CFG Scale ---#
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
    

    #----Seed----#

    seed_group = QGroupBox("Seed")
    seed_layout = QVBoxLayout()
    seed_container = QWidget()
    seed_h_layout = QHBoxLayout(seed_container)
    seed_h_layout.setContentsMargins(0, 0, 0, 0)
    self.random_seed_cb = QCheckBox("Losowy seed")
    self.random_seed_cb.setChecked(getattr(self, 'saved_use_random_seed', True))
    seed_h_layout.addWidget(self.random_seed_cb)
    self.seed_edit = QLineEdit(str(getattr(self, 'saved_seed', -1)))
    self.seed_edit.setMaximumWidth(150)
    seed_h_layout.addWidget(QLabel("Seed:"))
    seed_h_layout.addWidget(self.seed_edit)
    seed_h_layout.addStretch()
    seed_layout.addWidget(seed_container)
    seed_group.setLayout(seed_layout)
    form.addRow(seed_group)
    
    # ==============================
    # Modele i Preprocesory

    model_group = QGroupBox("Modele i Preprocesory")
    model_layout = QVBoxLayout()
    
    self.model_combo = QComboBox()
    if hasattr(self, 'sd_client') and self.sd_client is not None and hasattr(self, 'saved_models'):
        for m in self.saved_models:
            self.model_combo.addItem(m)
        if hasattr(self, 'saved_model'):
            self.model_combo.setCurrentText(self.saved_model)
    else:
        self.model_combo.addItem("Brak połączenia z SD")
    model_layout.addWidget(QLabel("Model SD:"))
    model_layout.addWidget(self.model_combo)
    
    self.control_combo = QComboBox()
    if hasattr(self, 'saved_controlnets') and self.saved_controlnets:
        for c in self.saved_controlnets:
            self.control_combo.addItem(c)
        if hasattr(self, 'saved_controlnet_model'):
            self.control_combo.setCurrentText(self.saved_controlnet_model)
    else:
        self.control_combo.addItem("Brak ControlNet")
    model_layout.addWidget(QLabel("Model ControlNet:"))
    model_layout.addWidget(self.control_combo)

    #już 7 poprawka
    self.prep_combo = QComboBox()
    if hasattr(self, 'saved_modules') and self.saved_modules:  #
        for p in self.saved_modules:
            self.prep_combo.addItem(p)
        saved_prep = getattr(self, 'saved_preprocessor', 'inpaint_only')
        if saved_prep in self.saved_modules:
            self.prep_combo.setCurrentText(saved_prep)
        else:
            self.prep_combo.setCurrentText(self.saved_modules[0] if self.saved_modules else "inpaint_only")
    else:
        self.prep_combo.addItem("inpaint_only")
        self.prep_combo.setCurrentText(getattr(self, 'saved_preprocessor', "inpaint_only"))
        
    model_layout.addWidget(QLabel("Preprocessor:"))
    model_layout.addWidget(self.prep_combo)
    
    model_group.setLayout(model_layout)
    form.addRow(model_group)
    
    # ==============================
    # ControlNet

    cn_group = QGroupBox("ControlNet - Zaawansowane")
    cn_layout = QVBoxLayout()
    
    # --- Control Weight ---#
    weight_container = QWidget()
    weight_layout = QHBoxLayout(weight_container)
    weight_layout.setContentsMargins(0, 0, 0, 0)
    weight_label = QLabel("Control Weight")
    weight_layout.addWidget(weight_label)
    self.weight_value = QLabel(f"{getattr(self, 'saved_control_weight', 1.0):.2f}")
    self.weight_value.setStyleSheet("min-width: 40px; color: white;")
    weight_layout.addWidget(self.weight_value)
    self.weight_slider = QSlider(Qt.Horizontal)
    self.weight_slider.setRange(0, 200)
    self.weight_slider.setValue(int(getattr(self, 'saved_control_weight', 1.0) * 100))
    self.weight_slider.valueChanged.connect(lambda v: self.weight_value.setText(f"{v/100:.2f}"))
    weight_layout.addWidget(self.weight_slider)
    cn_layout.addWidget(weight_container)
    
    # --- Guidance Start ---#
    gstart_container = QWidget()
    gstart_layout = QHBoxLayout(gstart_container)
    gstart_layout.setContentsMargins(0, 0, 0, 0)
    gstart_label = QLabel("Guidance Start")
    gstart_layout.addWidget(gstart_label)
    self.gstart_value = QLabel(f"{getattr(self, 'saved_guidance_start', 0.0):.2f}")
    self.gstart_value.setStyleSheet("min-width: 40px; color: white;")
    gstart_layout.addWidget(self.gstart_value)
    self.gstart_slider = QSlider(Qt.Horizontal)
    self.gstart_slider.setRange(0, 100)
    self.gstart_slider.setValue(int(getattr(self, 'saved_guidance_start', 0.0) * 100))
    self.gstart_slider.valueChanged.connect(lambda v: self.gstart_value.setText(f"{v/100:.2f}"))
    gstart_layout.addWidget(self.gstart_slider)
    cn_layout.addWidget(gstart_container)
    
    # --- Guidance End ---#
    gend_container = QWidget()
    gend_layout = QHBoxLayout(gend_container)
    gend_layout.setContentsMargins(0, 0, 0, 0)
    gend_label = QLabel("Guidance End")
    gend_layout.addWidget(gend_label)
    self.gend_value = QLabel(f"{getattr(self, 'saved_guidance_end', 1.0):.2f}")
    self.gend_value.setStyleSheet("min-width: 40px; color: white;")
    gend_layout.addWidget(self.gend_value)
    self.gend_slider = QSlider(Qt.Horizontal)
    self.gend_slider.setRange(0, 100)
    self.gend_slider.setValue(int(getattr(self, 'saved_guidance_end', 1.0) * 100))
    self.gend_slider.valueChanged.connect(lambda v: self.gend_value.setText(f"{v/100:.2f}"))
    gend_layout.addWidget(self.gend_slider)
    cn_layout.addWidget(gend_container)
    
    # --- Processor Resolution ---#
    proc_container = QWidget()
    proc_layout = QHBoxLayout(proc_container)
    proc_layout.setContentsMargins(0, 0, 0, 0)
    proc_label = QLabel("Processor Res")
    proc_layout.addWidget(proc_label)
    self.proc_value = QLabel(str(getattr(self, 'saved_processor_res', 512)))
    self.proc_value.setStyleSheet("min-width: 40px; color: white;")
    proc_layout.addWidget(self.proc_value)
    self.proc_res_slider = QSlider(Qt.Horizontal)
    self.proc_res_slider.setRange(64, 1024)
    self.proc_res_slider.setValue(getattr(self, 'saved_processor_res', 512))
    self.proc_res_slider.valueChanged.connect(lambda v: self.proc_value.setText(str(v)))
    proc_layout.addWidget(self.proc_res_slider)
    cn_layout.addWidget(proc_container)
    
    # --- Threshold A ---#
    tha_container = QWidget()
    tha_layout = QHBoxLayout(tha_container)
    tha_layout.setContentsMargins(0, 0, 0, 0)
    tha_label = QLabel("Threshold A")
    tha_layout.addWidget(tha_label)
    self.tha_value = QLabel(str(getattr(self, 'saved_threshold_a', 64)))
    self.tha_value.setStyleSheet("min-width: 30px; color: white;")
    tha_layout.addWidget(self.tha_value)
    self.th_a_slider = QSlider(Qt.Horizontal)
    self.th_a_slider.setRange(0, 255)
    self.th_a_slider.setValue(getattr(self, 'saved_threshold_a', 64))
    self.th_a_slider.valueChanged.connect(lambda v: self.tha_value.setText(str(v)))
    tha_layout.addWidget(self.th_a_slider)
    cn_layout.addWidget(tha_container)
    
    # --- Threshold B ---#
    thb_container = QWidget()
    thb_layout = QHBoxLayout(thb_container)
    thb_layout.setContentsMargins(0, 0, 0, 0)
    thb_label = QLabel("Threshold B")
    thb_layout.addWidget(thb_label)
    self.thb_value = QLabel(str(getattr(self, 'saved_threshold_b', 64)))
    self.thb_value.setStyleSheet("min-width: 30px; color: white;")
    thb_layout.addWidget(self.thb_value)
    self.th_b_slider = QSlider(Qt.Horizontal)
    self.th_b_slider.setRange(0, 255)
    self.th_b_slider.setValue(getattr(self, 'saved_threshold_b', 64))
    self.th_b_slider.valueChanged.connect(lambda v: self.thb_value.setText(str(v)))
    thb_layout.addWidget(self.th_b_slider)
    cn_layout.addWidget(thb_container)
    
    # --- Control Mode ---#
    mode_label = QLabel("Control Mode:")
    mode_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
    cn_layout.addWidget(mode_label)
    self.control_mode_group = QButtonGroup()
    for i, text in enumerate(["Balanced", "My prompt is more important", "ControlNet is more important"]):
        rb = QRadioButton(text)
        self.control_mode_group.addButton(rb, i)
        cn_layout.addWidget(rb)
    self.control_mode_group.button(getattr(self, 'saved_control_mode', 0)).setChecked(True)
    
    # --- Resize Mode ---#
    resize_label = QLabel("Resize Mode:")
    resize_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
    cn_layout.addWidget(resize_label)
    self.resize_mode_group = QButtonGroup()
    for i, text in enumerate(["Just Resize", "Crop and Resize", "Resize and Fill"]):
        rb = QRadioButton(text)
        self.resize_mode_group.addButton(rb, i)
        cn_layout.addWidget(rb)
    self.resize_mode_group.button(getattr(self, 'saved_resize_mode', 1)).setChecked(True)
    
    # --- Checkboxy ---#
    self.pixel_perfect_cb = QCheckBox("Pixel Perfect")
    self.pixel_perfect_cb.setChecked(getattr(self, 'saved_pixel_perfect', False))
    cn_layout.addWidget(self.pixel_perfect_cb)
    
    self.lowvram_cb = QCheckBox("Low VRAM")
    self.lowvram_cb.setChecked(getattr(self, 'saved_lowvram', False))
    cn_layout.addWidget(self.lowvram_cb)
    
    cn_group.setLayout(cn_layout)
    form.addRow(cn_group)
    

    #------ Inne opcje ----#

    other_group = QGroupBox("Inne opcje")
    other_layout = QVBoxLayout()
    
    self.timestamp_cb = QCheckBox("Dodaj timestamp do nazwy pliku")
    self.timestamp_cb.setChecked(getattr(self, 'saved_save_with_timestamp', False))
    other_layout.addWidget(self.timestamp_cb)
    
    other_group.setLayout(other_layout)
    form.addRow(other_group)
    

    #----- Połączenie z SD---###3

    connect_group = QGroupBox("Połączenie z SD")
    connect_layout = QVBoxLayout()
    self.sd_url_edit = QLineEdit(getattr(self, 'saved_sd_url', "http://127.0.0.1:7860"))
    connect_layout.addWidget(QLabel("Adres SD API:"))
    connect_layout.addWidget(self.sd_url_edit)
    connect_btn = QPushButton("Połącz z SD")
    
    def _connect():
        import sd
        url = self.sd_url_edit.text().strip() or None
        self.saved_sd_url = url or "http://127.0.0.1:7860"
        res = sd.connect_sd(window=self, url=url, timeout=4)  #'window=self' – poprawka, bo 'self' to dialog, ale connect_sd oczekuje window
        if res.get('ok'):
            QMessageBox.information(dialog, "Połączono", f"Znaleziono {len(res.get('models', []))} modeli, {len(res.get('controlnets', []))} ControlNet, {len(res.get('modules', []))} modułów.")
            #aktualizacja combo boxów
            self.model_combo.clear()
            self.model_combo.addItems(res.get('models', []) or ["Brak modeli"])
            self.control_combo.clear()
            self.control_combo.addItems(res.get('controlnets', []) or ["Brak ControlNet"])
            self.prep_combo.clear()
            modules = res.get('modules', []) or ['inpaint_only']
            self.prep_combo.addItems(modules)

            # NIE USTAWIAŁO preprocesora
            if hasattr(self, 'saved_preprocessor') and self.saved_preprocessor in modules:
                self.prep_combo.setCurrentText(self.saved_preprocessor)
        else:
            QMessageBox.warning(dialog, "Błąd połączenia", f"Nie można połączyć z SD:\n{res.get('error')}")

            
    connect_btn.clicked.connect(_connect)
    connect_layout.addWidget(connect_btn)
    connect_group.setLayout(connect_layout)
    form.addRow(connect_group)
    

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
        #podstawowe ustawienia SD
        self.saved_steps = self.steps_slider.value()
        self.saved_denoising = self.denoise_slider.value() / 100
        self.saved_cfg_scale = self.cfg_slider.value() / 10
        self.saved_prompt = self.prompt_edit.text().strip()
        self.saved_negative_prompt = self.neg_edit.text().strip()
        
        #seed
        try:
            self.saved_seed = int(self.seed_edit.text())
        except:
            self.saved_seed = -1
        self.saved_use_random_seed = self.random_seed_cb.isChecked()
        
        #3modele
        self.saved_model = self.model_combo.currentText()
        self.saved_controlnet_model = self.control_combo.currentText()
        self.saved_preprocessor = self.prep_combo.currentText() or 'inpaint_only'  
        
        #ControlNet zaawansowane
        self.saved_control_weight = self.weight_slider.value() / 100
        self.saved_guidance_start = self.gstart_slider.value() / 100
        self.saved_guidance_end = self.gend_slider.value() / 100
        self.saved_processor_res = self.proc_res_slider.value()
        self.saved_threshold_a = self.th_a_slider.value()
        self.saved_threshold_b = self.th_b_slider.value()
        self.saved_control_mode = self.control_mode_group.checkedId()
        self.saved_resize_mode = self.resize_mode_group.checkedId()
        self.saved_pixel_perfect = self.pixel_perfect_cb.isChecked()
        self.saved_lowvram = self.lowvram_cb.isChecked()
        
        #unne
        self.saved_save_with_timestamp = self.timestamp_cb.isChecked()
        self.saved_sd_url = self.sd_url_edit.text().strip()
        
        QMessageBox.information(dialog, "OK", "Ustawienia zapisane!")
        dialog.accept()
    except Exception as e:
        QMessageBox.critical(dialog, "Błąd", f"Błąd zapisywania ustawień: {e}")
