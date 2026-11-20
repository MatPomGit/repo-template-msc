# Instrukcja zastosowania szablonu

Ten katalog stanowi kompletny, przenośny **szkielet repozytorium `msc-*`**. Przy tworzeniu nowego badania kopiuj całą jego zawartość jako korzeń repozytorium. Następnie uzupełnij pola `REPLACE`, protokół i statusy, uruchom walidator i ustal uprawnienia repozytorium.

1. Utwórz prywatne lub publiczne repo `msc-<krótki-temat>`; przed publikacją wybierz politykę danych i praw.
2. Skopiuj zawartość katalogu szablonu do nowego repo (łącznie z `.github`, `.gitignore`, `.gitattributes`). Nie kopiuj otaczającego repozytorium Research Autopilot, historii jego commitów ani jego sekretów.
3. Zastąp `REPLACE_PROJECT_ID`, `REPLACE_OWNER`, tytuły, program ARC i licencję. Zachowaj Mateusza Pomianka jako autora podstawowego; zweryfikowanych współautorów dopisz do `CITATION.cff` i metadanych każdego odpowiedniego manuskryptu. Wypełnij `research/protocol.md`, `research/analysis-plan.md`, `research/ethics.md` i `software/dependencies.yaml`.
4. Uruchom `python scripts/validate_repository.py --root . --phase scaffold`, `python scripts/validate_documentation.py`, `python scripts/validate_pages.py` i `python -m unittest discover -s tests -v`. Wynik PASS oznacza **strukturę**, nie gotowość badania.
5. Jeśli GitHub otrzyma osobne repo oznaczone jako **Template repository**, można tworzyć nowe repozytoria przyciskiem `Use this template` lub GitHub CLI. Kopiowana jest zawartość plików, **nie** historia źródłowego projektu. Włączanie `is_template` wymaga odpowiednich uprawnień administracyjnych; sama struktura folderu nie ustawia flagi GitHub.
6. Uzupełnij i zatwierdź źródła, prawa oraz [publiczną witrynę](docs/pages.md). `pages/` zawiera wyłącznie odrębnie przejrzane materiały dla odwiedzających, a `docs/` nie może być publikowanym źródłem. Każdy zasób dodaj do `config/pages-policy.json`. Uruchom `--phase publish` przed odrębnym zatwierdzeniem publicznej części. Walidacja nie publikuje strony ani artykułu. Walidator nie ocenia etyki, cytowań ani wartości naukowej; wymaga oddzielnego audytu.
7. Program `arc-*` może odwoływać się do projektu linkiem lub submodułem przypiętym SHA. Nowe repo **nie jest** submodułem automatycznie. Wybór repo nadrzędnego wymaga zgodności z jego polityką WIP oraz prywatnością.

**Uwaga:** w trybie scaffold README dopuszcza `NOT_COLLECTED`, `NOT_REGISTERED` i inne uczciwe stany. Nie należy wpisywać fikcyjnego DOI ani wyniku tylko po to, aby spełnić schemat. `publish` sprawdza konfigurację szablonu, nie akceptację naukową.

## Kontrakty dla rozwijających się projektów MSC

Po utworzeniu manuskryptu zaktualizuj [architekturę](ARCHITECTURE.md), [przepływy danych](docs/architecture/data-flow.md), [reprodukowalność](docs/architecture/reproducibility.md), [model zagrożeń](docs/security/threat-model.md) i właściwe [ADR](docs/adr/README.md), nie powielając `research/decisions.md`. Przed pierwszymi badaniami sprawdź protokół, SAP, etykę i prawa do materiałów. Przed wydaniem zweryfikuj zamrożone SHA danych i kodu, Zotero, kompilację LaTeX, licencje i kanał zgłoszeń. Stosuj [limity znaków](docs/documentation.md).

GitHub Pages wymaga osobnego `pages/` i ręcznego audytu treści/widoczności. Nigdy nie konfiguruj publikacji z `main:/docs` ani z korzenia repo, również gdy repozytorium jest prywatne. Nie publikuj na stronie instrukcji dla agentów, uwag redakcyjnych ani niezatwierdzonych wyników. Szablon nie zawiera i nie potrzebuje pliku `CONTRIBUTING.md`.

## Autorstwo i współautorstwo

Mateusz Pomianek musi pozostać co najmniej jednym z autorów każdego projektu `msc-*` utworzonego z tego wzorca. Pozostali autorzy są opcjonalni: dopisuj ich po potwierdzeniu rzeczywistego wkładu, zgody, afiliacji i uzgodnieniu kolejności zgodnie z wymaganiami czasopisma. Nie kopiuj fikcyjnych danych współautorów. Spójność autorów sprawdzaj między `CITATION.cff` i domyślnym `manuscripts/P*/main.tex` lub zadeklarowanym alternatywnym źródłem.

## Środowisko CI i koszty

W repozytoriach **publicznych** dopuszczalne są GitHub-hosted runners (np. `ubuntu-latest`) do bezpiecznych testów i walidacji. Nie ma obowiązku używania runnerów lokalnych. W repozytoriach prywatnych dobierz runner zgodnie z uprawnieniami, poufnością i zasadą braku niezatwierdzonych kosztów. Nie przekazuj sekretów niezaufanym PR z forków ani nie uruchamiaj ich uprzywilejowanych zadań na maszynach z dostępem do prywatnych zasobów. Ustaw minimalne `GITHUB_TOKEN` permissions. Szablon ma podstawowe CI w `.github/workflows/msc-contract-tests.yml` uruchamiane tylko dla publicznych repozytoriów; patrz [audyt i plan napraw](reviews/2026-11-19-template-audit.md).

