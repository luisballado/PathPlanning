import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from pytransform3d.camera import make_world_grid, world2image, plot_camera
from pytransform3d.plot_utils import make_3d_axis
from pytransform3d.transformations import transform_from, plot_transform

# Función de orientación tipo "look at"
def look_at(eye, target, up=np.array([0, 0, 1])):
    forward = np.array(target) - np.array(eye)
    forward /= np.linalg.norm(forward)
    right = np.cross(up, forward)
    right /= np.linalg.norm(right)
    true_up = np.cross(forward, right)
    R = np.vstack([right, true_up, forward]).T
    return R

# Parámetros de cámara
focal_length = 0.0036
sensor_size = (0.00367, 0.00274)
image_size = (640, 480)
intrinsic_camera_matrix = np.array([
    [focal_length, 0, sensor_size[0] / 2],
    [0, focal_length, sensor_size[1] / 2],
    [0, 0, 1],
])

# Mundo
world_grid = make_world_grid(n_points_per_line=101)

# Crear figura
fig = plt.figure(figsize=(12, 5))
ax3d = fig.add_subplot(121, projection='3d')
ax2d = fig.add_subplot(122, aspect="equal")

# Trayectoria circular
def camera_pose_at_frame(i):
    angle = i * np.pi / 30
    position = [1.0 * np.cos(angle), 1.0 * np.sin(angle), 0.5]
    target = [0, 0, 0.5]  # La cámara mira hacia el centro del círculo
    orientation = look_at(position, target)
    return transform_from(orientation, position)

# Actualización por frame
def update(i):
    ax3d.cla()
    ax2d.cla()

    cam2world = camera_pose_at_frame(i)

    image_grid = world2image(
        world_grid, cam2world, sensor_size, image_size, focal_length, kappa=0.05
    )

    # Eje 3D
    ax3d.set_title("Camera and world frames")
    ax3d.set_xlim(-2, 2)
    ax3d.set_ylim(-2, 2)
    ax3d.set_zlim(0, 2)
    ax3d.view_init(elev=25, azim=-130)
    plot_transform(ax3d)
    plot_transform(ax3d, A2B=cam2world, s=0.3)
    plot_camera(ax3d, intrinsic_camera_matrix, cam2world,
                sensor_size=sensor_size, virtual_image_distance=0.5)
    ax3d.scatter(world_grid[:, 0], world_grid[:, 1], world_grid[:, 2], s=1, alpha=0.2)
    ax3d.scatter(world_grid[-1, 0], world_grid[-1, 1], world_grid[-1, 2], color="r")

    # Imagen proyectada
    ax2d.set_title("Camera image")
    ax2d.set_xlim(0, image_size[0])
    ax2d.set_ylim(0, image_size[1])
    ax2d.scatter(image_grid[:, 0], -(image_grid[:, 1] - image_size[1]))
    ax2d.scatter(image_grid[-1, 0], -(image_grid[-1, 1] - image_size[1]), color="r")

    return ax3d, ax2d

# Crear animación
anim = FuncAnimation(fig, update, frames=60, interval=100)
plt.show()
