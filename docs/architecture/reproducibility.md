# Architektura reprodukowalności

**Stan:** opis wymaganych dowodów, nie wykonanej walidacji. Kontrakt nadrzędny: [REPRODUCIBILITY.md](../../REPRODUCIBILITY.md).

Dla konkretnego manuskryptu utrwal źródło LaTeX/QMD, dokładny commit SHA, wersję TeX Live lub Quarto, profil wydawniczy, BibTeX wyeksportowany z Zotero, wszystkie źródła `figures/*.tex`, wersje SDK i aparatów, identyfikator danych oraz wynik kompilacji. Nie zastępuj zamrożonej wersji testowanej aktualnym HEAD biblioteki.

Zadbaj o rozdzielenie: walidacja statyczna repo, test kodu, kontrola cytowań, kompilacja PDF, replikacja wyniku numerycznego i pomiar fizyczny. Każdy stan raportuj niezależnie, z `PASS`, `FAIL`, `NOT_RUN`, `UNAVAILABLE` lub `NOT_APPLICABLE`.

Pakiet redakcyjny może wymagać osobnego przygotowania pod licencję wydawcy. Upublicznienie PDF, preprintu, repo lub danych badawczych jest decyzją właściciela, a nie skutkiem udanej kompilacji.
