from ultralytics import YOLO

# 1. Wczytaj gotowy model YOLO26 (wariant nano - najlżejszy, pod 4 GB VRAM)
model = YOLO("yolo26n.pt")

# 2. Detekcja na obrazie; device=0 = licz na GPU; save=True zapisuje obraz z ramkami
results = model.predict(source="https://ultralytics.com/images/bus.jpg", device=0, save=True)

# 3. Wypisz, co model wykrył
for r in results:
    for box in r.boxes:
        cls_id = int(box.cls[0])       # numer klasy
        name = model.names[cls_id]     # nazwa klasy, np. 'person'
        conf = float(box.conf[0])      # pewność detekcji 0-1
        print(f"{name}: {conf:.2f}")