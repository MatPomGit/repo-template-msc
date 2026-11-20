# Manuskrypt P01

**Status:** concept. **Główne pytanie:** do uzupełnienia. **Kontrybucja:** do uzupełnienia. **Zbiór danych:** NOT_COLLECTED.

Źródło tekstu: [main.tex](main.tex). Bibliografia: [references.bib](references.bib). Wyniki wypełniać tylko na podstawie identyfikowalnych, wygenerowanych artefaktów i rejestru dowodów. Cytowania sprawdzać w pełnym tekście źródeł. Nie traktować planów ani danych syntetycznych jako wyników empirycznych.

**Profil:** `generic-latex`; przełącz na oficjalny szablon wydawcy przed zgłoszeniem. Dokument `main.tex` to kanoniczne źródło. QMD jest opcjonalnym formatem alternatywnym, nie drugim niezależnym manuskryptem. 

## Rysunki

Rysunki TikZ znajdują się wyłącznie w [figures/](figures/README.md). W `main.tex` umieszczaj jedynie odwołania, np. `\input{figures/study-workflow.tex}`. Każdy rysunek ma osobny podpis i etykietę; przykład jest schematem demonstracyjnym, nie wynikiem empirycznym.

## Zotero

Bibliografia `references.bib` jest przygotowana do autoeksportu z Zotero/Better BibTeX. Plik [zotero.json](zotero.json) zawiera tylko niesekretne ustawienia, a [instrukcja](../../docs/zotero.md) opisuje konfigurację `Keep updated`. Eksport wymaga lokalnej instalacji Zotero i nie jest jeszcze aktywny w szablonie. Nie edytuj generowanego pliku `.bib` ręcznie.
