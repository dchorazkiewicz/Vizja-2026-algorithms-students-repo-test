# Automatyczny workflow pracy studenta i oceny technicznej

## Zakres dokumentu

Ten dokument opisuje wyłącznie **automatyczną i infrastrukturalną część pracy z zadaniami programistycznymi** na przedmiocie Algorithms and Complexity.

Nie opisuje wykładu ani przebiegu zajęć stacjonarnych. Punktem startowym są listy zadań publikowane studentom, a punktem końcowym — wersjonowany raport techniczny i informacja zwrotna wynikająca z kolejnych wersji pracy studenta.

## Zasada nadrzędna

Student pracuje w swoim repozytorium. Prowadzący nie musi ręcznie otwierać każdego forka i uruchamiać testów.

System ma automatycznie:

1. wykryć lub pobrać nową wersję pracy studenta;
2. zachować obserwowany stan repozytorium;
3. uruchomić prywatny grader;
4. zbudować raport techniczny;
5. porównać wynik z poprzednią wersją;
6. przygotować informację zwrotną;
7. opcjonalnie opublikować ją w GitHub Issue;
8. po kolejnej zmianie studenta powtórzyć cały proces.

## Warstwy repozytoriów

Docelowy model rozdziela kilka odpowiedzialności.

### 1. Workbook studenta

Publiczne repozytorium zawiera to, co student ma zobaczyć:

- treść zadań;
- sygnatury funkcji;
- starter code;
- wymagania dotyczące wejścia, wyjścia i kontraktu;
- ewentualny szablon opisu rozwiązania.

Nie zawiera prywatnych testów prowadzącego ani rozwiązań referencyjnych.

Student tworzy fork i pracuje we własnym repozytorium.

### 2. Fork studenta

Fork jest faktycznym miejscem pracy studenta.

Zawiera:

- implementacje;
- kolejne commity;
- poprawki;
- historię rozwoju rozwiązania;
- GitHub Issues i odpowiedzi, jeżeli ten kanał jest używany do komunikacji.

Oceniamy konkretną zaobserwowaną wersję repozytorium, najlepiej przez SHA.

### 3. Mirror

Prywatny mirror jest technicznym archiwum tego, co prowadzący rzeczywiście zaobserwował w repozytorium studenta.

Mirror powinien przechowywać co najmniej:

- repozytorium i właściciela;
- obserwowany commit SHA;
- timestamp synchronizacji;
- zmienione pliki;
- aktualny snapshot potrzebnych plików;
- historię wcześniejszych obserwacji;
- Issues i komentarze, jeżeli są częścią procesu;
- informację o force-push, usunięciu lub zmianie wcześniej obserwowanej historii.

Mirror nie jest miejscem wydawania decyzji dydaktycznych. Jest trwałym dowodem technicznym.

### 4. Prywatny grader

Grader należy do prowadzącego i student go nie widzi.

Może zawierać:

- unit tests;
- property-based tests;
- testy edge cases;
- analizę AST;
- instrumentowane sekwencje i wartości;
- liczenie operacji;
- eksperymenty wzrostu kosztu;
- testy side effects;
- diagnostykę pamięci;
- limity terminacji;
- rozwiązania referencyjne;
- reguły generowania raportów.

Student nie powinien móc dopasowywać kodu do pełnego zestawu prywatnych testów.

## Główny przepływ

```text
lista zadań
    ↓
oficjalny workbook
    ↓ fork
repozytorium studenta
    ↓ commit / push
synchronizacja
    ↓
prywatny mirror konkretnego SHA
    ↓
prywatny grader
    ↓
automatyczne dowody techniczne
    ↓
wersjonowany raport techniczny
    ↓
informacja zwrotna
    ↓
GitHub Issue / komentarz
    ↓
student poprawia rozwiązanie
    ↓
kolejny commit
    ↓
kolejna synchronizacja i kolejny raport
```

## Co badamy automatycznie

Jeżeli dana własność daje się rozsądnie sprawdzić automatycznie, powinniśmy to robić.

### Poprawność funkcjonalna

