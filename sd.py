from PIL import Image
import io
import base64
import urllib.request
import urllib.error
import socket
import json
from typing import List, Dict, Any, Optional
from PyQt5.QtWidgets import QMessageBox

def pil_to_base64(img_pil, fmt="PNG"):
    buf = io.BytesIO()
    img_pil.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def base64_to_pil(b64str):
    if "," in b64str:
        b64str = b64str.split(",", 1)[1]
    data = base64.b64decode(b64str)
    return Image.open(io.BytesIO(data)).convert("RGB")

def sd_inpaint_with_controlnet(window):
    try:
        #Pobranie parametrów z ustawień
        prompt = getattr(window, 'saved_prompt', "usuń obiekt i wypełnij tłem naturalnie")
        negative_prompt = getattr(window, 'saved_negative_prompt', "niska jakość, rozmycie, artefakty")
        steps = getattr(window, 'saved_steps', 25)
        denoising = getattr(window, 'saved_denoising', 0.7)
        cfg_scale = getattr(window, 'saved_cfg_scale', 7.0)
        model = getattr(window, 'saved_model', None)
        preprocessor = getattr(window, 'saved_preprocessor', 'inpaint_only')  #Poprawka: domyślny poprawny module dla Forge

        #Parametry ControlNet
        controlnet_model = getattr(window, 'saved_controlnet_model', None)
        control_weight = getattr(window, 'saved_control_weight', 1.0)
        guidance_start = getattr(window, 'saved_guidance_start', 0.0)
        guidance_end = getattr(window, 'saved_guidance_end', 1.0)
        processor_res = getattr(window, 'saved_processor_res', 512)
        threshold_a = getattr(window, 'saved_threshold_a', 64)
        threshold_b = getattr(window, 'saved_threshold_b', 64)
        control_mode = getattr(window, 'saved_control_mode', 0)
        resize_mode = getattr(window, 'saved_resize_mode', 1)
        pixel_perfect = getattr(window, 'saved_pixel_perfect', False)
        lowvram = getattr(window, 'saved_lowvram', False)

        #Seed
        use_random_seed = getattr(window, 'saved_use_random_seed', True)
        seed = -1 if use_random_seed else getattr(window, 'saved_seed', -1)

        #Konwersja obrazów do base64
        init_b64 = pil_to_base64(window.image)
        mask_b64 = pil_to_base64(window.mask.convert("L"))

  
        masked_image = window.image.copy()
        masked_image.putalpha(window.mask)  #maska jako alfa jako alpha
        masked_b64 = pil_to_base64(masked_image, fmt="PNG")

        #Konfiguracja ControlNet unit
        controlnet_unit = {
            "enabled": True,
            "input_image": masked_b64,e
            "mask": "", 
            "model": controlnet_model or "control_v11p_sd15_inpaint [ebff9138]",
            "module": preprocessor,  
            "weight": control_weight,
            "resize_mode": resize_mode,
            "low_vram": lowvram,  #'low_vram' zamiast 'lowvram'
            "processor_res": processor_res,
            "threshold_a": threshold_a,
            "threshold_b": threshold_b,
            "guidance_start": guidance_start,
            "guidance_end": guidance_end,
            "control_mode": control_mode,
            "pixel_perfect": pixel_perfect,
            "hr_option": "Both"  #obsługa high-res
        }


        sd_url = getattr(window, 'saved_sd_url', 'http://127.0.0.1:7860')

        payload = {
            "init_images": [init_b64],
            "mask": mask_b64,
            "inpaint_full_res": True,
            "inpaint_full_res_padding": 32,
            "inpainting_mask_invert": 0, 
            "denoising_strength": denoising,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "sampler_name": "DPM++ 2M Karras", #dodać więcej samplerów
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "seed": seed,
            "batch_size": 1,
            "width": window.image.width,
            "height": window.image.height,
            "alwayson_scripts": {"ControlNet": {"args": [controlnet_unit]}}
        }

        if model:
            payload["override_settings"] = {"sd_model_checkpoint": model} 

        ###############BEGGUING USUNĄC!
        #Wysłanie żądania z loggingiem
        print("Payload wysłany do SD Forge:", json.dumps(payload, indent=2))  #debugging
        req = urllib.request.Request(
            url=f"{sd_url}/sdapi/v1/img2img",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=600) as resp:
            body = resp.read().decode("utf-8")
            result = json.loads(body)

            if "images" in result and result["images"]:
                out_img = base64_to_pil(result["images"][0])
                if out_img.size != window.image.size:
                    out_img = out_img.resize(window.image.size, Image.Resampling.LANCZOS)
                window.image = out_img
                window.mask = Image.new("L", window.image.size, 0)
                # Aktualizacja wyświetlania
                if hasattr(window, 'draw_image'):
                    window.draw_image()
                QMessageBox.information(window, "Sukces", "Inpainting zakończony pomyślnie!")
            else:
                QMessageBox.critical(window, "Błąd", "Brak wyniku z SD API.")

    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode('utf-8')
        except Exception:
            err_body = ''
        QMessageBox.critical(window, "Błąd SD", f"HTTP error {e.code}: {err_body or e.reason}")
    except urllib.error.URLError as e:
        QMessageBox.critical(window, "Błąd SD", f"URL error: {e.reason}")
    except Exception as e:
        QMessageBox.critical(window, "Błąd SD", f"Wystąpił błąd: {str(e)}")

