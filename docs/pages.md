# Oddzielna, kontrolowana publikacja GitHub Pages

**Zasada:** `pages/` zawiera tylko zatwierdzone materiały dla czytelników, natomiast `docs/` jest prywatną dokumentacją roboczą w sensie przeznaczenia, nawet jeśli repozytorium jest publiczne. Nie publikuj plików `.github/`, `AGENTS.md`, `research/`, wewnętrznych dokumentów etycznych, roboczych analiz ani całego repozytorium.

`mkdocs.yml` ma zawsze `docs_dir: pages` i `site_dir: _site`. Każdy publiczny plik musi być na jawnej liście `config/pages-policy.json` i przejść `scripts/validate_pages.py`. Nie dopuszczaj symlinków, nieznanych zasobów, zewnętrznych pluginów kopiujących pliki ani linków do dokumentów wewnętrznych.

**Zakaz:** na witrynie nie wolno umieszczać poleceń do agenta AI, promptów, tekstów redakcyjnych, wskazówek dla autora, placeholderów, komentarzy o prowadzeniu repozytorium ani zachęt do `CONTRIBUTING`. Opis badania powinien być neutralny naukowo, zrozumiały dla niezaangażowanego czytelnika, bez niezatwierdzonych wyników i dat, których nie potwierdzono.

**Szczególna ostrożność w prywatnym repo:** GitHub Pages może być publiczne mimo prywatnego kodu. Zweryfikuj rzeczywistą konfigurację widoczności, domenę, uprawnienia, warunki kosztów i wygenerowane strony. Jeśli wymagana poufność nie jest zapewniona, **nie publikuj**. Zabroniony jest tryb `Deploy from a branch` wskazujący `main:/docs` lub root repo. Dopuszczony do rozważenia jest tylko osobno autoryzowany artefakt z wyjściowego `_site/` lub dedykowany branch z samymi zasobami publicznymi.

Przed publikacją wykonaj kontrolę tekstu i **wszystkich zasobów**, np. metadanych zdjęć, SVG i archiwów, oraz sprawdź wygenerowany HTML. Skan automatyczny wykrywa jedynie wybrane zagrożenia i nie jest zgodą właściciela ani audytem etycznym. Nie dodawaj automatycznego workflow publikującego na każdy merge.
