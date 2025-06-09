import matplotlib.pyplot as plt
import numpy as np
import heapq
import time

# Configuración de la cuadrícula
grid_size = 6
grid = np.zeros((grid_size, grid_size))
start = (5, 0)
goal = (0, 5)
obstacles = [(2, 2), (2, 3), (3, 2), (3, 3)]
for ox, oy in obstacles:
    grid[ox, oy] = -1

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

# Algoritmo D* Lite simplificado
def d_star_step_by_step(grid, start, goal, ax, pause=0.5):
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(goal, start), 0, goal))
    came_from = {}
    cost_so_far = {goal: 0}
    visited = set()

    while open_list:
        _, cost, current = heapq.heappop(open_list)

        if current == start:
            break

        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(current, grid):
            new_cost = cost + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(start, neighbor)
                heapq.heappush(open_list, (priority, new_cost, neighbor))
                came_from[neighbor] = current

        # Visualización parcial
        draw_grid(ax, grid, start, goal, came_from)
        plt.pause(pause)

    path = []
    current = start
    while current != goal:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []
    path.append(goal)
    return path

# Dibujo de la cuadrícula con el camino parcial
def draw_grid(ax, grid, start, goal, came_from):
    ax.clear()
    for x in range(grid_size):
        for y in range(grid_size):
            if (x, y) == start:
                ax.text(y, x, 'S', va='center', ha='center', fontsize=12, fontweight='bold')
            elif (x, y) == goal:
                ax.text(y, x, 'G', va='center', ha='center', fontsize=12, fontweight='bold')
            elif grid[x, y] == -1:
                ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='black'))

    for node in came_from:
        x, y = node
        ax.add_patch(plt.Circle((y, x), 0.2, color='skyblue', alpha=0.5))

    ax.set_xticks(np.arange(-0.5, grid_size, 1))
    ax.set_yticks(np.arange(-0.5, grid_size, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(grid_size - 0.5, -0.5)
    ax.set_title("D* paso a paso")

# Visualización inicial
fig, ax = plt.subplots()
plt.ion()
draw_grid(ax, grid, start, goal, {})
plt.pause(1)

# Simulación del primer camino
path1 = d_star_step_by_step(grid, start, goal, ax)

# Agregar un nuevo obstáculo
time.sleep(1)
new_obstacle = (4, 1)
grid[new_obstacle] = -1
ax.add_patch(plt.Rectangle((new_obstacle[1] - 0.5, new_obstacle[0] - 0.5), 1, 1, color='black'))
ax.set_title("Nuevo obstáculo descubierto")
plt.pause(1)

# Simulación del camino adaptado
path2 = d_star_step_by_step(grid, start, goal, ax)
plt.ioff()
plt.show()
