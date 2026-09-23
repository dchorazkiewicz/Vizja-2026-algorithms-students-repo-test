"""Student-facing starter for List 03."""


class Node:
    def __init__(self, key, left=None, right=None, height=1):
        self.key = key
        self.left = left
        self.right = right
        self.height = height


def inorder_keys(root) -> list[int]:
    raise NotImplementedError


def bst_contains(root, target) -> bool:
    raise NotImplementedError


def bst_insert(root, key):
    raise NotImplementedError


def bst_height(root) -> int:
    raise NotImplementedError


def is_valid_bst(root) -> bool:
    raise NotImplementedError


def rotate_left(root):
    raise NotImplementedError


def rotate_right(root):
    raise NotImplementedError


def avl_insert(root, key):
    raise NotImplementedError
