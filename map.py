import networkx as nx
from collections import deque
import heapq
import itertools
import matplotlib.pyplot as plt


# গ্রাফ ডেটা
graph = {
    'Dhaka': ['Barisal', 'Chattogram'],
    'Chattogram': ['Sylhet', 'Dhaka'],
    'Khulna': ['Rajshahi', 'Barisal'],
    'Rajshahi': ['Rangpur', 'Khulna'],
    'Barisal': ['Khulna', 'Dhaka'],
    'Sylhet': ['Chattogram'],
    'Rangpur': ['Rajshahi']
}

colors = ['red', 'green', 'blue', 'yellow']

# ভিজ্যুয়াল অবস্থান (বাংলাদেশের মতো)
pos = {
    'Dhaka': (0, 0),
    'Barisal': (-1, -1),
    'Chattogram': (2, 2),
    'Sylhet': (3, 3),
    'Khulna': (-2, -1),
    'Rajshahi': (-3, 0),
    'Rangpur': (-4, 1)
}

# কমন plot ফাংশন
def plot_graph(state, current_node=None, title="Map Coloring"):
    G = nx.Graph()
    for node in graph:
        G.add_node(node)
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    node_colors = []
    for node in G.nodes():
        if node == current_node:
            node_colors.append('gold')
        elif node in state:
            node_colors.append(state[node])
        else:
            node_colors.append('lightgray')

    plt.clf()
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1600,
            font_size=10, font_weight='bold', edge_color='gray')
    plt.title(title)
    plt.pause(0.5)

# রঙ বৈধ কি না যাচাই
def is_valid(state, node, color):
    for neighbor in graph.get(node, []):
        if neighbor in state and state[neighbor] == color:
            return False
    return True

# ব্যাকট্র্যাকিং এলগরিদম
def backtracking_coloring(state):
    if len(state) == 0:
        state['Rangpur'] = 'yellow'
        plot_graph(state, current_node='Rangpur', title="Backtracking")

    if len(state) == len(graph):
        return state

    uncolored = [node for node in graph if node not in state]
    node = uncolored[0]
    for color in colors:
        if node == 'Rangpur' and color != 'yellow':
            continue
        if is_valid(state, node, color):
            state[node] = color
            plot_graph(state, current_node=node, title="Backtracking")
            result = backtracking_coloring(state)
            if result:
                return result
            del state[node]
    return None

# BFS এলগরিদম
def bfs_coloring():
    state = {}
    queue = deque()
    state['Rangpur'] = 'yellow'
    queue.append('Rangpur')
    plot_graph(state, current_node='Rangpur', title="BFS")

    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in state:
                for color in colors:
                    if neighbor == 'Rangpur' and color != 'yellow':
                        continue
                    if is_valid(state, neighbor, color):
                        state[neighbor] = color
                        plot_graph(state, current_node=neighbor, title="BFS")
                        queue.append(neighbor)
                        break
    return state

# UCS এলগরিদম
def ucs_coloring():
    queue = []
    counter = itertools.count()
    start_state = {'Rangpur': 'yellow'}
    heapq.heappush(queue, (0, next(counter), start_state))

    step = 0
    while queue:
        cost, _, state = heapq.heappop(queue)
        if len(state) == len(graph):
            return state

        uncolored = [node for node in graph if node not in state]
        if not uncolored:
            continue

        node = uncolored[0]
        for color in colors:
            if node == 'Rangpur' and color != 'yellow':
                continue
            if is_valid(state, node, color):
                new_state = state.copy()
                new_state[node] = color
                step += 1
                if step % 5 == 0:
                    plot_graph(new_state, current_node=node, title="UCS")
                heapq.heappush(queue, (cost + 1, next(counter), new_state))
    return None

# প্রিন্ট ফাংশন
def print_coloring(state, algorithm_name):
    print(f"\n{algorithm_name} Coloring Result:")
    for division, color in state.items():
        print(f"{division}: {color}")
    print()

# মেইন ফাংশন
if __name__ == "__main__":
    plt.ion()
    plt.figure(figsize=(8,6))

    print("Running Backtracking...\n")
    result = backtracking_coloring({})
    print_coloring(result, "Backtracking")

    print("Running BFS...\n")
    result = bfs_coloring()
    print_coloring(result, "BFS")

    print("Running UCS...\n")
    result = ucs_coloring()
    print_coloring(result, "UCS")

    plt.ioff()
    plt.show()
