"""Detekcja + tracking w jednym miejscu (YOLO26 + ByteTrack).

Ultralytics łączy detekcję i tracking w metodzie `track`, więc trzymamy to razem.
Moduł nie wie nic o liczeniu ani rysowaniu - zwraca tylko surowe dane na klatkę.
"""

from ultralytics import YOLO


class Detector:
    def __init__(self, model, tracker, classes, device):
        self.model = YOLO(model)
        self.tracker = tracker
        self.classes = classes
        self.device = device

    def stream(self, source):
        """Generator: dla każdej klatki zwraca (frame, boxes, ids)."""
        results = self.model.track(
            source=source,
            tracker=self.tracker,
            classes=self.classes,
            persist=True,       # pamiętaj ID między klatkami
            stream=True,        # przetwarzaj klatka po klatce
            device=self.device,
            verbose=False,      # mniej logów w konsoli
        )
        for r in results:
            frame = r.orig_img
            if r.boxes.id is not None:
                boxes = r.boxes.xyxy.cpu().numpy()
                ids = r.boxes.id.int().cpu().tolist()
            else:
                boxes, ids = [], []
            yield frame, boxes, ids
