# Architektura repozytorium

Projekt `msc-*` jest właścicielem pytań naukowych, manuskryptów, analiz, protokołów i manifestów wyników. Samodzielne aplikacje i biblioteki są źródłami zewnętrznymi, nie kopiami wewnątrz tego repozytorium.

- `manuscripts/P01/`: kanoniczne źródło pojedynczego artykułu; kolejne `P02`, `P03` tylko dla niezależnych wkładów.
- `research/`: protokół, analiza, etyka, dane, decyzje i rejestr dowodów.
- `data/`: tylko bezpieczne opisy i manifesty; surowe pomiary poza Git.
- `results/`: odtwarzalne, zatwierdzone rezultaty lub manifesty; brak ręcznie wpisanych tabel jako pomiarów.
- `software/`: odwołania do repozytoriów `app-*`/`lib-*`, wersje, SHA i kontrakty.
- `equipment/`: odwołania po `equipment_id` do katalogu aparatury Research Autopilot.
- `docs/`: wewnętrzna dokumentacja naukowo-inżynierska; nie jest źródłem GitHub Pages.
- `pages/`: wyłącznie zatwierdzone materiały publiczne, z listą dopuszczonych zasobów i niezależną decyzją o publikacji.
- `docs/architecture/`: opis przepływów, granic kodu badawczego, pochodzenia danych i odtwarzalności.
- `docs/adr/`: decyzje architektoniczne (odrębne od decyzji naukowych w `research/decisions.md`).
- `docs/security/`, `docs/operations/`: model zagrożeń, incydenty i procedury odtwarzania, bez tajnych danych.
- `scripts/`, `tests/`: walidacja zgodności z szablonem.

Program nadrzędny `arc-*` linkuje tutaj i opcjonalnie dodaje submoduł wskazujący ustalony commit. Aktualna analiza musi niezależnie odczytać zdalny HEAD projektu i porównać go z `gitlink`. Publikacja strony oraz repozytorium źródłowe mają odrębne polityki dostępu.
