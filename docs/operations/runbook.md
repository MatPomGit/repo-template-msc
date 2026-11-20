# Runbook odtwarzania środowiska badawczego

**Status: NOT_CONFIGURED.** Szablon nie ma produkcyjnego procesu, urządzenia ani wyników do odtworzenia.

Przy rozpoczęciu projektu opisz sprawdzone polecenia tworzenia izolowanego środowiska, pobrania zamrożonego SHA kodu i zależności, weryfikacji danych, kompilacji LaTeX/BibTeX, wykonania analizy i raportowania jej wyniku. Nie wpisuj sekretów, prywatnych ścieżek użytkowników ani danych uczestników.

Oddziel od siebie: statyczną kontrolę kontraktu, kontrolę Zotero, kompilację redakcyjną i rzeczywistą analizę danych. Raportuj niezrealizowane kroki jako `NOT_RUN` lub `UNAVAILABLE`, nigdy `PASS`. Aktualizację i rollback środowiska przeprowadzaj wyłącznie w uprawnionych lokalizacjach, bez przerywania cudzych obliczeń.

Wytyczne źródłowe: [reprodukowalność](../../REPRODUCIBILITY.md), [formaty redakcyjne](../journal-formats.md), [Zotero](../zotero.md) i [dane](../../research/data-management.md).

## Ochrona gałęzi `main` i weryfikacja PR

Przed dopuszczeniem zmian R2/R3 skonfiguruj w GitHub (Settings → Rules → Rulesets) dla gałęzi domyślnej: **Require a pull request before merging**, co najmniej jedną rzeczywiście niezależną recenzję (`APPROVED` od innej tożsamości) i **Require status checks to pass** z dokładną nazwą joba `offline-msc-validation` (workflow `MSC research contract`). Zachowaj blokadę usunięcia i wymuszonego push, ograniczaj bypass i wyłącz bezpośrednie zapisy do `main`. Zweryfikuj źródło checka GitHub App oraz przeprowadź test odrzucenia merge bez review i bez wymaganego CI.

Dla repozytoriów **prywatnych** domyślny workflow ma warunek wykluczający uruchomienie; `SKIPPED` nie oznacza `PASS`. Przed ustawieniem statusu jako required zapewnij uprawniony, izolowany check działający na exact PR SHA, bez sekretów i danych uczestników, lub pozostaw merge na `HOLD`. Nie uruchamiaj niezaufanych PR na stałym runnerze.

Stan zaobserwowany 2026-11-20: ruleset `27652671` zawierał `deletion` i `non_fast_forward` oraz `bypass_mode: always`, bez wymaganego status check i review. Zmiana niniejszej dokumentacji **nie zmienia ustawień GitHub**. Do zamknięcia blokady niezbędne są uprawniona modyfikacja rulesetu i ponowny audyt. Wynik samych testów nie jest egzekwowaniem ochrony.
