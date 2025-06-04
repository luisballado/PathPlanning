import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from scipy.interpolate import make_interp_spline

# ----- PUNTOS DE CONTROL -----
control_points = np.array([
    [0, 10, 2],
    [2, 9, 2.5],
    [4, 8, 3],
    [6, 7, 2.5],
    [8, 6, 2],
    [10, 5, 2]
])

# ----- CREAR CURVA B-SPLINE -----
num_points = 200
t = np.linspace(0, 1, len(control_points))
spline = make_interp_spline(t, control_points, k=3)
t_fine = np.linspace(0, 1, num_points)
spline_points = spline(t_fine)

# ----- CONFIGURACIÓN DE LA FIGURA -----
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Animación del Vuelo de un VANT en Trayectoria B-Spline")

# Dibujar trayectoria
ax.plot(spline_points[:, 0], spline_points[:, 1], spline_points[:, 2], 'r-', label='Trayectoria B-Spline')
ax.plot(control_points[:, 0], control_points[:, 1], control_points[:, 2], 'bo--', label='Puntos de control')
ax.scatter(*control_points[0], color='green', s=100, label='Inicio')
ax.scatter(*control_points[-1], color='black', s=100, label='Fin')

# Crear marcador del dron
drone_marker, = ax.plot([], [], [], 'ro', markersize=10, label='VANT')

# Limites del espacio
ax.set_xlim(0, 12)
ax.set_ylim(4, 12)
ax.set_zlim(1, 4)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.view_init(elev=30, azim=135)
ax.legend()

# ----- FUNCIÓN DE ANIMACIÓN -----
def update(frame):
    x, y, z = spline_points[frame]
    drone_marker.set_data([x], [y])
    drone_marker.set_3d_properties([z])
    return drone_marker,

# Crear animación
anim = FuncAnimation(fig, update, frames=len(spline_points), interval=50, blit=True)

plt.tight_layout()
plt.show()
