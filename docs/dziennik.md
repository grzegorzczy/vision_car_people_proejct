# Dziennik projektu

Log decyzji i postępu prowadzony na bieżąco. Najnowsze wpisy na górze.

---

## 2026-08-11 — Decyzje startowe i zakres Projektu 1

**Wybór podejścia „uniwersalny silnik".** Architektura pipeline'u (ingest → detekcja →
tracking → logika → streaming) jest agnostyczna wobec obiektu. Przełączenie use-case'u =
podmiana wag modelu + reguł w module „logika"; reszta zostaje. To sam w sobie atut do CV.

**Kolejność obiektów — dwie fazy:**
- **Faza A (Projekt 1):** ludzie i pojazdy na gotowym YOLO26 (klasy COCO). Bez zbierania
  danych. Cel: opanować detekcję, tracking (ID) i zliczanie. Najłatwiejszy, szybki efekt.
- **Faza B:** obiekt przemysłowy (butelki / LEGO / `jumo devices`) z pełnym cyklem treningu.

**Źródła wideo:** kamerka (mam) do ludzi na żywo + gotowy publiczny klip drogowy do pojazdów;
2–3 własne krótkie klipy zapisane jako stały benchmark (do uczciwego porównania „przed/po").

**Integracja z platformą Ultralytics.** Cały projekt spinamy z kontem na platformie.
- Konto: Free, kredyt ~$24.93 (przyda się na trening w chmurze w Fazie B).
- Istniejące zasoby: dataset `jumo devices 2` (52 obrazy, 4 klasy), model `yolo26n-seg`,
  projekt `jumo devices`. Przepływ anotacja → trening → model już częściowo przećwiczony.
- `jumo devices` to naturalny kandydat na przemysłowy use-case w Fazie B.

**Model:** Ultralytics YOLO26 (najnowszy, styczeń 2026 — NMS-free, end-to-end, pod edge).

**Sposób pracy:** krok po kroku, kod pisze Grzegorz; każdy krok ma checkpoint i commit;
dokumentacja aktualizowana na bieżąco.

**Następny krok:** Etap 0, Krok 0.1 — założenie repo na GitHub. Szczegóły w
[`05_projekt1_plan.md`](05_projekt1_plan.md).
