import numpy as np
import pytransform3d.visualizer as pv
from pytransform3d.rotations import passive_matrix_from_angle, R_id
from pytransform3d.transformations import transform_from, concat

# Configuración
n_frames = 360  # Total: 6 segundos a 60 FPS
frames_per_phase = n_frames // 3

# Crear visualizador
fig = pv.figure()

# Base que se va a animar
handle = fig.plot_basis(R=R_id, p=[0, 0, 0], s=0.4)

# Función de animación por frame
def update_sequential_rotation(step, n_frames, handle):
    if step < frames_per_phase:
        # Primera fase: rotación sobre X
        angle_x = 2 * np.pi * (step / frames_per_phase)
        R_x = passive_matrix_from_angle(0, angle_x)
        R = R_x
    elif step < 2 * frames_per_phase:
        # Segunda fase: X ya rotó, ahora rota Y
        angle_y = 2 * np.pi * ((step - frames_per_phase) / frames_per_phase)
        R_x = passive_matrix_from_angle(0, 2 * np.pi)
        R_y = passive_matrix_from_angle(1, angle_y)
        R = concat(transform_from(R=R_x, p=[0, 0, 0]),
                   transform_from(R=R_y, p=[0, 0, 0]))[:3, :3]
    else:
        # Tercera fase: X y Y ya rotaron, ahora rota Z
        angle_z = 2 * np.pi * ((step - 2 * frames_per_phase) / frames_per_phase)
        R_x = passive_matrix_from_angle(0, 2 * np.pi)
        R_y = passive_matrix_from_angle(1, 2 * np.pi)
        R_z = passive_matrix_from_angle(2, angle_z)
        R_total = concat(transform_from(R=R_x, p=[0, 0, 0]),
                         transform_from(R=R_y, p=[0, 0, 0]))
        R_total = concat(R_total, transform_from(R=R_z, p=[0, 0, 0]))
        R = R_total[:3, :3]

    T = transform_from(R=R, p=[0, 0, 0])
    handle.set_data(T)
    return handle

# Iniciar animación
fig.view_init()
fig.set_zoom(0.8)
fig.animate(update_sequential_rotation, n_frames=n_frames, fargs=(n_frames, handle), loop=True)
fig.show()
