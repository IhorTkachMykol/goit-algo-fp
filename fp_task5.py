import uuid
import networkx as nx
import matplotlib.pyplot as plt

from collections import deque


# -------------------------------------------------
# Клас вузла
# -------------------------------------------------
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.color = "#1E1E1E"
        self.id = str(uuid.uuid4())


# -------------------------------------------------
# Побудова дерева з масиву (бінарна купа)
# -------------------------------------------------
def build_tree(heap, index=0):

    if index >= len(heap):
        return None

    node = Node(heap[index])

    node.left = build_tree(heap, 2 * index + 1)
    node.right = build_tree(heap, 2 * index + 2)

    return node


# -------------------------------------------------
# Генерація кольору
# Від темного до світлого
# -------------------------------------------------
def generate_color(step, total_steps):

    intensity = int(255 * (step / total_steps))

    return f'#{intensity:02X}{150:02X}{240:02X}'


# -------------------------------------------------
# Додавання вузлів у граф
# -------------------------------------------------
def add_edges(graph, node, pos, x=0, y=0, layer=1):

    if node is not None:

        graph.add_node(
            node.id,
            color=node.color,
            label=node.val
        )

        if node.left:

            graph.add_edge(node.id, node.left.id)

            l = x - 1 / 2 ** layer

            pos[node.left.id] = (l, y - 1)

            add_edges(
                graph,
                node.left,
                pos,
                x=l,
                y=y - 1,
                layer=layer + 1
            )

        if node.right:

            graph.add_edge(node.id, node.right.id)

            r = x + 1 / 2 ** layer

            pos[node.right.id] = (r, y - 1)

            add_edges(
                graph,
                node.right,
                pos,
                x=r,
                y=y - 1,
                layer=layer + 1
            )

    return graph


# -------------------------------------------------
# Візуалізація дерева
# -------------------------------------------------
def draw_tree(tree_root, title="Tree Traversal"):

    tree = nx.DiGraph()

    pos = {tree_root.id: (0, 0)}

    tree = add_edges(tree, tree_root, pos)

    colors = [
        node[1]['color']
        for node in tree.nodes(data=True)
    ]

    labels = {
        node[0]: node[1]['label']
        for node in tree.nodes(data=True)
    }

    plt.figure(figsize=(10, 6))

    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2500,
        node_color=colors
    )

    plt.title(title)

    plt.show()


# -------------------------------------------------
# DFS — обхід у глибину (СТЕК)
# -------------------------------------------------
def dfs_iterative(root):

    stack = [root]

    visited_order = []

    while stack:

        node = stack.pop()

        if node:

            visited_order.append(node)

            # Правий додаємо першим,
            # щоб лівий оброблявся першим
            stack.append(node.right)
            stack.append(node.left)

    return visited_order


# -------------------------------------------------
# BFS — обхід у ширину (ЧЕРГА)
# -------------------------------------------------
def bfs_iterative(root):

    queue = deque([root])

    visited_order = []

    while queue:

        node = queue.popleft()

        if node:

            visited_order.append(node)

            queue.append(node.left)
            queue.append(node.right)

    return visited_order


# -------------------------------------------------
# Фарбування вузлів
# -------------------------------------------------
def color_nodes(order):

    total = len(order)

    for i, node in enumerate(order):

        node.color = generate_color(i + 1, total)


# -------------------------------------------------
# Дані дерева
# -------------------------------------------------
heap = [10, 5, 15, 3, 7, 12, 18]

root = build_tree(heap)


# -------------------------------------------------
# DFS
# -------------------------------------------------
dfs_order = dfs_iterative(root)

color_nodes(dfs_order)

draw_tree(root, "DFS Traversal")


# -------------------------------------------------
# Скидання кольорів
# -------------------------------------------------
for node in dfs_order:
    node.color = "#1E1E1E"


# -------------------------------------------------
# BFS
# -------------------------------------------------
bfs_order = bfs_iterative(root)

color_nodes(bfs_order)

draw_tree(root, "BFS Traversal")
