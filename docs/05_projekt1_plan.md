# Projekt 1 — Licznik ludzi i pojazdów (Faza A)

**Cel:** zbudować działający system, który w czasie rzeczywistym wykrywa obiekty,
śledzi je (trwałe ID) i zlicza ich przekroczenia przez wirtualną linię — na kamerce
(ludzie) i na gotowym klipie drogowym (pojazdy).

Używamy **gotowego** modelu YOLO26 (klasy COCO: `person`, `car`, `bus`, `truck`),
więc **nie zbieramy własnych danych** — pełny cykl treningu przyjdzie w Fazie B.

Projekt 1 = **Etap 0 + Etap 1** z roadmapy.

---

## Jak pracujemy (ważne)

- **Krok po kroku, Ty piszesz kod.** Ja podaję cel kroku, minimalny fragment i wyjaśnienie
  *dlaczego*. Ty wpisujesz, uruchamiasz, mówisz co widzisz — dopiero potem następny krok.
- **Nic nie idzie dalej bez działającego checkpointu.** Każdy krok kończy się „sprawdź, że X".
- **Commit po każdym kroku** (Git) — historia = dowód procesu do portfolio.
- **Dziennik na bieżąco** w [`dziennik.md`](dziennik.md).

### Legenda kroków
Każdy krok opisany jest czterema polami:

- **Co robimy** — konkretne zadanie.
- **Stack** — jakiej technologii używamy.
- **Uczysz się** — co konkretnie wyniesiesz.
- **Platforma** — rola platformy Ultralytics (jeśli dotyczy).
- **Checkpoint** — jak potwierdzić, że działa.

---

## Etap 0 — Środowisko + pierwsza detekcja

### Krok 0.1 — Repo i konto
- **Co robimy:** zakładamy repozytorium na GitHub, klonujemy lokalnie, wrzucamy dotychczasowe `README.md` i `docs/`.
- **Stack:** Git, GitHub.
- **Uczysz się:** wersjonowanie projektu od zera; struktura repo.
- **Platforma:** upewniamy się, że jesteś zalogowany na platformie Ultralytics (masz konto Free).
- **Checkpoint:** repo widoczne na GitHub z dokumentacją.

### Krok 0.2 — Środowisko Pythona
- **Co robimy:** tworzymy środowisko wirtualne (`venv` lub `conda`), aktywujemy, instalujemy `ultralytics`.
- **Stack:** Python, venv/conda, pip.
- **Uczysz się:** izolacja zależności; dlaczego nie instalujemy globalnie.
- **Checkpoint:** `pip show ultralytics` pokazuje wersję; `yolo version` działa w terminalu.

### Krok 0.3 — GPU i CUDA
- **Co robimy:** sprawdzamy, czy PyTorch widzi kartę: `torch.cuda.is_available()`. Jeśli `False` — instalujemy build PyTorch pod CUDA.
- **Stack:** NVIDIA CUDA, PyTorch.
- **Uczysz się:** różnica CPU vs GPU w inferencji; jak potwierdzić, że liczysz na karcie.
- **Checkpoint:** `torch.cuda.is_available() == True` i `nvidia-smi` pokazuje proces przy uruchomieniu modelu.

### Krok 0.4 — Połączenie z platformą Ultralytics
- **Co robimy:** pobieramy klucz API z ustawień platformy i logujemy się z poziomu pakietu `ultralytics`, żeby lokalny kod „widział" konto (modele, eksporty).
- **Stack:** Ultralytics Platform (API key), Ultralytics SDK.
- **Uczysz się:** jak lokalny projekt spina się z chmurową platformą MLOps.
- **Platforma:** to jest moment integracji — od teraz modele i eksporty możemy śledzić w koncie. *(Dokładną komendę logowania potwierdzimy na żywo w aplikacji — API bywa aktualizowane.)*
- **Checkpoint:** logowanie bez błędu; lokalnie widać listę Twoich modeli z platformy.

### Krok 0.5 — Pierwsza detekcja
- **Co robimy:** ładujemy `yolo26n.pt`, puszczamy na jednym zdjęciu, potem na kamerce (`source=0`), oglądamy ramki.
- **Stack:** Ultralytics YOLO26, inferencja.
- **Uczysz się:** struktura wyniku detekcji (ramki, klasy, pewność); uruchomienie modelu na obrazie i na strumieniu.
- **Checkpoint:** na obrazie z kamerki widać ramki z etykietami (np. `person 0.91`), liczone na GPU.

**Koniec Etapu 0:** masz działające środowisko, GPU, połączenie z platformą i model wykrywający obiekty na żywo.

---

## Etap 1 — Detekcja + tracking + zliczanie (rdzeń Projektu 1)

