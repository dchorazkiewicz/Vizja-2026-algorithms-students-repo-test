from hypothesis import given, strategies as st


def inorder(root):
    if root is None:
        return []
    return inorder(root.left) + [root.key] + inorder(root.right)


def valid_bst(root):
    def visit(node, low, high):
        if node is None:
            return True
        if low is not None and node.key <= low:
            return False
        if high is not None and node.key >= high:
            return False
        return visit(node.left, low, node.key) and visit(node.right, node.key, high)
    return visit(root, None, None)


def valid_avl(root):
    def visit(node):
        if node is None:
            return True, 0, None, None
        left_ok, left_h, left_min, left_max = visit(node.left)
        right_ok, right_h, right_min, right_max = visit(node.right)
        expected = 1 + max(left_h, right_h)
        ok = (
            left_ok and right_ok
            and (left_max is None or left_max < node.key)
            and (right_min is None or node.key < right_min)
            and abs(left_h - right_h) <= 1
            and node.height == expected
        )
        minimum = left_min if left_min is not None else node.key
        maximum = right_max if right_max is not None else node.key
        return ok, expected, minimum, maximum
    return visit(root)[0]


@given(st.lists(st.integers(-100, 100), unique=True, max_size=40))
def test_bst_insert_property(solution, values):
    root = None
    for value in values:
        root = solution.bst_insert(root, value)
    assert inorder(root) == sorted(values)
    assert valid_bst(root)


@given(st.lists(st.integers(-100, 100), unique=True, max_size=40), st.integers(-100, 100))
def test_bst_contains_property(solution, values, target):
    root = None
    for value in values:
        root = solution.bst_insert(root, value)
    assert solution.bst_contains(root, target) == (target in values)


@given(st.lists(st.integers(-100, 100), unique=True, max_size=30))
def test_inorder_property(solution, values):
    root = None
    for value in values:
        root = solution.bst_insert(root, value)
    assert solution.inorder_keys(root) == sorted(values)


@given(st.lists(st.integers(-100, 100), unique=True, max_size=30))
def test_avl_insert_property(solution, values):
    root = None
    for value in values:
        root = solution.avl_insert(root, value)
    assert inorder(root) == sorted(values)
    assert valid_avl(root)


def test_global_bst_violation(solution):
    root = solution.Node(10)
    root.left = solution.Node(5)
    root.left.right = solution.Node(12)
    root.right = solution.Node(15)
    assert solution.is_valid_bst(root) is False


def test_height_convention(solution):
    assert solution.bst_height(None) == 0
    assert solution.bst_height(solution.Node(1)) == 1
