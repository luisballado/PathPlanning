import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Function to draw a 3D coordinate frame
def draw_frame(ax, origin, R, label, color, length=0.5):
    axes = R @ np.eye(3) * length
    for i, (c, axis) in enumerate(zip(color, ['x', 'y', 'z'])):
        ax.quiver(*origin, *axes[:, i], color=c, linewidth=2)
        ax.text(*(origin + axes[:, i]), f"{axis}_{label}", color=c)

# Function to draw drone rotors as ellipses
def draw_rotors(ax, center, size=0.1):
    rotor_offsets = np.array([[0.2, 0.2, 0],
                               [-0.2, 0.2, 0],
                               [-0.2, -0.2, 0],
                               [0.2, -0.2, 0]])
    for offset in rotor_offsets:
        pos = center + offset
        u = np.linspace(0, 2 * np.pi, 100)
        x = size * np.cos(u)
        y = size * 0.3 * np.sin(u)
        z = np.zeros_like(u)
        ax.plot(x + pos[0], y + pos[1], z + pos[2], color='cyan')

# Create figure and 3D axis
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# World frame at origin
draw_frame(ax, np.array([0, 0, 0]), np.eye(3), 'i', ['black', 'black', 'black'])

# Drone body frame
translation = np.array([1, 1, 1])
rotation_matrix = np.eye(3)  # No rotation for simplicity
draw_frame(ax, translation, rotation_matrix, 'b', ['darkred', 'darkgreen', 'darkblue'])

# Draw drone rotors
draw_rotors(ax, translation)

# Draw dashed translation vector
ax.plot([0, translation[0]], [0, translation[1]], [0, translation[2]], 
        linestyle='dashed', color='blue', linewidth=1.5)
ax.text(*(translation / 2), r'$\xi$', color='blue', fontsize=14)

# Settings
ax.set_xlim([-0.5, 2])
ax.set_ylim([-0.5, 2])
ax.set_zlim([-0.5, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Rigid Body Translation and Body Frame of a Quadrotor')

plt.tight_layout()
plt.show()
