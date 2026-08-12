import cv2
import time
from ultralytics import YOLO
import os

# --- Konfiguracja: tu zmieniasz źródło i klasy ---
SOURCE = "data/highway.mp4"   # 0 = kamerka (ludzie)
CLASSES = [2, 3, 5, 7]         # pojazdy; dla ludzi ustaw [0]

model = YOLO("yolo26n.pt")

cap = cv2.VideoCapture(SOURCE)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.release()
LINE_Y = h // 2

prev_cy, counted = {}, set()
count_up, count_down = 0, 0

results = model.track(source=SOURCE, tracker="bytetrack.yaml",
                      persist=True, stream=True, classes=CLASSES, device=0)

cv2.namedWindow("Licznik", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Licznik", 1280, 720)

os.makedirs("runs", exist_ok=True)
writer = cv2.VideoWriter("runs/detect/demo.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (w, h))
prev_t = time.time()

for r in results:
    frame = r.orig_img
    cv2.line(frame, (0, LINE_Y), (w, LINE_Y), (255, 0, 255), 2)

    if r.boxes.id is not None:
        boxes = r.boxes.xyxy.cpu().numpy()
        ids = r.boxes.id.int().cpu().tolist()
        for (x1, y1, x2, y2), tid in zip(boxes, ids):
            cy = int((y1 + y2) / 2)

            if tid in prev_cy and tid not in counted:
                if (prev_cy[tid] - LINE_Y) * (cy - LINE_Y) < 0:
                    if cy > prev_cy[tid]:      # środek zjechał w dół
                        count_down += 1
                    else:                      # środek pojechał w górę
                        count_up += 1
                    counted.add(tid)
            prev_cy[tid] = cy

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, str(tid), (int(x1), int(y1) - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.putText(frame, f"W dol: {count_down}   W gore: {count_up}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    now = time.time()
    fps = 1.0 / (now - prev_t) if now > prev_t else 0.0
    prev_t = now
    cv2.putText(frame, f"FPS: {fps:.1f}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    writer.write(frame)
    
    cv2.imshow("Licznik", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
writer.release()
cv2.destroyAllWindows()