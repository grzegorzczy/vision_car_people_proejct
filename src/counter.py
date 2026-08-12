"""Logika biznesowa: licznik przecięć poziomej linii, z kierunkiem.

Klasa trzyma stan (poprzednie pozycje, już policzone ID), więc pamięta obiekty
między klatkami. Nie wie nic o modelu ani o rysowaniu - dostaje gotowe boxes/ids.
"""


class LineCounter:
    def __init__(self, line_y):
        self.line_y = line_y
        self.prev_cy = {}     # id -> poprzednie Y środka
        self.counted = set()  # id już policzone (żeby nie liczyć dwa razy)
        self.down = 0
        self.up = 0

    def update(self, boxes, ids):
        for (x1, y1, x2, y2), tid in zip(boxes, ids):
            cy = int((y1 + y2) / 2)
            if tid in self.prev_cy and tid not in self.counted:
                # zmiana znaku (cy - line_y) = przecięcie linii
                if (self.prev_cy[tid] - self.line_y) * (cy - self.line_y) < 0:
                    if cy > self.prev_cy[tid]:
                        self.down += 1
                    else:
                        self.up += 1
                    self.counted.add(tid)
            self.prev_cy[tid] = cy
