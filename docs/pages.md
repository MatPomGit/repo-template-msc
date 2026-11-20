# GitHub Pages projektu badawczego MSC

**Cel:** publiczna, przystępna naukowo prezentacja jednego projektu `msc-*` i jego potwierdzonych rezultatów. Nie jest to repozytorium roboczej dokumentacji, prerejestracji, danych uczestników ani niejawna kopia manuskryptu. Sam katalog `pages/` nie publikuje strony. Wzorzec nie posiada autoryzacji do deploymentu.

## 1. Architektura publikacji

Treści publiczne umieszczaj **wyłącznie w `pages/`** i jawnie zatwierdzaj w `config/pages-policy.json`. `mkdocs.yml` określa `docs_dir: pages` oraz `site_dir: _site`. Katalog `docs/` służy wewnętrznym dokumentom technicznym i redakcyjnym, `research/` zawiera protokół, etykę i plan analiz, a `manuscripts/` kanoniczne źródła tekstów. Nie kopiuj tych katalogów ani `.github/`, `AGENTS.md`, `data/`, `results/`, prywatnych logów, plików Zotero i dowodów redakcyjnych do witryny.

**Nie wolno włączać GitHub Pages z `Deploy from a branch` wskazującego `main`, `/docs` ani root.** Dopuszczalny jest jedynie osobno zatwierdzony deployment gotowego katalogu `_site/` (przez kontrolowany artefakt GitHub Actions lub dedykowaną gałąź zawierającą wyłącznie sprawdzone zasoby). W repozytorium prywatnym sprawdź rzeczywistą widoczność witryny: prywatność kodu **nie gwarantuje** prywatności Pages. W razie wątpliwości nie publikuj.

## 2. Informacja o badaniu

Strona jest skierowana do osób spoza zespołu. Wyjaśnia pytanie naukowe, uzasadnienie, metody, ograniczenia, etap badania i dostępne materiały bez fikcyjnych rezultatów i nadinterpretacji. Zalecana struktura, tworzona **tylko gdy istnieje zweryfikowana treść**:

| Podstrona | Zawartość |
| --- | --- |
| O projekcie | Tytuł, cel, pytania badawcze, znaczenie i zakres zastosowań |
| Założenia i metodologia | Projekt badawczy, populacja/próba, typ pomiaru, ogólna procedura i plan analizy w zakresie zatwierdzonym do ujawnienia |
| Wyniki | Tylko rzeczywiste wyniki z zatwierdzonymi tabelami, wykresami i ograniczeniami; wyraźnie odróżnij pilotaż od badania głównego |
| Publikacje | Manuskrypty `P01…` z potwierdzonym etapem, autorami, DOI, preprintem lub odnośnikiem do legalnej wersji |
| Bibliografia | Rzeczywiście cytowane, zweryfikowane publikacje; bez prywatnych notatek z Zotero |
| Otwarta nauka | Dostępne prerejestracje, zatwierdzone materiały i dane, repozytorium, licencja oraz ograniczenia dostępu |

Nie twórz pustych zakładek, instrukcji dla agentów AI, promptów, uwag redakcyjnych i komentarzy dla właściciela. Zakaz `CONTRIBUTING` oraz niepotwierdzonych deklaracji etycznych, rekrutacyjnych, klinicznych i wydawniczych. Wyjaśnienia mają być neutralne, spójne i zrozumiałe, bez paternalistycznych zastrzeżeń nieadekwatnych do odbiorcy.

## 3. Manuskrypt na stronie: oddzielna zgoda

Kanonicznym źródłem każdego tekstu pozostaje `PROJECT_STATE.yaml:manuscript_source`, domyślnie `manuscripts/P01/main.tex` wraz z `references.bib` i plikami rysunków. Publiczna strona może zawierać **podgląd rzeczywistego PDF** wyłącznie po sprawdzeniu praw autorów, wydawcy, współautorów i decyzji o upublicznieniu właściwej wersji (draft/preprint/accepted/published). Nie utożsamiaj roboczego PDF z preprintem ani z tekstem opublikowanym przez czasopismo.

