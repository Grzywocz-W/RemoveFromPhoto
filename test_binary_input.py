import io
import base64
import unittest
from PIL import Image
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import sd
import helpers


def make_png_bytes(color=(255, 0, 0), size=(8, 8)):
    img = Image.new('RGB', size, color)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


class BinaryInputTests(unittest.TestCase):
    def test_bytes_to_pil_image_roundtrip(self):
        b = make_png_bytes((10, 20, 30), (4, 5))
        img = helpers.bytes_to_pil_image(b)
        self.assertEqual(img.size, (4, 5))
        self.assertEqual(img.mode, 'RGB')

    def test_bytes_to_mask_image(self):
        img = Image.new('L', (4, 4), 128)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        mask_b = buf.getvalue()
        m = helpers.bytes_to_mask_image(mask_b)
        self.assertEqual(m.mode, 'L')
        self.assertEqual(m.size, (4, 4))

    def test_sdclient_inpaint_bytes_patched(self):
        # Przygotowanie fake'owego obrazu wynikowego
        out_img = Image.new('RGB', (2, 2), (1, 2, 3))
        ob = io.BytesIO()
        out_img.save(ob, format='PNG')
        out_b64 = base64.b64encode(ob.getvalue()).decode('utf-8')

        def fake_send_request(base_url, method, path, json_body=None, headers=None, timeout=5):
            self.assertEqual(method, 'POST')
            self.assertTrue(path.endswith('/img2img') or path == '/sdapi/v1/img2img')
            return {'images': [out_b64]}

        # Podmieniamy (mock) funkcję send_request z modułu
        sd.send_request = fake_send_request

        client = sd.SDClient('http://127.0.0.1:7860', timeout=2)
        img_bytes = make_png_bytes((9, 9, 9), (2, 2))
        mask_bytes = make_png_bytes((255, 255, 255), (2, 2))
        res = client.inpaint_bytes(img_bytes, mask_bytes)
        self.assertEqual(res.size, (2, 2))
        self.assertEqual(res.getpixel((0, 0)), (1, 2, 3))


if __name__ == '__main__':
    unittest.main()
