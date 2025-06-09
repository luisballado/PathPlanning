# Reimportar y reconfigurar después del reinicio del entorno

import matplotlib.pyplot as plt
import numpy as np
import heapq
from matplotlib.widgets import Button

# Parámetros de la cuadrícula
grid_size = 10
grid = np.zeros((grid_size, grid_size))
start = (9, 0)
goal = (0, 9)
obstacles = []

# Heurística Manhattan
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Vecinos válidos
def get_neighbors(node, grid):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for d in directions:
        nx, ny = node[0] + d[0], node[1] + d[1]
        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
            if grid[nx, ny] != -1:
                neighbors.append((nx, ny))
    return neighbors

# Algoritmo A* inverso (versión simplificada de D*)
def d_star(grid, start, goal):
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(goal, start), 0, goal))
    came_from = {}
    cost_so_far = {goal: 0}

    while open_list:
        _, cost, current = heapq.heappop(open_list)

        if current == start:
            break

        for neighbor in get_neighbors(current, grid):
            new_cost = cost + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(start, neighbor)
                heapq.heappush(open_list, (priority, new_cost, neighbor))
                came_from[neighbor] = current

    path = []
    current = start
    while current != goal:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []
    path.append(goal)
    return path

# Visualización del grid
def draw_grid():
    ax.clear()
    for x in range(grid_size):
        for y in range(grid_size):
            if (x, y) == start:
                ax.text(y, x, 'S', va='center', ha='center', fontsize=12, fontweight='bold', color='blue')
            elif (x, y) == goal:
                ax.text(y, x, 'G', va='center', ha='center', fontsize=12, fontweight='bold', color='green')
            elif grid[x, y] == -1:
                ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='black'))

    path = d_star(grid, start, goal)
    for (x, y) in path:
        ax.add_patch(plt.Circle((y, x), 0.2, color='orange', alpha=0.5))

    ax.set_xticks(np.arange(-0.5, grid_size, 1))
    ax.set_yticks(np.arange(-0.5, grid_size, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(grid_size - 0.5, -0.5)
    ax.set_title("Haz clic para agregar obstáculos. Ruta = naranja")
    fig.canvas.draw()

# Evento de clic para agregar obstáculos
def onclick(event):
    if event.inaxes != ax:
        return
    col, row = int(round(event.xdata)), int(round(event.ydata))
    if 0 <= row < grid_size and 0 <= col < grid_size:
        if (row, col) not in [start, goal] and grid[row, col] != -1:
            grid[row, col] = -1
            obstacles.append((row, col))
            draw_grid()

# Crear figura interactiva
fig, ax = plt.subplots()
draw_grid()
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