Gdy właściciel dopuści publiczny PDF, prezentuj **wersję, datę kompilacji, commit SHA źródeł i status tekstu** oraz link alternatywny do pobrania. PDF może być udostępniony jako osobny, zatwierdzony artefakt, ale nie należy kopiować automatycznie całego katalogu `manuscripts/` ani publikować wprost dokumentów redakcyjnych. Weryfikuj powiązanie pliku z exact SHA, bezpieczeństwo metadanych PDF, prawa do grafik i wymagania licencyjne szablonu czasopisma. Nie publikuj nowszego draftu nad niezmiennym oznaczeniem starej wersji.

Publikacje identyfikuj faktycznym `MSC-*` oraz lokalnym `P01…`. Dołącz DOI/URL dopiero po potwierdzeniu; statusy `submitted`, `accepted` i `published` wymagają źródłowego dowodu. Dla wersji podlegającej embargo publikuj tylko zatwierdzone informacje i dozwolony link, bez pełnego tekstu.

## 4. Prywatność danych i dostępność

Nie umieszczaj na Pages surowych EEG, okulometrii, wideo, danych psychometrycznych, informacji o zdrowiu, kluczy reidentyfikacji, identyfikatorów uczestników ani metadanych urządzeń z prywatnego repozytorium `devices`. Obrazy, wykresy i zrzuty przygotuj z zatwierdzonych wyników lub wyraźnie oznaczonych danych syntetycznych. Przed publikacją sprawdź EXIF/XMP/IPTC, GPS, osadzone miniatury, podpisy, komentarze i nazwy plików. Przegląd graficzny musi potwierdzać skale osi, jednostki, liczebności, niepewność i kontekst statystyczny.

Stosuj responsywny układ, prawidłową hierarchię nagłówków, kontrast, klawiaturę, tekst alternatywny i WCAG 2.2 AA jako cel jakościowy. Zadbaj o polską i ewentualną angielską wersję z identycznie sprawdzonymi faktami. Nie dodawaj trackerów, zewnętrznego JavaScriptu, formularzy zbierających dane lub zewnętrznych fontów bez osobnej kontroli prywatności i zgody.

## 5. Walidacja i publikacja

1. Sprawdź exact SHA, status badania, prawa do tekstów i ilustracji, etykę oraz zakres zgody na ujawnienie wyników. Ustal docelową domenę i widoczność witryny, również dla repo prywatnego.
2. Wykonaj `python scripts/validate_pages.py`, `python scripts/validate_documentation.py`, `python -m mkdocs build --strict` oraz `python scripts/validate_site.py --strict`. Pierwszy walidator kontroluje źródła; drugi weryfikuje cały wygenerowany katalog `_site/`, w tym skrypty i przypięte zasoby motywu. Sprawdzane są również 24 zatwierdzone sumy SHA-256 plików motywu, aktywny HTML i zasoby zewnętrzne; domyślny `highlight.js` z CDN jest wyłączony. Nie jest to publikacja.
3. Przejrzyj faktyczny render i wszystkie pliki wynikowe, PDF, obrazy, metadane, linki, indeks wyszukiwania, dostępność i brak treści instruktażowych dla agentów. Kontrola statyczna nie gwarantuje ochrony przed każdym wyciekiem.
4. Uzyskaj niezależną recenzję na finalnym SHA i **osobną decyzję właściciela** dla zawartości, domeny i widoczności. Brak obowiązkowego CI/review w rulesecie gałęzi oznacza `GATE_UNENFORCED`, nie zatwierdzenie.
5. Po świadomym wdrożeniu zweryfikuj rzeczywistą witrynę oraz możliwość wycofania. W razie ujawnienia danych zatrzymaj publikację i zastosuj [procedurę incydentową](security/incident-response.md). Kopie cache mogą pozostać dostępne.

**Oddzielaj cztery działania:** publikację Pages, wersjonowane wydanie artefaktu badawczego, preprint/zgłoszenie manuskryptu i upublicznienie danych. Szczegóły: [wytyczne wydań](releases.md).

