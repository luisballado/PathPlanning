import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import heapq
import math

from scipy.interpolate import splprep, splev



# Parámetros
grid_size = 30
mapa = np.zeros((grid_size, grid_size), dtype=int)

# Obstáculos fijos
mapa[10:15, 20] = 2
mapa[20, 10:15] = 2
mapa[5, 5:10] = 2

# Posiciones iniciales de los robots
robots = [(5, 5), (1, 15), (25, 25)]
paths = [[] for _ in robots]
colors = ['red', 'blue', 'green']

# Funciones auxiliares
def simulate_laser(mapa, rx, ry, max_range=10, step_angle=5):
    endpoints = []
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

def smooth_path(path):
    if len(path) >= 4:
        pts = np.array(path)
        x, y = pts[:, 0], pts[:, 1]
        tck, _ = splprep([x, y], s=0)
        u_fine = np.linspace(0, 1.0, 10)
        return list(zip(*splev(u_fine, tck)))
    else:
        return path

def dividir_fronteras_por_rango(robot_pos, fronteras, rango_laser):
    visibles = []
    ocultas = []
    rx, ry = robot_pos
    for fx, fy in fronteras:
        dist = math.hypot(rx - fx, ry - fy)
        if dist <= rango_laser:
            visibles.append((fx, fy))
        else:
            ocultas.append((fx, fy))
    return visibles, ocultas


def raycast_with_endpoints(mapa, rx, ry, max_range=2, step_angle=5):
    endpoints = []
    for angle in range(0, 360, step_angle):
        rad = math.radians(angle)
        for r in range(1, max_range + 1):
            x = int(rx + r * math.cos(rad))
            y = int(ry + r * math.sin(rad))
            if 0 <= x < mapa.shape[1] and 0 <= y < mapa.shape[0]:
                if mapa[y, x] == 2:
                    endpoints.append((x, y))
                    break
                if r == max_range:
                    endpoints.append((x, y))
            else:
                break
    return endpoints


# Simulación paso a paso
robot_states = [list(p) for p in robots]
frames = []
step = 0
max_steps = 100


while step < max_steps:
    current_frame = (mapa.copy(), list(robot_states), [])
    #sensado
    for idx, (rx, ry) in enumerate(robot_states):
        simulate_laser(mapa, rx, ry)

    frontiers = find_frontiers(mapa)
    if not frontiers:
        break

    paths_this_step = []
    new_positions = []
    for idx, (rx, ry) in enumerate(robot_states):

    #Si es toda la lista sigue ofertando
        fronteras_visibles,fronteras_ocultas = dividir_fronteras_por_rango((rx,ry), frontiers, rango_laser=10)
                
        if not fronteras_visibles:
            new_positions.append((rx, ry))
            continue
        
        closest = min(fronteras_visibles, key=lambda f: math.dist((rx, ry), f))
        
        path = astar(mapa, (rx, ry), closest)
        
        #print(path)
                
        if len(path) > 1:
            next_step = path[1]
        else:
            next_step = (rx, ry)
        new_positions.append(next_step)
        paths[idx].append(next_step)
        paths_this_step.append((idx, path))
        if next_step in frontiers:
            frontiers.remove(next_step)
    robot_states = new_positions
    current_frame = (mapa.copy(), list(robot_states), paths_this_step)
    frames.append(current_frame)

# Crear animación con matplotlib.animation
fig, ax = plt.subplots(figsize=(6, 6))

def update(frame_data):
    ax.clear()
    mapa, robots_pos, paths_step = frame_data
    ax.imshow(mapa, cmap='gray_r')
    for idx, path in paths_step:
        if path:
            xs, ys = zip(*path)
            ax.plot(xs, ys, color=colors[idx])
    for idx, (x, y) in enumerate(robots_pos):
        endpoints = raycast_with_endpoints(mapa, x, y, max_range=10)
        for ex, ey in endpoints:
            ax.plot([x, ex], [y, ey], color=colors[idx], alpha=0.2, linewidth=0.8)
        ax.plot(x, y, 'o', color=colors[idx])


    # Dibujar fronteras en color magenta
    frontiers = find_frontiers(mapa)
    for fx, fy in frontiers:
        ax.plot(fx, fy, 's', color='magenta', markersize=9)
        
    ax.set_title("Exploración Multi-Robot")
    ax.axis('off')

ani = animation.FuncAnimation(fig, update, frames=frames, interval=300, repeat=False)
plt.close()  # no mostrar imagen estática

# Guardar animación como archivo .mp4
video_path = "exploracion_multi_robot.mp4"
ani.save(video_path, writer='ffmpeg', fps=2)
