# Real-Time People & Vehicle Counter (YOLO26 + ByteTrack)

Licznik ludzi i pojazdów w czasie rzeczywistym: system wykrywa obiekty na wideo lub
z kamerki, śledzi je z trwałym ID i zlicza przekroczenia wirtualnej linii — z podziałem
na kierunek. Działa na GPU, w architekturze modularnej.

## Demo

![Licznik ludzi i pojazdów w czasie rzeczywistym](assets/demo.gif)

*Detekcja YOLO26 + tracking ByteTrack: trwałe ID, kierunkowy licznik przekroczeń i FPS — na GPU.*

## Co robi

- Wykrywa obiekty modelem **YOLO26** (klasy COCO — np. `person`, `car`, `bus`, `truck`).
- Nadaje każdemu obiektowi **trwałe ID** (tracker **ByteTrack**), więc nie liczy go dwa razy.
- Liczy **przekroczenia wirtualnej linii** z rozróżnieniem kierunku (w górę / w dół).
- Pokazuje **FPS** i zapisuje nagranie wynikowe (`runs/demo.mp4`).
- Przełączenie między pojazdami a ludźmi = zmiana dwóch wartości w `src/config.py`.

## Jak to działa (pipeline)

```
źródło (wideo / kamerka)
        │
        ▼
Detector  ── YOLO26 + ByteTrack ──►  (klatka, ramki, ID)
        │
        ▼
LineCounter ── logika przecięcia linii, kierunek ──►  liczniki
        │
        ▼
draw ── nakładka (ramki, ID, liczniki, FPS) ──►  podgląd + zapis do pliku
```

## Stack

Python · **Ultralytics YOLO26** · **ByteTrack** · OpenCV · PyTorch (CUDA).
Testowane na NVIDIA GeForce RTX 3050 Ti Laptop (CUDA 12.6), inferencja ~60+ FPS.

## Struktura projektu

```
src/
├── config.py     # konfiguracja: model, źródło, klasy, pozycja linii
├── detector.py   # klasa Detector: YOLO26 + ByteTrack -> (klatka, ramki, ID)
├── counter.py    # klasa LineCounter: logika przecięcia linii + kierunek
├── draw.py       # rysowanie nakładek (OpenCV)
└── app.py        # spina wszystko w pętli (punkt wejścia)
```

## Uruchomienie

```bash
# 1. środowisko
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows (PowerShell)
pip install ultralytics
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126

# 2. konfiguracja w src/config.py
#    pojazdy:  SOURCE = "data/highway.mp4"   CLASSES = [2, 3, 5, 7]
#    ludzie:   SOURCE = 0                     CLASSES = [0]

# 3. uruchom (z katalogu projektu)
python -m src.app
```

Wynik: okno z detekcją, trwałymi ID, licznikiem kierunkowym i FPS; nagranie w `runs/demo.mp4`.
Zatrzymanie: klawisz `q`.

## Dokumentacja

- [`docs/instrukcja.md`](docs/instrukcja.md) — **pełny log komend krok po kroku** (setup → uruchomienie), z wyjaśnieniami.
- [`docs/05_projekt1_plan.md`](docs/05_projekt1_plan.md) — plan tego projektu (kroki 0.1–1.6).
- [`docs/01_architektura.md`](docs/01_architektura.md), [`docs/02_roadmap.md`](docs/02_roadmap.md),
  [`docs/03_stack_i_narzedzia.md`](docs/03_stack_i_narzedzia.md) — **szersza ścieżka rozwoju**
  (docelowy system edge-to-cloud: trening własnego modelu, TensorRT, streaming, DeepStream,
  Jetson, PLC). To plan nauki, **nie** funkcje tego repo.

## Status

**Ukończone:** działający, modularny licznik ludzi i pojazdów w czasie rzeczywistym.

Kolejne etapy ścieżki rozwoju (fine-tuning własnego modelu, optymalizacja TensorRT,
streaming zdarzeń, wdrożenie na Jetson) realizowane są w osobnych projektach.
