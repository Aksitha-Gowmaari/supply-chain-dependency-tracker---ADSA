class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def insert(root, data):
    if root is None:
        return Node(data)

    if data < root.data:
        root.left = insert(root.left, data)
    else:
        root.right = insert(root.right, data)

    return root

def inorder(root):
    if root is not None:
        inorder(root.left)
        print(root.data, end=" ")
        inorder(root.right)

def preorder(root):
    if root is not None:
        print(root.data, end=" ")
        preorder(root.left)
        preorder(root.right)

def postorder(root):
    if root is not None:
        postorder(root.left)
        postorder(root.right)
        print(root.data, end=" ")

n = int(input())
arr = list(map(int, input().split()))

root = None

for i in range(n):
    root = insert(root, arr[i])

print("Inorder:", end=" ")
inorder(root)
print()

print("Preorder:", end=" ")
preorder(root)
print()

print("Postorder:", end=" ")
postorder(root)
print()