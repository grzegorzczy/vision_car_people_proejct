# Roadmap: projekt douczeniowy pod „NVIDIA Edge AI / Real-Time Data Specialist"

Cel: **jeden projekt od A do Z**, który przeprowadzi Cię przez wszystkie must-have z oferty i zamieni linijkę „Currently learning" w realny, pokazywalny projekt z liczbami. Bazujemy na tym, co już masz: aplikacja z folderu `wizja` (real-time YOLO + dashboard) oraz konto na **Ultralytics Platform** z datasetem `jumo devices 2` (52 zdjęcia, 4 klasy) i modelem `yolo26n-seg`.

Wszystko odpala się na Twoim laptopie (RTX 3050, dGPU x86) — **nie potrzebujesz Jetsona**. TensorRT i DeepStream działają na desktopowym GPU NVIDIA. Ultralytics Platform jest na darmowym planie, więc pilnuj limitów (masz 100 GB storage, 3 deploymenty).

---

## Projekt: „Edge Vision Analytics"

Real-time'owy serwis analityki wideo, który:

1. **wykrywa i liczy/śledzi** obiekty ze strumienia z kamery (Twój dataset `jumo devices`, albo cokolwiek),
2. działa na modelu **zoptymalizowanym TensorRT** (FP16/INT8),
3. jest podawany przez **pipeline strumieniowy** (DeepStream lub własny, wielostrumieniowy),
4. **publikuje zdarzenia do brokera** (Kafka/MQTT) i dalej do **dashboardu w chmurze** (edge-to-cloud),
5. jest w całości **skonteneryzowany** (Docker) z prostym MLOps.

To jest jeden do jednego to, co robi „NVIDIA Edge AI / Real-Time Data Specialist".

### Jak projekt pokrywa wymagania oferty

| Wymaganie z oferty (must-have) | Faza, która to realizuje |
|---|---|
| NVIDIA GPU: CUDA, **TensorRT**, **DeepStream** | Faza 3 (TensorRT) + Faza 4 (DeepStream) |
| Edge AI / real-time / streaming inference | Faza 2–4 |
| Computer vision + dane sensorowe/telemetryczne | Faza 1–2 (CV) + Faza 7 (telemetria, opcjonalnie) |
| Architektura **edge-to-cloud** | Faza 5 |
| Wdrażanie modeli AI na produkcję | Faza 3 + Faza 6 |
| Wzorce real-time / **event-driven** | Faza 5 |
| Integracja AI z platformami danych | Faza 5 |
| Streaming data (**Kafka**/Flink/Spark) | Faza 5 |
| Praca zespołowa data+infra+AI | całość (Docker, repo, README) |
| Digital twins / symulacje (mile widziane) | Faza 4/7 (wideo z symulacji / Factory I/O) |
| MLOps / edge operations (mile widziane) | Faza 6 |

---

## Fazy (kamienie milowe)

Każda faza kończy się **artefaktem do portfolio** (kod, benchmark, GIF, diagram).

### Faza 0 — Fundament i środowisko · ~0,5 dnia
- Sprawdź sterownik NVIDIA + CUDA (`nvidia-smi`), zainstaluj **Docker** i **NVIDIA Container Toolkit** (żeby kontenery widziały GPU).
- Załóż jedno repo `edge-vision-analytics` (mono-repo) — tu ląduje wszystko.
- **Artefakt:** działające `docker run --gpus all ...` i szkielet repo.

### Faza 1 — Dataset i własny model na Ultralytics Platform · ~2–3 dni
- Rozbuduj `jumo devices 2` (52 zdjęcia to mało): dorób zdjęcia w różnym świetle/tle/kątach, **anotuj w Platform** (Annotate). Cel: 150–300 zdjęć/klasę.
- Wytrenuj model na Platform (masz już `yolo26n-seg`) — zapisz **mAP@0.5, precision, recall** z walidacji.
- **Ultralytics Platform:** moduły *Annotate* → *Train* → *Models*. Tu poznajesz zarządzanie datasetem, wersjonowanie modeli i metryki — to jest Twój „model registry".
- **Artefakt:** wytrenowany model + tabela metryk + zrzuty z Platform.

### Faza 2 — Baseline real-time inference · ~1 dzień
- Podłącz model do aplikacji z folderu `wizja` (masz gotowy pipeline kamera → YOLO → dashboard). Zmierz **FPS na PyTorch/CUDA** (FP32) na RTX 3050.
- **Artefakt:** baseline FPS + krótki zapis wideo z detekcją.

### Faza 3 — Optymalizacja TensorRT · ~2 dni · KLUCZOWE
- Wyeksportuj model do silnika TensorRT (jedna linijka, potwierdzona w dokumentacji Ultralytics):
  ```python
  from ultralytics import YOLO
  model = YOLO("yolo26n-seg.pt")
  model.export(format="engine", imgsz=640, dynamic=True, batch=8)             # FP32/FP16
  model.export(format="engine", quantize=16)                                  # FP16
  model.export(format="engine", quantize=8, data="jumo.yaml", workspace=4)    # INT8 (PTQ + kalibracja)
  ```
