import importlib.util
import sys


REQUIRED_LIBS = {
    "PyQt5": "PyQt5",
    "PIL": "Pillow",
    "cv2": "opencv-python",
    "numpy": "numpy",
    "requests": "requests"
}

def check_dependencies():
    missing = []
    
    
    for import_name, install_name in REQUIRED_LIBS.items():
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            print(f" Missing: {install_name}, install: pip instal {install_name}")
            missing.append(install_name)
    #print(f" [V] OK: {install_name}")

