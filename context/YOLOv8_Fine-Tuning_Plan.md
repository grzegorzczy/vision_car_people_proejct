# Plan fine-tuningu YOLOv8 — projekt sortujący (Computer Vision)

Cel: przejść od pre-trenowanego `yolov8n` (COCO, klasy generyczne) do **własnego modelu wytrenowanego na realnych produktach z linii**, żeby mieć twarde metryki (mAP / precision / recall) do wpisania w CV i pokazania na rozmowie. To domyka jedyną słabość projektu ("nie trenowałeś własnego modelu").

## 1. Zbiór danych (dataset)

- Zdefiniuj **własne klasy** produktów, które realnie sortujesz (np. 3–6 klas zamiast mapowania na COCO).
- Nagraj krótkie wideo każdego produktu na taśmie/pod kamerą przy różnych: oświetleniach, kątach, tłach, pozycjach. Wyciągnij klatki (np. co N-tą) skryptem OpenCV.
- Cel na start: **~150–300 zdjęć na klasę** (transfer learning nie potrzebuje dziesiątek tysięcy). Im bardziej zróżnicowane, tym lepiej.
- Podział: **train / val / test ≈ 70 / 20 / 10**. Test trzymaj "na czysto" — służy tylko do finalnej metryki.

## 2. Etykietowanie (labeling)

- Narzędzia: **Roboflow** (najszybsze, eksport prosto do formatu YOLO), CVAT albo Label Studio.
- Format YOLO: jeden `.txt` na obraz, w każdej linii `class_id x_center y_center width height` (znormalizowane 0–1).
- Struktura: `dataset/images/{train,val,test}` + `dataset/labels/{train,val,test}` + plik `data.yaml` z listą klas.

## 3. Augmentacja

- Ultralytics ma wbudowaną augmentację (mosaic, flip, HSV, scale) — na start wystarczy domyślna.
- Dla realnej linii warto dołożyć: zmiany jasności/kontrastu (oświetlenie hali), lekki blur (ruch taśmy), losowe tła.

## 4. Trening (transfer learning)

```bash
# start od wag pre-trenowanych (nie od zera) — szybciej i mniej danych
yolo detect train \
  model=yolov8n.pt \
  data=dataset/data.yaml \
  epochs=100 \
  imgsz=640 \
  batch=16 \
  patience=20 \
  device=0            # GPU
```

- `yolov8n` = najszybszy (edge/real-time). Jeśli dokładność za niska, spróbuj `yolov8s`.
- `patience` = early stopping, gdy val przestaje się poprawiać.
- Monitoruj krzywe (loss, mAP) — Ultralytics zapisuje wykresy i `results.csv` w `runs/detect/train`.

## 5. Ewaluacja (metryki do CV)

```bash
yolo detect val model=runs/detect/train/weights/best.pt data=dataset/data.yaml split=test
```

Zapisz i zapamiętaj:

- **mAP@0.5** oraz **mAP@0.5:0.95** (główna metryka detekcji),
- **precision** i **recall** per klasa,
- **inference speed** (ms/klatkę na Twoim GPU) — masz już 30 FPS, potwierdź po fine-tuningu,
- confusion matrix (które klasy się mylą).

## 6. Wdrożenie do istniejącego projektu

- Podmień `MODEL_PATH` w `vision/config.py` na `best.pt`.
- Zaktualizuj `COCO_TO_OBJECT` / mapę klas — teraz model zwraca Twoje własne `class_id`, więc mapowanie się upraszcza (albo znika).
- Przetestuj cały pipeline (kamera → model → Modbus → Factory I/O) na modelu własnym.
- (Opcjonalnie) eksport do **ONNX / TensorRT** dla szybszej inferencji — kolejny mocny punkt w CV.

## 7. Co wpiszemy do CV po treningu

Zamień/rozszerz punkt flagowy o realne liczby, np.:

> „Trained a custom YOLOv8 object-detection model on a self-collected, hand-labeled dataset of N images across K product classes (transfer learning, data augmentation), reaching **mAP@0.5 = XX%** at 30 FPS on GPU."

To zamienia projekt z "odpaliłem gotowy YOLO" na "zbudowałem i wytrenowałem własny model" — duża różnica dla rekrutera CV/ML.

---

### Minimalny nakład, maksymalny efekt
Jeśli masz mało czasu: 3 klasy × 150 zdjęć, Roboflow do labelowania, 1 trening `yolov8n` 100 epok. To realnie 1–2 dni pracy, a daje Ci komplet metryk i historię "custom model training" w CV.
