# Instrukcja — kroki wykonawcze (hands-on)

Punktowy zapis dokładnie tego, co uruchamiamy w każdym kroku. Uzupełniany na bieżąco.
Cel: powtarzalność (dało się to odtworzyć od zera) i gotowy materiał do sekcji „Setup" w README/CV.

Legenda statusu: `[x]` zrobione · `[ ]` do zrobienia.

---

## Etap 0 — Środowisko + pierwsza detekcja

### [x] Krok 0.1 — Repo i konto GitHub

1. Otwórz VS Code → `Terminal → New Terminal` w folderze projektu.
2. `git --version` — sprawdź, że Git jest zainstalowany.
3. Na github.com: **New repository** → nazwa → **Public** → bez „Add a README".
4. `git init` — załóż lokalne repo.
5. `git branch -M main` — nazwij główną gałąź `main`.
6. `git add .` — dodaj pliki do stagingu (poza `.gitignore`).
7. `git commit -m "Init: dokumentacja projektu VisionLine"` — pierwsza migawka.
8. `git remote add origin URL_REPO` — podłącz zdalne repo.
9. `git push -u origin main` — wyślij na GitHub.

- **Checkpoint:** pliki widoczne na GitHub, README renderuje się na stronie repo. ✅

### [x] Krok 0.2 — Środowisko wirtualne (venv) + instalacja

1. `python --version` — sprawdź Pythona (3.8+).
2. `python -m venv .venv` — utwórz środowisko wirtualne w `.venv/`.
3. `.\.venv\Scripts\Activate.ps1` — aktywuj (Windows/PowerShell). Prompt pokaże `(.venv)`.
   - Jeśli blokada: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, potem ponów.
4. `python -m pip install --upgrade pip` — zaktualizuj pip.
5. `pip install ultralytics` — instaluj Ultralytics (ciągnie PyTorch).
6. `yolo version` — sprawdź instalację. → **8.4.117** ✅

- **Checkpoint:** prompt z `(.venv)` i `yolo version` zwraca numer. ✅

### [x] Krok 0.3 — GPU i CUDA

Sprzęt: RTX 3050 Ti Laptop (4 GB VRAM), sterownik 561.17, CUDA 12.6.

1. `nvidia-smi` — karta, sterownik, maks. wersja CUDA. → CUDA 12.6 ✅
2. Sprawdź PyTorch:
   `python -c "import torch; print('torch', torch.__version__); print('CUDA dostepne:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'brak')"`
   → wyszło `2.13.0+cpu`, `False` (pip dał wersję CPU).
3. Naprawa — podmiana na build CUDA 12.6:
   - `pip uninstall -y torch torchvision`
   - `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126`
   - (fallback: `.../whl/cu124`)
4. Ponów sprawdzenie → `2.13.0+cu126`, `CUDA: True`, `RTX 3050 Ti Laptop GPU`. ✅

- **Checkpoint:** `torch.cuda.is_available() == True`. ✅
- **Uwaga:** 4 GB VRAM → używamy małych wariantów modelu (`yolo26n`/`yolo26s`).

### [x] Krok 0.4 — Połączenie z platformą Ultralytics

1. `platform.ultralytics.com` → Settings → API Keys → skopiuj klucz (`ul_...`).
2. `yolo login TWOJ_KLUCZ_API` — logowanie i zapis klucza. → SUCCESS
   (KLUCZA NIE ZAPISUJEMY W REPO — jest sekretem, siedzi w `settings.json` poza projektem.)
3. `yolo settings` — sprawdź, że `api_key` zapisany.

- **Checkpoint:** logowanie „SUCCESS", klucz widoczny w ustawieniach.
- **Bezpieczeństwo:** klucza nie commitujemy; siedzi w `settings.json` poza repo.

### [ ] Krok 0.5 — Pierwsza detekcja

A) Test CLI (pobiera wagi `yolo26n.pt`):
   `yolo predict model=yolo26n.pt source='https://ultralytics.com/images/bus.jpg'`
   → obraz z ramkami w `runs/detect/predict/`.
B) Skrypt `first_detection.py` (YOLO → predict na GPU → wypisz klasy i pewność):
   `python first_detection.py`
C) Kamerka na żywo:
   `yolo predict model=yolo26n.pt source=0 show=True device=0` (stop: `q` / Ctrl+C)

- **Checkpoint:** obraz z ramkami + podgląd z kamerki z detekcją na GPU.

---

## Etap 1 — Detekcja + tracking + zliczanie

_(kroki 1.1–1.6 — uzupełnimy przy realizacji)_

---

## Codzienny rytm pracy (skrót)

Po każdym kroku:

1. `git add .`
2. `git commit -m "Krok X.Y: <co zrobione>"`
3. `git push`
