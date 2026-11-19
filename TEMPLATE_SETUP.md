# Instrukcja zastosowania szablonu

Ten katalog stanowi kompletny, przenośny **szkielet repozytorium `msc-*`**. Przy tworzeniu nowego badania kopiuj całą jego zawartość jako korzeń repozytorium. Następnie uzupełnij pola `REPLACE`, protokół i statusy, uruchom walidator i ustal uprawnienia repozytorium.

1. Utwórz prywatne lub publiczne repo `msc-<krótki-temat>`; przed publikacją wybierz politykę danych i praw.
2. Skopiuj zawartość katalogu szablonu do nowego repo (łącznie z `.github`, `.gitignore`, `.gitattributes`). Nie kopiuj otaczającego repozytorium Research Autopilot, historii jego commitów ani jego sekretów.
3. Zastąp `REPLACE_PROJECT_ID`, `REPLACE_OWNER`, tytuły, program ARC i licencję. Zachowaj Mateusza Pomianka jako autora podstawowego; zweryfikowanych współautorów dopisz do `CITATION.cff` i metadanych każdego odpowiedniego manuskryptu. Wypełnij `research/protocol.md`, `research/analysis-plan.md`, `research/ethics.md` i `software/dependencies.yaml`.
4. Uruchom `python scripts/validate_repository.py --root . --phase scaffold` oraz `python -m unittest discover -s tests -v`. Wynik PASS oznacza **strukturę**, nie gotowość badania.
5. Jeśli GitHub otrzyma osobne repo oznaczone jako **Template repository**, można tworzyć nowe repozytoria przyciskiem `Use this template` lub GitHub CLI. Kopiowana jest zawartość plików, **nie** historia źródłowego projektu. Włączanie `is_template` wymaga odpowiednich uprawnień administracyjnych; sama struktura folderu nie ustawia flagi GitHub.
6. Uzupełnij i zatwierdź źródła, prawa oraz witrynę. Uruchom `--phase publish` przed publikacją publicznej części. Walidator nie ocenia etyki, cytowań ani wartości naukowej; wymaga oddzielnego audytu.
7. Program `arc-*` może odwoływać się do projektu linkiem lub submodułem przypiętym SHA. Nowe repo **nie jest** submodułem automatycznie. Wybór repo nadrzędnego wymaga zgodności z jego polityką WIP oraz prywatnością.

**Uwaga:** w trybie scaffold README dopuszcza `NOT_COLLECTED`, `NOT_REGISTERED` i inne uczciwe stany. Nie należy wpisywać fikcyjnego DOI ani wyniku tylko po to, aby spełnić schemat. `publish` sprawdza konfigurację szablonu, nie akceptację naukową.

## Autorstwo i współautorstwo

Mateusz Pomianek musi pozostać co najmniej jednym z autorów każdego projektu `msc-*` utworzonego z tego wzorca. Pozostali autorzy są opcjonalni: dopisuj ich po potwierdzeniu rzeczywistego wkładu, zgody, afiliacji i uzgodnieniu kolejności zgodnie z wymaganiami czasopisma. Nie kopiuj fikcyjnych danych współautorów. Spójność autorów sprawdzaj między `CITATION.cff` i domyślnym `manuscripts/P*/main.tex` lub zadeklarowanym alternatywnym źródłem.

## Środowisko CI i koszty

W repozytoriach **publicznych** dopuszczalne są GitHub-hosted runners (np. `ubuntu-latest`) do bezpiecznych testów i walidacji. Nie ma obowiązku używania runnerów lokalnych. W repozytoriach prywatnych dobierz runner zgodnie z uprawnieniami, poufnością i zasadą braku niezatwierdzonych kosztów. Nie przekazuj sekretów niezaufanym PR z forków ani nie uruchamiaj ich uprzywilejowanych zadań na maszynach z dostępem do prywatnych zasobów. Ustaw minimalne `GITHUB_TOKEN` permissions. Szablon ma podstawowe CI w `.github/workflows/msc-contract-tests.yml` uruchamiane tylko dla publicznych repozytoriów; patrz [audyt i plan napraw](reviews/2026-11-19-template-audit.md).

## Migracja istniejących projektów bez zmiany ścieżek naukowych

Obowiązkowe dokumenty pozostają wymagane, lecz `PROJECT_STATE.yaml` może wskazywać ich rzeczywiste ścieżki: `protocol_path`, `analysis_plan_path`, `ethics_path`, `data_management_path`, `preregistration_path`, `decisions_path`, `evidence_register_path`, `software_manifest_path`. Dla manuskryptu o niestandardowej nazwie ustaw `manuscript_root`, `manuscript_source` i opcjonalnie `bibliography_path`. Nazwa pliku może być `praca.qmd` lub `main.tex`. Nie stosować ścieżek absolutnych, `..` ani linków poza repozytorium. Dla nowego MSC pozostają domyślne pliki `manuscripts/P01`.

W przypadku istniejącej migracji `msc-mgr` nie należy kopiować atrapy P01 tylko po to, aby zaliczyć test struktury. Braki dotyczące realnego protokołu, etyki, bibliografii lub prerejestracji pozostają błędami; naukowa gotowość wymaga niezależnej oceny.

## LaTeX jako format kanoniczny (v1.1.0)

Nowe `msc-*` otrzymują `manuscripts/P01/main.tex`, `references.bib`, `manuscript_format: latex` oraz jawne `manuscript_source`. Neutralny szablon `article` jest przeznaczony do pisania szkicu, a przed zgłoszeniem trzeba użyć właściwego szablonu czasopisma. Informacje o *Sensors*, *Information Fusion*, *New Ideas in Psychology*, *Journal of Biomedical Informatics*, *Scientific Reports* i *Future Internet* są w [docs/journal-formats.md](docs/journal-formats.md). QMD nie znika z walidatora: istniejące badania mogą pozostać w QMD bez zmian, pod warunkiem jawnej deklaracji `manuscript_format: quarto` i zgodnego `manuscript_source`. Przy zmianie formatu nie twórz automatycznie alternatywnego źródła artykułu bez uzgodnienia kanonicznej wersji.
