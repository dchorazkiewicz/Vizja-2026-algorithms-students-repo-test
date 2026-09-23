"""Simulated student submission: strong tree implementation."""


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
    node = root

    while node is not None:
        if target == node.key:
            return True
        if target < node.key:
            node = node.left
        else:
            node = node.right

    return False


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
    def valid(node, lower, upper):
        if node is None:
            return True

        if lower is not None and node.key <= lower:
            return False
        if upper is not None and node.key >= upper:
            return False

        return (
            valid(node.left, lower, node.key)
            and valid(node.right, node.key, upper)
        )

    return valid(root, None, None)


def _stored_height(node):
    return node.height if node is not None else 0


def _update_height(node):
    node.height = 1 + max(_stored_height(node.left), _stored_height(node.right))


def rotate_left(root):
    pivot = root.right
    moved_subtree = pivot.left

    pivot.left = root
    root.right = moved_subtree

    _update_height(root)
    _update_height(pivot)
    return pivot


def rotate_right(root):
    pivot = root.left
    moved_subtree = pivot.right

    pivot.right = root
    root.left = moved_subtree

    _update_height(root)
    _update_height(pivot)
    return pivot


def avl_insert(root, key):
    if root is None:
        return Node(key)

    if key < root.key:
        root.left = avl_insert(root.left, key)
    elif key > root.key:
        root.right = avl_insert(root.right, key)
    else:
        return root

    _update_height(root)
    balance = _stored_height(root.left) - _stored_height(root.right)

    if balance > 1:
        if key < root.left.key:
            return rotate_right(root)
        root.left = rotate_left(root.left)
        return rotate_right(root)

    if balance < -1:
        if key > root.right.key:
            return rotate_left(root)
        root.right = rotate_right(root.right)
        return rotate_left(root)

    return root
