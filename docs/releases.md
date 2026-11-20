# Wydania i artefakty naukowe MSC

**Stan wzorca:** `SCAFFOLD / NOT_RELEASED`. Zielony CI oznacza pozytywną walidację struktury, nie powstanie wyników, udaną kompilację manuskryptu ani autoryzację publikacji. W MSC należy rozróżnić **wersję projektu**, **wersję każdego manuskryptu**, **wydanie artefaktu odtwarzalności**, **prerejestrację**, **preprint**, **zgłoszenie do czasopisma** i **publikację danych**.

## 1. Tożsamość i wersjonowanie

- Repozytorium `msc-*` jest kanonicznym właścicielem protokołu, planu analizy, manuskryptów `P01…` i odnośników do wyników. ARC prowadzi jedynie rejestr relacji; APP i LIB wersjonują własny kod. Sprzęt i szczegóły połączenia należą do odrębnego repozytorium `devices`.
- `PROJECT_STATE.yaml:template_version` oznacza wersję **szablonu**, a nie aktualność tekstu naukowego. Dla faktycznych wydań projektu stosuj SemVer 2.0.0: `MAJOR` przy niezgodnej zmianie kontraktu/danych, `MINOR` przy zgodnym rozszerzeniu pakietu, `PATCH` przy korekcie niewpływającej na znaczenie wyników. Numer wydania projektu nie jest numerem zgłoszenia redakcyjnego.
- Każdy manuskrypt `P01`, `P02` itd. prowadzi **odrębne wersje** `vX.Y.Z` lub udokumentowane rewizje. W opisie wersji podaj tytuł, datę kompilacji, exact Git SHA źródeł, hash PDF oraz status naukowy i redakcyjny. Zamrożona wersja złożona do czasopisma musi pozostać odtwarzalna mimo dalszych zmian w `main`.
- Nigdy nie przenoś opublikowanego tagu na nowy commit ani nie nadpisuj potajemnie artefaktów. Po korekcie udostępnij nową wersję i powiąż ją z poprzednią.

## 2. Macierz kanałów wydawniczych

| Kanał | Artefakt i odbiorca | Dodatkowa bramka |
| --- | --- | --- |
| **Wewnętrzna migawka badania** | Protokół, SAP, manifest danych, SHA kodu i zależności, kontrolowany raport metod | Autoryzowany dostęp; ochrona danych i identyfikatorów; statusy nieprzeprowadzonych kontroli |
| **GitHub Release MSC** | Dozwolony ZIP ze źródłami/wykresami oraz wersjonowane publiczne lub ograniczone artefakty | Licencje, jawny zakres dystrybucji, kompletność i test odtwarzania na exact SHA |
| **Pakiet zgłoszenia do czasopisma** | PDF + kompletne TeX/BibTeX/rysunki lub alternatywny format redakcyjny | Autorzy, cel czasopisma, aktualny Guide for Authors, embargo, etyka, oświadczenia |
| **Preprint / accepted manuscript** | Wersja tekstu dopuszczona przez współautorów i wydawcę | Prawa do upublicznienia danej wersji, ewentualna polityka embargo i repozytorium preprintowe |
| **Publiczny PDF na GitHub Pages** | Podgląd **zatwierdzonej** wersji z datą, numerem, SHA i statusem | Osobna zgoda na witrynę i licencję PDF; kontrola metadanych i widoczności |
| **Zbiory danych i kod analiz** | Zanonimizowane albo kontrolowane zasoby w właściwym repozytorium | Zgody, etyka, prawa, ryzyko reidentyfikacji, licencja, polityka retencji i dostępu |

`--phase publish` w `scripts/validate_repository.py` dotyczy gotowości wybranych metadanych publicznych, a **nie** automatycznej kwalifikacji do GitHub Release, prerejestracji, preprintu ani zgłoszenia redakcyjnego. Nie publikuj jednego „wszystkiego ZIP” obejmującego `research/`, dane uczestników, dokumenty etyczne i korespondencję redakcyjną.

## 3. Kompletny pakiet źródłowy manuskryptu

Kanoniczna lokalizacja wynika z `PROJECT_STATE.yaml:manuscript_source` (dla nowego wzorca `manuscripts/P01/main.tex`); `bibliography_path` wskazuje bibliografię. Dla LaTeX uwzględnij wszystkie referencje `\input` i `figures/*.tex`, źródła rysunków, legalnie dystrybuowane `.cls/.sty`, bibliografię `references.bib` i metadane Zotero/Better BibTeX bez notatek, prywatnych załączników i tokenów. QMD jest dopuszczalne wyłącznie po jawnym wyborze; nie twórz dwóch niezależnych kanonicznych tekstów.

