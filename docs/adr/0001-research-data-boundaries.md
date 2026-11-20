# ADR-0001: granice danych badawczych i publikacji

**Status:** proposed  
**Data:** 2026-11-20  
**Zakres:** bezpieczeństwo, prywatność, publikacja

## Kontekst

Projekt manuskryptowy może zawierać dane pomiarowe i informacje zastrzeżone oraz prowadzić publiczną stronę. Sam fakt prywatności repozytorium nie oznacza, że źródła Pages nie zostaną upublicznione.

## Propozycja

Wewnątrz projektu rozdzielamy kod, konfigurację, dane pomiarowe, dokumentację `docs/` i materiały publiczne w `pages/`. Wszystkie zasoby witryny mają być dopuszczane pojedynczo, bez automatycznego kopiowania plików repozytorium. Publikacja wymaga zweryfikowania zgód, etyki, praw licencyjnych, statusów naukowych i widoczności strony.

## Alternatywy

Publikacja całego `docs/` upraszcza budowę, ale ujawnia dokumentację wewnętrzną i nie pozwala kontrolować pojedynczych zasobów. Automatyczny eksport manuskryptów może ujawnić niezaakceptowane hipotezy, dane i informacje wydawnicze.

## Konsekwencje

Potrzebna jest jawna lista dopuszczonych plików, kontrola przed publikacją, ścieżka zatwierdzenia i rozdział odpowiedzialności. Projekt potomny musi ocenić rzeczywisty przepływ danych oraz zatwierdzić lub odrzucić ten ADR. Propozycja nie stanowi pozytywnej oceny etycznej ani gotowości witryny.