- zwykłe unit tests;
- przypadki brzegowe;
- niepoprawne wejścia;
- oczekiwane wyjątki;
- property-based testing;
- testy metamorficzne;
- brakujące funkcje lub pliki.

### Struktura implementacji

Przez AST można badać między innymi:

- obecność pętli;
- liczbę pętli;
- głębokość zagnieżdżeń;
- użycie rekurencji;
- liczbę i położenie `return`;
- użycie `if`;
- użycie zakazanych skrótów;
- `min`, `max`, `sum`, `sorted`, `.sort()`, `.index()`;
- slicing;
- list comprehensions;
- importy;
- `print`;
- stan globalny;
- konstrukcje niezgodne z celem konkretnego zadania.

### Zachowanie podczas wykonania

Instrumentowane obiekty pozwalają obserwować rzeczywiste wykonanie bez wymagania, aby student sam logował algorytm.

Możemy mierzyć:

- liczbę odczytów;
- indeksy rzeczywiście odwiedzone;
- liczbę zapisów;
- liczbę rozpoczętych iteracji;
- slicing;
- porównania;
- operacje arytmetyczne;
- early termination;
- mutację wejścia;
- kolejność dostępu do danych.

### Złożoność

Dla kolejnych rozmiarów wejścia możemy zbierać koszt operacyjny:

```text
n = 64
n = 128
n = 256
n = 512
...
```

i obserwować, jak rośnie liczba istotnych operacji.

Preferujemy liczenie operacji nad samym czasem ściennym, ponieważ wynik jest mniej zależny od maszyny wykonującej test.

Możemy automatycznie rozpoznawać zachowanie zbliżone do:

- O(1);
- O(n);
- O(n log n);
- O(n²);

oraz flagować implementacje, których wzrost jest niezgodny z wymaganiem zadania.

To nie zastępuje formalnego dowodu złożoności, ale daje bardzo mocny empiryczny dowód dotyczący rzeczywistej implementacji.

### Pamięć i efekty uboczne

Możemy badać:

- czy wejście zostało zmodyfikowane;
- czy funkcja in-place rzeczywiście zmienia ten sam obiekt;
- czy tworzona jest kopia całych danych;
- czy występuje slicing;
- czy powstają pomocnicze listy;
- czy pamięć pomocnicza rośnie z `n`;
- stdout i stderr;
- dostęp do plików lub inne niepożądane efekty.

## Raport techniczny

Dla każdej obserwowanej wersji pracy studenta powinien powstać osobny raport techniczny.

Raport musi wskazywać:

- studenta;
- repozytorium;
- commit SHA;
- moment obserwacji;
- wersję gradera;
- wersję zestawu testów;
- listę znalezionych plików;
- listę brakujących plików;
- wyniki testów;
- obserwacje AST;
- pomiary runtime;
- charakter wzrostu kosztu;
- diagnostykę pamięci;
- błędy wykonania;
- timeouty;
- ostrzeżenia.

Raport jest **dowodem technicznym**, a nie samą oceną końcową.

Przykładowy fragment:

```text
student: ...
repository: ...
sha: abc123

Task 02 — first_index

FUNCTIONAL
PASS 427/427

STRUCTURE
PASS explicit loop
PASS no list.index()
PASS no slicing

EXECUTION
target position: 3
elements inspected: 4
early termination: yes

COMPLEXITY
64   -> 64 reads
128  -> 128 reads
256  -> 256 reads
512  -> 512 reads

observed growth: linear
```

Jeżeli czegoś brakuje, raport również ma to jawnie powiedzieć:

```text
Task 04
solution function not found

Task 05
file missing

Task 06
execution timeout
```

Brak pracy jest także wynikiem technicznym i powinien być wersjonowany tak samo jak poprawna implementacja.

## Wersjonowanie raportów

Nie chcemy jednego nadpisywanego statusu.

Dla kolejnych commitów studenta:

```text
SHA A → report A
SHA B → report B
SHA C → report C
```

Dzięki temu możemy odpowiedzieć:

- co student miał wcześniej;
- co poprawił;
- czy poprawa usunęła problem;
- czy pojawiła się regresja;
- kiedy zmieniła się charakterystyka algorytmu;
- do jakiej wersji odnosiła się wcześniejsza informacja zwrotna.

