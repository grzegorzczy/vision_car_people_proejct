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

### [ ] Krok 0.2 — Środowisko wirtualne (venv) + instalacja
_(uzupełnimy przy realizacji)_

### [ ] Krok 0.3 — GPU i CUDA
_(uzupełnimy przy realizacji)_

### [ ] Krok 0.4 — Połączenie z platformą Ultralytics
_(uzupełnimy przy realizacji)_

### [ ] Krok 0.5 — Pierwsza detekcja
_(uzupełnimy przy realizacji)_

---

## Etap 1 — Detekcja + tracking + zliczanie
_(kroki 1.1–1.6 — uzupełnimy przy realizacji)_

---

## Codzienny rytm pracy (skrót)
Po każdym kroku:
1. `git add .`
2. `git commit -m "Krok X.Y: <co zrobione>"`
3. `git push`
