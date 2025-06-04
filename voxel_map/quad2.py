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

# ----- CURVA B-SPLINE -----
num_points = 200
t = np.linspace(0, 1, len(control_points))
spline = make_interp_spline(t, control_points, k=3)
spline_points = spline(np.linspace(0, 1, num_points))

# Derivada para orientación (tangente)
spline_deriv = spline.derivative()
tangents = spline_deriv(np.linspace(0, 1, num_points))
tangents /= np.linalg.norm(tangents, axis=1)[:, np.newaxis]  # normalizar

# Crear ejes ortogonales (x_b, y_b, z_b) para cada punto
x_b = tangents
z_b = np.tile(np.array([0, 0, 1]), (num_points, 1))  # eje z global
y_b = np.cross(z_b, x_b)
y_b /= np.linalg.norm(y_b, axis=1)[:, np.newaxis]
z_b = np.cross(x_b, y_b)
z_b /= np.linalg.norm(z_b, axis=1)[:, np.newaxis]

# ----- CONFIGURACIÓN DE LA FIGURA -----
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("VANT con Sistema de Coordenadas Local en Trayectoria B-Spline")

# Dibujar trayectoria y puntos de control
ax.plot(spline_points[:, 0], spline_points[:, 1], spline_points[:, 2], 'r-', label='Trayectoria B-Spline')
ax.plot(control_points[:, 0], control_points[:, 1], control_points[:, 2], 'bo--', label='Puntos de control')
ax.scatter(*control_points[0], color='green', s=100, label='Inicio')
ax.scatter(*control_points[-1], color='black', s=100, label='Fin')

# Inicializar sistema de coordenadas local del VANT
quivers = {
    'x': ax.quiver([], [], [], [], [], [], color='blue', length=1, normalize=True),
    'y': ax.quiver([], [], [], [], [], [], color='green', length=1, normalize=True),
    'z': ax.quiver([], [], [], [], [], [], color='purple', length=1, normalize=True)
}

# Límites
ax.set_xlim(0, 12)
ax.set_ylim(4, 12)
ax.set_zlim(1, 4)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.view_init(elev=30, azim=135)
ax.legend()

# ----- ANIMACIÓN -----
def update(frame):
    p = spline_points[frame]
    xb, yb, zb = x_b[frame], y_b[frame], z_b[frame]

    # Actualizar vectores del sistema coordenado local
    for vec, dir_vec in zip(['x', 'y', 'z'], [xb, yb, zb]):
        quivers[vec].remove()  # eliminar la flecha anterior
        quivers[vec] = ax.quiver(
            p[0], p[1], p[2], dir_vec[0], dir_vec[1], dir_vec[2],
            color=quivers[vec]._facecolor[0], length=0.8, normalize=True
        )
    return quivers['x'], quivers['y'], quivers['z']

anim = FuncAnimation(fig, update, frames=num_points, interval=50, blit=False)

plt.tight_layout()
plt.show()
