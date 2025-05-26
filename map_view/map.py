import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import heapq
import itertools
import imageio
import os

# -------------------------------
# Graph Data and Position
# -------------------------------
graph = {
    'Dhaka': [('Barisal', 2), ('Chattogram', 4)],
    'Chattogram': [('Sylhet', 3), ('Dhaka', 4)],
    'Khulna': [('Rajshahi', 5), ('Barisal', 3)],
    'Rajshahi': [('Rangpur', 6), ('Khulna', 5)],
    'Barisal': [('Khulna', 3), ('Dhaka', 2)],
    'Sylhet': [('Chattogram', 3)],
    'Rangpur': [('Rajshahi', 6)]
}

positions = {
    'Dhaka': (0, 0),
    'Barisal': (-1, -1),
    'Chattogram': (2, 2),
    'Sylhet': (3, 3),
    'Khulna': (-2, -1),
    'Rajshahi': (-3, 0),
    'Rangpur': (-4, 1)
}

colors = ['red', 'green', 'blue', 'yellow']
frames = []  # for animation

# -------------------------------
# Utility Functions
# -------------------------------
def draw_graph(state, current_node=None, title=""):
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node]:
            G.add_edge(node, neighbor, weight=weight)

    node_colors = []
    for node in G.nodes():
        if node == current_node:
            node_colors.append('gold')
        elif node in state:
            node_colors.append(state[node])
        else:
            node_colors.append('lightgray')

    plt.clf()
    nx.draw(G, positions, with_labels=True, node_color=node_colors, node_size=1600,
            font_size=10, font_weight='bold', edge_color='gray')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, positions, edge_labels=labels)
    plt.title(title)

    filename = f"frame_{len(frames)}.png"
    plt.savefig(filename)
    frames.append(filename)

# -------------------------------
# Algorithms
# -------------------------------
def is_valid(state, node, color):
    for neighbor, _ in graph.get(node, []):
        if neighbor in state and state[neighbor] == color:
            return False
    return True

def backtracking_coloring(state):
    if len(state) == 0:
        state['Rangpur'] = 'yellow'
        draw_graph(state, current_node='Rangpur', title="Backtracking")

    if len(state) == len(graph):
        return state

    uncolored = [n for n in graph if n not in state]
    node = uncolored[0]
    for color in colors:
        if node == 'Rangpur' and color != 'yellow':
            continue
        if is_valid(state, node, color):
            state[node] = color
            draw_graph(state, current_node=node, title="Backtracking")
            result = backtracking_coloring(state)
            if result:
                return result
            del state[node]
    return None

def dijkstra(start):
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node]:
            G.add_edge(node, neighbor, weight=weight)

    path = nx.single_source_dijkstra_path(G, start)
    dist = nx.single_source_dijkstra_path_length(G, start)

    for target in path:
        draw_graph({}, current_node=target, title=f"Dijkstra path to {target}")
    return path, dist

# -------------------------------
# GUI and Animation
# -------------------------------
def save_gif():
    images = [imageio.imread(f) for f in frames]
    imageio.mimsave("map_coloring.gif", images, fps=1)
    for f in frames:
        os.remove(f)

def run_backtracking():
    frames.clear()
    state = backtracking_coloring({})
    result_text.set("Backtracking Result:\n" + "\n".join([f"{k}: {v}" for k, v in state.items()]))
    save_gif()

def run_dijkstra():
    frames.clear()
    path, dist = dijkstra('Rangpur')
    lines = [f"{dest}: {dist[dest]} units" for dest in dist]
    result_text.set("Dijkstra Distance from Rangpur:\n" + "\n".join(lines))
    save_gif()

# -------------------------------
# Tkinter GUI Setup
# -------------------------------
root = tk.Tk()
root.title("Bangladesh Map Coloring & Pathfinding")

frame = ttk.Frame(root, padding=20)
frame.grid()

ttk.Label(frame, text="Select Algorithm:").grid(row=0, column=0, pady=5)
ttk.Button(frame, text="Backtracking Coloring", command=run_backtracking).grid(row=1, column=0, pady=5)
ttk.Button(frame, text="Dijkstra Pathfinding", command=run_dijkstra).grid(row=2, column=0, pady=5)

result_text = tk.StringVar()
result_label = ttk.Label(frame, textvariable=result_text, justify="left")
result_label.grid(row=3, column=0, pady=10)

root.mainloop()

