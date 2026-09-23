"""Simulated student submission: correct results through unnecessarily expensive methods."""


class Node:
    def __init__(self, key, left=None, right=None, height=1):
        self.key = key
        self.left = left
        self.right = right
        self.height = height


def inorder_keys(root) -> list[int]:
    result = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        result.append(node.key)
        visit(node.right)

    visit(root)
    return result


def bst_contains(root, target) -> bool:
    return target in inorder_keys(root)


def bst_insert(root, key):
    if root is None:
        return Node(key)

    node = root
    while True:
        if key == node.key:
            return root
        if key < node.key:
            if node.left is None:
                node.left = Node(key)
                return root
            node = node.left
        else:
            if node.right is None:
                node.right = Node(key)
                return root
            node = node.right


def bst_height(root) -> int:
    if root is None:
        return 0
    return 1 + max(bst_height(root.left), bst_height(root.right))


def is_valid_bst(root) -> bool:
    keys = inorder_keys(root)
    for index in range(1, len(keys)):
        if keys[index - 1] >= keys[index]:
            return False
    return True


def _height(node):
    return node.height if node is not None else 0


def _update(node):
    node.height = 1 + max(_height(node.left), _height(node.right))


def rotate_left(root):
    pivot = root.right
    moved = pivot.left
    pivot.left = root
    root.right = moved
    _update(root)
    _update(pivot)
    return pivot


def rotate_right(root):
    pivot = root.left
    moved = pivot.right
    pivot.right = root
    root.left = moved
    _update(root)
    _update(pivot)
    return pivot


def avl_insert(root, key):
    keys = inorder_keys(root)

    if key not in keys:
        keys.append(key)
        keys.sort()

    def build(low, high):
        if low >= high:
            return None
        middle = (low + high) // 2
        node = Node(keys[middle])
        node.left = build(low, middle)
        node.right = build(middle + 1, high)
        _update(node)
        return node

    return build(0, len(keys))
