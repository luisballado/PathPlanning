import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Función para dibujar un vóxel en forma de cubo en una ubicación (x, y, z)
def draw_voxel(ax, x, y, z, color):
    r = [0, 1]
    vertices = np.array([[x+i, y+j, z+k] for i in r for j in r for k in r])
    faces = [
        [vertices[0], vertices[1], vertices[3], vertices[2]],
        [vertices[4], vertices[5], vertices[7], vertices[6]],
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[1], vertices[3], vertices[7], vertices[5]],
        [vertices[0], vertices[2], vertices[6], vertices[4]],
    ]
    cube = Poly3DCollection(faces, facecolors=color, edgecolors='k', linewidths=0.3, alpha=1.0)
    ax.add_collection3d(cube)

# ----- Configuración del mapa -----
grid_size = (12, 12, 6)  # Tamaño del mapa (x, y, z)
occupancy_3d = np.full(grid_size, 0.5)  # Inicializar mapa con voxeles desconocidos (0.5)

# ----- Espacio libre (explorado) -----
# Cambia estas líneas para definir el volumen libre explorado
occupancy_3d[2:10, 2:10, 1:4] = 0.0  # Región libre

# ----- Obstáculos -----
# Agrega tus obstáculos aquí marcando voxeles como 1.0 (ocupado)
occupancy_3d[4, 4, 2] = 1.0
occupancy_3d[6, 6, 2] = 1.0
occupancy_3d[5, 7, 3] = 1.0
occupancy_3d[7, 3, 1] = 1.0

# ----- Identificación de tipo de vóxeles -----
free_voxels = np.argwhere(occupancy_3d == 0.0)
occupied_voxels = np.argwhere(occupancy_3d == 1.0)
frontiers = []
for x in range(1, grid_size[0]-1):
    for y in range(1, grid_size[1]-1):
        for z in range(1, grid_size[2]-1):
            if occupancy_3d[x, y, z] == 0.0:
                neighbors = occupancy_3d[x-1:x+2, y-1:y+2, z-1:z+2]
                if np.any(neighbors == 0.5):
                    frontiers.append((x, y, z))
frontiers = np.array(frontiers)

# Posición del dron
robot_pos = (0, 10, 2)

# ----- Visualización estilo RViz -----
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Visualización Estilo RViz: Mapa Voxelizado 3D")

# Dibujar voxeles
for (x, y, z) in free_voxels:
    draw_voxel(ax, x, y, z, color='lightblue')
for (x, y, z) in occupied_voxels:
    draw_voxel(ax, x, y, z, color='indigo')
for (x, y, z) in frontiers:
    draw_voxel(ax, x, y, z, color='limegreen')

# Trayectoria simulada del dron (modificable)
trajectory = np.array([
    [2, 2, 1],
    [3, 3, 1],
    [4, 4, 1],
    [5, 5, 2],
    [6, 5, 2],
    [7, 5, 2],
    [robot_pos[0], robot_pos[1], robot_pos[2]]
])
ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], color='red', linewidth=2, label='Trayectoria')

# Dron (última posición)
ax.scatter(*robot_pos, color='red', s=200)

# Plano del suelo
xg, yg = np.meshgrid(np.arange(0, grid_size[0]), np.arange(0, grid_size[1]))
zg = np.zeros_like(xg)
ax.plot_surface(xg, yg, zg, color='lavender', alpha=0.2, zorder=0)

# Configuración de la vista
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(0, grid_size[0])
ax.set_ylim(0, grid_size[1])
ax.set_zlim(0, grid_size[2])
ax.view_init(elev=30, azim=140)
ax.legend(loc='upper left')
plt.tight_layout()
plt.show()
