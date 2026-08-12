"""Konfiguracja projektu w jednym miejscu.

Zmieniając wartości tutaj, przełączasz cały pipeline (np. z pojazdów na ludzi)
bez dotykania logiki w pozostałych modułach.
"""

MODEL = "yolo26n.pt"            # wagi modelu (nano - pod 4 GB VRAM)
SOURCE = "data/highway.mp4"     # ścieżka do wideo albo 0 = kamerka
CLASSES = [2, 3, 5, 7]          # COCO: car, motorcycle, bus, truck; dla ludzi = [0]
TRACKER = "bytetrack.yaml"      # konfiguracja trackera
DEVICE = 0                      # 0 = GPU, "cpu" = CPU
LINE_RATIO = 0.5                # pozycja linii jako ułamek wysokości kadru
OUTPUT = "runs/demo.mp4"        # gdzie zapisać nagranie demo
