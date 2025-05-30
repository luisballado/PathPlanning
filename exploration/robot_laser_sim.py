import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import heapq
import math
import os
import random

# Funciones reutilizadas (copiadas aquí por reinicio de kernel)
def simulate_laser(mapa, rx, ry, max_range=5, step_angle=5):
    for angle in range(0, 360, step_angle):
        rad = math.radians(angle)
        for r in range(1, max_range):
            x = int(rx + r * math.cos(rad))
            y = int(ry + r * math.sin(rad))
            if 0 <= x < mapa.shape[1] and 0 <= y < mapa.shape[0]:
                if mapa[y, x] == 2:
                    break
                if mapa[y, x] == 0:
                    mapa[y, x] = 1
            else:
                break

def find_frontiers(mapa):
    frontiers = []
    for y in range(1, mapa.shape[0] - 1):
        for x in range(1, mapa.shape[1] - 1):
            if mapa[y, x] == 1:
                neighbors = [(x + dx, y + dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]]
                if any(mapa[ny, nx] == 0 for nx, ny in neighbors):
                    frontiers.append((x, y))
    return frontiers

def astar(mapa, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: math.dist(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        x, y = current
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < mapa.shape[1] and 0 <= ny < mapa.shape[0] and mapa[ny, nx] in [0, 1]:
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + math.dist(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []

grid_size = 60
# Reinicializar mapa y robots
mapa = np.zeros((grid_size, grid_size), dtype=int)

obstaculos = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (0, 1), (14, 1), (15, 1), (16, 1), (18, 1), (0, 2), (2, 2), (3, 2), (4, 2), (6, 2), (7, 2), (8, 2), (10, 2), (11, 2), (12, 2), (14, 2), (15, 2), (16, 2), (18, 2), (0, 3), (2, 3), (3, 3), (4, 3), (6, 3), (7, 3), (8, 3), (10, 3), (11, 3), (12, 3), (18, 3), (0, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (10, 4), (11, 4), (12, 4), (14, 4), (15, 4), (16, 4), (18, 4), (0, 5), (4, 5), (5, 5), (6, 5), (10, 5), (11, 5), (12, 5), (14, 5), (15, 5), (16, 5), (18, 5), (0, 6), (1, 6), (2, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (10, 6), (11, 6), (12, 6), (14, 6), (15, 6), (16, 6), (17, 6), (18, 6), (0, 7), (1, 7), (2, 7), (6, 7), (7, 7), (8, 7), (10, 7), (11, 7), (12, 7)]

for obs_x,obs_y in obstaculos:
    mapa[obs_x, obs_y] = 2

robots = [(5, 2), (8, 2), (25, 2)]
paths = [[] for _ in robots]

# Crear carpeta temporal para imágenes si no existe
output_folder = "data/simulation_steps"
os.makedirs(output_folder, exist_ok=True)

# Simulación iterativa con visualización cada 10 pasos
step = 0
max_steps = 100
image_paths = []
frames = []

while step < max_steps:
    step += 1
    for idx, (rx, ry) in enumerate(robots):
        simulate_laser(mapa, rx, ry)

    frontiers = find_frontiers(mapa)
    if not frontiers:
        break

    new_robots = []
    for idx, (rx, ry) in enumerate(robots):

        if not frontiers:
            new_robots.append((rx, ry))
            continue
        
        closest = min(frontiers, key=lambda f: math.dist((rx, ry), f))
        path = astar(mapa, (rx, ry), closest)
        if len(path) > 1:
            next_step = path[1]
        else:
            next_step = (rx, ry)
        new_robots.append(next_step)
        paths[idx].append(next_step)
        if next_step in frontiers:
            frontiers.remove(next_step)
    robots = new_robots
    current_frame = (mapa.copy(), list(robots), paths)
    frames.append(current_frame)


fig, ax = plt.subplots(figsize(6,6))
    
def update(frame_data):
    ax.clear()
    mapa, robots, paths = frame_data
    ax.imshow(mapa, cmap='gray_r')
    colors = ['red', 'blue', 'green']
    for idx, path in enumerate(paths):
        if path:
            xs, ys = zip(*path)
            ax.plot(xs, ys, color=colors[idx], label=f'Robot {idx+1}')
    for idx, (x, y) in enumerate(robots):
        ax.plot(x, y, 'o', color=colors[idx])

    # Dibujar fronteras en color magenta
    frontiers = find_frontiers(mapa)
    for fx, fy in frontiers:
        ax.plot(fx, fy, 's', color='magenta', markersize=5)
            
    ax.set_title(f"Paso {step}")
    ax.axis('off');

ani = animation.FuncAnimation(fig, update, frames=frames, interval=300, repeat=False)
        #ax.legend()
        #plt.axis('off')
        #filename = f"{output_folder}/step_{step:03d}.png"
        #plt.savefig(filename)
plt.close()
        #image_paths.append(filename)


# Guardar animación como archivo .mp4
video_path = "exploracion_multi_robot.mp4"
ani.save(video_path, writer='ffmpeg', fps=2)


