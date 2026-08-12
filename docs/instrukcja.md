# Instrukcja — kroki wykonawcze (hands-on)

Punktowy zapis dokładnie tego, co uruchamiamy w każdym kroku. Uzupełniany na bieżąco.
Cel: powtarzalność (dało się to odtworzyć od zera) i gotowy materiał do sekcji „Setup" w README/CV.

Zasada formatowania: **każda komenda w osobnym bloku kodu**, opis obok jako tekst.

Legenda statusu: `[x]` zrobione · `[ ]` do zrobienia.

---

## Etap 0 — Środowisko + pierwsza detekcja

### [x] Krok 0.1 — Repo i konto GitHub

Otwórz VS Code → `Terminal → New Terminal` w folderze projektu.

**1. Sprawdź, że Git jest zainstalowany:**

```
git --version
```

**2. Załóż repo na GitHub** (przez stronę): New repository → nazwa → Public → bez „Add a README".

**3. Zainicjuj i wyślij repo:**

```
git init
git branch -M main
git add .
git commit -m "Init: dokumentacja projektu VisionLine"
git remote add origin URL_REPO
git push -u origin main
```

Znaczenie: `init` zakłada lokalne repo, `branch -M main` nazywa gałąź główną, `add .` dodaje pliki (poza `.gitignore`), `commit` robi migawkę, `remote add` podłącza repo zdalne, `push` wysyła na GitHub.

- **Checkpoint:** pliki widoczne na GitHub, README renderuje się na stronie repo. ✅

### [x] Krok 0.2 — Środowisko wirtualne (venv) + instalacja

**1. Sprawdź Pythona (3.8+):**

```
python --version
```

**2. Utwórz środowisko wirtualne w `.venv/`:**

```
python -m venv .venv
```

**3. Aktywuj je (Windows/PowerShell)** — prompt pokaże `(.venv)`:

```
.\.venv\Scripts\Activate.ps1
```

Jeśli PowerShell zablokuje skrypt, odblokuj raz dla siebie i ponów aktywację:

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**4. Zaktualizuj pip i zainstaluj Ultralytics** (ciągnie PyTorch):

```
python -m pip install --upgrade pip
pip install ultralytics
```

**5. Sprawdź instalację:**

```
yolo version
```

→ `8.4.117`

- **Checkpoint:** prompt z `(.venv)` i `yolo version` zwraca numer. ✅

### [x] Krok 0.3 — GPU i CUDA

Sprzęt: RTX 3050 Ti Laptop (4 GB VRAM), sterownik 561.17, CUDA 12.6.

**1. Sprawdź kartę, sterownik i maks. wersję CUDA:**

```
nvidia-smi
```

→ CUDA 12.6.

**2. Sprawdź, czy PyTorch widzi GPU:**

```
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

→ wyszło `2.13.0+cpu`, `False` — pip dał wersję tylko na CPU.

**3. Napraw — podmień na build pod CUDA 12.6** (fallback: `cu124`):

```
pip uninstall -y torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

**4. Ponów sprawdzenie z punktu 2:**

→ `2.13.0+cu126`, `CUDA: True`, `RTX 3050 Ti Laptop GPU`.

- **Checkpoint:** `torch.cuda.is_available() == True`. ✅
- **Uwaga:** 4 GB VRAM → używamy małych wariantów modelu (`yolo26n`/`yolo26s`).

### [x] Krok 0.4 — Połączenie z platformą Ultralytics

**1. Pobierz klucz API:** `platform.ultralytics.com` → Settings → API Keys → skopiuj klucz (`ul_...`).

**2. Zaloguj się** (klucz zapisze się w `settings.json`):

```
yolo login TWOJ_KLUCZ_API
```

**3. Sprawdź, że klucz zapisany:**

```
yolo settings
```

- **Checkpoint:** logowanie „SUCCESS". ✅
- **Bezpieczeństwo:** klucza NIE wpisujemy do plików w repo ani do czatu. Siedzi w `settings.json` poza projektem.

### [x] Krok 0.5 — Pierwsza detekcja

**A) Test z linii komend** (pobiera wagi `yolo26n.pt`):

