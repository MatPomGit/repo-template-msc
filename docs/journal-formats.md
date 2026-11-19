# Format źródeł manuskryptów i profile wydawnicze

**Stan weryfikacji: 2026-11-19. Standard MSC v1.1.0.** Podstawowym plikiem źródłowym artykułu jest `main.tex` z `references.bib`. QMD/Markdown pozostają formatami dopuszczalnymi dla istniejących badań i uzasadnionych wyjątków, ale nie są nowym domyślnym wyborem.

## Hierarchia decyzji

1. Rozpocznij w neutralnym `manuscripts/P01/main.tex` i prowadź bibliografię w BibTeX. Nie fałszuj wyników, referencji ani statusu pracy.
2. Gdy zostanie zatwierdzony cel publikacyjny, wybierz **oficjalny** szablon danego wydawcy; to szablon czasopisma rozstrzyga, nie standard ogólny. Nie przechowuj nieuprawnionych kopii plików `.cls`/`.sty` w otwartym repo.
3. Zapisz w `PROJECT_STATE.yaml` ścieżkę i format źródła, a w manuskrypcie konfigurację czasopisma i sposób kompilacji. Utrzymuj pełne źródła, grafiki, bibliografię i dający się odtworzyć PDF.
4. Twórz osobno paczkę redakcyjną zależną od wydawcy; wynik złożenia PDF nie oznacza, że redakcja przyjęła zgłoszenie.

## Sprawdzone czasopisma i zasady

| Czasopismo | Pierwsze zgłoszenie | Źródła i poprawki | Profil LaTeX |
|---|---|---|---|
| **Sensors** (MDPI) | Dopuszczalne free format, ale zalecany oficjalny szablon | Przy LaTeX pełny ZIP: `.tex`, bibliografia, grafika i pliki niezbędne do rekompilacji PDF; limit sumaryczny 120 MB; przy rewizji wymagane dopasowanie do instrukcji | `mdpi` |
| **Future Internet** (MDPI) | Jak Sensors, możliwe free format | Kompletny ZIP źródeł LaTeX, 120 MB; osobne zgody/etyka i wymagane sekcje | `mdpi` |
| **Information Fusion** (Elsevier) | Zgodnie z ogólnymi wytycznymi Elsevier większość tytułów akceptuje PDF w pierwszej recenzji; indywidualny Guide for Authors należy sprawdzić przed wysyłką | `elsarticle`, źródła TeX/BibTeX i rysunki w archiwum według wskazań Editorial Manager | `elsarticle` |
| **New Ideas in Psychology** (Elsevier) | Jak wyżej, zasady tytułu i rodzaju artykułu wymagają osobnej kontroli | Format źródeł zależny od etapu; bez nieuzgodnionej zmiany już złożonej wersji | `elsarticle` |
| **Journal of Biomedical Informatics** (Elsevier) | Jak wyżej, wymagania szczegółowe do weryfikacji w Guide for Authors | `elsarticle` i edytowalne źródła redakcyjne | `elsarticle` |
| **Scientific Reports** (Nature Portfolio) | Pierwsze zgłoszenie może być Word, LaTeX lub PDF; redakcja preferuje Word | Przy rewizji sam PDF tekstu jest niedopuszczalny; trzeba dostarczyć Word/LaTeX i osobne pliki figur | `springer-nature` |

Podawane zasady Elsevier opisują zweryfikowany standard wydawcy, a **nie indywidualnie potwierdzone limity lub wymogi każdego czasopisma**. ScienceDirect nie udostępniło treści Guide for Authors do odczytu podczas przeglądu. Dlatego w trybie `submission-ready` wymagana jest ponowna kontrola konkretnego czasopisma, kategorii artykułu i instrukcji redakcyjnych (np. highlights, graphical abstract, podwójnie anonimowy recenzent).

### Oficjalne instrukcje

- Sensors: https://www.mdpi.com/journal/sensors/instructions
- Future Internet: https://www.mdpi.com/journal/futureinternet/instructions
- MDPI LaTeX: https://www.mdpi.com/authors/latex
- Elsevier LaTeX: https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions
- Information Fusion: https://www.sciencedirect.com/journal/information-fusion/publish/guide-for-authors
- New Ideas in Psychology: https://www.sciencedirect.com/journal/new-ideas-in-psychology/publish/guide-for-authors
- Journal of Biomedical Informatics: https://www.sciencedirect.com/journal/journal-of-biomedical-informatics/publish/guide-for-authors
- Scientific Reports: https://www.nature.com/srep/author-instructions/submission-guidelines
- Springer Nature LaTeX: https://www.springernature.com/gp/authors/campaigns/latex-author-support

**Ważne:** warunki licencyjne niektórych szablonów wydawców, zwłaszcza MDPI, mogą ograniczać ich zastosowanie do zgłoszeń redakcyjnych. Nie publikuj automatycznie skompilowanych PDF opartych na takich plikach jako preprintów. W preprintach używaj neutralnego szablonu z odpowiednimi prawami.

## Kompilacja

W katalogu `manuscripts/P01`:
```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Wymagany jest rzeczywisty TeX Live/MiKTeX z odpowiednimi pakietami i BibTeX (jeśli używasz bibliografii). Zapisz wersje narzędzi, log i wynik kompilacji. Alternatywny Quarto pozostaje możliwy: `manuscript_format: quarto`, `manuscript_source: .../praca.qmd`. Kompilacja samego PDF bez źródeł nie stanowi kompletnego pakietu redakcyjnego.

## Rysunki TikZ w plikach źródłowych

Wszystkie rysunki TikZ tworzy się poza `main.tex`, w katalogu `manuscripts/P01/figures/`. **Jeden rysunek = jeden plik `.tex`** zawierający kod `tikzpicture`, podpis i etykietę. W pliku głównym umieszcza się wyłącznie np. `\input{figures/study-workflow.tex}`; deklaracje pakietów i bibliotek TikZ znajdują się w preambule. W kompilacji `latexmk` zachowuje się ścieżki względne względem katalogu manuskryptu.

Do paczki redakcyjnej dla MDPI, Elsevier i Springer Nature dołączaj **wszystkie źródła rysunków**, bibliografię, niezbędne pliki pomocnicze oraz wymagane przez konkretne czasopismo osobne wersje ilustracji. Jeśli redakcja żąda TIFF/EPS/PDF, przygotuj zewnętrzną grafikę z zatwierdzonego źródła TikZ, a nie zastępuj nim źródła. Nie publikuj rysunków zawierających dane chronione ani hipotetycznych wyników jako wyników empirycznych.

## Zotero i bibliografia

Dla nowych manuskryptów preferowane jest Zotero + Better BibTeX z autoeksportem do wersjonowanego `references.bib`. Wybór klasy wydawcy zmienia styl cytowań, nie źródło metadanych. Nie przełączaj automatycznie BibTeX na Biber/BibLaTeX bez sprawdzenia szablonu konkretnego czasopisma. Instrukcje: [docs/zotero.md](zotero.md).
