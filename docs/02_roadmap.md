# Roadmap — etapy 0–7

Każdy etap: **cel → co budujemy → co potrafisz po nim → co masz do pokazania w CV.**
Zasada nadrzędna: najpierw ma *działać*, potem ma być *szybkie*, potem *skalowalne*.

> **Zakres tego repozytorium:** zrealizowane są **Etapy 0–1** — licznik ludzi i pojazdów
> na gotowym YOLO26 (klasy COCO, bez własnych danych). Szczegóły: [`05_projekt1_plan.md`](05_projekt1_plan.md),
> komendy: [`instrukcja.md`](instrukcja.md).
>
> **Etapy 2–7** (trening własnego modelu, TensorRT, Kafka, DeepStream, Jetson, PLC) realizujemy
> w kolejnym, osobnym projekcie — ta roadmapa pozostaje jako mapa całej ścieżki rozwoju.

---

## Etap 0 — Środowisko + pierwsza detekcja
**Cel:** uruchomić GPU laptopa i zobaczyć detekcję na wideo.
**Budujemy:** venv/conda, instalacja Ultralytics + PyTorch (CUDA), test `nvidia-smi`,
skrypt, który puszcza gotowy YOLO26 na pliku `.mp4` i rysuje ramki.
**Umiesz:** potwierdzić, że CUDA działa; uruchomić model na wideo; czytać wynik detekcji.
**Do CV:** — (fundament).

## Etap 1 — MVP: detekcja + tracking + zliczanie
**Cel:** pierwszy realny use-case end-to-end (na gotowym modelu, klasy COCO np. „person").
**Budujemy:** integracja ByteTrack, wirtualna linia/strefa, licznik przekroczeń,
nakładka na obraz (liczba, FPS).
**Umiesz:** różnicę detekcja vs tracking; zliczać obiekty bez podwójnego liczenia; mierzyć FPS.
**Do CV:** działający „people/object counter" — pierwszy widoczny efekt (GIF do README).

## Etap 2 — Własne dane + dotrenowanie YOLO26
**Cel:** model rozpoznaje **Twój** obiekt/defekt, nie tylko klasy COCO.
**Budujemy:** zebranie/nagranie danych, anotacja (Roboflow albo CVAT), podział train/val,
`data.yaml`, **fine-tuning** YOLO26, ewaluacja (mAP, confusion matrix), analiza błędów.
**Umiesz:** cały cykl treningu: dane → anotacja → trening → metryki → iteracja.
**Do CV:** to jest sedno — „dotrenowałem model detekcji na własnym zbiorze, mAP X%".

## Etap 3 — Optymalizacja: eksport do TensorRT + konteneryzacja
**Cel:** produkcyjna, szybka inferencja i powtarzalne środowisko.
**Budujemy:** eksport `YOLO26 → ONNX → TensorRT` (FP16, potem INT8),
benchmark FPS/latencja przed/po, **Dockerfile** (obraz z CUDA + zależności),
uruchomienie całego MVP w kontenerze na GPU (`--gpus all`).
**Umiesz:** czym jest TensorRT i po co; różnica FP32/FP16/INT8; Docker z dostępem do GPU.
**Do CV:** „Przyspieszyłem inferencję Nx przez TensorRT; wdrożenie w Dockerze" — mocny punkt.

## Etap 4 — Streaming zdarzeń: Kafka + dashboard
**Cel:** system staje się event-driven i edge-to-cloud.
**Budujemy:** producer zdarzeń → Kafka (docker-compose), konsument agregujący,
zapis do bazy, prosty dashboard (metryki na żywo, alarmy).
**Umiesz:** wzorzec producer/consumer; projektowanie „schematu zdarzenia"; po co rozdziela się edge i cloud.
**Do CV:** „Pipeline streamingowy zdarzeń (Kafka), architektura edge-to-cloud, dashboard real-time".

## Etap 5 — DeepStream (pipeline wideo high-throughput)
**Cel:** profesjonalny, wydajny pipeline wideo NVIDIA (wiele strumieni).
**Budujemy:** przeniesienie inferencji do DeepStream (dekod sprzętowy, batch, wiele kamer),
model z Etapu 3 jako engine TensorRT w DeepStream.
**Umiesz:** czym jest DeepStream i kiedy go używać zamiast „ręcznego" OpenCV; obsługa wielu źródeł.
**Do CV:** bezpośrednie trafienie w wymóg „DeepStream / video analytics / high-throughput".

## Etap 6 — Jetson (edge deployment na urządzeniu)
**Cel:** to samo, ale na realnym urządzeniu edge (po zakupie Jetson).
**Budujemy:** flash Jetsona (JetPack), przeniesienie kontenera/DeepStream, rekompilacja engine
TensorRT pod architekturę Jetsona, pomiar FPS/temperatury/poboru.
**Umiesz:** deployment na ARM/Jetson; różnice wydajności desktop vs edge; ograniczenia zasobów.
**Do CV:** „Wdrożenie modelu na NVIDIA Jetson" — dokładnie to, czego szukają w ofertach.

## Etap 7 — Integracja przemysłowa (PLC / czujniki)
**Cel:** zamknięcie pętli — wizja steruje/zgłasza do świata fizycznego.
**Budujemy:** adapter zdarzeń → PLC (OPC UA lub Modbus TCP), np. sygnał „reject";
opcjonalnie wejście z czujnika (trigger/synchronizacja z taśmą).
**Umiesz:** połączyć CV z automatyką przemysłową — Twój backend PLC staje się atutem.
**Do CV:** unikalny wyróżnik — „CV + PLC / OPC UA", łączenie AI z realnym sterowaniem.

---

## Kolejność vs sprzęt

| Etapy | Sprzęt | Inwestycja |
|---|---|---|
| 0–4 | Laptop z GPU NVIDIA | brak (masz) |
| 5 | Laptop z GPU (DeepStream w Dockerze) | brak |
| 6 | NVIDIA Jetson | zakup po Etapie 5 |
| 7 | PLC (masz) + ew. czujnik | opcjonalna |

**Rekomendacja:** rób etapy po kolei. Po Etapie 4 masz już kompletny, imponujący projekt
do CV *bez* dodatkowych zakupów. Jetson (6) i PLC (7) to „wisienki", które go wyróżnią.
