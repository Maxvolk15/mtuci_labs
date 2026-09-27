class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    return root


def search(root, key):
    current = root
    visited = 0
    while current is not None:
        visited += 1
        if key == current.key:
            return current, visited
        if key < current.key:
            current = current.left
        else:
            current = current.right
    return None, visited


def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.key] + inorder(node.right)


def preorder(node):
    if node is None:
        return []
    return [node.key] + preorder(node.left) + preorder(node.right)


def postorder(node):
    if node is None:
        return []
    return postorder(node.left) + postorder(node.right) + [node.key]


def _find_min(node):
    while node.left is not None:
        node = node.left
    return node


def delete(root, key):
    if root is None:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        successor = _find_min(root.right)
        root.key = successor.key
        root.right = delete(root.right, successor.key)
    return root


def height(node):
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))
