import sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

import sd

def main():
	url = 'http://127.0.0.1:7860'
	timeout = 3
	if len(sys.argv) >= 2:
		url = sys.argv[1]
	if len(sys.argv) >= 3:
		try:
			timeout = int(sys.argv[2])
		except Exception:
			pass

	res = sd.connect_sd(url=url, timeout=timeout, window=None)
	print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == '__main__':
	main()
