"""Simulated student submission: structural and invariant defects."""


class Node:
    def __init__(self, key, left=None, right=None, height=1):
        self.key = key
        self.left = left
        self.right = right
        self.height = height


def inorder_keys(root) -> list[int]:
    if root is None:
        return []
    return [root.key] + inorder_keys(root.left) + inorder_keys(root.right)


def bst_contains(root, target) -> bool:
    node = root
    while node is not None:
        if target == node.key:
            return True
        if target < node.key:
            node = node.right
        else:
            node = node.left
    return False


def bst_insert(root, key):
    if root is None:
        return Node(key)

    node = root
    while True:
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
        return -1
    return 1 + max(bst_height(root.left), bst_height(root.right))


def is_valid_bst(root) -> bool:
    if root is None:
        return True

    if root.left is not None and root.left.key >= root.key:
        return False
    if root.right is not None and root.right.key <= root.key:
        return False

    return is_valid_bst(root.left) and is_valid_bst(root.right)


def _height(node):
    return node.height if node is not None else 0


def rotate_left(root):
    pivot = root.right
    root.right = pivot.left
    pivot.left = root
    return pivot


def rotate_right(root):
    pivot = root.left
    root.left = pivot.right
    pivot.right = root
    return pivot


def avl_insert(root, key):
    return bst_insert(root, key)
