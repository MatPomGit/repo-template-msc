# Reprodukowalność

Dla każdego zatwierdzonego wyniku zapisuj: Git SHA manuskryptu i kodu analizy; wersje zależności i środowiska; identyfikatory aparatury; schemat danych i jednostki; protokół, ustawienia kalibracji, randomizacji, ziarno RNG; wersję i sumę kontrolną zbioru danych; polecenia odtworzenia; liczbę obserwacji i wyłączeń; status wykonania; odchylenia i wyniki negatywne.

Przed analizą bieżącego portfolio odczytaj najnowsze SHA repozytoriów powiązanych. Przed odtworzeniem eksperymentu odtwórz zamrożone SHA, a nie ich najnowsze gałęzie. Stany `NOT_RUN`, `UNAVAILABLE`, `FAIL`, `PASS` są różne. Test statyczny nie oznacza walidacji metrologicznej.
