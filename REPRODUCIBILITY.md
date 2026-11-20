# Reprodukowalność

Przed udostępnieniem publicznym zweryfikuj pochodzenie wszystkich rezultatów; `docs/`, konfiguracje reprodukowalności i raporty testów nie są automatycznie materiałami publicznymi. Witrynę przygotowuj wyłącznie w `pages/`.

Dla każdego zatwierdzonego wyniku zapisuj: Git SHA manuskryptu i kodu analizy; wersje zależności i środowiska; identyfikatory aparatury; schemat danych i jednostki; protokół, ustawienia kalibracji, randomizacji, ziarno RNG; wersję i sumę kontrolną zbioru danych; polecenia odtworzenia; liczbę obserwacji i wyłączeń; status wykonania; odchylenia i wyniki negatywne.

Przed analizą bieżącego portfolio odczytaj najnowsze SHA repozytoriów powiązanych. Przed odtworzeniem eksperymentu odtwórz zamrożone SHA, a nie ich najnowsze gałęzie. Stany `NOT_RUN`, `UNAVAILABLE`, `FAIL`, `PASS` są różne. Test statyczny nie oznacza walidacji metrologicznej.


## Powtarzalność kompilacji LaTeX

Dla manuskryptu przechowuj wersję TeX Live/MiKTeX, wybrany profil czasopisma, rzeczywisty SHA, bibliografię BibTeX, pliki `.sty`/`.cls` wymagane przez redakcję (jeśli można je legalnie dystrybuować), rysunki, log kompilacji i nieedytowane źródło `.tex`. PDF jest artefaktem pochodnym. QMD pozostaje wspierane wyłącznie po jawnym wyborze formatu i wskazaniu kanonicznego źródła.

Źródła rysunków TikZ muszą być odrębnymi plikami `manuscripts/<ID>/figures/*.tex`. Do odtworzenia PDF nie wystarcza sam `main.tex`: archiwum zgłoszenia i proces walidacji muszą obejmować wszystkie pliki referencjonowane przez `\input`. Każdy rysunek zawiera podpis, etykietę i opis źródła danych. Przy zmianie klasy wydawcy należy oddzielnie sprawdzić wymagany format grafiki (np. PDF, EPS, TIFF), ale nie usuwać kanonicznego źródła TikZ.

## Reprodukowalność bibliografii Zotero

Wersjonuj `references.bib` i przypięte klucze cytowań Better BibTeX razem z manuskryptem. Dla wydania zapisz Git SHA po ostatnim sprawdzonym eksporcie, uruchom `scripts/check_zotero.py` oraz kompilację BibTeX/PDF. Status eksportu z Zotero wymaga lokalnego potwierdzenia; CI nie potwierdza aktualności zdalnej biblioteki. Nie udostępniaj baz Zotero ani prywatnych załączników.
