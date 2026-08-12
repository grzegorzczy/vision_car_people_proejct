import cv2
from ultralytics import solutions

# 1. Otwórz wideo
cap = cv2.VideoCapture("data/highway.mp4")
assert cap.isOpened(), "Nie moge otworzyc wideo"

# 2. Odczytaj rozmiar klatki (żeby linię dopasować do wideo)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 3. Linia pozioma w połowie wysokości, przez całą szerokość
line_points = [(0, h // 2), (w, h // 2)]

# 4. Konfiguracja licznika
counter = solutions.ObjectCounter(
    model="yolo26n.pt",
    region=line_points,
    classes=[2, 3, 5, 7],   # COCO: car, motorcycle, bus, truck
    show=True,
    device=0,
)

# 5. Pętla po klatkach — licznik sam rysuje ramki, linię i wyniki
while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break
    counter(frame)

cap.release()
cv2.destroyAllWindows()