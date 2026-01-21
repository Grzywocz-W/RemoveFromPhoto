import sys
import os #dla obsługi języków
import traceback
import sd
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QGroupBox, QFormLayout, 
    QScrollArea, QLineEdit, QLabel, QWidget, QHBoxLayout, QComboBox, 
    QSlider, QPushButton, QCheckBox, QButtonGroup, QRadioButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import file_configurator
from file_configurator import LangKeys

def open_settings(self):
    dialog = QDialog(self)
    dialog.setWindowTitle("Ustawienia SD + ControlNet")
    dialog.resize(680, 750)

    lang = getattr(self, 'lang_data', None)# z pliku_file_configurator

    if not lang:
        print("file_configurator is null")
        return

    dialog = QDialog(self)
    dialog.setWindowTitle(lang[LangKeys.SETTINGS_TITLE].strip()) # "Ustawienia SD + ControlNet"
    dialog.resize(680, 750)
    
    # --- CIEMNY MOTYW ---
##    dialog.setStyleSheet("""
##        QDialog {
##            background-color: #1e1e1e;
##            color: white;
##            padding: 0;
##            margin: 0;
##        }
##        QScrollArea {
##            background-color: #1e1e1e;
##            border: none;
##        }
##        QScrollArea > QWidget {
##            background-color: #1e1e1e;
##            margin: 0;
##        }
##        QGroupBox {
##            font-weight: bold;
##            border: 1px solid #444;
##            border-radius: 6px;
##            margin: 0;
##            padding-top: 10px;
##            background-color: #2d2d2d;
##        }
##        QGroupBox::title {
##            subcontrol-origin: margin;
##            subcontrol-position: top left;
##            padding: 0 8px;
##            color: #FFD700;
##            font-size: 14pt;
##        }
##        QFormLayout {
##            margin: 5px;
##            spacing: 5px;
##        }
##        QLineEdit, QComboBox {
##            background-color: #333;
##            color: white;
##            border: 1px solid #555;
##            padding: 4px;
##            border-radius: 4px;
##        }
##        QCheckBox, QRadioButton {
##            color: white;
##        }
##        QLabel {
##            color: white;
##        }
##        QSlider::groove:horizontal {
##            border: 1px solid #444;
##            height: 8px;
##            background: #333;
##            margin: 2px 0;
##            border-radius: 4px;
##        }
##        QSlider::handle:horizontal {
##            background: #FFD700;
##            border: 1px solid #AAA;
##            width: 16px;
##            margin: -4px 0;
##            border-radius: 8px;
##        }
##        QPushButton {
##            background: qlineargradient(
##                x1:0, y1:0, x2:1, y2:1,
##                stop:0 #667eea,
##                stop:1 #764ba2
##            );
##            color: white;
##            border-radius: 8px;
##            padding: 8px 16px;
##            font-weight: bold;
##            border: none;
##        }
##        QPushButton:hover {
##            background: qlineargradient(
##                x1:0, y1:0, x2:1, y2:1,
##                stop:0 #7b93f7,
##                stop:1 #8a5cb8
##            );
##        }
##        QPushButton:pressed {
##            background: qlineargradient(
##                x1:0, y1:0, x2:1, y2:1,
##                stop:0 #5568d3,
##                stop:1 #643a8e
##            );
##        }
##    """)

    dialog.setStyleSheet("""
            QDialog { 
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #141E30,
                    stop:1 #243B55
                );
                color: #e0e0e0; 
            }
            QScrollArea { 
                background: transparent; 
                border: none; 
            }
            QScrollArea > QWidget > QWidget { 
                background: transparent; 
            }
            QGroupBox { 
                font-weight: bold; 
                border: 1px solid #4a5b70; 
                border-radius: 8px; 
                margin-top: 15px; 
                background-color: rgba(30, 30, 30, 150);
                padding-top: 15px;
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                subcontrol-position: top left; 
                left: 15px;
                padding: 0 5px; 
                color: #5CA9FF; 
                font-size: 11pt;
                background-color: transparent; 
            }
            QLineEdit, QComboBox { 
                background-color: #2b2b2b; 
                color: white; 
                border: 1px solid #555; 
                padding: 6px; 
                border-radius: 5px; 
            }
            QComboBox::drop-down { border: 0; width: 25px; }
            QCheckBox, QRadioButton, QLabel { 
                color: #e0e0e0; 
                font-size: 10pt;
                background: transparent;
            }
            QSlider::groove:horizontal { 
                border: 1px solid #444; 
                height: 6px; 
                background: #222; 
                margin: 2px 0; 
                border-radius: 3px; 
            }
            QSlider::sub-page:horizontal {
                background: #5CA9FF;
                border-radius: 3px;
            }
            QSlider::handle:horizontal { 
                background: #ffffff; 
                border: 1px solid #5CA9FF; 
                width: 14px; 
                height: 14px; 
                margin: -5px 0; 
                border-radius: 7px; 
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
            QScrollBar:vertical {
                border: none;
                background: #1e1e1e;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    
    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)
    main_layout.setContentsMargins(10, 10, 10, 10)

    #--------Języki-------#
    lang_group = QGroupBox("Language / Język")
    lang_layout_box = QVBoxLayout()
    
    self.settings_lang_combo = QComboBox()
    
    load_language_files(self.settings_lang_combo)

    current_lang = getattr(self, 'current_lang_file', "ENG_RFP.txt")
    
    index = self.settings_lang_combo.findData(current_lang)
    
    if index >= 0:
        self.settings_lang_combo.setCurrentIndex(index)

    self.settings_lang_combo.currentIndexChanged.connect(lambda: change_language_on_selection(self, dialog))

    
    
    lang_layout_box.addWidget(self.settings_lang_combo)
    lang_group.setLayout(lang_layout_box)
    
    main_layout.addWidget(lang_group)


    #  Tworzymy grupę i przypisujemy ją do dialogu (dla odświeżania języka)
    widget = QGroupBox(lang[LangKeys.GRP_SD_SETTINGS].strip())
    dialog.group_sd = widget

    #Tworzymy układ (form) ZANIM go użyjemy
    form = QFormLayout(widget)
    form.setContentsMargins(10, 10, 10, 10)

    default_prompt_text = "remove object, fill with natural background"
    default_neg_text = "low quality, blurry, artifacts, text, watermark"

    #Tworzymy Prompt - etykietę przypisujemy do dialogu, a potem dodajemy do form
    dialog.lbl_prompt = QLabel(lang[LangKeys.LBL_PROMPT].strip())
    self.prompt_edit = QLineEdit(getattr(self, 'saved_prompt', default_prompt_text))
    form.addRow(dialog.lbl_prompt, self.prompt_edit)

    dialog.lbl_neg_prompt = QLabel(lang[LangKeys.LBL_NEG_PROMPT].strip())
    self.neg_edit = QLineEdit(getattr(self, 'saved_negative_prompt', default_neg_text))
    form.addRow(dialog.lbl_neg_prompt, self.neg_edit)
    

    #------Parametry Stable Diffusion----#

    sd_group = QGroupBox(lang[LangKeys.GRP_SD_PARAMS].strip())
    sd_layout = QVBoxLayout()
    
    # --- Kroki ---#
    steps_container = QWidget()
    steps_layout = QHBoxLayout(steps_container)
    steps_layout.setContentsMargins(0, 0, 0, 0)
    steps_label = QLabel(lang[LangKeys.LBL_STEPS].strip())
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
    denoise_label = QLabel(lang[LangKeys.LBL_DENOISING].strip())
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
    cfg_label = QLabel(lang[LangKeys.LBL_CFG].strip())
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

    seed_group = QGroupBox(lang[LangKeys.GRP_SEED].strip())
    seed_layout = QVBoxLayout()
    seed_container = QWidget()
    seed_h_layout = QHBoxLayout(seed_container)
    seed_h_layout.setContentsMargins(0, 0, 0, 0)
    self.random_seed_cb = QCheckBox(lang[LangKeys.CB_RANDOM_SEED].strip())
    self.random_seed_cb.setChecked(getattr(self, 'saved_use_random_seed', True))
    seed_h_layout.addWidget(self.random_seed_cb)
    self.seed_edit = QLineEdit(str(getattr(self, 'saved_seed', -1)))
    self.seed_edit.setMaximumWidth(150)
    seed_h_layout.addWidget(QLabel(lang[LangKeys.LBL_SEED].strip()))
    seed_h_layout.addWidget(self.seed_edit)
    seed_h_layout.addStretch()
    seed_layout.addWidget(seed_container)
    seed_group.setLayout(seed_layout)
    form.addRow(seed_group)
    
    # ==============================
    # Modele i Preprocesory

    model_group = QGroupBox(lang[LangKeys.GRP_MODELS].strip())
    model_layout = QVBoxLayout()
    
    self.model_combo = QComboBox()
    if hasattr(self, 'sd_client') and self.sd_client is not None and hasattr(self, 'saved_models'):
        for m in self.saved_models:
            self.model_combo.addItem(m)
        if hasattr(self, 'saved_model'):
            self.model_combo.setCurrentText(self.saved_model)
    else:
        self.model_combo.addItem(lang[LangKeys.COMBO_NO_CONNECTION].strip())
    model_layout.addWidget(QLabel(lang[LangKeys.LBL_SD_MODEL].strip()))
    model_layout.addWidget(self.model_combo)
    
    self.control_combo = QComboBox()
    if hasattr(self, 'saved_controlnets') and self.saved_controlnets:
        for c in self.saved_controlnets:
            self.control_combo.addItem(c)
        if hasattr(self, 'saved_controlnet_model'):
            self.control_combo.setCurrentText(self.saved_controlnet_model)
    else:
        self.control_combo.addItem(lang[LangKeys.COMBO_NO_CONTROLNET].strip())
    model_layout.addWidget(QLabel(lang[LangKeys.LBL_CN_MODEL].strip()))
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
        
    model_layout.addWidget(QLabel(lang[LangKeys.LBL_PREPROCESSOR].strip()))
    model_layout.addWidget(self.prep_combo)
    
    model_group.setLayout(model_layout)
    form.addRow(model_group)
    
    # ==============================
    # ControlNet

    cn_group = QGroupBox(lang[LangKeys.GRP_CN_ADV].strip())
    cn_layout = QVBoxLayout()
    
    # --- Control Weight ---#
    weight_container = QWidget()
    weight_layout = QHBoxLayout(weight_container)
    weight_layout.setContentsMargins(0, 0, 0, 0)
    weight_label = QLabel(lang[LangKeys.LBL_WEIGHT].strip())
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
    gstart_label = QLabel(lang[LangKeys.LBL_G_START].strip())
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
    gend_label = QLabel(lang[LangKeys.LBL_G_END].strip())
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
    proc_label = QLabel(lang[LangKeys.LBL_PROC_RES].strip())
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
    tha_label = QLabel(lang[LangKeys.LBL_THRESH_A].strip())
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
    thb_label = QLabel(lang[LangKeys.LBL_THRESH_B].strip())
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
    mode_label = QLabel(lang[LangKeys.LBL_CTRL_MODE].strip())
    mode_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
    dialog.lbl_mode = mode_label
    cn_layout.addWidget(mode_label)

    self.control_mode_group = QButtonGroup()

    #to muszą być raddiobuttony!!!!
    rb_balanced = QRadioButton(lang[LangKeys.RB_BALANCED].strip())
    self.control_mode_group.addButton(rb_balanced, 0)
    cn_layout.addWidget(rb_balanced)
    dialog.rb_balanced = rb_balanced

    rb_prompt = QRadioButton(lang[LangKeys.RB_PROMPT_IMP].strip())
    self.control_mode_group.addButton(rb_prompt, 1)
    cn_layout.addWidget(rb_prompt)
    dialog.rb_prompt = rb_prompt

    rb_cn = QRadioButton(lang[LangKeys.RB_CN_IMP].strip())
    self.control_mode_group.addButton(rb_cn, 2)
    cn_layout.addWidget(rb_cn)
    dialog.rb_cn = rb_cn

    self.control_mode_group.button(getattr(self, 'saved_control_mode', 0)).setChecked(True)
    
    # --- Resize Mode ---#
    resize_label = QLabel(lang[LangKeys.LBL_RESIZE_MODE].strip()) 
    resize_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
    dialog.lbl_resize = resize_label # Przypisanie
    cn_layout.addWidget(resize_label)

    self.resize_mode_group = QButtonGroup()

    rb_just = QRadioButton(lang[LangKeys.RB_JUST_RESIZE].strip())
    self.resize_mode_group.addButton(rb_just, 0)
    cn_layout.addWidget(rb_just)
    dialog.rb_just = rb_just

    rb_crop = QRadioButton(lang[LangKeys.RB_CROP_RESIZE].strip())
    self.resize_mode_group.addButton(rb_crop, 1)
    cn_layout.addWidget(rb_crop)
    dialog.rb_crop = rb_crop

    rb_fill = QRadioButton(lang[LangKeys.RB_RESIZE_FILL].strip())
    self.resize_mode_group.addButton(rb_fill, 2)
    cn_layout.addWidget(rb_fill)
    dialog.rb_fill = rb_fill

    self.resize_mode_group.button(getattr(self, 'saved_resize_mode', 1)).setChecked(True)
    
    # --- Checkboxy ---#
    self.pixel_perfect_cb = QCheckBox(lang[LangKeys.CB_PIXEL_PERF].strip())
    self.pixel_perfect_cb.setChecked(getattr(self, 'saved_pixel_perfect', False))
    cn_layout.addWidget(self.pixel_perfect_cb)
    
    self.lowvram_cb = QCheckBox(lang[LangKeys.CB_LOW_VRAM].strip())
    self.lowvram_cb.setChecked(getattr(self, 'saved_lowvram', False))
    cn_layout.addWidget(self.lowvram_cb)
    
    cn_group.setLayout(cn_layout)
    form.addRow(cn_group)
    

    #------ Inne opcje ----#

    other_group = QGroupBox(lang[LangKeys.GRP_OTHER].strip())
    other_layout = QVBoxLayout()
    
    self.timestamp_cb = QCheckBox(lang[LangKeys.CB_TIMESTAMP].strip())
    self.timestamp_cb.setChecked(getattr(self, 'saved_save_with_timestamp', False))
    other_layout.addWidget(self.timestamp_cb)
    
    other_group.setLayout(other_layout)
    form.addRow(other_group)
    

    #----- Połączenie z SD---###3

    



    connect_group = QGroupBox(lang[LangKeys.GRP_CONNECT].strip())
    connect_layout = QVBoxLayout()
    
    self.sd_url_edit = QLineEdit(getattr(self, 'saved_sd_url', "http://127.0.0.1:7860"))
    connect_layout.addWidget(QLabel(lang[LangKeys.LBL_API_URL].strip()))
    connect_layout.addWidget(self.sd_url_edit)
    
    connect_btn = QPushButton(lang[LangKeys.BTN_CONNECT].strip())
    
    connect_btn.clicked.connect(lambda: logic_connect_to_sd(
        main_window=self, 
        dialog=dialog, 
        url_edit=self.sd_url_edit, 
        combo_model=self.model_combo, 
        combo_control=self.control_combo, 
        combo_prep=self.prep_combo
    ))
    
    connect_layout.addWidget(connect_btn)
    connect_group.setLayout(connect_layout)
    form.addRow(connect_group)



    
    
    main_layout.addWidget(widget)

    scroll.setWidget(main_widget)
    layout.addWidget(scroll)
    btn_layout = QHBoxLayout()
    save_btn = QPushButton(lang[LangKeys.BTN_SAVE_SETTINGS].strip())
    dialog.btn_save_sets = save_btn
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

        file_configurator.save_config(self)#self, bo settings jest już w window

        
        lang = getattr(self, 'lang_data', None)
        if lang:
             QMessageBox.information(dialog, lang[LangKeys.MSG_OK].strip(), lang[LangKeys.MSG_SETTINGS_SAVED].strip())
        else:
             QMessageBox.information(dialog, "OK", "Ustawienia zapisane!")
             
        dialog.accept()
    except Exception as e:
        QMessageBox.critical(dialog, "Error", f"Error{e}")





def load_language_files(combo_box):
    #nie zmieniamy. Jest to przestrzeń na konfigurację
    lang_dir = "Language"
    
    combo_box.clear()
    
    if not os.path.exists(lang_dir):
        combo_box.addItem("Missing: Language folder", None)
        return

    try:
        f = os.listdir(lang_dir)
        isin = False
        
        for fname in sorted(f):
            if fname.endswith("_RFP.txt"):#format ma być własnie taki
                display_name = fname.replace("_RFP.txt", "")
                combo_box.addItem(display_name, fname)
                isin = True
        
        if not isin:
            combo_box.addItem("None", None)
            
    except Exception as e:
        print(f"Erro {e}")
        combo_box.addItem("ERROR", None)



def change_language_on_selection(main_window, dialog): # Dodaj parametr dialog
    selected = main_window.settings_lang_combo.currentData()
    if not selected:
        return
    try:

        file_configurator.language_version(main_window, selected)
        # Wywołujemy odświeżanie tekstów w oknie ustawień:
        refresh_settings_dialog_text(main_window, dialog)
        main_window.repaint()

    except Exception as e:
        print(f"Error: {e}, check language packs.")



def logic_connect_to_sd(main_window, dialog, url_edit, combo_model, combo_control, combo_prep):
    lang = getattr(main_window, 'lang_data', {})
    try:
        url = url_edit.text().strip() or None
        if not url:
            url = "http://127.0.0.1:7860"
        
        main_window.saved_sd_url = url

        res = sd.connect_sd(window=main_window, url=url, timeout=5)

        if res.get('ok'):
            combo_model.clear()
            combo_model.addItems(res.get('models', []) or ["Brak modeli"])
            
            combo_control.clear()
            combo_control.addItems(res.get('controlnets', []) or ["Brak ControlNet"])
            
            combo_prep.clear()
            modules = res.get('modules', []) or ['inpaint_only']
            combo_prep.addItems(modules)

            if hasattr(main_window, 'saved_preprocessor') and main_window.saved_preprocessor in modules:
                combo_prep.setCurrentText(main_window.saved_preprocessor)
            
            #QMessageBox.information(dialog, "Sukces", f"Połączono z SD!\nZaładowano {len(res.get('models', []))} modeli.")

        else:
            error_msg = res.get('error', 'Unknown error')
            title = lang[LangKeys.MSG_CONN_ERR_TITLE].strip()
            body_fmt = lang[LangKeys.MSG_CONN_ERR_BODY].strip()
            
            QMessageBox.warning(dialog, title, body_fmt.format(error_msg))

    except Exception as e:
            print("!!! CRITICAL ERROR IN CONNECT !!!")
            traceback.print_exc()
            
            title = lang.get(LangKeys.MSG_ERR_TITLE, "Error")
            body_fmt = lang.get(LangKeys.MSG_GENERIC_ERR, "An error occurred: {}")
            
            QMessageBox.critical(dialog, title, body_fmt.format(str(e)))



# Aktualizuje język w oknie settings po zmianie jezyka
def refresh_settings_dialog_text(main_window, dialog):
    lang = getattr(main_window, 'lang_data', None)
    if not lang: return

    # Tytuł okna i Grupy
    dialog.setWindowTitle(lang[LangKeys.SETTINGS_TITLE].strip())
    if hasattr(dialog, 'group_sd'): dialog.group_sd.setTitle(lang[LangKeys.GRP_SD_SETTINGS].strip())
    if hasattr(dialog, 'sd_params_group'): dialog.sd_params_group.setTitle(lang[LangKeys.GRP_SD_PARAMS].strip())
    if hasattr(dialog, 'seed_group'): dialog.seed_group.setTitle(lang[LangKeys.GRP_SEED].strip())
    if hasattr(dialog, 'model_group'): dialog.model_group.setTitle(lang[LangKeys.GRP_MODELS].strip())
    if hasattr(dialog, 'cn_adv_group'): dialog.cn_adv_group.setTitle(lang[LangKeys.GRP_CN_ADV].strip())
    if hasattr(dialog, 'other_group'): dialog.other_group.setTitle(lang[LangKeys.GRP_OTHER].strip())
    if hasattr(dialog, 'connect_group'): dialog.connect_group.setTitle(lang[LangKeys.GRP_CONNECT].strip())

    # Etykiety (Labels) - przykłady dla kluczowych elementów
    if hasattr(dialog, 'lbl_prompt'): dialog.lbl_prompt.setText(lang[LangKeys.LBL_PROMPT].strip())
    if hasattr(dialog, 'lbl_neg_prompt'): dialog.lbl_neg_prompt.setText(lang[LangKeys.LBL_NEG_PROMPT].strip())
    if hasattr(dialog, 'lbl_steps'): dialog.lbl_steps.setText(lang[LangKeys.LBL_STEPS].strip())
    if hasattr(dialog, 'lbl_denoise'): dialog.lbl_denoise.setText(lang[LangKeys.LBL_DENOISING].strip())
    if hasattr(dialog, 'lbl_cfg'): dialog.lbl_cfg.setText(lang[LangKeys.LBL_CFG].strip())
    if hasattr(dialog, 'lbl_mode'): dialog.lbl_mode.setText(lang[LangKeys.LBL_CTRL_MODE].strip())
    if hasattr(dialog, 'lbl_resize'): dialog.lbl_resize.setText(lang[LangKeys.LBL_RESIZE_MODE].strip())

    # Przyciski
    if hasattr(dialog, 'btn_save_sets'): dialog.btn_save_sets.setText(lang[LangKeys.BTN_SAVE_SETTINGS].strip())
    if hasattr(dialog, 'btn_connect'): dialog.btn_connect.setText(lang[LangKeys.BTN_CONNECT].strip())

    # RadioButtony
    if hasattr(dialog, 'rb_balanced'): dialog.rb_balanced.setText(lang[LangKeys.RB_BALANCED].strip())
    if hasattr(dialog, 'rb_prompt'): dialog.rb_prompt.setText(lang[LangKeys.RB_PROMPT_IMP].strip())
    if hasattr(dialog, 'rb_cn'): dialog.rb_cn.setText(lang[LangKeys.RB_CN_IMP].strip())