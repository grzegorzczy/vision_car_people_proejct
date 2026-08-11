# -*- coding: utf-8 -*-
"""
test_logic.py — szybkie testy logiki klasyfikacji (Faza 2).

Sprawdzamy decyzje linii BEZ kamery i BEZ modelu — na sztucznych detekcjach.
Uruchomienie:  python test_logic.py
"""

from collections import namedtuple

from vision import classifier, config

# Atrapa detekcji — classify() potrzebuje tylko .coco_id i .confidence
Fake = namedtuple("Fake", "coco_id confidence")

# ID klas COCO uzywanych w projekcie
BOTTLE, CUP, SCISSORS, PHONE, BOOK, KEYBOARD, PERSON = 39, 41, 76, 67, 73, 66, 0
AIRPLANE = 4   # klasa spoza naszej mapy (test odrzucania)


def case(name, dets, expect_code, expect_decision):
    r = classifier.classify(dets)
    ok = (r.object_code == expect_code and r.decision == expect_decision)
    flag = "[ OK ]" if ok else "[FAIL]"
    print(f"{flag} {name:38s} -> kod={r.object_code} ({r.name}), "
          f"decyzja={r.decision}, detekcje={r.detection_count}")
    return ok


def main():
    print("=" * 70)
    print(" TESTY LOGIKI SORTOWANIA (Faza 2)")
    print("=" * 70)
    results = []

    results.append(case("Pusta klatka", [], config.OBJ_NONE, classifier.DECISION_NONE))
    results.append(case("Sama osoba", [Fake(PERSON, 0.95)], config.OBJ_PERSON, classifier.DECISION_IGNORE))
    # KLUCZOWY test z Twojego zrzutu: 2 osoby + telefon -> wygrywa PRODUKT (telefon)
    results.append(case("2 osoby (93/89) + telefon (79)",
                        [Fake(PERSON, 0.93), Fake(PERSON, 0.89), Fake(PHONE, 0.79)],
                        config.OBJ_PHONE, classifier.DECISION_ACT2))
    results.append(case("Kubek", [Fake(CUP, 0.82)], config.OBJ_CUP, classifier.DECISION_ACT1))
    results.append(case("Nozyczki (przepusc)", [Fake(SCISSORS, 0.80)], config.OBJ_SCISSORS, classifier.DECISION_PASS))
    results.append(case("Klawiatura (przepusc)", [Fake(KEYBOARD, 0.88)], config.OBJ_KEYBOARD, classifier.DECISION_PASS))
    results.append(case("Butelka", [Fake(BOTTLE, 0.76)], config.OBJ_BOTTLE, classifier.DECISION_ACT3))
    results.append(case("Ksiazka", [Fake(BOOK, 0.70)], config.OBJ_BOOK, classifier.DECISION_PASS))
    # dwa produkty -> wygrywa wyzsza pewnosc (butelka 0.90 > telefon 0.60)
    results.append(case("Butelka (90) + telefon (60)",
                        [Fake(BOTTLE, 0.90), Fake(PHONE, 0.60)],
                        config.OBJ_BOTTLE, classifier.DECISION_ACT3))
    # klasa spoza mapy -> ignorowana, brak obiektu
    results.append(case("Tylko klasa spoza mapy (samolot)",
                        [Fake(AIRPLANE, 0.99)], config.OBJ_NONE, classifier.DECISION_NONE))

    print("-" * 70)
    passed = sum(results)
    total = len(results)
    tag = "[ OK ]" if passed == total else "[FAIL]"
    print(f"{tag} WYNIK: {passed}/{total} testow zaliczonych.")
    print("=" * 70)


if __name__ == "__main__":
    main()
