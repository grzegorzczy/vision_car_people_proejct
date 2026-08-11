# -*- coding: utf-8 -*-
"""
check_env.py — diagnostyka srodowiska (Faza 0).

Jedno polecenie sprawdza, czy wszystkie klocki sa na miejscu:
Python, PyTorch + CUDA (GPU), OpenCV, Ultralytics, Flask, pymodbus
oraz poprawnosc kontraktu w config.py.

Uruchomienie (z katalogu projektu, aktywny venv):
    python check_env.py
"""

import sys

OK = "[ OK ]"
FAIL = "[FAIL]"
WARN = "[WARN]"


def check_import(label, import_fn):
    try:
        info = import_fn()
        print(f"{OK}  {label}: {info}")
        return True
    except Exception as e:
        print(f"{FAIL}  {label}: {e}")
        return False


def main():
    print("=" * 60)
    print(" DIAGNOSTYKA SRODOWISKA — Vision + variTRON 300")
    print("=" * 60)
    print(f"[INFO] Python: {sys.version.split()[0]}  ({sys.executable})")
    print("-" * 60)

    results = []

    # --- PyTorch + CUDA (najwazniejsze: inferencja na GPU) ---
    def _torch():
        import torch
        cuda = torch.cuda.is_available()
        gpu = torch.cuda.get_device_name(0) if cuda else "brak (CPU)"
        return f"torch {torch.__version__} | CUDA dostepne: {cuda} | GPU: {gpu}"
    results.append(check_import("PyTorch/CUDA", _torch))

    # --- OpenCV ---
    def _cv2():
        import cv2
        return f"opencv {cv2.__version__}"
    results.append(check_import("OpenCV", _cv2))

    # --- Ultralytics (YOLOv8) ---
    def _ultra():
        import ultralytics
        return f"ultralytics {ultralytics.__version__}"
    results.append(check_import("Ultralytics", _ultra))

    # --- Flask (dashboard, Faza 5) ---
    def _flask():
        import flask  # noqa: F401 (sprawdzamy sam import)
        # Zalecane zamiast flask.__version__ (wycofywane w Flask 3.2):
        from importlib.metadata import version
        return f"flask {version('flask')}"
    results.append(check_import("Flask", _flask))

    # --- pymodbus (klient Modbus, Faza 3) ---
    def _modbus():
        import pymodbus
        return f"pymodbus {pymodbus.__version__}"
    results.append(check_import("pymodbus", _modbus))

    # --- Kontrakt: config.py ---
    def _config():
        from vision import config
        n_cls = len(config.OBJECT_NAMES)
        n_coco = len(config.COCO_TO_OBJECT)
        regs = (config.REG_OBJECT_CODE, config.REG_CONFIDENCE, config.REG_DETECTION_COUNT)
        return (f"klasy={n_cls}, mapa COCO={n_coco}, rejestry HR={regs}, "
                f"host={config.MODBUS_HOST}:{config.MODBUS_PORT}, prog={config.CONFIDENCE_THRESHOLD}")
    results.append(check_import("config.py (kontrakt)", _config))

    print("-" * 60)
    passed = sum(results)
    total = len(results)
    if passed == total:
        print(f"{OK}  WSZYSTKO GOTOWE: {passed}/{total} testow zaliczonych.")
    else:
        print(f"{WARN}  {passed}/{total} zaliczonych — uzupelnij brakujace pakiety powyzej.")
    print("=" * 60)


if __name__ == "__main__":
    main()
