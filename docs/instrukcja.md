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

_(kroki 1.1–1.6 — uzupełnimy przy realizacji)_

---

## Codzienny rytm pracy (skrót)

Po każdym kroku:

```
git add .
git commit -m "Krok X.Y: <co zrobione>"
git push
```
