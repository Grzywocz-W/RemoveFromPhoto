from enum import Enum
import os

def load_from_file(window):
    config_file = "config.txt"
    if not os.path.exists(config_file):
        #print("Ustawienia domyślne")
        return
    
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
       
        
        settings = []
        for line in lines:
            settings.append(line.strip())

        
        if len(settings) < len(conf_sett):
            #print("Corrupted file")
            return
            
        window.saved_sd_url = settings[conf_sett.url.value]

        try:
            tool_id = int(settings[conf_sett.tool.value])
            tool_indx = window.tool_combo.findData(tool_id)
            if tool_indx in [0,1]:
                window.tool_combo.setCurrentIndex(tool_indx)
        except ValueError:
            pass

        try:
            method_id = int(settings[conf_sett.inpaint_method.value])
            method_idx = window.fill_combo.findData(method_id)
            if method_idx in [0,1,2,3,4]:
                window.fill_combo.setCurrentIndex(method_idx)
        except ValueError:
            pass


        window.saved_prompt = settings[conf_sett.prompt.value]
        

        window.saved_negative_prompt = settings[conf_sett.negative_prompt.value]

        try:
            window.saved_steps = int(settings[conf_sett.steps.value])
        except ValueError:
            window.saved_steps = 25

        try:
            window.saved_denoising = float(settings[conf_sett.denoising.value])
        except ValueError:
            window.saved_denoising = 0.7

        try:
            window.saved_cfg_scale = float(settings[conf_sett.cfg_scale.value])
        except ValueError:
            window.saved_cfg_scale = 7.0

        try:
            window.current_lang_file = settings[conf_sett.language.value]
        except Exception:
            window.current_lang_file = "ENG_RFP.txt"


    except Exception as e:
        print(f"Error {e}")
                
            

def save_config(window):
    config_file = "config.txt"
    url = getattr(window, 'saved_sd_url', "Brak URL")

    
    dzejson = ""

    #first)lauch
    dzejson += "0" + "\n"

    #url
    dzejson += url + "\n"

    #tool
    tool_combo = getattr(window, 'tool_combo', None)
    tool_id = tool_combo.currentData()
    dzejson += str(tool_id) + "\n"

    #fill
    fill_combo = getattr(window, 'fill_combo', None)
    fill_id = fill_combo.currentData()
    dzejson += str(fill_id) + "\n"

    prompt = getattr(window, 'saved_prompt')
    dzejson += str(prompt) + "\n"
    
    negative_prompt = getattr(window, 'saved_negative_prompt')
    dzejson += str(negative_prompt) + "\n"
    
    steps = getattr(window, 'saved_steps')
    dzejson += str(steps) + "\n"
    
    denoising = getattr(window, 'saved_denoising')
    dzejson += str(denoising) + "\n"
    
    cfg_scale = getattr(window, 'saved_cfg_scale')
    dzejson += str(cfg_scale) + "\n"

    current_lang = getattr(window, 'current_lang_file', "ENG_RFP.txt")
    dzejson += str(current_lang) + "\n"
    
    
    print(dzejson)
    with open(config_file, "w", encoding="utf-8") as save:
        save.write(dzejson)


def language_version(window,file = "ENG_RFP.txt"):
    #l_file = open("Language/ENG_RFP.txt",'r',encoding="utf-8")
    #l_file = open("Language/PL_RFP.txt",'r',encoding="utf-8")
    if not file:
        file = "ENG_RFP.txt"

    window.current_lang_file = file
    
    file =  f"Language/{file}"

    with open(file, 'r', encoding="utf-8") as l_file:
        lang = l_file.readlines()

    try:
        if len(lang) >= 92:#75 to długość tego pliku. Jak coś dodajecie to zmieńcie wartość
##            for linie in lang:
##                if linie:
##                    print(linie.strip())
            #### BEZ tego nie zedytujemy okna settings
            window.lang_data = lang
            window.setWindowTitle(lang[LangKeys.WINDOW_TITLE].strip())
            ####### DAJCIE stripy, bo inaczej przyciski się psują

            window.tool_label.setText(lang[LangKeys.LBL_TOOL].strip())
            window.fill_label.setText(lang[LangKeys.LBL_FILL].strip())

            window.tool_combo.setItemText(0, lang[LangKeys.TOOL_LASSO].strip())
            window.tool_combo.setItemText(1, lang[LangKeys.TOOL_BRUSH].strip())


            #ComboBox - Wypełnienie
            window.fill_combo.setItemText(0, lang[LangKeys.FILL_NEIGHBOR].strip())
            window.fill_combo.setItemText(1, lang[LangKeys.FILL_EMPTY].strip())
            window.fill_combo.setItemText(2, lang[LangKeys.FILL_SD].strip())
            window.fill_combo.setItemText(3, lang[LangKeys.FILL_CRIMINISI].strip())
            window.fill_combo.setItemText(4, lang[LangKeys.FILL_TELEA].strip())
            window.fill_combo.setItemText(5, lang[LangKeys.FILL_AUTO].strip())

            #Buttony
            window.btn_open.setText(lang[LangKeys.BTN_OPEN].strip())
            window.btn_erase.setText(lang[LangKeys.BTN_ERASE].strip())
            window.btn_save.setText(lang[LangKeys.BTN_SAVE].strip())
            window.btn_reset.setText(lang[LangKeys.BTN_RESET].strip())
            window.btn_undo.setText(lang[LangKeys.BTN_UNDO].strip())
            window.btn_settings.setText(lang[LangKeys.BTN_SETTINGS].strip())

            #Labele
            window.brush_label.setText(lang[LangKeys.LBL_BRUSH_SIZE].strip())
            window.scale_label.setText(lang[LangKeys.LBL_SCALE].strip())
        #else:
            
    except Exception as e:
        print(f'language_version error {e}')


