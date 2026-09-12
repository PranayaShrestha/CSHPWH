import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
F_r_tow_alpha = 0.75
FrUl = 4.0

# Ranges
Ti = np.linspace(20, 100, 50)
Gt = np.linspace(200, 1200, 50)

Ti_mesh, Gt_mesh = np.meshgrid(Ti, Gt)

Ta = 20.0

# Efficiency
eff = F_r_tow_alpha - FrUl * ((Ti_mesh - Ta) / Gt_mesh)

# 3D Plot
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(Ti_mesh, Gt_mesh, eff, cmap='viridis')

ax.set_xlabel('Inlet Temperature Ti (°C)')
ax.set_ylabel('Solar Irradiance Gt (W/m²)')
ax.set_zlabel('Efficiency')
ax.set_title('Solar Collector Efficiency Surface')

fig.colorbar(surf, shrink=0.5, aspect=10)
plt.show()