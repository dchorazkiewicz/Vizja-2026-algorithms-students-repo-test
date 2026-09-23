# List 01 — specyfikacja zadań

## T1 — Clamp

Implementuj:

```python
def clamp(value: int, lower: int, upper: int) -> int:
    ...
```

### Kontrakt

Precondition:

```text
lower <= upper
```

Postcondition:

- gdy `value < lower`, zwróć `lower`;
- gdy `value > upper`, zwróć `upper`;
- w przeciwnym razie zwróć `value`.

### Cel dydaktyczny

- selection;
- precondition/postcondition;
- rozróżnienie specyfikacji i implementacji;
- koszt O(1).

### Automatyczne kontrole

- poprawność dla wartości wewnątrz, poniżej i powyżej przedziału;
- wartości graniczne;
- property-based tests;
- AST: obecność `if`;
- AST: zakaz `min`, `max`, `sorted`.

---

## T2 — First occurrence

Implementuj:

```python
def first_index(values, target) -> int:
    ...
```

### Postcondition

- jeżeli `target` występuje, wynik jest najmniejszym indeksem `i`, dla którego `values[i] == target`;
- jeżeli nie występuje, wynik to `-1`;
- wejście nie może zostać zmodyfikowane.

### Cel dydaktyczny

- iteracja;
- kolejność przeglądania;
- early return;
- best case O(1), worst case O(n).

### Automatyczne kontrole

- pusta sekwencja;
- pierwszy/ostatni element;
- duplikaty;
- brak targetu;
- property-based testing;
- AST: wymagana pętla;
- AST: zakaz `.index()` i `next()`;
- instrumentacja: dla trafienia na indeksie 1 nie powinny być czytane dalsze elementy;
- wzrost liczby odczytów dla przypadku worst-case powinien być liniowy.

---

## T3 — Minimum i maksimum w jednym przejściu

Implementuj:

```python
def min_max(values) -> tuple[int, int]:
    ...
```

### Precondition

Sekwencja jest niepusta.

### Postcondition

Zwróć parę `(minimum, maximum)`.

### Failure behaviour

Dla pustego wejścia zgłoś `ValueError`.

### Wymagania algorytmiczne

- jedno przejście po danych;
- nie modyfikuj wejścia;
- O(n) czasu;
- O(1) pamięci pomocniczej;
- bez `min`, `max`, `sorted`, `.sort()`;
- bez slicing tworzącego kopię.

### Automatyczne kontrole

- liczby dodatnie/ujemne;
- duplikaty;
- jeden element;
- losowe wejścia;
- brak modyfikacji wejścia;
- AST: pętla, brak shortcutów, brak slicing;
- instrumentacja: liczba odczytów proporcjonalna do n;
- empiryczny wykładnik wzrostu bliski 1.

---

## T4 — Reverse in place

Implementuj:

```python
def reverse_in_place(values) -> None:
    ...
```

### Postcondition

Po wykonaniu:

```text
values[i] == old(values[n - 1 - i])
```

dla każdego poprawnego indeksu.

### Side effect

Funkcja **ma zmienić ten sam obiekt** i zwrócić `None`.

### Wymagania

- O(n) czasu;
- O(1) pamięci pomocniczej;
- bez `reversed`;
- bez `values[::-1]`;
- bez tworzenia kopii całej listy.

### Automatyczne kontrole

- pusta i jednoelementowa lista;
- długości parzyste i nieparzyste;
- zachowanie identity obiektu;
- zwracane `None`;
- AST: brak slicing/reversed;
- instrumentacja: zapisów i odczytów powinno być O(n).

---

## T5 — First negative running sum

Implementuj:

```python
def first_negative_running_sum(values) -> int:
    ...
```

Zwróć pierwszy indeks, dla którego suma prefiksowa staje się **ściśle ujemna**. Jeżeli nigdy się to nie dzieje, zwróć `-1`.

Przykład:

```text
[4, -1, -2, -5, 8]
running sums: 4, 3, 1, -4, 4
result: 3
```

### Cel dydaktyczny

- znaczenie zmiennej stanu;
- akumulator;
- early termination;
- rozpoznanie rozwiązania O(n) zamiast O(n²).

### Zakazane skróty

W szczególności nie należy wielokrotnie liczyć:

```python
sum(values[:i + 1])
```

### Automatyczne kontrole

- puste wejście;
- wynik na pierwszym elemencie;
- brak wyniku;
- późny wynik;
- AST: zakaz `sum()` i slicing;
- instrumentacja: jeżeli pierwszy element daje wynik, dalsza sekwencja nie może być czytana;
- worst case ma rosnąć liniowo.

---

## T6 — Analyse scores

Implementuj:

```python
def analyse_scores(scores, passing_score: int) -> tuple[float, int, int, int]:
    ...
```

Zwróć:

```text
(average, minimum, maximum, number_of_passing_scores)
```

### Precondition dla poprawnych danych

- `scores` jest niepuste;
- każdy wynik jest w zakresie 0..100;
- `passing_score` jest w zakresie 0..100.

### Failure behaviour

Dla naruszenia kontraktu zgłoś `ValueError`.

### Wymagania algorytmiczne

- jedno przejście po `scores`;
- nie modyfikuj wejścia;
- O(n) czasu;
- O(1) pamięci pomocniczej;
- bez `sum`, `min`, `max`, `sorted`.

### Cel dydaktyczny

To capstone pierwszej listy:

- validation;
- accumulation;
- selection;
- kilka znaczeń stanu jednocześnie;
- failure behaviour;
- świadome projektowanie jednego przejścia.

### Automatyczne kontrole

- edge cases;
- niepoprawne wyniki;
- niepoprawny próg;
- losowe dane;
- AST: zakaz shortcutów;
- AST: jedna pętla w funkcji;
- instrumentacja: liniowa liczba odczytów;
- brak modyfikacji wejścia.
