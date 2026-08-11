# Docelowa struktura repo

Budujemy ją stopniowo — katalog pojawia się dopiero, gdy dochodzimy do jego etapu.
Poniżej stan docelowy (po Etapie ~4), żebyś widział, dokąd zmierzamy.

```
Computer_vision_project/
├── README.md                  # opis projektu (jest)
├── docs/                      # dokumentacja na bieżąco (jest)
│   ├── 01_architektura.md
│   ├── 02_roadmap.md
│   ├── 03_stack_i_narzedzia.md
│   ├── 04_struktura_repo.md
│   └── dziennik.md            # log postępu: co zrobione, co się nauczyłeś, problemy
│
├── src/                       # kod źródłowy
│   ├── ingest/                # wczytywanie wideo (plik/USB/RTSP)
│   ├── detection/             # wrapper na YOLO26 (inferencja)
│   ├── tracking/              # ByteTrack
│   ├── logic/                 # reguły: liczenie, strefy, defekty → zdarzenia
│   ├── streaming/             # producer/consumer Kafka
│   └── app.py                 # spięcie pipeline'u
│
├── training/                  # trening modelu (Etap 2)
│   ├── data.yaml
│   ├── train.py
│   └── runs/                  # wyniki treningu (ignorowane w git)
│
├── models/                    # wagi i enginy (duże pliki → git-lfs lub ignore)
│   ├── yolo26.pt
│   └── yolo26_fp16.engine     # TensorRT (Etap 3)
│
├── deploy/
│   ├── Dockerfile
│   ├── docker-compose.yml     # Kafka + baza + dashboard
│   └── deepstream/            # konfiguracja DeepStream (Etap 5)
│
├── dashboard/                 # wizualizacja metryk (Etap 4)
├── data/                      # próbki wideo do testów (małe; duże → ignore)
├── tests/                     # testy jednostkowe kluczowej logiki
├── requirements.txt
├── .gitignore
└── .env.example               # konfiguracja (ścieżki, adres Kafki) bez sekretów
```

## Zasady porządku
- **Rozdzielone moduły** (`detection`, `tracking`, `logic`) — łatwo testować i podmieniać.
- **Duże pliki poza gitem** — wideo, wagi, enginy przez `.gitignore` (ew. git-lfs).
- **`docs/dziennik.md`** — prowadzony na bieżąco; przy rekrutacji pokazuje Twój proces myślenia.
- **`.env.example`** zamiast twardych ścieżek — profesjonalny standard, żadnych sekretów w repo.
