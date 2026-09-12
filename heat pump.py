import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -----------------------------
# Constants
# -----------------------------
DLM = 1.25

T_medium = 35.0
T_cold = 20.0

Cp = 4184

# Tank properties
tank_radius = 0.3
tank_height = 1.8
thermal_resistance = 2.0

# Heat pump power input
P_input = 2.09 * 3600

# Tank area
tank_area = (
    2*np.pi*tank_height*tank_radius
    + 2*np.pi*tank_radius**2
)

# -----------------------------
# Parameter ranges
# -----------------------------
T_medium = np.linspace(15, 25, 50)
Volume = np.linspace(0.05, 0.30, 50)
T_hot = 55.0
T_hot_mesh, Volume_mesh = np.meshgrid(
    T_hot,
    Volume
)

# -----------------------------
# Thermal energy requirement
# -----------------------------
Q_thermal = (
    Volume_mesh
    * 1000
    * Cp
    * (T_hot_mesh - T_medium)
) / 3600

# -----------------------------
# Standby losses
# -----------------------------
hourly_loss_rate = (
    tank_area
    * (T_hot_mesh - T_cold)
) / thermal_resistance

Q_standby = hourly_loss_rate * 24

# -----------------------------
# Total energy
# -----------------------------
Q_total = (
    Q_standby
    + DLM * Q_thermal
)

# -----------------------------
# COP
# -----------------------------
COP = Q_total / P_input

# -----------------------------
# Plot
# -----------------------------
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(
    T_medium,
    Volume_mesh,
    COP,
    cmap='plasma'
)

ax.set_xlabel('Inlet Water Temperature (°C)')
ax.set_ylabel('Daily Water Volume (m³)')
ax.set_zlabel('COP')
ax.set_title('Heat Pump COP Surface')

fig.colorbar(
    surf,
    shrink=0.5,
    aspect=10,
    label='COP'
)

plt.show()