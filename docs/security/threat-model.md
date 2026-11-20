# Model zagrożeń projektu MSC

**Status: NOT_ASSESSED.** Dokument opisuje pytania do weryfikacji, a nie przeprowadzone badanie bezpieczeństwa.

| Obszar | Ryzyko | Wymagana weryfikacja |
| --- | --- | --- |
| Uczestnicy | Reidentyfikacja, naruszenie zgód, utrata poufności | Protokół, podstawa RODO, uprawnienia i retencja |
| Aparatura | Niezwalidowane parametry lub błędna kalibracja | Model urządzenia, SDK, test fizyczny, log bez danych osobowych |
| Analiza | Zanieczyszczenie danych, niewłaściwe wyłączenia, brak reprodukowalności | SAP, źródło, SHA, raport, wersje |
| Bibliografia | Ujawnione załączniki lub nieprawdziwe cytowania | Test Zotero i źródła referencji |
| CI | Niezaufany kod, sekrety, runner produkcyjny | Izolacja, minimalne uprawnienia, polityka kosztów |
| Pages | Upowszechnienie wewnętrznych instrukcji i danych z prywatnego repo | Jawna allowlista, recenzja HTML i widoczności |

Przed pierwszym pomiarem, analizą na rzeczywistych danych oraz publicznym wydaniem uzupełnij zasoby, granice zaufania, scenariusze, prawdopodobieństwo i skutek, właściciela ryzyka, środki zaradcze oraz rzeczywisty dowód. `NOT_ASSESSED` nie oznacza niskiego ryzyka.

Powiązane źródła: [architektura](../architecture/data-flow.md), [etyka](../../research/ethics.md), [SECURITY](../../SECURITY.md) i [ADR](../adr/0001-research-data-boundaries.md).
