import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# Function to create a rotation matrix using Euler angles (ZYX order)
def euler_zyx_matrix(yaw, pitch, roll):
    cy, sy = np.cos(yaw), np.sin(yaw)
    cp, sp = np.cos(pitch), np.sin(pitch)
    cr, sr = np.cos(roll), np.sin(roll)

    Rz = np.array([[cy, -sy, 0],
                   [sy,  cy, 0],
                   [0,    0, 1]])
    Ry = np.array([[cp, 0, sp],
                   [0,  1, 0],
                   [-sp, 0, cp]])
    Rx = np.array([[1, 0, 0],
                   [0, cr, -sr],
                   [0, sr, cr]])

    return Rz @ Ry @ Rx

# Create trajectory (simulated B-spline-like curve)
t_vals = np.linspace(0, np.pi, 60)
x_vals = 0.5*t_vals + 0.2*np.sin(2*t_vals)
y_vals = 0.3*t_vals + 0.2*np.cos(3*t_vals)
z_vals = 0.2*t_vals

# Setup figure
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Draw world frame
def draw_frame(ax, origin, R, label, color, length=0.3):
    axes = R @ np.eye(3) * length
    for i, (c, axis) in enumerate(zip(color, ['x', 'y', 'z'])):
        ax.quiver(*origin, *axes[:, i], color=c, linewidth=2)
        ax.text(*(origin + axes[:, i]), f"{axis}_{label}", color=c)

# Update function for animation
def update_frame(i):
    ax.cla()
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_zlim(-0.5, 2.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Quadrotor B-spline Trajectory with Euler Angles')

    # Draw full trajectory
    ax.plot(x_vals, y_vals, z_vals, 'gray', linewidth=1, linestyle='--')

    # Current position and orientation
    x, y, z = x_vals[i], y_vals[i], z_vals[i]
    yaw = np.deg2rad(i * 5)
    pitch = np.deg2rad(10)
    roll = np.deg2rad(5)
    R = euler_zyx_matrix(yaw, pitch, roll)

    draw_frame(ax, np.array([x, y, z]), R, 'b', ['red', 'green', 'blue'])

    # Draw rotors
    rotor_offsets = np.array([[0.2, 0.2, 0],
                               [-0.2, 0.2, 0],
                               [-0.2, -0.2, 0],
                               [0.2, -0.2, 0]])
    for offset in rotor_offsets:
        pos = np.array([x, y, z]) + R @ offset
        u = np.linspace(0, 2 * np.pi, 100)
        circle_x = 0.07 * np.cos(u)
        circle_y = 0.03 * np.sin(u)
        circle_z = np.zeros_like(u)
        rot_circle = R @ np.vstack((circle_x, circle_y, circle_z))
        ax.plot(pos[0] + rot_circle[0],
                pos[1] + rot_circle[1],
                pos[2] + rot_circle[2], color='cyan')

# Create animation
ani = animation.FuncAnimation(fig, update_frame, frames=len(x_vals), interval=100)

# Save animation
output_path = 'quadrotor_trajectory.mp4'
ani.save(output_path, fps=10, extra_args=['-vcodec', 'libx264'])

plt.close(fig)
output_path
