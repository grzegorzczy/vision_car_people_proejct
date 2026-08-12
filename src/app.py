"""Punkt wejścia - spina wszystkie moduły w jeden pipeline.

Uruchom z katalogu projektu:  python -m src.app
"""

import os
import time

import cv2

from src import config
from src import draw
from src.detector import Detector
from src.counter import LineCounter


def get_frame_size(source):
    """Odczytaj szerokość/wysokość źródła (do ustawienia linii i zapisu)."""
    cap = cv2.VideoCapture(source)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return w, h


def main():
    w, h = get_frame_size(config.SOURCE)
    line_y = int(h * config.LINE_RATIO)

    detector = Detector(config.MODEL, config.TRACKER, config.CLASSES, config.DEVICE)
    counter = LineCounter(line_y)

    os.makedirs("runs", exist_ok=True)
    writer = cv2.VideoWriter(config.OUTPUT, cv2.VideoWriter_fourcc(*"mp4v"), 30, (w, h))

    cv2.namedWindow("Licznik", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Licznik", 1280, 720)

    prev_t = time.time()
    for frame, boxes, ids in detector.stream(config.SOURCE):
        counter.update(boxes, ids)

        now = time.time()
        fps = 1.0 / (now - prev_t) if now > prev_t else 0.0
        prev_t = now

        draw.draw_line(frame, line_y, w)
        draw.draw_boxes(frame, boxes, ids)
        draw.draw_stats(frame, counter.down, counter.up, fps)

        writer.write(frame)
        cv2.imshow("Licznik", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    writer.release()
    cv2.destroyAllWindows()
    print(f"Podsumowanie -> w dol: {counter.down}, w gore: {counter.up}")


if __name__ == "__main__":
    main()
