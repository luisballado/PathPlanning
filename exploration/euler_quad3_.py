import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
from pytransform3d.rotations import passive_matrix_from_angle
from pytransform3d.transformations import transform_from

# Estado inicial
R_global = np.eye(3)
pos_global = np.array([0.0, 0.0, 0.0])

# Crear figura
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.35)

# Dibujar sistema coordenado móvil
basis_lines = []

def draw_basis(R, pos, length=0.4):
    global basis_lines
    for line in basis_lines:
        line.remove()
    basis_lines = []

    colors = ['r', 'g', 'b']
    for i in range(3):
        vec = R[:, i] * length
        line = ax.quiver(*pos, *vec, color=colors[i], linewidth=2)
        basis_lines.append(line)

# Inicialización de escena
def init_plot():
    ax.clear()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    draw_basis(R_global, pos_global)
    fig.canvas.draw_idle()

# Actualización cuando se mueven sliders
def update(val):
    global R_global, pos_global

    roll = s_roll.val
    pitch = s_pitch.val
    yaw = s_yaw.val
    thrust = s_thrust.val

    # Construir rotaciones incrementales
    R_roll = passive_matrix_from_angle(0, roll)
    R_pitch = passive_matrix_from_angle(1, pitch)
    R_yaw = passive_matrix_from_angle(2, yaw)
    R_delta = R_yaw @ R_pitch @ R_roll

    # Actualizar orientación acumulada
    R_global = R_global @ R_delta

    # Aplicar thrust en Z del frame actual
    dz = R_global[:, 2] * thrust
    pos_global = pos_global + dz

    init_plot()

# Crear sliders
axcolor = 'lightgoldenrodyellow'
ax_roll = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_pitch = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_yaw = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_thrust = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)

s_roll = Slider(ax_roll, 'Roll (rad)', -0.1, 0.1, valinit=0.0)
s_pitch = Slider(ax_pitch, 'Pitch (rad)', -0.1, 0.1, valinit=0.0)
s_yaw = Slider(ax_yaw, 'Yaw (rad)', -0.1, 0.1, valinit=0.0)
s_thrust = Slider(ax_thrust, 'Thrust', 0.0, 0.1, valinit=0.0)

# Conectar sliders con función
s_roll.on_changed(update)
s_pitch.on_changed(update)
s_yaw.on_changed(update)
s_thrust.on_changed(update)

# Mostrar
init_plot()
plt.show()
