# Reimportar y ejecutar desde cero tras el reinicio del entorno
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.interpolate import splprep, splev

# Crear puntos de control en forma de S
control_points = [(2, 2), (5, 10), (2, 18), (5, 25)]
x, y = zip(*control_points)
tck, _ = splprep([x, y], s=0)
u_fine = np.linspace(0, 1, 100)
spline_path = list(zip(*splev(u_fine, tck)))

# Parámetros del UAV
dt = 0.1
x_uav, y_uav, theta = 2.0, 2.0, 0.0

# Controlador tipo "carro" no holonómico (proporcional)
def step_controller(target, current_pos, theta):
    k_v = 1.0
    k_w = 2.0
    tx, ty = target
    cx, cy = current_pos
    dx = tx - cx
    dy = ty - cy
    distance = np.hypot(dx, dy)
    angle_to_target = np.arctan2(dy, dx)
    angle_error = np.arctan2(np.sin(angle_to_target - theta), np.cos(angle_to_target - theta))

    v = k_v * distance
    omega = k_w * angle_error
    return v, omega

# Simulación del seguimiento
positions = []
headings = []
uav_pos = (x_uav, y_uav, theta)
for target in spline_path:
    v, omega = step_controller(target, (uav_pos[0], uav_pos[1]), uav_pos[2])
    x_new = uav_pos[0] + v * np.cos(uav_pos[2]) * dt
    y_new = uav_pos[1] + v * np.sin(uav_pos[2]) * dt
    theta_new = uav_pos[2] + omega * dt
    uav_pos = (x_new, y_new, theta_new)
    positions.append((x_new, y_new))
    headings.append(theta_new)

# Función para dibujar FOV (triángulo)
def draw_fov(ax, x, y, theta, fov_angle=60, range_view=5):
    left_angle = theta - np.radians(fov_angle/2)
    right_angle = theta + np.radians(fov_angle/2)
    left = (x + range_view * np.cos(left_angle), y + range_view * np.sin(left_angle))
    right = (x + range_view * np.cos(right_angle), y + range_view * np.sin(right_angle))
    ax.plot([x, left[0]], [y, left[1]], 'c--', alpha=0.4)
    ax.plot([x, right[0]], [y, right[1]], 'c--', alpha=0.4)
    ax.fill([x, left[0], right[0]], [y, left[1], right[1]], 'cyan', alpha=0.2)

# Animación
fig, ax = plt.subplots(figsize=(6, 6))

def update(i):
    ax.clear()
    # Dibujar spline
    xs, ys = zip(*spline_path)
    ax.plot(xs, ys, 'k--', label='Trayectoria B-spline')

    # Dibujar UAV y FOV
    if i < len(positions):
        ux, uy = positions[i]
        heading = headings[i]
        ax.plot(ux, uy, 'ro', label='UAV')
        draw_fov(ax, ux, uy, heading, fov_angle=60, range_view=5)

        # Trayectoria seguida hasta el momento
        traj_x, traj_y = zip(*positions[:i+1])
        ax.plot(traj_x, traj_y, 'r-', alpha=0.6)

    ax.set_xlim(0, 30)
    ax.set_ylim(0, 30)
    ax.set_aspect('equal')
    ax.set_title("UAV siguiendo B-spline con FOV de cámara")
    ax.legend()
    ax.grid(True)

ani = animation.FuncAnimation(fig, update, frames=len(positions), interval=100, repeat=False)
plt.close()

# Guardar animación
video_path = "uav_con_fov.mp4"
ani.save(video_path, writer='ffmpeg', fps=10)

video_path