Przed zatwierdzeniem wykonaj `python scripts/check_zotero.py --root . --require-setup` (gdy bibliografia rzeczywiście skonfigurowana) oraz kompilację odpowiedniego dokumentu w izolowanym środowisku, np. `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` w katalogu manuskryptu. Zapisz wersję TeX Live, profil czasopisma, log, wynik kompilacji, SHA PDF i test otwarcia pełnego dokumentu. Domyślne CI szablonu **nie wykonuje** kompilacji LaTeX i nie może jej poświadczyć.

Oficjalny profil czasopisma, dokumenty etyczne, sekcje o danych, autorstwie i finansowaniu należy zweryfikować indywidualnie. Szablony wydawców mogą ograniczać prawo do publicznej dystrybucji skompilowanego PDF. Wytyczne: [profile czasopism](journal-formats.md).

## 4. Wymagane dowody i manifest

Przed wydaniem przygotuj **nieśledzony** manifest `outputs/msc-release-evidence.json` z `schema_version`, `project_id`, `track_id`, `version`, `channel`, `commit_sha`, `manuscript_source`, `output_path`, `output_sha256` i odnośnikami do faktycznych testów. Dla wszystkich wyników mapuj pochodzenie:

`MSC commit SHA -> protokół/SAP i zatwierdzenie etyki -> wersja danych i SHA256 -> kod APP/LIB wraz z digestem -> aparatura i kalibracja -> parametry analizy/RNG -> raport/statystyka -> źródła TeX/BibTeX -> PDF -> wersja wydania/DOI`.

Nie wstawiaj rzeczywistych danych osobowych ani prywatnych URI do publicznego manifestu. Osobno odnotuj `PASS`, `FAIL`, `NOT_RUN`, `UNAVAILABLE` i `NOT_APPLICABLE`, wraz z dowodem każdego wyniku. Samo pole `tests_passed: true` albo lokalna suma SHA-256 **nie weryfikuje pochodzenia** artefaktu. Dla zewnętrznej dystrybucji wymagaj kontroli tożsamości repozytorium, workflow i exact SHA, niezależnej atestacji lub równoważnego zaufanego mechanizmu oraz udokumentowanej autoryzacji.

## 5. Bramki przed wydaniem

1. **Naukowa:** zamrożony protokół i SAP, zgody i rzeczywisty stan etyki, kompletność dowodów, kontrola jakości, ograniczenia badania, zgodność liczebności i statystyki z wynikami; żadnego wymyślonego wyniku.
2. **Techniczna:** struktura `scaffold`, statyczne testy, bibliografia, kompilacja manuskryptu i test otwarcia PDF, kompletność rysunków, zgodność SHA wszystkich zależności oraz audyt prywatności artefaktu.
3. **Redakcyjna i prawna:** potwierdzeni współautorzy, kolejność i afiliacje, zgodność z instrukcjami czasopisma, prawa do rysunków/kwestionariuszy, embargo, licencja i dozwolony kanał dystrybucji.
4. **Integracyjna:** aktualny CI na exact SHA oraz niezależna recenzja wymuszana przez ruleset `main`. Jeśli GitHub nie egzekwuje CI/PR review, zastosuj `GATE_UNENFORCED / HOLD`; recenzja własnej pracy nie jest niezależnym zatwierdzeniem.
5. **Autoryzacja:** właściciel jawnie zatwierdza konkretną wersję i odbiorcę (`internal`, `release`, `journal-submission`, `preprint`, `pages`, `dataset`). Zgoda na jedno zdarzenie nie oznacza zgody na inne.

## 6. Wydanie, korekty i wycofanie

Wydanie techniczne powinno mieć tag wskazujący exact SHA, datę, changelog, sumy SHA-256, kompatybilność i instrukcję odtworzenia. Nie buduj pakietu z ruchomego HEAD po walidacji starszego commita. Sprawdź podpis/atestację tam, gdzie dostępna, a po publikacji odrębnie zweryfikuj pobrany artefakt. Dla publikacji czasopisma zapisuj rzeczywisty `submission receipt`, numer i datę rewizji, decyzję redakcji oraz DOI tylko po otrzymaniu dowodów. Nie umieszczaj poufnych dokumentów redakcyjnych w publicznym release.

Korekta statystyczna lub zmiana danych po wydaniu wymaga nowej wersji oraz oceny wpływu na manuskrypt, suplement i publiczne opisy. W razie naruszenia prywatności zatrzymaj dystrybucję, zachowaj ślad błędu, postępuj zgodnie z [procedurą incydentową](security/incident-response.md) i powiadom uprawnionych odbiorców. Usunięcie pliku nie gwarantuje usunięcia pobranych kopii.

**Brak realnej kompilacji, danych, zatwierdzeń i atestacji w szablonie oznacza `NOT_RUN`**, a nie pozytywny wynik procesu wydawniczego. Osobne zasady publicznej witryny: [GitHub Pages](pages.md).