Aktualny status może być materializowany osobno, ale historia raportów pozostaje zachowana.

## Informacja zwrotna przez GitHub Issue

Raport techniczny może zostać przekształcony w krótszą informację zwrotną dla studenta.

Przykład:

```text
Lista 01 / Task 05

Wynik funkcji jest poprawny dla wszystkich testowanych przypadków.

Implementacja wielokrotnie oblicza sumę prefiksu i tworzy slicing.
W pomiarze koszt rośnie około kwadratowo.

Spróbuj utrzymywać bieżącą sumę w jednej zmiennej i przetwarzać każdy element najwyżej raz.

Analysed commit: abc123
```

Taką informację można opublikować jako Issue lub komentarz w repozytorium studenta.

Issue staje się wtedy kanałem interakcji:

1. system publikuje wynik dla konkretnego SHA;
2. student odpowiada lub poprawia kod;
3. pojawia się nowy commit;
4. synchronizacja pobiera nową wersję;
5. grader generuje kolejny raport;
6. system może opublikować aktualizację.

## Automatyczna synchronizacja

Docelowo synchronizacja forków nie musi wymagać ręcznego polecenia.

Możliwy jest scheduler uruchamiający proces np. okresowo:

```text
scheduler
    ↓
lista aktywnych forków
    ↓
czy HEAD zmienił się od ostatniej obserwacji?
    ├── nie → brak pracy
    └── tak
          ↓
       mirror nowego SHA
          ↓
       uruchom grader
          ↓
       zapisz raport
          ↓
       porównaj z poprzednim raportem
          ↓
       przygotuj feedback / attention
```

W przyszłości trigger może być również event-driven, ale okresowy scheduler jest prostym i przewidywalnym mechanizmem startowym.

## Deduplikacja i idempotencja

Ten sam commit nie powinien być oceniany wielokrotnie bez powodu.

Kluczem wykonania może być na przykład:

```text
student_repository
+ commit_sha
+ grader_version
+ test_suite_version
```

Jeżeli wszystkie cztery wartości są takie same, wynik powinien być odtwarzalny i nie powinien tworzyć nowej logicznej oceny technicznej.

Ponowne uruchomienie jest uzasadnione, gdy zmieni się:

- kod studenta;
- grader;
- zestaw testów;
- konfiguracja zadania.

## Rozdzielenie faktu technicznego od decyzji dydaktycznej

Automatyzacja może stwierdzić:

```text
tests: 100% pass
observed growth: quadratic
forbidden shortcut: detected
input mutation: none
```

To są fakty techniczne.

Dopiero osobne reguły dydaktyczne lub prowadzący określają, czy oznacza to:

- zaliczenie;
- poprawę;
- ostrzeżenie;
- potrzebę rozmowy;
- brak działania.

Dzięki temu zmiana testów lub gradera nie przepisuje automatycznie historii decyzji dydaktycznych.

## Relacja z Vizja_classes_databases

Automatyczny pipeline powinien docelowo przekazywać do `Vizja_classes_databases` tylko semantyczne, audytowalne wyniki, np.:

- student przesłał nową wersję;
- grader zakończył się poprawnie;
- zadanie funkcjonalnie przechodzi testy;
- implementacja ma wykryty problem ze złożonością;
- wymagany plik nie istnieje;
- raport techniczny jest dostępny pod konkretnym identyfikatorem;
- feedback został opublikowany;
- student odpowiedział;
- pojawiła się kolejna wersja rozwiązania.

Pełne techniczne logi i snapshoty mogą pozostać w warstwie mirror/grader.

## Docelowa pętla

Najważniejszą jednostką procesu nie jest pojedynczy test, tylko **kolejna wersja pracy studenta**:

```text
implementacja
→ obserwacja
→ test
→ raport
→ feedback
→ poprawa
→ nowa obserwacja
→ nowy raport
```

System ma dzięki temu nie tylko sprawdzać rozwiązania, ale również pokazywać rozwój pracy studenta w czasie.
