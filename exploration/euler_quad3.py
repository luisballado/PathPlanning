import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# Create trajectory (simulated B-spline-like curve)
t_vals = np.linspace(0, np.pi, 60)
x_vals = 0.5 * t_vals + 0.2 * np.sin(2 * t_vals)
y_vals = 0.3 * t_vals + 0.2 * np.cos(3 * t_vals)
z_vals = 0.2 * t_vals

# Compute direction vectors along trajectory (simple finite difference)
trajectory_points = np.vstack((x_vals, y_vals, z_vals)).T
directions = np.gradient(trajectory_points, axis=0)
directions = np.array([v / np.linalg.norm(v) for v in directions]) #normal direccion

# Setup figure
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Draw world frame
def draw_frame(ax, origin, R, label, color, length=0.3):
    axes = R @ np.eye(3) * length
    for i, (c, axis) in enumerate(zip(color, ['x', 'y', 'z'])):
        ax.quiver(*origin, *axes[:, i], color=c, linewidth=2)
        ax.text(*(origin + axes[:, i]), f"{axis}_{label}", color=c)

# Function to draw field of view (as rays)
def draw_fov(ax, origin, direction, length=0.6, angle=np.pi/10):
    direction = direction / np.linalg.norm(direction)
    up = np.array([0, 0, 1]) if abs(direction[2]) < 0.95 else np.array([0, 1, 0])
    right = np.cross(direction, up)
    up = np.cross(right, direction)
    right /= np.linalg.norm(right)
    up /= np.linalg.norm(up)

    for theta in np.linspace(-angle, angle, 5):
        for phi in np.linspace(-angle, angle, 5):
            offset = direction + np.tan(theta) * right + np.tan(phi) * up
            offset = offset / np.linalg.norm(offset) * length
            ax.plot([origin[0], origin[0] + offset[0]],
                    [origin[1], origin[1] + offset[1]],
                    [origin[2], origin[2] + offset[2]],
                    color='orange', alpha=0.6)

def update_frame(i):
    ax.cla()
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_zlim(-0.5, 2.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Quadrotor FOV Aligned to Trajectory')

    # Dibuja sistema de coordenadas inercial
    draw_frame(ax, origin=np.array([0, 0, 0]), R=np.eye(3), label='w', color=['red', 'green', 'blue'])

    # Trayectoria completa
    ax.plot(x_vals, y_vals, z_vals, 'gray', linewidth=1, linestyle='--')

    # Posición y dirección actuales
    position = trajectory_points[i]
    direction = directions[i]

    # Vector que conecta inercial con móvil
    origin_inertial = np.array([0, 0, 0])
    vector_to_mobile = position - origin_inertial
    ax.quiver(*origin_inertial, *vector_to_mobile, color='purple', linewidth=2, arrow_length_ratio=0.1)

    # Cálculo del sistema móvil
    x_axis = direction
    up_ref = np.array([0, 0, 1]) if abs(direction[2]) < 0.95 else np.array([0, 1, 0])
    y_axis = np.cross(up_ref, x_axis)
    z_axis = np.cross(x_axis, y_axis)
    y_axis /= np.linalg.norm(y_axis)
    z_axis /= np.linalg.norm(z_axis)
    R = np.vstack((x_axis, y_axis, z_axis)).T

    # Dibuja sistema móvil y FOV
    draw_frame(ax, position, R, 'b', ['red', 'green', 'blue'])
    draw_fov(ax, position, direction)

    # ✅ Construir transformación homogénea
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = position

    # ✅ Imprimir matriz en consola
    np.set_printoptions(precision=3, suppress=True)
    print(f"\nFrame {i}:")
    print("Posición del sistema móvil:")
    print(position)
    print("Rotación R (col. = ejes x, y, z del sistema móvil):")
    print(R)
    print("Transformación homogénea T (del móvil al inercial):")
    print(T)

    
# Create animation
ani = animation.FuncAnimation(fig, update_frame, frames=len(x_vals), interval=100)

plt.show()

# Save animation
#output_path = 'quadrotor_fov_aligned_trajectory.mp4'
#ani.save(output_path, fps=10, extra_args=['-vcodec', 'libx264'])

#plt.close(fig)
#output_path