class conf_sett(Enum):
    first_launch = 0
    url = 1
    tool = 2
    inpaint_method = 3
    prompt = 4
    negative_prompt = 5
    steps = 6
    denoising = 7
    cfg_scale = 8
    language = 9




from enum import IntEnum, auto

class LangKeys(IntEnum):
    #Główne Okno (Main Window)
    WINDOW_TITLE = 0
    LBL_TOOL = 1
    TOOL_LASSO = 2
    TOOL_BRUSH = 3
    LBL_FILL = 4
    FILL_NEIGHBOR = 5
    FILL_EMPTY = 6
    FILL_SD = 7
    FILL_CRIMINISI = 8
    FILL_TELEA = 9
    FILL_AUTO = 10
    
    #Przyciski Główne
    BTN_OPEN = 11
    BTN_ERASE = 12
    BTN_SAVE = 13
    BTN_RESET = 14
    BTN_UNDO = 15
    BTN_SETTINGS = 16
    
    #Suwaki UI
    LBL_BRUSH_SIZE = 17
    LBL_SCALE = 18
    
    #Ustawienia (Settings Dialog)
    SETTINGS_TITLE = 19
    GRP_SD_SETTINGS = 20
    LBL_PROMPT = 21
    LBL_NEG_PROMPT = 22
    
    GRP_SD_PARAMS = 23
    LBL_STEPS = 24
    LBL_DENOISING = 25
    LBL_CFG = 26
    
    GRP_SEED = 27
    CB_RANDOM_SEED = 28
    LBL_SEED = 29
    
    GRP_MODELS = 30
    COMBO_NO_CONNECTION = 31
    LBL_SD_MODEL = 32
    COMBO_NO_CONTROLNET = 33
    LBL_CN_MODEL = 34
    LBL_PREPROCESSOR = 35
    
    GRP_CN_ADV = 36
    LBL_WEIGHT = 37
    LBL_G_START = 38
    LBL_G_END = 39
    LBL_PROC_RES = 40
    LBL_THRESH_A = 41
    LBL_THRESH_B = 42
    
    LBL_CTRL_MODE = 43
    RB_BALANCED = 44
    RB_PROMPT_IMP = 45
    RB_CN_IMP = 46
    
    LBL_RESIZE_MODE = 47
    RB_JUST_RESIZE = 48
    RB_CROP_RESIZE = 49
    RB_RESIZE_FILL = 50
    
    CB_PIXEL_PERF = 51
    CB_LOW_VRAM = 52
    
    GRP_OTHER = 53
    CB_TIMESTAMP = 54
    
    GRP_CONNECT = 55
    LBL_API_URL = 56
    BTN_CONNECT = 57
    COMBO_NO_MODELS = 58
    BTN_SAVE_SETTINGS = 59
    
    #Komunikaty i Błędy (Messages)
    MSG_CONNECTED_TITLE = 60
    MSG_CONNECTED_BODY = 61
    MSG_CONN_ERR_TITLE = 62
    MSG_CONN_ERR_BODY = 63
    MSG_OK = 64
    MSG_SETTINGS_SAVED = 65
    MSG_ERR_TITLE = 66
    MSG_SAVE_ERR = 67
    MSG_SUCCESS_TITLE = 68
    MSG_INPAINT_DONE = 69
    MSG_NO_RESULT = 70
    MSG_SD_ERR_TITLE = 71
    MSG_GENERIC_ERR = 72
    
    #Wartości domyślne
    DEFAULT_PROMPT = 73
    DEFAULT_NEG_PROMPT = 74


    MSG_ERR_INVALID_SIZE = 75
    MSG_WARN_BIG_IMAGE = 76
    MSG_ERR_OPEN_FAIL = 77
    MSG_WARN_NO_IMG_SAVE = 78
    TITLE_SAVE_DIALOG = 79
    MSG_SAVED_PATH = 80
    MSG_WARN_LOAD_IMG = 81
    MSG_WARN_NO_SEL = 82
    STATUS_PROCESSING = 83
    STATUS_READY = 84
    MSG_WARN_CONNECT_FIRST = 85
    MSG_INFO_NO_UNDO = 86
    TITLE_OPEN_DIALOG = 87
    FILE_FILTER_IMG = 88
    GRP_LANGUAGE = 89
    LBL_BRUSH_NAME = 90
    LBL_SCALE_NAME = 91