### Krok 1.1 — Źródła wideo
- **Co robimy:** przygotowujemy `data/` — kamerka do ludzi + pobrany publiczny klip drogowy do pojazdów. Zapisujemy 1–2 krótkie klipy jako stały benchmark.
- **Stack:** OpenCV, pliki wideo.
- **Uczysz się:** różne źródła (kamera vs plik); po co stały zestaw testowy.
- **Checkpoint:** oba źródła odtwarzają się w oknie podglądu.

### Krok 1.2 — Tracking (ByteTrack)
- **Co robimy:** zamieniamy `predict` na `track` z trackerem ByteTrack (`persist=True`), oglądamy trwałe ID nad obiektami.
- **Stack:** Ultralytics `track`, ByteTrack.
- **Uczysz się:** różnica detekcja vs tracking; czym jest ID ścieżki i po co.
- **Checkpoint:** ten sam człowiek/samochód ma stałe ID między klatkami.

### Krok 1.3 — Wirtualna linia i licznik
- **Co robimy:** definiujemy linię w kadrze; liczymy `+1`, gdy środek ścieżki ją przekroczy. Najpierw pokażemy to gotowym `solutions.ObjectCounter` z Ultralytics (żeby zobaczyć efekt), potem **napiszemy własną logikę przecięcia** — żebyś rozumiał, co się dzieje.
- **Stack:** geometria (przecięcie linii), Ultralytics Solutions.
- **Uczysz się:** logika zliczania bez podwójnego liczenia; kiedy użyć gotowca, a kiedy własnego kodu.
- **Checkpoint:** licznik rośnie dokładnie raz na obiekt przekraczający linię.

### Krok 1.4 — Filtr klas i kierunek
- **Co robimy:** liczymy tylko wybrane klasy (`person` albo pojazdy) i rozdzielamy kierunek (w górę/w dół).
- **Stack:** filtrowanie klas COCO.
- **Uczysz się:** mapowanie ID klas; liczenie kierunkowe (wejścia/wyjścia).
- **Checkpoint:** osobne liczniki „in" i „out" zgadzają się z tym, co widać.

### Krok 1.5 — Nakładka i FPS
- **Co robimy:** rysujemy na obrazie liczniki i FPS; zapisujemy wynikowe wideo do pliku.
- **Stack:** OpenCV (rysowanie, zapis), pomiar FPS.
- **Uczysz się:** jak mierzyć wydajność; przygotowanie materiału demo (GIF do README).
- **Checkpoint:** nagrany klip z widocznym licznikiem i FPS.

### Krok 1.6 — Refaktor do modułów
- **Co robimy:** rozbijamy skrypt na `src/ingest`, `src/detection`, `src/tracking`, `src/logic`, `src/app.py` (zgodnie ze strukturą repo).
- **Stack:** czysty kod, podział odpowiedzialności.
- **Uczysz się:** projektowanie tak, by dało się podmienić obiekt (przygotowanie pod Fazę B).
- **Checkpoint:** `python src/app.py --source ...` działa jak wcześniej, ale kod jest modularny; commit.

**Koniec Etapu 1 = koniec Projektu 1:** działający, modularny licznik ludzi i pojazdów, nagrane demo, wszystko w repo na GitHub.

---

## Rola platformy Ultralytics w Projekcie 1

W Fazie A (gotowy model) platforma pełni rolę **lekką, ale realną**:

- **Rejestr modeli i eksportów** — logujemy używany model i (później) eksporty, żeby ćwiczyć przepływ MLOps.
- **Explore / datasety** — źródło gotowych zbiorów i podgląd danych.
- **Deployments** — miejsce, gdzie w kolejnych etapach pojawi się wdrożony model.

Platforma wchodzi **na pełną moc w Fazie B** (Etap 2), gdzie robimy: upload własnych danych →
anotacja → **trening w chmurze** (masz kredyt) → eksport modelu → deployment. Ten przepływ
masz już częściowo przećwiczony na `jumo devices` / `yolo26n-seg`.

---

## Definicja ukończenia Projektu 1 (co masz do CV)

- Repo na GitHub z czytelnym README i dokumentacją procesu.
- Działający licznik: ludzie (kamerka) + pojazdy (wideo), z trackingiem i FPS.
- Nagrane demo (GIF/wideo).
- Konto Ultralytics spięte z projektem.
- Zdanie do CV: *„Zbudowałem modularny pipeline detekcji + trackingu + zliczania w czasie
  rzeczywistym (YOLO26, ByteTrack), uruchomiony na GPU, zintegrowany z platformą Ultralytics."*

## Co dalej — Faza B (zapowiedź)
Podmieniamy obiekt na przemysłowy (butelki/LEGO albo `jumo devices`), przechodzimy pełny
cykl treningu na platformie i optymalizację TensorRT. Szczegóły w [roadmapie](02_roadmap.md), Etap 2+.
