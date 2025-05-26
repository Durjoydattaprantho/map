import networkx as nx
import matplotlib.pyplot as plt
import heapq
import itertools
from collections import deque

# Node names
nodes = [ 'Dhaka','Chattogram', 'Rajshahi', 'Barishal', 'Khulna', 'Rangpur', 'Mymensingh', 'Sylhet']
n = len(nodes)

# Adjacency Matrix
adj_matrix = [
    [0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1],
    [0, 1, 1, 0, 0, 0, 1, 0]
]

colors = ['red', 'green', 'blue', 'yellow']

# Position for plotting
pos = {
    'Dhaka': (0, 0),
    'Barishal': (-1, -1),
    'Chattogram': (2, -1),
    'Khulna': (-2, -2),
    'Rajshahi': (-3, 0),
    'Rangpur': (-3, 2),
    'Mymensingh': (1, 1),
    'Sylhet': (3, 1)
}

def get_neighbors(index):
    return [i for i in range(n) if adj_matrix[index][i] == 1]

def is_valid(state, node_index, color):
    for neighbor_index in get_neighbors(node_index):
        if neighbor_index in state and state[neighbor_index] == color:
            return False
    return True

def plot_graph(state, current_node=None, title="Map Coloring"):
    G = nx.Graph()
    for i in range(n):
        G.add_node(nodes[i])
    for i in range(n):
        for j in range(i+1, n):
            if adj_matrix[i][j] == 1:
                G.add_edge(nodes[i], nodes[j])

    node_colors = []
    for i in range(n):
        if i == current_node:
            node_colors.append('gold')
        elif i in state:
            node_colors.append(state[i])
        else:
            node_colors.append('lightgray')

    plt.clf()
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1600,
            font_size=10, font_weight='bold', edge_color='gray')
    plt.title(title)
    plt.pause(0.5)

def backtracking_coloring(state):
    if len(state) == 0:
        state[5] = 'yellow'  # Rangpur fixed
        plot_graph(state, current_node=5, title="Backtracking")

    if len(state) == n:
        return state

    uncolored = [i for i in range(n) if i not in state]
    node = uncolored[0]
    for color in colors:
        if node == 5 and color != 'yellow':
            continue
        if is_valid(state, node, color):
            state[node] = color
            plot_graph(state, current_node=node, title="Backtracking")
            result = backtracking_coloring(state)
            if result:
                return result
            del state[node]
    return None

def bfs_coloring():
    state = {}
    queue = deque()
    state[5] = 'yellow'
    queue.append(5)
    plot_graph(state, current_node=5, title="BFS")

    while queue:
        node = queue.popleft()
        for neighbor in get_neighbors(node):
            if neighbor not in state:
                for color in colors:
                    if neighbor == 5 and color != 'yellow':
                        continue
                    if is_valid(state, neighbor, color):
                        state[neighbor] = color
                        plot_graph(state, current_node=neighbor, title="BFS")
                        queue.append(neighbor)
                        break
    return state

def ucs_coloring():
    queue = []
    counter = itertools.count()
    start_state = {5: 'yellow'}
    heapq.heappush(queue, (0, next(counter), start_state))

    step = 0
    while queue:
        cost, _, state = heapq.heappop(queue)
        if len(state) == n:
            return state

        uncolored = [i for i in range(n) if i not in state]
        if not uncolored:
            continue

        node = uncolored[0]
        for color in colors:
            if node == 5 and color != 'yellow':
                continue
            if is_valid(state, node, color):
                new_state = state.copy()
                new_state[node] = color
                step += 1
                if step % 4 == 0:
                    plot_graph(new_state, current_node=node, title="UCS")
                heapq.heappush(queue, (cost + 1, next(counter), new_state))
    return None

def print_coloring(state, name):
    print(f"\n{name} Coloring Result:")
    for i in range(n):
        print(f"{nodes[i]}: {state.get(i, 'Uncolored')}")

if __name__ == "__main__":
    plt.ion()
    plt.figure(figsize=(10, 8))

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
