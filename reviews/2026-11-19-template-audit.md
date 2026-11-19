# Audyt szablonu `repo-template-msc` — 2026-11-19

**Zakres:** stan gałęzi `main` na commit `807a00b87d2ddc1bcb135c33238376ca32deb616`.  
**Status:** niezależny przegląd statyczny, bez uruchamiania testów ani zmiany polityki GitHub.  
**Przeznaczenie:** szablon samodzielnego repozytorium naukowo-manuskryptowego `msc-*`, nie gotowy wzór składu pracy dyplomowej.

## Werdykt

**Ocena orientacyjna: 6,5/10 (ekspercka, nie wynik automatycznego testu).** Architektura i metodologia są mocne, ale reguły nie są jeszcze automatycznie egzekwowane. Repozytorium nadaje się jako punkt wyjścia, lecz nie należy deklarować pełnej gotowości operacyjnej.

| Obszar | Ocena orientacyjna |
| --- | ---: |
| Architektura | 8/10 |
| Metodologia | 8/10 |
| Reprodukowalność | 7/10 |
| Etyka i ochrona danych | 7/10 |
| Walidacja automatyczna | 4/10 |
| CI i bramki jakości | 2/10 |
| Onboarding | 7/10 |
| Integracja z programami ARC | 7/10 |

### Potwierdzone mocne strony

1. Poprawny podział odpowiedzialności: repo `msc-*` posiada protokół, analizy i publikacje; narzędzia `app-*`/`lib-*` pozostają osobnymi zależnościami.
2. Rozdzielenie prerejestracji, oceny etycznej i publikacji; zakaz fikcyjnych wyników i identyfikatorów DOI.
3. Wymóg identyfikowalności kodu, danych, aparatury i środowiska (`REPRODUCIBILITY.md`, `research/evidence-register.csv`).
4. Odrębny katalog `docs/` dla treści kwalifikujących się do publicznego udostępniania.
5. Poprawnie skonfigurowany status źródłowego repozytorium jako GitHub Template (`is_template=true`).

## Ustalenia i ryzyka

| ID | Priorytet | Ustalenie i dowód | Zalecenie |
| --- | --- | --- | --- |
| F01 | P0 | Brak `.github/workflows/`; zero zarejestrowanych uruchomień Actions przy przeglądzie. | Dodać minimalny CI dla walidatora i testów; wymagać sukcesu jako status check po zweryfikowaniu stabilności. |
| F02 | P0 | `scripts/validate_repository.py` sprawdza w większości obecność plików i dopasowuje klucze `PROJECT_STATE.yaml` wyrażeniami regularnymi. | Parsować YAML, walidować schemat, typy i dozwolone stany; sprawdzać powiązania publikacji, dowodów i manifestów. |
| F03 | P0 | Kontrola ścieżek wyłapuje tylko segmenty `raw`, `private` i `processed-private`; `.gitignore` nie zastępuje skanowania treści, a pliki można dodać z `git add -f`. | Włączyć kontrolę sekretów, zakazanych danych i formatów oraz review danych przed publikacją. Żadna kontrola automatyczna nie gwarantuje anonimizacji. |
| F04 | P1 | `main.qmd` miał placeholder `[Autorzy]`, a instrukcja setupu nie precyzowała niezmiennego autora podstawowego. | Wzorzec zawiera Mateusza Pomianka jako autora; można dodać rzeczywistych współautorów. Nie zastępować autora podstawowego. |
| F05 | P1 | Brak inicjalizatora repo z parametrów projektu i spójnej obsługi placeholderów. | Dodać idempotentny skrypt `init` oraz test tworzenia nowego repozytorium. |
| F06 | P1 | `PROJECT_STATE.yaml` może odbiegać od dokumentów, danych i manuskryptów; walidator nie weryfikuje tego kompleksowo. | Dodać kontrole spójności statusów, identyfikatorów, referencji, dat i dowodów; brak danych nie może być `PASS`. |
| F07 | P1 | `results/` i `software/dependencies.yaml` są deklaratywne; brak małego, weryfikowalnego przykładu od danych syntetycznych do wyniku. | Dodać testowy pipeline bez prawdziwych danych uczestników, z manifestem, sumami SHA i instrukcją odtworzenia. |
| F08 | P2 | Brak formalnego procesu wersjonowania wzorca i testów zgodności z już wygenerowanymi repozytoriami. | Wprowadzić SemVer szablonu, changelog i test migracji. |
| F09 | P1 | Ruleset `main` blokuje usuwanie i non-fast-forward, ale nie wymaga review ani przejścia CI; uprawniona rola może go obejść. | Po wdrożeniu CI ustawić wymagane statusy i przegląd PR, o ile pozwalają na to możliwości konta i polityka repo. |
| F10 | P1 | `CITATION.cff` zawiera ogólnikowy komunikat cytowania, a prawidłowe wprowadzanie współautorów nie było opisane. | Uporządkować komunikat oraz kontrakt autorstwa i metadanych artykułów. |

