import copy

from hypothesis import given, strategies as st


class StableItem:
    def __init__(self, key, tag):
        self.key = key
        self.tag = tag

    @staticmethod
    def _key(other):
        return other.key if isinstance(other, StableItem) else other

    def __lt__(self, other): return self.key < self._key(other)
    def __le__(self, other): return self.key <= self._key(other)
    def __gt__(self, other): return self.key > self._key(other)
    def __ge__(self, other): return self.key >= self._key(other)
    def __eq__(self, other): return self.key == self._key(other)


def assert_stable(values):
    groups = {}
    for item in values:
        groups.setdefault(item.key, []).append(item.tag)
    assert all(tags == sorted(tags) for tags in groups.values())


@given(st.lists(st.integers(-100, 100), max_size=100).map(sorted), st.integers(-100, 100))
def test_binary_search_property(solution, values, target):
    result = solution.binary_search(values, target)
    expected = values.index(target) if target in values else -1
    assert result == expected


def test_binary_search_duplicate_is_leftmost(solution):
    assert solution.binary_search([1, 2, 2, 2, 4], 2) == 1


@given(st.lists(st.integers(-100, 100), max_size=60))
def test_insertion_sort_property(solution, values):
    expected = sorted(values)
    original = values
    result = solution.insertion_sort_in_place(values)
    assert result is None
    assert values is original
    assert values == expected


def test_insertion_sort_stability(solution):
    values = [
        StableItem(2, 0),
        StableItem(1, 1),
        StableItem(2, 2),
        StableItem(1, 3),
        StableItem(2, 4),
    ]
    solution.insertion_sort_in_place(values)
    assert [item.key for item in values] == [1, 1, 2, 2, 2]
    assert_stable(values)


@given(st.lists(st.integers(-100, 100), max_size=60))
def test_selection_sort_property(solution, values):
    expected = sorted(values)
    original = values
    result = solution.selection_sort_in_place(values)
    assert result is None
    assert values is original
    assert values == expected


@given(
    st.lists(st.integers(-100, 100), max_size=40).map(sorted),
    st.lists(st.integers(-100, 100), max_size=40).map(sorted),
)
def test_merge_sorted_property(solution, left, right):
    left_before = copy.deepcopy(left)
    right_before = copy.deepcopy(right)
    result = solution.merge_sorted(left, right)
    assert result == sorted(left + right)
    assert left == left_before
    assert right == right_before


def test_merge_sorted_stability(solution):
    left = [StableItem(1, 0), StableItem(2, 1), StableItem(2, 2)]
    right = [StableItem(2, 3), StableItem(2, 4), StableItem(3, 5)]
    result = solution.merge_sorted(left, right)
    assert [item.key for item in result] == [1, 2, 2, 2, 2, 3]
    assert_stable(result)


@given(st.lists(st.integers(-100, 100), max_size=60))
def test_merge_sort_property(solution, values):
    before = copy.deepcopy(values)
    result = solution.merge_sort(values)
    assert result == sorted(values)
    assert values == before
    assert result is not values


def test_merge_sort_stability(solution):
    values = [
        StableItem(2, 0),
        StableItem(1, 1),
        StableItem(2, 2),
        StableItem(1, 3),
        StableItem(2, 4),
    ]
    result = solution.merge_sort(values)
    assert [item.key for item in result] == [1, 1, 2, 2, 2]
    assert_stable(result)


@given(st.lists(st.integers(-100, 100), max_size=60))
def test_quick_sort_property(solution, values):
    expected = sorted(values)
    original = values
    result = solution.quick_sort_in_place(values)
    assert result is None
    assert values is original
    assert values == expected
