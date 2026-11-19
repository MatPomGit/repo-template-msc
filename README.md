# [Tytuł projektu badawczego]

**Typ:** samodzielny projekt manuskryptowy `msc-*`  
**Program:** `arc-neuro` / `arc-ai` / `arc-xr` / `arc-robo` (wybrać jeden główny)  
**Status:** planowany; brak wyników empirycznych  
**Wersja szablonu:** 1.2.0  
**Autor podstawowy:** Mateusz Pomianek (pozostaje w każdym projekcie); dodatkowi współautorzy: opcjonalnie, po potwierdzeniu wkładu

## Cel i wkład naukowy

Opisz główne pytanie, wkład, populację/zestaw danych i ograniczenia. Nie traktuj tytułu roboczego ani planowanych wyników jako dowodu.

**Kanoniczny format artykułów:** LaTeX (`manuscripts/P01/main.tex`, `references.bib`); QMD/Markdown tylko jako jawnie skonfigurowane alternatywy. Rysunki TikZ zapisuj w osobnych plikach `manuscripts/P01/figures/*.tex` i dołączaj przez `\input{figures/nazwa.tex}`; nie umieszczaj środowisk `tikzpicture` w `main.tex`. Przed zgłoszeniem przełącz na oficjalny profil czasopisma. Zasady: [formaty redakcyjne](docs/journal-formats.md).

## Rejestr publikacji

| ID | Tytuł roboczy | Stan | Źródło |
| --- | --- | --- | --- |
| P01 | [Tytuł] | concept | [manuscripts/P01/README.md](manuscripts/P01/README.md) |

## Badanie i reprodukowalność

Protokół: [research/protocol.md](research/protocol.md). Plan analiz: [research/analysis-plan.md](research/analysis-plan.md). Etyka: [research/ethics.md](research/ethics.md). Dane: [research/data-management.md](research/data-management.md). Źródła dowodów: [research/evidence-register.csv](research/evidence-register.csv). Decyzje: [research/decisions.md](research/decisions.md). Aparatura: [equipment/README.md](equipment/README.md). Oprogramowanie: [software/dependencies.yaml](software/dependencies.yaml).

Wersje kodu oraz zależności muszą być przypięte do SHA, tagu lub digestu; brak zwalidowanego pomiaru oznacz `NOT_VERIFIED`, nie `PASS`.

## Otwarta nauka

Strona projektu: **NOT_CONFIGURED**. Prerejestracja: **NOT_REGISTERED**. Preprint: **NOT_PUBLISHED**. Zbiór danych: **NOT_PUBLISHED**. Identyfikatory DOI i URL dodawać dopiero po ich potwierdzeniu. Publiczna strona MkDocs pochodzi wyłącznie z `docs/` i nie ujawnia danych uczestników.

## Uruchamianie i jakość

```bash
python scripts/validate_repository.py --root . --phase scaffold
python -m unittest discover -s tests -v
# po uzupełnieniu materiałów gotowych do publikacji:
python scripts/validate_repository.py --root . --phase publish
```

## Audyt wzorca

Zidentyfikowane braki, priorytety oraz kryteria akceptacji: [audyt z 2026-11-19](reviews/2026-11-19-template-audit.md). Publiczne repozytoria korzystają z izolowanego, odczytowego workflow CI. Kompilacja pełnego LaTeX wymaga osobnego, zweryfikowanego środowiska.

## Własność i licencja

Przed publikacją ustal autorstwo, instytucję, licencję kodu, prawne podstawy udostępniania materiałów i ewentualne licencje kwestionariuszy. Domyślny plik `LICENSE` **nie nadaje otwartej licencji**.

## Zotero i bibliografia

Zotero + Better BibTeX pozwala automatycznie eksportować odrębną kolekcję manuskryptu do `manuscripts/P01/references.bib`. CI sprawdza spójność cytowań lokalnie, bez konta i API. Konfiguracja: [docs/zotero.md](docs/zotero.md); komenda: `python scripts/check_zotero.py --root .`.
