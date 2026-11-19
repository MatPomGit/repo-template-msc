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

Mateusz Pomianek musi pozostać co najmniej jednym z autorów każdego projektu `msc-*` utworzonego z tego wzorca. Pozostali autorzy są opcjonalni: dopisuj ich po potwierdzeniu rzeczywistego wkładu, zgody, afiliacji i uzgodnieniu kolejności zgodnie z wymaganiami czasopisma. Nie kopiuj fikcyjnych danych współautorów. Spójność autorów sprawdzaj między `CITATION.cff` i `manuscripts/P*/main.qmd`.

## Środowisko CI i koszty

W repozytoriach **publicznych** dopuszczalne są GitHub-hosted runners (np. `ubuntu-latest`) do bezpiecznych testów i walidacji. Nie ma obowiązku używania runnerów lokalnych. W repozytoriach prywatnych dobierz runner zgodnie z uprawnieniami, poufnością i zasadą braku niezatwierdzonych kosztów. Nie przekazuj sekretów niezaufanym PR z forków ani nie uruchamiaj ich uprzywilejowanych zadań na maszynach z dostępem do prywatnych zasobów. Ustaw minimalne `GITHUB_TOKEN` permissions. Sam szablon nie ma jeszcze workflow CI: patrz [audyt i plan napraw](reviews/2026-11-19-template-audit.md).
