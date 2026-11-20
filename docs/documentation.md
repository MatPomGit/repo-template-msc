# Standard dokumentacji i budżety znaków MSC

Kanoniczne źródła prawdy są rozdzielone: [README](../README.md) opisuje projekt, [ARCHITECTURE](../ARCHITECTURE.md) organizację systemu, [RESEARCH](../RESEARCH.md) proces naukowy, [protokół](../research/protocol.md) plan badania, [SAP](../research/analysis-plan.md) analizę, [REPRODUCIBILITY](../REPRODUCIBILITY.md) odtwarzalność, [SECURITY](../SECURITY.md) ochronę danych. [ADR](adr/README.md) dokumentują decyzje architektoniczne; `research/decisions.md` zapisuje decyzje naukowe. Nie kopiuj treści między dokumentami.

## Limity

Źródłem konfiguracji jest [config/documentation-policy.json](../config/documentation-policy.json). Długość oznacza **liczbę znaków Unicode** (pythonowe `len(text)`, z białymi znakami), nie bajty UTF-8. Kontrolę uruchamia `python scripts/validate_documentation.py` i CI.

| Typ dokumentu | Maksimum znaków |
| --- | ---: |
| `AGENTS.md`, `README.md`, `ARCHITECTURE.md` | 12 000 |
| `SECURITY.md`, procedura agentów i odtwarzalność | 10 000 |
| `CODE_OF_CONDUCT.md`, `SUPPORT.md`, pojedyncze ADR | 6 000–6 500 |
| `GOVERNANCE.md` | 7 000 |
| Wewnętrzne rozdziały dokumentacji | 8 500–10 000 |
| Strony publiczne w `pages/` | 6 000 |
| `research/protocol.md`, `research/analysis-plan.md` | 12 000 |

Ścieżki protokołu, SAP, etyki i dokumentów naukowych mogą być mapowane z `PROJECT_STATE.yaml`: limit podąża za aktualnym plikiem, a nie zmusza do zachowania pierwotnej nazwy. Nie uznawaj starego placeholdera za dokument kanoniczny.

**Manuskrypty `.tex`, `.qmd`, bibliografie `.bib`, dane i wyniki nie podlegają tym limitom redakcyjnym.** Nie skracaj opisu metod ani dowodów dla spełnienia budżetu dokumentacji administracyjnej. W długim protokole utwórz jeden właściwy odrębny aneks i powiąż go z protokołem, zamiast usuwać uzasadnienia etyczne lub powtarzalne szczegóły. Zmiana limitów wymaga uzasadnienia i testów w PR.

## Fazy aktualizacji

**Scaffold:** zachowaj prawdziwe stany `NOT_ASSESSED`, `NOT_COLLECTED` i `NOT_RUN`; dokumenty nie poświadczają wykonania badań.

**Przed pierwszym pomiarem:** utrwal protokół, SAP, rzeczywiste decyzje etyczne, plan zarządzania danymi, bezpieczeństwo i aparaturę. Oddziel działania nieprzeprowadzone od potwierdzonych.

**Pierwsza analiza:** uzupełnij przepływy i parametry, SHA kodu, dane wejściowe, plan kontroli jakości, status wyników i dowody. Nie dopisuj fikcyjnych cytowań ani pomiarów.

**Manuskrypt i zgłoszenie:** wykorzystuj jeden kanoniczny LaTeX/BibTeX na artykuł, rysunki TikZ w `figures/` i osobne profile redakcyjne. Weryfikuj przypisy Zotero, kompilację, wydawnicze warunki licencji i prawa do danych. `QMD` dopuszczaj wyłącznie po świadomym wyborze.

**Publikacja Pages:** pisz wyłącznie w `pages/`, na podstawie zatwierdzonych faktów. Nie kopiuj `docs/`, protokołów, notatek redakcyjnych i instrukcji do agentów. Kontroluj zawartość, linki i widoczność witryny, szczególnie przy prywatnym repozytorium. Pełna polityka: [GitHub Pages](pages.md).

Budżety znaków służą ograniczeniu redundancji. Brak testów, nieaktualne odnośniki, dane prywatne i niepotwierdzone twierdzenia stanowią niezależne błędy jakości.
