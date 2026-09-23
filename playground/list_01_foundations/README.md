# List 01 — Contracts, State and Simple Algorithms

## Cel eksperymentu

Ta lista jest pierwszym prototypem modelu pracy dla przedmiotu Algorithms and Complexity.

Nie chodzi wyłącznie o sprawdzenie, czy funkcja zwraca poprawną wartość. Grader ma zbierać automatyczne dowody dotyczące tego, **jak algorytm został zaimplementowany i jak zachowuje się podczas wykonania**.

Lista odpowiada pierwszemu blokowi sylabusa:

- przetwarzanie imperatywne;
- preconditions i postconditions;
- reprezentacja algorytmu;
- cechy algorytmów;
- pseudokod;
- strukturalizacja algorytmów;
- pierwsze argumenty poprawności, terminacji i kosztu.

## Model zadania

Student docelowo otrzymuje:

1. opis problemu;
2. gotową sygnaturę funkcji;
3. wymagania dotyczące kontraktu i zachowania;
4. pustą implementację do uzupełnienia;
5. szablon krótkiego opisu projektu.

Student nie musi projektować API. Ma zaimplementować algorytm zgodny ze specyfikacją.

W tym playgroundzie przechowujemy obok siebie:

- `starter.py` — wersję przeznaczoną do późniejszego wydania studentowi;
- `reference_solution.py` — rozwiązania referencyjne;
- `TASKS.md` — dokładny design sześciu zadań;
- `DESIGN_TEMPLATE.md` — część opisowa, którą można później wymagać od studenta;
- `tests/` — automatyczne testy;
- `grader/` — narzędzia do badania kodu i wykonania.

## Warstwy automatycznej weryfikacji

### 1. Wynik

Klasyczne testy jednostkowe i property-based testing sprawdzają poprawność rezultatów, edge cases i failure behaviour.

### 2. AST — struktura kodu

Pythonowy moduł `ast` pozwala parsować kod do Abstract Syntax Tree i sprawdzać między innymi:

- czy istnieje pętla;
- czy występuje wybór `if`;
- czy są zagnieżdżone pętle;
- czy student używa zakazanych shortcutów, np. `min`, `max`, `sum`, `sorted`, `.index()`;
- czy tworzy slicing;
- czy tworzy list comprehensions;
- czy importuje biblioteki;
- czy używa rekurencji;
- czy używa `print`, `global` lub innych niepożądanych konstrukcji.

AST nie dowodzi samodzielnie złożoności, ale jest silnym dowodem strukturalnym.

### 3. Instrumentowane dane wejściowe

`TrackedSequence` zachowuje się podobnie do sekwencji, ale zapisuje liczbę:

- odczytów elementów;
- zapisów;
- prób slicing;
- rozpoczętych iteracji.

Funkcja studenta dostaje więc obiekt, na którym może normalnie pracować, a grader obserwuje realne interakcje bez proszenia studenta o ręczne logowanie.

### 4. Trace / log algorytmu

Dla wybranych zadań można później dodać jawny hook `emit`, jeżeli chcemy badać deklarowany przez studenta stan pośredni. Nie powinien być on jednak jedynym źródłem dowodu, ponieważ log można sfałszować. Dlatego ważniejsza jest instrumentacja po stronie gradera.

### 5. Empiryczna złożoność

Uruchamiamy tę samą funkcję dla rosnących rozmiarów wejścia i liczymy operacje zamiast opierać ocenę na czasie ściennym.

Dla kosztu `C(n)` szacujemy wykładnik:

```text
p ≈ log(C(2n) / C(n)) / log(2)

p ≈ 0  → zachowanie stałe
p ≈ 1  → zachowanie liniowe
p ≈ 2  → zachowanie kwadratowe
```

To nie jest formalny dowód Big O, lecz bardzo użyteczny automatyczny test zgodności implementacji z oczekiwanym charakterem wzrostu.

### 6. Pamięć

Sprawdzamy m.in.:

- slicing;
- tworzenie nowych list;
- list comprehensions;
- kopiowanie wejścia.