```
yolo predict model=yolo26n.pt source='https://ultralytics.com/images/bus.jpg'
```

→ obraz z ramkami w `runs/detect/predict/`.

**B) Własny skrypt `first_detection.py`:**

```python
from ultralytics import YOLO

# 1. Wczytaj gotowy model YOLO26 (wariant nano - najlżejszy, pod 4 GB VRAM)
model = YOLO("yolo26n.pt")

# 2. Detekcja na obrazie; device=0 = licz na GPU; save=True zapisuje obraz z ramkami
results = model.predict(source="https://ultralytics.com/images/bus.jpg", device=0, save=True)

# 3. Wypisz, co model wykrył
for r in results:
    for box in r.boxes:
        cls_id = int(box.cls[0])       # numer klasy
        name = model.names[cls_id]     # nazwa klasy, np. 'person'
        conf = float(box.conf[0])      # pewność detekcji 0-1
        print(f"{name}: {conf:.2f}")
```

Uruchom:

```
python first_detection.py
```

**C) Kamerka na żywo** (stop: `q` w oknie lub `Ctrl+C`):

```
yolo predict model=yolo26n.pt source=0 show=True device=0
```

- **Wynik:** `person 0.96` na żywo, inferencja ~7–15 ms/klatkę (60+ FPS na GPU). ✅
- **Ważne rozróżnienie:** wagi `yolo26n.pt` i zdjęcie `bus.jpg` pobrały się z publicznych zasobów Ultralytics — NIE z konta na platformie. Logowanie (0.4) przyda się dopiero w Fazie B (trening w chmurze, rejestr modeli).
- **Checkpoint:** obraz z ramkami + podgląd z kamerki z detekcją na GPU. ✅

**KONIEC ETAPU 0** — commit:

```
git commit -am "Etap 0: srodowisko, GPU/CUDA, platforma, detekcja"
git push
```

---

## Porządki w repo (Git)

Operacje jednorazowe do utrzymania czystego repozytorium — komenda + wyjaśnienie.

### Usunięcie pliku/folderu z repo (ale nie z dysku)

```
git rm -r --cached NAZWA
git add .
git commit -m "Usun NAZWA z repo, dodaj do .gitignore"
git push
```

Znaczenie: `git rm -r --cached NAZWA` przestaje śledzić plik/folder w Git (`-r` = rekurencyjnie, `--cached` = zostawia go lokalnie na dysku). Użyte do usunięcia folderu `context/` (był tylko kontekstem dla LLM). Pamiętaj dopisać wzorzec do `.gitignore`, żeby nie wrócił.

### Pliki tymczasowe Worda

Word tworzy pliki `~$nazwa.docx`, gdy dokument jest otwarty. Ignorujemy je w `.gitignore` wzorcem:

```
~$*.docx
```

### Sekrety (klucz API)

- Klucza API NIGDY nie wpisujemy do plików w repo ani do czatu.
- Trzymamy go poza projektem (`settings.json` po `yolo login`) albo w `.env` (który jest w `.gitignore`).
- Gdy klucz się wymknie: unieważnij go na platformie (Revoke) i wygeneruj nowy.

---

## Etap 1 — Detekcja + tracking + zliczanie

### [x] Krok 1.1 — Źródła wideo

**1. Utwórz folder na dane** (jest w `.gitignore`, filmy nie idą do repo):

```
mkdir data
```

**2. Pobierz krótki klip drogowy** (darmowe, bez logowania) i zapisz jako `data/traffic.mp4`:

- Pexels: <https://www.pexels.com/videos/> (szukaj „traffic" / „highway")
- Pixabay: <https://pixabay.com/videos/>
- Coverr: <https://coverr.co/>

Wybierz krótki klip (10–20 s), Download w HD.

**3. Sprawdź, że model łyka wideo** (wykrywa `car`/`truck`/`bus`):

```
yolo predict model=yolo26n.pt source=data/traffic.mp4 show=True device=0
```

**4. Ludzie:** źródło = kamerka (`source=0`) z Kroku 0.5, nic nie trzeba dorabiać.

