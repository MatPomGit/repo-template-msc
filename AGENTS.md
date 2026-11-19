# Instrukcje dla agentów w projekcie `msc-*`

1. Obowiązuje polityka właściciela, Research Autopilot i granice zgód. Nie twórz drugiego schedulera, kolejki, kontrolera ani automatycznej publikacji.
2. Prawda naukowa znajduje się w niniejszym repozytorium i jego protokołach. Nie przepisuj wyników z innych projektów bez pochodzenia i wskazania pierwotnego właściciela.
3. Przed modyfikacją czytaj `README.md`, `PROJECT_STATE.yaml`, `RESEARCH.md`, `research/protocol.md`, `research/analysis-plan.md` i bieżące Issues/PR. Weryfikuj aktualne SHA źródeł i submodułów, nie tylko przypięte wersje.
4. Zawsze rozróżniaj koncepcję, symulację, test kodu, pilotaż, rzeczywisty pomiar, wynik, recenzję i publikację. Brak danych = `NOT_COLLECTED`.
5. Nie generuj fikcyjnych danych, DOI, approvals, rezultatów, ani cytowań. Odnotuj wyniki negatywne i odchylenia od protokołu.
6. Dane uczestników, dane zdrowotne, nagrania twarzy/EEG/gaze, sekrety i zastrzeżone treści skal nigdy nie trafiają do Git ani do publicznego artefaktu Pages.
7. Przed rekrutacją sprawdź status zgody etycznej, prawną podstawę przetwarzania oraz wersje kwestionariuszy. Prawa do skal potwierdź oddzielnie.
8. Wykorzystuj kanoniczny katalog aparatury Research Autopilot. Nie duplikuj jego kart ani nie uznawaj wykrycia USB/BLE za pomiar zwalidowany.
9. Stosuj wersjonowane zależności: `msc-*` nauka, `app-*` aplikacje, `lib-*` pakiety; submoduły lub repozytoria źródłowe nie mogą być automatycznie podmieniane podczas reprodukcji zamrożonego eksperymentu.
10. GitHub Pages jest publiczną projekcją zawartości `docs/`, nie kopią prywatnego repo. Publikację zewnętrzną i duże wydatki poprzedza wymagane zatwierdzenie.
11. Limit otwartych PR, reguły niezależnego przeglądu i zero dodatkowych wydatków są dziedziczone z aktualnej polityki Research Autopilot. Brak miejsca w WIP oznacza wstrzymanie nowego PR, nie obejście przez push do `main`.
12. Po zmianach uruchom `python scripts/validate_repository.py --root . --phase scaffold`, zapisując SHA, zakres i faktyczny rezultat. `PASS` tylko po wykonanym teście.