`grader/complexity.py` zawiera też pomocniczy pomiar przez `tracemalloc`. Pomiar runtime jest diagnostyczny; wymagania strukturalne powinny być głównym kryterium.

### 7. Side effects

Możemy sprawdzić, czy funkcja:

- nie modyfikuje wejścia, gdy kontrakt tego zabrania;
- modyfikuje dokładnie ten sam obiekt, gdy wymagane jest in-place;
- nie wypisuje przypadkowych danych;
- nie tworzy niepożądanego globalnego stanu.

### 8. Terminacja i bezpieczeństwo

Docelowy prywatny grader powinien uruchamiać kod studenta w izolacji, bez sekretów i sieci, z limitami CPU, pamięci i czasu. Workflow playgroundu ma limit czasu całego joba; właściwy sandbox powstanie później.

## Zadania

1. `clamp` — selection, contract, O(1).
2. `first_index` — linear scan i early exit.
3. `min_max` — jedno przejście, O(1) auxiliary space.
4. `reverse_in_place` — jawny side effect i pamięć O(1).
5. `first_negative_running_sum` — stan akumulatora i early termination.
6. `analyse_scores` — capstone: validation, accumulation, decomposition i jedno przejście.

Szczegóły: [TASKS.md](TASKS.md).

## Uruchamianie

Domyślnie testujemy rozwiązanie referencyjne:

```bash
python -m pip install -r playground/list_01_foundations/requirements-dev.txt
pytest -q playground/list_01_foundations/tests
```

Można wskazać inny plik z implementacją:

```bash
SOLUTION_FILE=/path/to/student_solution.py \
pytest -q playground/list_01_foundations/tests
```

Dzięki temu te same testy będzie można później uruchamiać przeciwko snapshotowi rozwiązania pobranemu z mirrora studenta.


## Trzy przykładowe profile studenta

Playground zawiera teraz trzy kompletne przykłady:

- `samples/student_good.py` — rozwiązanie poprawne wynikowo i zgodne z wymaganym sposobem implementacji;
- `samples/student_medium.py` — wyniki są poprawne, ale kod używa shortcutów, dodatkowych przejść lub nie kończy się tak wcześnie, jak powinien;
- `samples/student_bad.py` — zawiera zarówno błędy poprawności, jak i błędy algorytmiczne.

To pozwala testować nie tylko zadania, ale również **sam grader**. Testy sprawdzają, że dobry profil przechodzi, średni jest rozpoznawany jako poprawny funkcjonalnie lecz metodycznie słabszy, a słaby profil generuje zarówno błędy wynikowe, jak i algorytmiczne.

## Rozszerzony raport implementacji

`grader/evaluate.py` generuje raport łączący:

- poprawność funkcjonalną;
- metryki AST;
- zakazane skróty;
- liczbę pętli i głębokość zagnieżdżeń;
- odczyty i zapisy danych;
- indeksy rzeczywiście odwiedzone przez algorytm;
- liczbę iteracji po sekwencji;
- porównania na instrumentowanych wartościach;
- early termination;
- empiryczny wzrost kosztu dla kolejnych rozmiarów n;
- trace wykonanych linii i wywołań;
- stdout/stderr;
- diagnostyczny pomiar pamięci.

Przykład:

```bash
python -m playground.list_01_foundations.grader.evaluate \
  --solution playground/list_01_foundations/samples/student_medium.py \
  --markdown report.md \
  --json report.json
```

## GitHub Actions jako laboratorium

Workflow `.github/workflows/list-01-playground.yml` przy każdym pushu:

1. uruchamia pełne testy gradera;
2. sprawdza, czy trzy profile studenta są poprawnie rozróżniane;
3. generuje osobne raporty dla profilu dobrego, średniego i słabego;
4. publikuje je w GitHub Actions Job Summary;
5. zapisuje log pytest, JUnit XML oraz raporty Markdown/JSON jako artifact.

W ten sposób publiczne repozytorium jest jednocześnie działającą demonstracją tego, ile informacji można automatycznie wydobyć z bardzo prostych implementacji algorytmów.
