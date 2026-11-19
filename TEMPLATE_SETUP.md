# Instrukcja zastosowania szablonu

Ten katalog stanowi kompletny, przenośny **szkielet repozytorium `msc-*`**. Przy tworzeniu nowego badania kopiuj całą jego zawartość jako korzeń repozytorium. Następnie uzupełnij pola `REPLACE`, protokół i statusy, uruchom walidator i ustal uprawnienia repozytorium.

1. Utwórz prywatne lub publiczne repo `msc-<krótki-temat>`; przed publikacją wybierz politykę danych i praw.
2. Skopiuj zawartość katalogu szablonu do nowego repo (łącznie z `.github`, `.gitignore`, `.gitattributes`). Nie kopiuj otaczającego repozytorium Research Autopilot, historii jego commitów ani jego sekretów.
3. Zastąp `REPLACE_PROJECT_ID`, `REPLACE_OWNER`, autorów, tytuły, program ARC i licencję. Wypełnij `research/protocol.md`, `research/analysis-plan.md`, `research/ethics.md` i `software/dependencies.yaml`.
4. Uruchom `python scripts/validate_repository.py --root . --phase scaffold` oraz `python -m unittest discover -s tests -v`. Wynik PASS oznacza **strukturę**, nie gotowość badania.
5. Jeśli GitHub otrzyma osobne repo oznaczone jako **Template repository**, można tworzyć nowe repozytoria przyciskiem `Use this template` lub GitHub CLI. Kopiowana jest zawartość plików, **nie** historia źródłowego projektu. Włączanie `is_template` wymaga odpowiednich uprawnień administracyjnych; sama struktura folderu nie ustawia flagi GitHub.
6. Uzupełnij i zatwierdź źródła, prawa oraz witrynę. Uruchom `--phase publish` przed publikacją publicznej części. Walidator nie ocenia etyki, cytowań ani wartości naukowej; wymaga oddzielnego audytu.
7. Program `arc-*` może odwoływać się do projektu linkiem lub submodułem przypiętym SHA. Nowe repo **nie jest** submodułem automatycznie. Wybór repo nadrzędnego wymaga zgodności z jego polityką WIP oraz prywatnością.

**Uwaga:** w trybie scaffold README dopuszcza `NOT_COLLECTED`, `NOT_REGISTERED` i inne uczciwe stany. Nie należy wpisywać fikcyjnego DOI ani wyniku tylko po to, aby spełnić schemat. `publish` sprawdza konfigurację szablonu, nie akceptację naukową.
