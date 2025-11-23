from PIL import Image
import io
import base64
import urllib.request
import urllib.error
import socket
import json
from typing import List, Dict, Any, Optional

def sd_inpaint(img, mask, prompt, negative_prompt, steps, denoising, cfg_scale, model, preprocessor):
    import base64
    from io import BytesIO
    import json
    import urllib.request

    # konwersja obrazu + maski na base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    buffered_mask = BytesIO()
    mask.save(buffered_mask, format="PNG")
    mask_b64 = base64.b64encode(buffered_mask.getvalue()).decode()

    payload = {
        "mask": mask_b64,
        "init_images": [img_b64],
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": steps,
        "denoising_strength": denoising,
        "cfg_scale": cfg_scale,
    }

    if model:
        try:
            payload["sd_model_checkpoint"] = model
        except Exception:
            pass

    payload.setdefault("inpaint_full_res", True)
    payload.setdefault("inpaint_full_res_padding", 0)

    if "inpainting_fill" not in payload:
        payload["inpainting_fill"] = 1
    payload.setdefault("mask_blur", 4)
    payload.setdefault("resize_mode", 0)

    if preprocessor:
        try:
            payload.setdefault("alwayson_scripts", {})
            payload["alwayson_scripts"].setdefault("controlnet", {})
            payload["alwayson_scripts"]["controlnet"]["args"] = [
                {
                    "enabled": True,
                    "model": preprocessor,
                    "module": "inpaint",
                    "input_image": mask_b64,
                    "weight": 1.0
                }
            ]
        except Exception:
            pass

    req = urllib.request.Request(
        url="http://127.0.0.1:7860/sdapi/v1/img2img",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            try:
                r = json.loads(body)
            except Exception:
                raise ValueError(f"Non-JSON response from SD API: {body}")

            if not isinstance(r, dict) or "images" not in r:
                raise ValueError(f"Unexpected response from SD API: {r}")

            img_b64_out = r["images"][0]
            if "," in img_b64_out:
                img_b64_out = img_b64_out.split(",", 1)[1]
            img_out = Image.open(BytesIO(base64.b64decode(img_b64_out)))
            return img_out
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode('utf-8')
        except Exception:
            err_body = ''
        raise ConnectionError(f"HTTP error {e.code} when requesting img2img: {err_body or e.reason}")
    except urllib.error.URLError as e:
        raise ConnectionError(f"URL error when requesting img2img: {e.reason}")



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
        endpoints = ['/controlnet/model_list', '/controlnet/models', '/sdapi/v1/controlnet/model_list']
        for ep in endpoints:
            try:
                data = self._get_json(ep)

                items = None
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict):
                    for k in ('model_list', 'models', 'controlnets', 'modelList'):
                        if k in data and isinstance(data[k], list):
                            items = data[k]
                            break
                    if items is None:
                        for v in data.values():
                            if isinstance(v, list):
                                items = v
                                break

                if not items:
                    continue

                cns: List[str] = []
                for item in items:
                    name = None
                    if isinstance(item, str):
                        name = item
                    elif isinstance(item, dict):
                        name = item.get('name') or item.get('model_name') or item.get('title') or item.get('label')
                    if isinstance(name, str):
                        if ' [' in name and name.strip().endswith(']'):
                            name = name.rsplit(' [', 1)[0]
                        cns.append(name)
                return cns
            except Exception:
                continue
        return []


def connect_sd(window=None, url: Optional[str] = None, timeout: int = 5) -> Dict[str, Any]:
    """
    Łączy z API Stable Diffusion WebUI, pobiera listę modeli i ControlNetów.
    Zwraca dict: { 'ok': bool, 'models': [...], 'controlnets': [...], 'error': str }
    """
    base = url or 'http://127.0.0.1:7860'
    client = SDClient(base_url=base, timeout=timeout)

    models = []
    controlnets = []
    try:
        data = client._get_json('/sdapi/v1/sd-models')
        if isinstance(data, list):
            for m in data:
                if isinstance(m, dict):
                    name = m.get('model_name') or m.get('title') or m.get('name') or m.get('model')
                    if name:
                        models.append(name)
                elif isinstance(m, str):
                    models.append(m)

    except Exception as e:
        # ERROR
        result = {'ok': False, 'models': [], 'controlnets': [], 'error': str(e)}
        if window is not None:
            window.sd_connected = False
            window.sd_client = None
        return result

    if window is not None:
        window.saved_models = models


    try:
        controlnets = client.list_controlnets()
    except Exception:
        controlnets = []

    if window is not None:
        try:
            window.saved_controlnets = controlnets
        except Exception:
            pass

    # --- Aktualizacja UI, jeśli działa GUI ---
    if window is not None:
        window.sd_connected = True
        window.sd_client = client

        # MODELE SD
        if hasattr(window, "model_combo"):
            window.model_combo.clear()
            if models:
                for m in models:
                    window.model_combo.addItem(m)
            else:
                window.model_combo.addItem("Brak modeli wykrytych")

        # CONTROLNET
        if hasattr(window, "prep_combo"):
            window.prep_combo.clear()
            if controlnets:
                for c in controlnets:
                    window.prep_combo.addItem(c)
            else:
                window.prep_combo.addItem("Brak ControlNet")

    return {'ok': True, 'models': models, 'controlnets': controlnets, 'error': ''}