class SDClient:
    def __init__(self, base_url: str = "http://127.0.0.1:7860", timeout: int = 5):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def _get_json(self, path: str) -> Any:
        url = f"{self.base_url}{path}"
        req = urllib.request.Request(url, headers={"User-Agent": "RemoveFromPhoto SDClient/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = resp.read().decode('utf-8')
                return json.loads(data)
        except urllib.error.HTTPError as e:
            raise ConnectionError(f"HTTP error {e.code} when requesting {url}")
        except urllib.error.URLError as e:
            raise ConnectionError(f"URL error when requesting {url}: {e.reason}")
        except socket.timeout:
            raise TimeoutError(f"Timeout after {self.timeout}s when requesting {url}")
        except json.JSONDecodeError:
            raise ValueError(f"Received non-JSON response from {url}")

    def list_models(self) -> List[str]:
        data = self._get_json('/sdapi/v1/sd-models')
        models: List[str] = []
        if isinstance(data, list):
            for m in data:
                if isinstance(m, dict):
                    name = m.get('model_name') or m.get('title') or m.get('name') or m.get('model')
                    if name:
                        models.append(name)
        return models

    def list_controlnets(self) -> List[str]:

        try:
            data = self._get_json('/controlnet/model_list')
            items = data.get('model_list', [])
            cns: List[str] = [item for item in items if isinstance(item, str)]
            return cns
        except Exception:
            return []

    def list_modules(self) -> List[str]:  #Pobierz listę modułów (preprocessors)
        try:
            data = self._get_json('/controlnet/module_list')
            items = data.get('module_list', [])
            return [item for item in items if isinstance(item, str) and 'inpaint' in item.lower()]
        except Exception:
            return ['inpaint_only', 'inpaint_only+lama', 'none']

def connect_sd(window=None, url: Optional[str] = None, timeout: int = 5) -> Dict[str, Any]:
    base = url or 'http://127.0.0.1:7860'
    client = SDClient(base_url=base, timeout=timeout)
    models = []
    controlnets = []
    modules = []
    try:
        models = client.list_models()
    except Exception as e:
        result = {'ok': False, 'models': [], 'controlnets': [], 'modules': [], 'error': str(e)}
        if window is not None:
            window.sd_connected = False
            window.sd_client = None
        return result
    try:
        controlnets = client.list_controlnets()
        modules = client.list_modules()  #Pobierz moduły
    except Exception:
        pass
    if window is not None:
        window.saved_models = models
        window.saved_controlnets = controlnets
        window.saved_modules = modules  #Zapisz 
        window.sd_connected = True
        window.sd_client = client
        # Aktualizacja UI
        if hasattr(window, "model_combo"):
            window.model_combo.clear()
            window.model_combo.addItems(models or ["Brak modeli"])
        if hasattr(window, "control_combo"):
            window.control_combo.clear()
            window.control_combo.addItems(controlnets or ["Brak ControlNet"])
        if hasattr(window, "prep_combo"):
            window.prep_combo.clear()
            window.prep_combo.addItems(modules or ["inpaint_only"]) 
    return {'ok': True, 'models': models, 'controlnets': controlnets, 'modules': modules, 'error': ''}
