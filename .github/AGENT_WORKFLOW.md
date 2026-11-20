# Operacyjny cykl pracy agenta MSC

**Zakres:** projekt manuskryptowy, nadrzędny [AGENTS.md](../AGENTS.md). Instrukcja nie przyznaje dostępu do danych, hostów, czasopism ani uprawnień administracyjnych.

## DoR i rozpoznanie

Zweryfikuj rzeczywistą default branch, aktualny SHA, Issues/PR/drafty, zależności `arc-*`, `app-*`, `lib-*`, lease i status CI. Najpierw dokończ to samo zadanie, zamiast mnożyć PR. Przeczytaj `RESEARCH.md`, protokół, SAP, etykę, `PROJECT_STATE.yaml`, `REPRODUCIBILITY.md` i aktualny manuskrypt. Przygotuj w Issue cel, właściciela, bieżącą bazę SHA, mierzalne kryteria, ryzyko R0-R3, potrzebne dowody, uprawnienia i ograniczenia danych. Przed każdym działaniem zewnętrznym sprawdź odrębną zgodę.

## Implementacja i nauka

Wprowadzaj minimalne, odwracalne zmiany z testami. Nie uznawaj nowego pytania badawczego za część zatwierdzonego protokołu bez zapisu decyzji. Nie twórz duplikatów manuskryptów, narzędzi, rejestrów ani alternatywnych źródeł jednego artykułu. LaTeX i `references.bib` są domyślne, TikZ pozostaje w `figures/`, a eksport Zotero nie jest edytowany ręcznie. Dane rzeczywiste nie są dostępne dla nieuprawnionych agentów; testy na syntetycznych nie oznaczają pomiaru fizycznego.

Szablony dokumentów uzupełniaj razem z rzeczywistymi zmianami. Architektura i ADR opisują granice informatyczne; protokół i `research/decisions.md` opisują naukę. Stosuj [budżety znaków](../docs/documentation.md), nie usuwając wymaganej treści naukowej.

## Testy i recenzja

Kontrole szkieletu: `python scripts/validate_repository.py --root . --phase scaffold`, `python scripts/validate_documentation.py`, `python scripts/validate_pages.py`, `python scripts/check_zotero.py --root .` oraz `python -m unittest discover -s tests -v`. Na CI nie uruchamiaj nieznanych skryptów z nieufnego PR z dostępem do sekretów/stałego runnera. Dla realnego manuskryptu sprawdź osobno PDF/LaTeX/BibTeX, wyniki liczbowe, dane i zgodność z profilem czasopisma.

Każdy rezultat ma właściwe SHA, polecenie, środowisko, `PASS/FAIL/NOT_RUN/UNAVAILABLE/SKIPPED`. Recenzent sprawdza finalny diff, pochodzenie danych, metodologię i rzeczywiste dowody; wykonawca nie deklaruje własnego przeglądu jako niezależny. `COMMENTED` nie jest formalnym `APPROVED`, a zielony CI nie daje zgody etycznej ani prawa do wydania.

## Integracja i publikacja

Przed merge sprawdź base/HEAD SHA, zmienione pliki, aktualne testy, recenzję i właściwe uprawnienia. Nie obchodź branch protection. Po merge sprawdź faktyczny commit `main`. Ukończony PR nie jest złożonym manuskryptem, opublikowaną witryną, prerejestracją ani zaakceptowaną pracą.

GitHub Pages ma wyłącznie jawnie wybrane `pages/` i [politykę](../docs/pages.md). Przed udostępnieniem wymagaj niezależnego przeglądu finalnego HTML, pozostałych zasobów i widoczności witryny oraz osobnej zgody właściciela. Nie publikuj automatycznie `docs/` lub danych badawczych. Dla prywatnego repo szczególnie sprawdź, czy strona nie będzie publiczna.

## DoD, blokady i wznowienie

Zadanie zakończone ma mierzalne kryteria spełnione rzeczywistym dowodem na aktualnym SHA, aktualne dokumenty, właściwy review oraz uprawnioną integrację. Niewykonalne kroki oznacz `UNAVAILABLE`, brak testu `NOT_RUN`, brak danych `NOT_COLLECTED`. Zapisz raport w Issue/PR: źródłowy SHA, wynikowy SHA, zmienione pliki, testy, ryzyka, decyzje i następny krok. Przy blokadzie pozostaw jeden punkt wznowienia zamiast duplikować zadania. Sprzątaj tylko własne, bezpiecznie rozliczone zasoby. Nie przerywaj cudzych procesów badawczych.