W szczególności `data/participants.csv` nie jest zakazaną ścieżką przez obecną listę segmentów walidatora. Jest to przykład luki w pokryciu, **nie dowód wystąpienia wycieku**.

## Zasady przyjęte dla szablonu

**Autorstwo.** Mateusz Pomianek pozostaje co najmniej jednym z autorów we wszystkich repozytoriach wygenerowanych z tego wzorca, w `CITATION.cff` i metadanych manuskryptów. Pozostali współautorzy są opcjonalni; dodaje się wyłącznie rzeczywiste osoby po ustaleniu ich wkładu, zgody na przypisanie autorstwa, kolejności i wymagań docelowego czasopisma. Nie należy tworzyć fikcyjnych autorów ani identyfikatorów.

**Runnery.** Dla **publicznych** repozytoriów dopuszczalne są **GitHub-hosted runners** (np. `ubuntu-latest`) do testów strukturalnych, lintingu i innych bezpiecznych zadań. Nie wymaga się lokalnego runnera. Dla repozytoriów prywatnych decyzja zależy od uprawnień, kosztów, wrażliwości danych i zatwierdzonej infrastruktury. W PR z niezaufanych forków nie uruchamiać uprzywilejowanego kodu, nie przekazywać sekretów i nie udostępniać zasobów prywatnych; stosować zasadę najmniejszych uprawnień (`permissions: contents: read`). Uwzględnić limity usług i nie generować dodatkowych wydatków bez zgody.

**Granice szablonu.** Nie duplikować globalnego harmonogramowania, katalogów aparatury ani kodu bibliotek; dokumentować kontrakty i przypięte SHA. Dane osobowe nie są materiałem do testów repozytorium.

## Plan napraw i definicja ukończenia

### P0 — wymogi blokujące przyjęcie jako obowiązującego standardu
- [ ] CI na `pull_request` i `push`, uruchamiające walidator oraz testy; polityka runnerów oparta na publiczności repo i bezpieczeństwie.
- [ ] Walidacja poprawności YAML, schematów i referencji; testy negatywne wykrywające nieprawidłowe stany.
- [ ] Kontrola prywatności/sekretów w CI oraz zasady przeglądu ryzyka; brak danych uczestników w artefaktach.

### P1 — wymogi stabilnego użycia
- [ ] Inicjalizator zachowujący Mateusza Pomianka i pozwalający dopisać współautorów.
- [ ] Kontrola spójności `PROJECT_STATE.yaml`, manuskryptów i rejestru dowodów.
- [ ] Test reprodukcji minimalnego przykładu z danymi syntetycznymi i udokumentowanym SHA.
- [ ] Wymagany status CI i review dla `main` po wykazaniu poprawności workflow.

### P2 — rozszerzenia opcjonalne
- [ ] SemVer, changelog i migracje.
- [ ] Opcjonalne integracje bibliograficzne, publikacyjne i analityczne, niewymagane dla pustego repozytorium.

## Scenariusz akceptacyjny

Utworzyć repo `msc-example` przez `Use this template`, wprowadzić wymagane metadane przy zachowaniu autora podstawowego, dopisać testowego współautora, wykonać walidację i syntetyczny pipeline, otworzyć PR z celowo błędnym statusem i potwierdzić jego zablokowanie. Następnie poprawić błąd i potwierdzić poprawny status CI. Dla repo publicznego można wykonać tę próbę na GitHub-hosted runner; test nie wymaga danych rzeczywistych.

**Zakres niniejszego PR:** zapis audytu, autorstwa i polityki runnerów oraz korekta wzorcowych metadanych. **Nie obejmuje:** wdrożenia CI, skanowania danych, inicjalizatora, nowych rulesetów ani wykonania scenariusza akceptacyjnego. Wymienione wyżej zadania pozostają otwarte.
