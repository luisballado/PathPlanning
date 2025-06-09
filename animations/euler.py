import numpy as np
import pytransform3d.visualizer as pv
from pytransform3d.rotations import matrix_from_euler
from pytransform3d.transformations import transform_from

# Ángulos finales: roll(X), pitch(Y), yaw(Z)
final_roll = np.deg2rad(30)
final_pitch = np.deg2rad(40)
final_yaw = np.deg2rad(90)

n_frames = 200
n_steps = 100

def update_trajectory(step, n_frames, trajectory):
    progress = (step + 1) / float(n_frames)

    # Inicializar array de matrices homogéneas
    H = np.empty((n_steps, 4, 4))
    
    for i, t in enumerate(np.linspace(0, progress, n_steps)):
        # Interpolación de ángulos
        roll = t * final_roll
        pitch = t * final_pitch
        yaw = t * final_yaw

        # Rotación ZYX extrínseca
        R = matrix_from_euler(2, 1, 0, np.array([yaw, pitch, roll]), extrinsic=True)
        T = transform_from(R=R, p=[t, 0, t])

        # Asegurar que sea homogénea
        H[i] = T

    # Actualizar trayectoria
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
