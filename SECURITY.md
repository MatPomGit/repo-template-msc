# Bezpieczeństwo i poufność projektu MSC

**Status: szablon / kanał zgłoszeń nieustalony.** Zanim projekt przyjmie rzeczywiste dane, skonfiguruj prawdziwy, prywatny kanał zgłoszeń do właściciela i sprawdź możliwość jego obsługi. Nie publikuj poufnych zgłoszeń ani danych pozwalających na reidentyfikację w Issues lub na Pages.

## Zakres ochrony

Dane uczestników, EEG, eye-tracking, nagrania, dane zdrowotne, klucze i zastrzeżone materiały psychometryczne przechowuj wyłącznie zgodnie z zatwierdzonym protokołem, podstawą prawną, zgodą i zasadami retencji. Prywatne repo nie jest automatycznie bezpiecznym repozytorium danych osobowych. Identyfikatory aparatury mogą pozostawać w uprawnionym prywatnym katalogu; nie ujawniaj ich w witrynie.

Przed testem lub uruchomieniem kodu z niezaufanego PR wymagaj izolacji i minimalnych uprawnień. Nie dopuszczaj sekretów ani danych rzeczywistych do nieuprawnionych runnerów, logów lub artefaktów. Nie utożsamiaj technicznego PASS z oceną etyczną lub metrologiczną.

## Zgłaszanie i incydenty

Luki, podejrzenie ujawnienia i niewłaściwe przetwarzanie danych zgłaszaj poza publicznymi kanałami. Do czasu ustalenia rzeczywistego prywatnego kontaktu status obsługi zgłoszeń to `NOT_CONFIGURED`. Nie podawaj fikcyjnego adresu ani obietnicy czasu odpowiedzi.

Zobacz [model zagrożeń](docs/security/threat-model.md), [postępowanie przy incydencie](docs/security/incident-response.md), [ADR bezpieczeństwa](docs/adr/0001-research-data-boundaries.md) i [politykę Pages](docs/pages.md). Zewnętrzne udostępnienie zawsze podlega odrębnej ocenie praw, etyki, poufności i widoczności witryny.