- **Dlaczego plik + kamerka:** plik daje powtarzalną scenę (potrzebne do pomiaru „przed/po" w Etapie 3 TensorRT), kamerka daje demo na żywo.
- **Checkpoint:** `data/traffic.mp4` odtwarza się z wykrytymi pojazdami; kamerka działa dla ludzi. ✅

### [x] Krok 1.2 — Tracking (ByteTrack)

Uwaga z realizacji: `show=True` = live okno (OpenCV `cv2.imshow`). CLI `yolo track` i skrypt
robią to samo — CLI to wrapper na `model.track(...)`. W bardzo gęstej scenie ID rosną do 1000+
(zasłonięcia) → do czystego licznika lepszy prostszy klip.

**A) Podgląd z linii komend** (`track` zamiast `predict` → ramki z `id`):

```
yolo track model=yolo26n.pt source=data/traffic.mp4 tracker=bytetrack.yaml show=True device=0
```

**B) Skrypt `track_demo.py`** — wyciąganie ID w kodzie:

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")

# track zamiast predict; persist=True = pamiętaj ID między klatkami
# stream=True = przetwarzaj klatka po klatce (oszczędza pamięć na wideo)
results = model.track(
    source="data/traffic.mp4",
    tracker="bytetrack.yaml",
    persist=True,
    stream=True,
    show=True,
    device=0,
)

for r in results:
    if r.boxes.id is not None:              # czy są śledzone obiekty
        ids = r.boxes.id.int().tolist()     # lista ID w tej klatce
        print("Sledzone ID:", ids)
```

```
python track_demo.py
```

- **Dlaczego:** detektor daje ramki na każdej klatce osobno; tracker łączy je w ścieżki z trwałym `id`. `r.boxes.id` = te numery (podstawa pod zliczanie).
- **Checkpoint:** ten sam obiekt ma stały numer przez kolejne klatki; skrypt wypisuje listy ID.

### [ ] Krok 1.3 — Wirtualna linia + licznik

Skrypt `counter.py` (gotowy `ObjectCounter` z Ultralytics):

```python
import cv2
from ultralytics import solutions

cap = cv2.VideoCapture("data/highway.mp4")
assert cap.isOpened(), "Nie moge otworzyc wideo"

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

