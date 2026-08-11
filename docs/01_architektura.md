# Architektura systemu

## Zasada: Edge liczy, chmura obserwuje

Podział na dwie warstwy jest celowy — to dokładnie wzorzec **edge-to-cloud**
z Twoich ofert. Ciężka inferencja dzieje się lokalnie (przy kamerze), a do chmury
lecą tylko lekkie **zdarzenia** (nie surowe wideo).

```
                          ┌────────────────────────── EDGE (laptop GPU → Jetson) ──────────────────────────┐
                          │                                                                                 │
   ┌─────────┐            │   ┌───────────┐   ┌──────────────┐   ┌───────────┐   ┌───────────────────┐      │
   │ Kamera  │  klatki    │   │ Ingest    │   │ Inferencja   │   │ Tracking  │   │ Logika biznesowa  │      │
   │ / plik  │ ─────────► │   │ (dekod)   │──►│ YOLO26+TRT   │──►│ ByteTrack │──►│ liczenie/reguły   │      │
   │ / RTSP  │            │   └───────────┘   └──────────────┘   └───────────┘   └─────────┬─────────┘      │
   └─────────┘            │                                                                │ zdarzenia      │
                          │                                                                ▼                │
                          │                                                        ┌───────────────┐        │
                          │                                                        │ Producer      │        │
                          │                                                        │ (Kafka)       │        │
                          └────────────────────────────────────────────────────────────┬──────────┘        │
                                                                                        │                   │
                          ┌──────────────────────────── CHMURA / SERWER ────────────────┼───────────────────┘
                          │                                                             ▼
                          │   ┌───────────┐      ┌──────────────┐      ┌────────────────────┐
                          │   │ Kafka     │─────►│ Konsument /  │─────►│ Baza + Dashboard   │
                          │   │ (broker)  │      │ agregacja    │      │ (metryki, alarmy)  │
                          │   └───────────┘      └──────────────┘      └────────────────────┘
                          └───────────────────────────────────────────────────────────────────┘

   Rozszerzenie (Etap 7):  Logika biznesowa ──► sygnał ──► PLC / czujniki / wykonawcze
```

## Komponenty (co robi każdy klocek)

**1. Ingest (dekodowanie wideo)**
Wczytuje źródło: plik `.mp4`, kamera USB, albo strumień RTSP. Rozbija na klatki.
Na starcie: OpenCV. Później: sprzętowy dekoder NVIDIA (w DeepStream).

**2. Inferencja (YOLO26)**
Model wykrywa obiekty na klatce — zwraca ramki + klasy + pewność.
Najpierw model gotowy (pretrained), potem **dotrenowany na Twoich danych**.
Na produkcji przyspieszony przez **TensorRT** (FP16/INT8).

**3. Tracking (ByteTrack)**
Łączy detekcje między klatkami w ścieżki z trwałym ID. Bez tego nie da się
poprawnie **zliczać** ani liczyć czasu przebywania w strefie.

**4. Logika biznesowa**
Tu żyje sens aplikacji: linia zliczania, strefa alarmowa, reguła „defekt".
Zamienia detekcje w **zdarzenia** (np. `{"typ":"reject","id":417,"ts":...}`).

**5. Producer → Kafka**
Wypycha zdarzenia do brokera. To granica edge↔cloud i punkt, w którym system
staje się **event-driven** (a nie „skrypt, który coś rysuje").

**6. Konsument + Dashboard**
Odbiera zdarzenia, agreguje (sztuk/min, % braków), zapisuje i pokazuje na wykresie.
Alarmy w czasie rzeczywistym.

## Decyzje projektowe (i dlaczego)

- **Zdarzenia, nie wideo, do chmury** — realny wzorzec przemysłowy: tanio, skalowalnie,
  bez problemów z prywatnością i pasmem.
- **Tracking oddzielony od detekcji** — bo to dwa różne problemy; łatwiej testować i podmieniać.
- **TensorRT dopiero po działającym MVP** — najpierw poprawność, potem wydajność.
- **PLC jako osobny „adapter" na końcu** — rdzeń wizji nie zależy od sprzętu, więc PLC
  (albo czujnik, albo webhook) doklejamy bez przebudowy.