- Zbenchmarkuj **FP32 vs FP16 vs INT8**: FPS + mAP. Na consumer-GPU FP16 daje ~1.5–2× szybciej niż FP32 (w dokumentacji RTX 3060: 1.06 → 0.62 ms/klatkę), INT8 jeszcze więcej kosztem drobnego spadku mAP.
- **Uwaga:** kalibracja INT8 jest **specyficzna dla urządzenia** — rób ją na tym GPU, na którym będzie inferencja.
- **Artefakt:** tabela benchmarku (FP32/FP16/INT8: FPS, mAP, rozmiar modelu) — to jest złota liczba do CV.

### Faza 4 — DeepStream: analityka wideo real-time · ~3–4 dni · KLUCZOWE
- Uruchom **DeepStream z oficjalnego kontenera NVIDIA** (unikasz bolesnej instalacji): `nvcr.io/nvidia/deepstream`.
- Podłącz swój silnik TensorRT do DeepStream (repo społeczności **DeepStream-Yolo** ma gotowe configi pod modele Ultralytics).
- Dodaj: **tracker** (śledzenie obiektów), **liczenie po linii/strefie**, obsługę **wielu strumieni** naraz (multi-stream = „high-throughput").
- **Artefakt:** demo wielostrumieniowe + GIF (np. 4 strumienie z licznikiem obiektów).

### Faza 5 — Streaming i edge-to-cloud · ~3–4 dni · KLUCZOWE (Kafka)
- Z pipeline'u publikuj **zdarzenia detekcji** (klasa, timestamp, licznik, confidence) do brokera — zacznij od **MQTT** (proste, znasz z OT!), potem to samo przez **Kafka** (`docker compose` z Kafką).
- Napisz **konsumenta**, który zapisuje/agreguje zdarzenia i zasila **dashboard** (prosty web / Grafana) — to jest architektura edge → cloud.
- (Opcjonalnie) dorzuć **Flink/Spark** do agregacji strumienia (np. liczba obiektów/min w oknie czasowym) — to domyka „Kafka/Flink/Spark".
- **Artefakt:** działający tor zdarzeń kamera → broker → dashboard + diagram architektury.

### Faza 6 — Produkcja / MLOps · ~2–3 dni
- Spakuj cały stack w **`docker compose up`**: inferencja (DeepStream/TensorRT) + broker + konsument + dashboard.
- Wersjonowanie modelu: użyj **Ultralytics Platform** jako rejestru (który model = która wersja engine).
- Dodaj prosty **CI** (GitHub Actions: lint + build obrazu) i podstawowy **monitoring latencji/FPS**.
- **Artefakt:** `docker compose up` odpala całość + README z diagramem i instrukcją.

### Faza 7 — Stretch (opcjonalnie) · gdy będzie czas
- **Fuzja telemetrii:** wrzuć na tę samą szynę Kafka strumień sensorowy (możesz wykorzystać model/dane z pracy mgr) — „video + telemetry" to dokładnie język oferty.
- **Digital twin:** zamiast kamery podawaj nagranie/symulację (np. Factory I/O) jako źródło strumienia.
- **Jetson:** jeśli zdobędziesz urządzenie — Ultralytics Platform ma gotowe targety Jetson/TensorRT do wdrożenia.

---

## Efekt końcowy (co masz po projekcie)

- **Jedno repo na GitHub** z README, diagramem architektury edge-to-cloud, krótkim demo (GIF/wideo) i **tabelą benchmarku TensorRT**.
- **Aktualizacja CV:** linię „Currently learning: TensorRT/DeepStream/Kafka" zamieniamy na realny projekt z liczbami, np.:
  > *„Built a real-time edge video-analytics pipeline: TensorRT-optimized YOLO (X× FP16 speedup on RTX 3050), multi-stream DeepStream analytics with tracking/counting, and a Kafka event stream to a live dashboard — fully containerized (Docker)."*
- **Argument na rozmowę:** masz unikalne przecięcie CV + sensory/OT + real-time + edge-to-cloud, teraz podparte konkretnym projektem w stacku NVIDIA.

## Harmonogram
Realnie **3–4 tygodnie po godzinach** (albo ~5–6 weekendów). Fazy 3–5 są najważniejsze pod ofertę — jeśli czasu jest mało, zrób minimum: Faza 1 → 3 → 4 → 5 (pomiń rozbudowę datasetu i część MLOps).

## Zasoby
- Ultralytics Platform: docs.ultralytics.com/platform (Annotate / Train / Models / Deploy)
- TensorRT export (Ultralytics): docs.ultralytics.com/integrations/tensorrt
- NVIDIA DeepStream: docs.nvidia.com/metropolis/deepstream + repo `marcoslucianops/DeepStream-Yolo`
- Kafka quickstart: kafka.apache.org/quickstart (najłatwiej przez Docker Compose)
- NVIDIA Jetson + Ultralytics (na przyszłość): docs.ultralytics.com/guides/nvidia-jetson

---

### Minimalna wersja (jeśli chcesz szybki efekt)
Faza 1 (mały custom model) → Faza 3 (TensorRT + benchmark) → Faza 4 (DeepStream, 1–2 strumienie) → Faza 5 (MQTT → dashboard). To już pokrywa TensorRT + DeepStream + streaming + edge-to-cloud i daje pełnoprawny projekt do CV w ~2 tygodnie.