line_points = [(0, h // 2), (w, h // 2)]   # linia pozioma na srodku

counter = solutions.ObjectCounter(
    model="yolo26n.pt",
    region=line_points,
    classes=[2, 3, 5, 7],   # COCO: car, motorcycle, bus, truck
    show=True,
    device=0,
)

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break
    counter(frame)

cap.release()
cv2.destroyAllWindows()
```

```
python counter.py
```

- **Jak działa:** `ObjectCounter` = detekcja + tracking + logika przecięcia linii. Gdy środek śledzonego obiektu przejdzie przez `region`, rośnie licznik (z kierunkiem in/out).
- **Regulacja:** linię przesuwasz zmieniając `h // 2` (np. `int(h*0.6)`).
- **Checkpoint:** widać linię, licznik in/out rośnie przy przecięciach. ✅

### [ ] Krok 1.3b — Własna logika licznika (zrozumienie)

Skrypt `counter_manual.py` — ręczna wersja, żeby zrozumieć, co robi `ObjectCounter`.
Idea: dla każdego ID pamiętamy poprzednie Y środka; gdy zmieni się znak `(cy - LINE_Y)`,
obiekt przeszedł przez linię → `+1` (raz, dzięki zbiorowi `counted`).

```python
import cv2
from ultralytics import YOLO

model = YOLO("yolo26n.pt")

cap = cv2.VideoCapture("data/highway.mp4")
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.release()
LINE_Y = h // 2

VEHICLES = [2, 3, 5, 7]     # car, motorcycle, bus, truck
prev_cy, counted, count = {}, set(), 0

results = model.track(source="data/highway.mp4", tracker="bytetrack.yaml",
                      persist=True, stream=True, classes=VEHICLES, device=0)

for r in results:
    frame = r.orig_img
    cv2.line(frame, (0, LINE_Y), (w, LINE_Y), (255, 0, 255), 2)
    if r.boxes.id is not None:
        boxes = r.boxes.xyxy.cpu().numpy()
        ids = r.boxes.id.int().cpu().tolist()
        for (x1, y1, x2, y2), tid in zip(boxes, ids):
            cy = int((y1 + y2) / 2)
            if tid in prev_cy and tid not in counted:
                if (prev_cy[tid] - LINE_Y) * (cy - LINE_Y) < 0:
                    count += 1
                    counted.add(tid)
            prev_cy[tid] = cy
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, str(tid), (int(x1), int(y1) - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(frame, f"Licznik: {count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.imshow("Reczny licznik", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()
```

```
python counter_manual.py
```

- **Sedno:** `(prev - LINE_Y) * (cy - LINE_Y) < 0` = zmiana znaku = przecięcie linii.
- **Checkpoint:** własny licznik rośnie podobnie jak `ObjectCounter`. ✅

**Sterowanie rozmiarem okna** (gdy wideo jest np. 4K i okno przerasta ekran) — rozmiar okna
nie wpływa na detekcję (model liczy wewnętrznie w 640 px). Dwa sposoby:

```python
# Sposob 1 (zalecany): okno skalowalne, obraz bez zmian. Dodaj PRZED petla:
cv2.namedWindow("Reczny licznik", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Reczny licznik", 1280, 720)
```

```python
# Sposob 2: zmniejsz sama klatke przed wyswietleniem (zachowuje proporcje):
disp = cv2.resize(frame, None, fx=0.5, fy=0.5)
cv2.imshow("Reczny licznik", disp)
```

### [ ] Krok 1.4 — Kierunek in/out + liczenie ludzi

Rozszerzenie `counter_manual.py`: konfiguracja `SOURCE`/`CLASSES` na górze + rozdzielenie
kierunku. W momencie przecięcia porównujemy `cy` z `prev_cy[tid]`:

```python
if cy > prev_cy[tid]:   # środek zjechał w dół
    count_down += 1
else:                   # środek pojechał w górę
    count_up += 1
```

Uruchomienie:

```
python counter_manual.py
```

- Pojazdy: `SOURCE = "data/highway.mp4"`, `CLASSES = [2, 3, 5, 7]`.
- Ludzie (kamerka): `SOURCE = 0`, `CLASSES = [0]`.
- Wskazówka: dla ruchu lewo-prawo lepsza linia pionowa (porównuj `cx` zamiast `cy`).
- **Uwaga:** `SOURCE = 0` (bez nawiasów — pojedyncza wartość), `CLASSES = [0]` (lista).
- **Checkpoint:** dwa liczniki (w dół / w górę) rosną zgodnie z kierunkiem; działa dla pojazdów i ludzi. ✅

### [ ] Krok 1.5 — FPS na nakładce + zapis demo

Dodatki do `counter_manual.py`:

```python
# 1) na gorze pliku
import time

# 2) po cv2.resizeWindow(...):
import os
os.makedirs("runs", exist_ok=True)
writer = cv2.VideoWriter("runs/demo.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (w, h))
prev_t = time.time()

# 3) w petli, tuz przed cv2.imshow(...):
now = time.time()
fps = 1.0 / (now - prev_t) if now > prev_t else 0.0
prev_t = now
cv2.putText(frame, f"FPS: {fps:.1f}", (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
writer.write(frame)

# 4) po petli, przed destroyAllWindows():
writer.release()
```

- **FPS** = `1 / (czas jednej klatki)` — wydajność całego pipeline'u (detekcja+tracking+rysowanie).
- **VideoWriter**: `mp4v` kodek, `30` FPS pliku, `(w, h)` = rozmiar klatki. `release()` finalizuje plik.
- Kończ klawiszem `q` (nie Ctrl+C), żeby plik był kompletny. `runs/` jest w `.gitignore`.
- **Checkpoint:** widać licznik FPS; `runs/demo.mp4` otwiera się z ramkami i licznikami.

### [ ] Krok 1.6 — Refaktor do modułów `src/`

_(rozbicie skryptu na ingest / detection+tracking / logic / app.py — uzupełnimy przy realizacji)_

---

## Codzienny rytm pracy (skrót)

Po każdym kroku:

```
git add .
git commit -m "Krok X.Y: <co zrobione>"
git push
```
