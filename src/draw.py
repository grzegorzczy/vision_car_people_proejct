"""Rysowanie nakładek na klatce (OpenCV).

Osobny moduł, bo prezentacja to inna odpowiedzialność niż logika liczenia.
Dzięki temu łatwo zmienić wygląd bez ruszania reszty.
"""

import cv2


def draw_line(frame, line_y, w):
    cv2.line(frame, (0, line_y), (w, line_y), (255, 0, 255), 2)


def draw_boxes(frame, boxes, ids):
    for (x1, y1, x2, y2), tid in zip(boxes, ids):
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, str(tid), (int(x1), int(y1) - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


def draw_stats(frame, down, up, fps):
    cv2.putText(frame, f"W dol: {down}   W gore: {up}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, f"FPS: {fps:.1f}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
