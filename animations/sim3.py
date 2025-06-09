import numpy as np
import pytransform3d.visualizer as pv
from pytransform3d.rotations import passive_matrix_from_angle, R_id
from pytransform3d.transformations import transform_from, concat

# Configuración
n_frames = 360
frames_per_phase = n_frames // 3

# Crear visualizador
fig = pv.figure()

# Base móvil a animar
handle = fig.plot_basis(R=R_id, p=[0, 0, 0], s=0.4)

# Ejes fijos con vectores (colores = etiquetas visuales)
# Rojo: X
fig.plot_vector(vector=[1, 0, 0], origin=[0, 0, 0], s=0.6, c=[1, 0, 0])
# Verde: Y
fig.plot_vector(vector=[0, 1, 0], origin=[0, 0, 0], s=0.6, c=[0, 1, 0])
# Azul: Z
fig.plot_vector(vector=[0, 0, 1], origin=[0, 0, 0], s=0.6, c=[0, 0, 1])

# Función de actualización de animación secuencial
def update_sequential_rotation(step, n_frames, handle):
    if step < frames_per_phase:
        # Primera fase: rotar X
        angle_x = 2 * np.pi * (step / frames_per_phase)
        R = passive_matrix_from_angle(0, angle_x)
    elif step < 2 * frames_per_phase:
        # Segunda fase: rotar Y (ya rotó X)
        angle_y = 2 * np.pi * ((step - frames_per_phase) / frames_per_phase)
        R_x = passive_matrix_from_angle(0, 2 * np.pi)
        R_y = passive_matrix_from_angle(1, angle_y)
        R = R_y @ R_x
    else:
        # Tercera fase: rotar Z (X e Y ya completos)
        angle_z = 2 * np.pi * ((step - 2 * frames_per_phase) / frames_per_phase)
        R_x = passive_matrix_from_angle(0, 2 * np.pi)
        R_y = passive_matrix_from_angle(1, 2 * np.pi)
        R_z = passive_matrix_from_angle(2, angle_z)
        R = R_z @ R_y @ R_x

    # Aplicar transformación rotada a la base
    T = transform_from(R=R, p=[0, 0, 0])
    handle.set_data(T)
    return handle

# Visualización
fig.view_init()
fig.set_zoom(0.8)
fig.animate(update_sequential_rotation, n_frames=n_frames, fargs=(n_frames, handle), loop=False)
fig.show()
