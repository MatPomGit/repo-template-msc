# Integracja manuskryptów MSC z Zotero

**Standard v1.2.0, 19.11.2026.** Zotero jest źródłem metadanych bibliograficznych, a Better BibTeX eksportuje je do wersjonowanego `references.bib`. GitHub Actions sprawdza cytowania bez logowania się do Zotero.

## Konfiguracja lokalna

1. Zainstaluj [Zotero](https://www.zotero.org/) i rozszerzenie [Better BibTeX](https://retorque.re/zotero-better-bibtex/installation/).
2. Utwórz osobną kolekcję dla artykułu P01. W Zotero wybierz **Export Collection…** i translator **Better BibTeX**. Nie wybieraj Better BibLaTeX dla domyślnego `natbib`/BibTeX.
3. Zaznacz **Keep updated** i zapisz eksport do `manuscripts/P01/references.bib`. Wyłącz eksport notatek, załączników i adnotacji, a zawartość obejrzyj przed commitem. Początkowy plik z komentarzem jest placeholderem do zastąpienia.
4. Sprawdź, czy eksport rzeczywiście aktualizuje plik po edycji kolekcji. Dopiero wtedy w `manuscripts/P01/zotero.json` ustaw `auto_export_status` na `configured`. To deklaracja użytkownika, nie atestacja synchronizacji.
5. Wstawiaj w LaTeX `\citep{klucz}`, `\citet{klucz}` lub `\cite{klucz}`. Po użyciu rekordu przypnij jego citation key w Zotero. Nie edytuj ręcznie eksportu, bo ponowny eksport go nadpisze.
6. Przed commitem uruchom `python scripts/check_zotero.py --root .`. Przed złożeniem: `python scripts/check_zotero.py --root . --require-setup` oraz kompilację PDF z BibTeX (np. `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` z katalogu manuskryptu).

## Pliki i kolejne artykuły

- `manuscripts/P01/zotero.json`: lokalny opis sposobu eksportu, bez API key, identyfikatora konta i hasła.
- `manuscripts/P01/references.bib`: plik generowany przez Better BibTeX, kontrolowany wersjami Git. Wybieraj konkretną kolekcję, nie całą prywatną bibliotekę.
- `manuscripts/P01/main.tex`: kanoniczny plik manuskryptu LaTeX; `\bibliography{references}` wykorzystuje eksport.
- `manuscripts/P01/figures/*.tex`: osobne źródła rysunków TikZ; cytowania występujące w figurach też są kontrolowane.
- Dla P02, P03 itd. twórz oddzielną kolekcję i oddzielne `references.bib` oraz `zotero.json`. Nigdy nie podłączaj dwóch autoeksportów do jednego pliku.

## Wymagania redakcyjne

**MDPI (Sensors, Future Internet):** używaj Better BibTeX i oficjalnego stylu czasopisma; paczka źródeł obejmuje `.bib` i rysunki z `figures/`. **Elsevier (Information Fusion, New Ideas in Psychology, Journal of Biomedical Informatics):** neutralny `natbib`/BibTeX można dostosować do `elsarticle` z zachowaniem kluczy. **Scientific Reports:** stosuj oficjalny szablon Springer Nature i wytyczne dotyczące plików rewizyjnych. Nie kopiuj automatycznie klas i stylów bez kontroli licencji.

Istniejące QMD może korzystać z tej samej bibliografii i cytowań `[@klucz]`; nie trzeba konwertować opublikowanych czy już zgłoszonych manuskryptów. Better BibLaTeX i Biber wymagają odrębnego, jawnego wyboru.

## Bezpieczeństwo i ograniczenia

GitHub CI **nie łączy się z Zotero**, nie pobiera załączników i nie ustala świeżości eksportu. Skrypt jest statyczną kontrolą brakujących i powielonych kluczy oraz niepożądanych pól załączników, a nie pełnym parserem BibTeX, recenzją źródeł ani kontrolą DOI. Nigdy nie umieszczaj w repo `zotero.sqlite`, kopii biblioteki, danych uczestników, prywatnych PDF czy tokenów API.

Oficjalna dokumentacja: [Auto-export / Keep updated](https://retorque.re/zotero-better-bibtex/exporting/auto/), [Citation keys](https://retorque.re/zotero-better-bibtex/citing/index.html), [Export preferences](https://retorque.re/zotero-better-bibtex/preferences/export/index.html).
