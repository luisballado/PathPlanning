import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# === SETTINGS ===
n_takeoff = 50
n_helix = 300
total_frames = n_takeoff + n_helix

# === TAKEOFF: strictly vertical in Z ===
z_takeoff = np.linspace(0, 0.5, n_takeoff)
takeoff_points = np.vstack([np.zeros(n_takeoff), np.zeros(n_takeoff), z_takeoff]).T

# === DYNAMIC HELIX ===
turns = 2
theta = np.linspace(0, 2 * np.pi * turns, n_helix)
radius = 0.5 + 0.2 * np.sin(2 * theta)           # variable radius
height = 1.5 + 0.5 * np.cos(1 * theta)           # variable height

x_helix = radius * np.cos(theta)
y_helix = radius * np.sin(theta)
z_helix = height * theta / (2 * np.pi * turns)

helix_points = np.vstack([x_helix, y_helix, z_helix]).T

# === ROTATE helix only (45° around X) ===
angle = np.deg2rad(45)
Rx = np.array([
    [1, 0, 0],
    [0, np.cos(angle), -np.sin(angle)],
    [0, np.sin(angle),  np.cos(angle)]
])
helix_points = helix_points @ Rx.T

# === SHIFT helix to start where takeoff ends ===
offset = takeoff_points[-1] - helix_points[0]
helix_points += offset

# === CONCATENATE final trajectory ===
trajectory_points = np.vstack([takeoff_points, helix_points])
directions = np.gradient(trajectory_points, axis=0)
directions = np.array([v / np.linalg.norm(v) for v in directions])

# === PLOT SETUP ===
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def draw_quadrotor(ax, R, pos, arm_length=0.2):
    # Offset de rotores en marco cuerpo
    d = arm_length / np.sqrt(2)
    offsets = np.array([
        [ d,  d, 0],
        [-d,  d, 0],
        [-d, -d, 0],
        [ d, -d, 0]
    ])

    # Transformar a mundo
    rotor_positions = [pos + R @ offset for offset in offsets]

    # Dibujar brazos
    for rotor_pos in rotor_positions:
        ax.plot([pos[0], rotor_pos[0]],
                [pos[1], rotor_pos[1]],
                [pos[2], rotor_pos[2]],
                color='k', linewidth=2)

    # Dibujar rotores
    for rotor_pos in rotor_positions:
        ax.scatter(*rotor_pos, color='red', s=30)


def draw_basis(ax, R, pos, length=0.2):
    colors = ['r', 'g', 'b']
    for i in range(3):
        axis = R[:, i] * length
        ax.quiver(*pos, *axis, color=colors[i], linewidth=2)

def draw_fov(ax, origin, direction, angle=np.pi/12, length=0.4):
    direction = direction / np.linalg.norm(direction)
    up = np.array([0.0, 0.0, 1.0]) if abs(direction[2]) < 0.95 else np.array([0.0, 1.0, 0.0])
    right = np.cross(direction, up)
    up = np.cross(right, direction)
    right /= np.linalg.norm(right)
    up /= np.linalg.norm(up)

    for t in np.linspace(-angle, angle, 4):
        for p in np.linspace(-angle, angle, 4):
            offset = direction + np.tan(t) * right + np.tan(p) * up
            offset = offset / np.linalg.norm(offset) * length
            ax.plot(
                [origin[0], origin[0] + offset[0]],
                [origin[1], origin[1] + offset[1]],
                [origin[2], origin[2] + offset[2]],
                color='orange', alpha=0.5
            )

def update(i):
    ax.cla()
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(0, 2.5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Quadrotor Takeoff + Tilted Helix + FOV")

    # Path and inertial frame
    ax.plot(*trajectory_points.T, 'gray', linestyle='--', linewidth=1)
    draw_basis(ax, np.eye(3), np.zeros(3), length=0.3)

    # Position & orientation of drone
    pos = trajectory_points[i]

    if i < n_takeoff:
        # Durante el takeoff: frame alineado con mundo
        R = np.eye(3)
        x_axis = np.array([1.0, 0.0, 0.0])

    else:
        # Luego del takeoff: orientar con dirección de trayectoria
        x_axis = directions[i]
        up_ref = np.array([0.0, 0.0, 1.0])
        y_axis = np.cross(up_ref, x_axis)
        if np.linalg.norm(y_axis) < 1e-3:
            y_axis = np.array([0.0, 1.0, 0.0])
        y_axis = y_axis / np.linalg.norm(y_axis)
        z_axis = np.cross(x_axis, y_axis)
        R = np.vstack((x_axis, y_axis, z_axis)).T
            

    draw_quadrotor(ax,R,pos)
    draw_basis(ax, R, pos)
    draw_fov(ax, pos, x_axis)
    ax.scatter(*pos, color='black', s=40)

    # === IMPRIMIR INFORMACIÓN DEL SISTEMA MÓVIL ===
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = pos
    
    np.set_printoptions(precision=3, suppress=True)
    print(f"\nFrame {i + 1}/{total_frames}")
    print("Posición del sistema móvil (en mundo):")
    print(pos)
    print("Rotación (matriz R del móvil al inercial):")
    print(R)
    print("Transformación homogénea T (móvil al inercial):")
    print(T)

# === ANIMATE ===
ani = FuncAnimation(fig, update, frames=total_frames, interval=50, repeat=True)
plt.show()

