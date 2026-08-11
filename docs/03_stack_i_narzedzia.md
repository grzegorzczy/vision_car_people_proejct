# Stack technologiczny i narzędzia

Dobór jest celowy: **każda technologia = wymóg z ofert pracy**, nic „na zapas".

## Rdzeń wizji
- **Python** — język całego pipeline'u.
- **Ultralytics YOLO26** — najnowszy (styczeń 2026) model detekcji: NMS-free, end-to-end,
  zoptymalizowany pod edge. Używamy do detekcji i dotrenowania na własnych danych.
- **OpenCV** — dekodowanie wideo, rysowanie nakładek (na starcie).
- **ByteTrack** — tracking wielu obiektów (trwałe ID między klatkami).

## Trening i dane
- **Roboflow** lub **CVAT** — anotacja i zarządzanie zbiorem.
- **PyTorch (CUDA)** — backend treningu (idzie z Ultralytics).
- Metryki: **mAP**, precision/recall, confusion matrix.

## Optymalizacja i deployment
- **CUDA** — obliczenia na GPU NVIDIA (podstawa wszystkiego).
- **TensorRT** — przyspieszenie inferencji (FP16/INT8) na produkcji.
- **ONNX** — format pośredni w eksporcie `YOLO26 → ONNX → TensorRT`.
- **Docker** (`--gpus all`) — powtarzalne środowisko, wdrożenie w kontenerze.
- **NVIDIA DeepStream** — pipeline wideo high-throughput, wiele strumieni (Etap 5).

## Streaming i chmura
- **Apache Kafka** — broker zdarzeń (edge → cloud), wzorzec event-driven.
- Baza (np. **PostgreSQL** lub **SQLite** na start) — składowanie metryk/zdarzeń.
- Dashboard — prosty (np. **Streamlit** lub lekki web) do metryk i alarmów na żywo.
- *(Opcjonalnie później: Flink/Spark, jeśli chcesz mocniej pokazać przetwarzanie strumieni.)*

## Sprzęt edge
- **Laptop z GPU NVIDIA** — Etapy 0–5.
- **NVIDIA Jetson** + **JetPack** — Etap 6 (po zakupie).

## Integracja przemysłowa (Etap 7)
- **OPC UA** lub **Modbus TCP** — komunikacja z PLC.
- Twój istniejący **backend PLC** — jako odbiornik zdarzeń / sterowanie.

## Platforma MLOps
- **Ultralytics Platform** — chmurowe konto spięte z projektem: zarządzanie modelami,
  anotacja danych, **trening w chmurze** (mamy kredyt), eksport i deployment. Integrujemy
  już w Etapie 0; pełne wykorzystanie w Fazie B (trening własnego modelu).

## Narzędzia pracy
- **Git + GitHub** — wersjonowanie kodu i dokumentacji, portfolio.
- **Markdown** — dokumentacja prowadzona na bieżąco w `docs/`.
- **docker-compose** — lokalne postawienie Kafki + bazy + dashboardu.

---

## Czego świadomie NIE robimy na starcie
- Nie zaczynamy od Jetsona (najpierw laptop — taniej i szybciej iterować).
- Nie zaczynamy od DeepStream (najpierw prosty OpenCV — łatwiej zrozumieć i debugować).
- Nie optymalizujemy przed działającym MVP (TensorRT dopiero w Etapie 3).
- Nie dokładamy Flink/Spark, dopóki Kafka nie działa i nie jest zrozumiała.
