# Manifest dydaktyczny: dlaczego Python

## Cel nadrzędny

Na tym przedmiocie uczymy przede wszystkim **algorytmów**, a nie konkretnego języka programowania.

Język ma być narzędziem do:

- precyzyjnego zapisu algorytmu;
- uruchamiania go na rzeczywistych danych;
- automatycznego testowania poprawności;
- obserwowania sposobu wykonania;
- badania kosztu i złożoności;
- dostarczania studentowi możliwie szybkiej, obiektywnej informacji zwrotnej.

Dlatego domyślnym językiem ćwiczeń w tym modelu jest **Python**.

## Dlaczego nie oznacza to, że Java lub C++ są gorsze

Te same algorytmy można implementować i testować w C++, Javie oraz wielu innych językach.

C++ i Java dają bardzo mocne możliwości testowania, profilowania i analizy kodu. C++ pozwala m.in. przeciążać operatory i bardzo dokładnie obserwować kopiowanie, przenoszenie oraz alokację. Java oferuje dojrzałe narzędzia do analizy kodu, instrumentacji i testów.

Wybór Pythona nie wynika więc z braku możliwości w innych językach.

Wynika z celu dydaktycznego.

## Python minimalizuje narzut języka

Python ma prostą składnię i niewielką ilość kodu technicznego potrzebnego do zapisania podstawowych algorytmów.

Student może skupić się na:

- stanie algorytmu;
- kolejności operacji;
- warunkach;
- pętlach;
- niezmiennikach;
- poprawności;
- terminacji;
- koszcie wykonania;

zamiast na szczegółach systemu typów, deklaracjach, szablonach, zarządzaniu pamięcią czy rozbudowanej strukturze programu.

To jest szczególnie ważne na przedmiocie Algorithms and Complexity, gdzie język implementacji powinien możliwie mało zasłaniać sam algorytm.

## Python daje prowadzącemu naturalną obserwowalność algorytmu

Dynamiczny model Pythona pozwala w naturalny sposób podstawiać do funkcji obiekty kontrolowane przez grader.

Zamiast zwykłej listy można przekazać obiekt zachowujący się jak sekwencja i automatycznie rejestrować:

- liczbę odczytów elementów;
- liczbę zapisów;
- liczbę rozpoczętych iteracji;
- slicing;
- moment zakończenia przeglądania danych;
- próby modyfikacji wejścia.

Podobnie można instrumentować wartości i operacje, aby liczyć porównania lub inne operacje istotne dla danego algorytmu.

Student może przy tym pisać naturalny kod Pythona. Nie trzeba deformować API tylko po to, żeby grader mógł obserwować wykonanie.

## Python daje bardzo prosty dostęp do AST

Moduł standardowy `ast` pozwala analizować strukturę programu bez uruchamiania go.

Możemy automatycznie sprawdzić między innymi:

- czy student użył pętli;
- czy pętle są zagnieżdżone;
- czy występuje rekurencja;
- czy użyto `min`, `max`, `sum`, `sorted`, `.sort()`, `.index()`;
- czy student tworzy slicing;
- czy tworzy dodatkowe listy;
- czy używa list comprehensions;
- czy występują niepożądane importy;
- czy występują efekty uboczne takie jak `print` lub stan globalny.

Dzięki temu automatyczna ocena może dotyczyć nie tylko odpowiedzi programu, ale również techniki algorytmicznej.

## Weryfikujemy algorytm na kilku niezależnych poziomach

Docelowy grader powinien łączyć:

1. **unit tests** — czy wynik jest poprawny dla konkretnych przypadków;
2. **property-based tests** — czy własności wyniku zachodzą dla dużej klasy generowanych wejść;
3. **AST** — jak wygląda struktura implementacji;
4. **instrumented execution** — co program faktycznie robi z wejściem;
5. **operation counting** — ile istotnych operacji zostało wykonanych;
6. **complexity experiments** — jak koszt rośnie wraz z rozmiarem wejścia;
7. **side-effect checks** — czy wejście zostało zmodyfikowane zgodnie z kontraktem;
8. **memory diagnostics** — czy rozwiązanie tworzy niepotrzebne kopie lub struktury;
9. **termination limits** — czy implementacja kończy działanie w rozsądnym limicie.

Każda warstwa odpowiada na inne pytanie. Sam poprawny wynik nie wystarcza do stwierdzenia, że student zaimplementował wymagany algorytm.

## Złożoność ma być czymś obserwowalnym

Jednym z najważniejszych celów jest automatyczne badanie charakteru kosztu implementacji.

Zamiast opierać się wyłącznie na czasie wykonania, który zależy od maszyny, możemy liczyć operacje istotne dla algorytmu, np.:

- odczyty;
- zapisy;
- porównania;
- zamiany;
- odwiedzone wierzchołki;
- przebadane krawędzie;
- wywołania rekurencyjne.

Następnie uruchamiamy algorytm dla rosnących rozmiarów wejścia i obserwujemy wzrost kosztu.

To pozwala studentowi zobaczyć w praktyce różnicę pomiędzy zachowaniem:

- stałym;
- liniowym;
- liniowo-logarytmicznym;
- kwadratowym;
- i innymi klasami wzrostu.

## Zasada projektowa

**Mierzymy maksymalnie dużo, ale nie komplikujemy studentowi implementacji tylko po to, żeby graderowi było wygodniej.**

Instrumentacja ma być przede wszystkim po stronie prowadzącego.

Student powinien otrzymywać możliwie naturalny kontrakt, np.:

```python
def first_index(values, target) -> int:
    ...
```

a grader ma samodzielnie zbierać możliwie dużo dowodów dotyczących jakości implementacji.

## Wniosek

Python jest tutaj językiem dydaktycznym pierwszego wyboru nie dlatego, że inne języki nie pozwalają na głębokie testowanie.

Wybieramy go dlatego, że:

> pozwala nam skupić się na samych algorytmach i jednocześnie daje wyjątkowo naturalne możliwości automatycznej obserwacji, instrumentacji i analizy ich implementacji.

Jeżeli później będziemy chcieli pokazać ten sam algorytm w C++ lub Javie, możemy to zrobić. Algorytm pozostaje centralnym obiektem nauki, a język jest jego reprezentacją.
