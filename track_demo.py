from ultralytics import YOLO

model = YOLO("yolo26n.pt")

# track zamiast predict; persist=True = pamiętaj ID między klatkami
# stream=True = przetwarzaj klatka po klatce (oszczędza pamięć na wideo)
results = model.track(
    source="data/traffic.mp4",
    tracker="bytetrack.yaml",
    persist=True,
    stream=True,
    show=True,
    device=0,
)

for r in results:
    if r.boxes.id is not None:              # czy są śledzone obiekty
        ids = r.boxes.id.int().tolist()     # lista ID w tej klatce
        print("Sledzone ID:", ids)