**Bramka dla prywatnych repozytoriów:** ten workflow celowo pomija job (`SKIPPED`). Nie traktuj tego statusu jako `PASS` ani dowodu na aktualnym HEAD. Dla zmian R2/R3 przed scaleniem wykonaj w zaakceptowanym środowisku izolowanym, bez sekretów i dostępu do danych uczestników: `python3 -B scripts/validate_repository.py --root . --phase scaffold`, `python3 -B scripts/validate_documentation.py`, `python3 -B scripts/validate_pages.py`, `python3 -B scripts/check_zotero.py --root .` i `python3 -B -m unittest discover -s tests -v`. W PR zapisz exact SHA, środowisko, polecenia, wyniki, logi i niezależną recenzję; dopiero po ich potwierdzeniu autoryzuj integrację. Jeśli brak bezpiecznego środowiska lub dowodów, pozostaw `BLOCKED`. Nie uruchamiaj niezaufanego PR na stałym HomeServerze/Andromedzie i nie zlecaj płatnych runnerów bez osobnej zgody. Sam szablon nie konfiguruje branch protection ani zewnętrznego wymaganego statusu; właściciel projektu musi zapewnić egzekwowanie bramki, np. wymaganą recenzją i regułami gałęzi.

## Migracja istniejących projektów bez zmiany ścieżek naukowych

Obowiązkowe dokumenty pozostają wymagane, lecz `PROJECT_STATE.yaml` może wskazywać ich rzeczywiste ścieżki: `protocol_path`, `analysis_plan_path`, `ethics_path`, `data_management_path`, `preregistration_path`, `decisions_path`, `evidence_register_path`, `software_manifest_path`. Dla manuskryptu o niestandardowej nazwie ustaw `manuscript_root`, `manuscript_source` i opcjonalnie `bibliography_path`. Nazwa pliku może być `praca.qmd` lub `main.tex`. Nie stosować ścieżek absolutnych, `..` ani linków poza repozytorium. Dla nowego MSC pozostają domyślne pliki `manuscripts/P01`.

W przypadku istniejącej migracji `msc-mgr` nie należy kopiować atrapy P01 tylko po to, aby zaliczyć test struktury. Braki dotyczące realnego protokołu, etyki, bibliografii lub prerejestracji pozostają błędami; naukowa gotowość wymaga niezależnej oceny.

## LaTeX jako format kanoniczny (v1.1.0)

Nowe `msc-*` otrzymują `manuscripts/P01/main.tex`, `references.bib`, `manuscript_format: latex` oraz jawne `manuscript_source`. Neutralny szablon `article` jest przeznaczony do pisania szkicu, a przed zgłoszeniem trzeba użyć właściwego szablonu czasopisma. Informacje o *Sensors*, *Information Fusion*, *New Ideas in Psychology*, *Journal of Biomedical Informatics*, *Scientific Reports* i *Future Internet* są w [docs/journal-formats.md](docs/journal-formats.md). QMD nie znika z walidatora: istniejące badania mogą pozostać w QMD bez zmian, pod warunkiem jawnej deklaracji `manuscript_format: quarto` i zgodnego `manuscript_source`. Przy zmianie formatu nie twórz automatycznie alternatywnego źródła artykułu bez uzgodnienia kanonicznej wersji.

## Obowiązkowe wydzielenie TikZ

Dla nowych manuskryptów LaTeX rysunki TikZ umieszczaj w `manuscripts/P01/figures/` (jeden rysunek w jednym pliku `.tex`). `main.tex` zawiera jedynie `\input{figures/study-workflow.tex}`. Nie przenoś środowiska `tikzpicture` do dokumentu głównego. Zachowuj podpisy i identyfikatory `\label`, uwzględnij pliki `figures/*.tex` w archiwum źródłowym i przygotuj dodatkowy format grafiki zgodnie z wymaganiami konkretnego czasopisma. Szablon zawiera wyłącznie schemat demonstracyjny, który należy zastąpić przed zgłoszeniem.

## Zotero / Better BibTeX

Dla każdego manuskryptu utwórz lokalnie kolekcję Zotero i ustaw automatyczny eksport translatora Better BibTeX z opcją **Keep updated** do odpowiedniego `references.bib`. Nie eksportuj notatek, adnotacji ani załączników. Po prawdziwej konfiguracji zmień status w `zotero.json` na `configured`. Do pierwszego zgłoszenia użyj `python scripts/check_zotero.py --root . --require-setup`; CI korzysta z odczytowego trybu offline. Instrukcje: [docs/zotero.md](docs/zotero.md).

## Publiczna witryna i wydania naukowe MSC

Stosuj [standard GitHub Pages](docs/pages.md) dla treści w osobnym `pages/` oraz [procedurę wydań](docs/releases.md) dla wersji manuskryptów, pakietów źródeł, reprodukowalności i GitHub Releases. Odróżniaj wersję szablonu od wersji konkretnego artykułu. Każdy `P01…` może mieć własny numer wersji, datę kompilacji i dokładny SHA. PDF umieszczaj na stronie **dopiero po zgodzie na upublicznienie tej wersji** i kontroli praw wydawcy.

Przed zatwierdzeniem sprawdź listę źródeł publicznych, pełny wynik `_site/`, metadane obrazów/PDF, bibliografię, statusy naukowe, licencje, udokumentowane dowody testów i niezależną recenzję. `--phase publish` nie publikuje ani nie podpisuje manuskryptu. GitHub Release, prerejestracja, preprint, zgłoszenie do czasopisma, udostępnienie danych i wdrożenie Pages są **odrębnymi decyzjami**. Szablon nie powinien wykonywać automatycznego wydawania ani deployu.
