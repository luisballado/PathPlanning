import numpy as np
from scipy.interpolate import BSpline
import pytransform3d.visualizer as pv
from pytransform3d.rotations import passive_matrix_from_angle, R_id
from pytransform3d.transformations import transform_from

# Crear puntos de control para la trayectoria
control_points = np.array([
    [0.0, 0.0, 0.0],
    [0.5, 1.0, 0.5],
    [1.0, 0.5, 1.5],
    [1.5, -1.0, 2.0],
    [2.0, 0.0, 2.5],
    [2.5, 1.0, 3.0],
    [3.0, 0.0, 3.5]
])

# Generar nudos uniformes para B-spline cúbica (k=3)
degree = 3
n_ctrl_pts = len(control_points)
n_knots = n_ctrl_pts + degree + 1
knots = np.linspace(0, 1, n_knots - 2 * degree)  # n_internal_knots
knots = np.concatenate(([0] * degree, knots, [1] * degree))

# Crear B-splines para x, y, z
spline_x = BSpline(knots, control_points[:, 0], degree)
spline_y = BSpline(knots, control_points[:, 1], degree)
spline_z = BSpline(knots, control_points[:, 2], degree)

# Parámetros
n_frames = 200
n_steps = 100

def update_trajectory(step, n_frames, trajectory):
    progress = (step + 1) / float(n_frames)
    H = np.empty((n_steps, 4, 4))

    for i, t in enumerate(np.linspace(0, progress, n_steps)):
        # Obtener posición de la B-spline
        p = np.array([
            spline_x(t),
            spline_y(t),
            spline_z(t)
        ])

        # Rotación: por simplicidad, rotamos sobre Z en función de t
        R = passive_matrix_from_angle(2, 2 * np.pi * t)  # rotación continua sobre Z

        # Construir transformación homogénea
        T = transform_from(R=R, p=p)
        H[i] = T

    trajectory.set_data(H)
    return trajectory

# Crear figura y trayectoria inicial
fig = pv.figure()

H_init = np.repeat(np.eye(4)[np.newaxis, :, :], n_steps, axis=0)
trajectory = pv.Trajectory(H_init, s=0.2, c=[0, 0, 0])
trajectory.add_artist(fig)

fig.view_init()
fig.set_zoom(0.5)

if "__file__" in globals():
    fig.animate(update_trajectory, n_frames=n_frames, fargs=(n_frames, trajectory), loop=True)
    fig.show()
else:
    fig.save_image("__open3d_rendered_image.jpg")
