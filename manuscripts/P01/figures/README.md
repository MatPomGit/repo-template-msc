# Rysunki w manuskrypcie MSC

Każdy rysunek TikZ ma **osobny plik `.tex` w tym katalogu**, np. `study-workflow.tex`. `main.tex` zawiera jedynie wywołanie `\\input{figures/study-workflow.tex}`, a nie kod rysunku. Rysunek w pliku pomocniczym zawiera środowiska `figure` i `tikzpicture`, podpis `\\caption` i etykietę `\\label`. Preambuła z `\\usepackage{tikz}` i bibliotekami należy do dokumentu głównego lub osobnego pliku konfiguracyjnego.

Rysunki są częścią źródeł artykułu: przechowuj je w Git wraz z bibliografią i plikami wymaganymi do kompilacji. Rysunek przykładowy ma charakter wyłącznie schematyczny i nie stanowi wyniku badania. Przed zgłoszeniem sprawdź czytelność, skale i jednostki, zgodność z instrukcjami czasopisma oraz ewentualną konieczność dostarczenia osobnych plików PDF/EPS/TIFF. Dla utrzymania reprodukowalności nie wklejaj renderów wyników z nieudokumentowanego źródła ani rysunków z niezweryfikowanymi danymi.

Struktura:
```text
manuscripts/P01/
├── main.tex
├── references.bib
└── figures/
    ├── README.md
    └── study-workflow.tex
```
