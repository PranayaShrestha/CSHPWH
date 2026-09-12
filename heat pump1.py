import numpy as np
import matplotlib.pyplot as plt

# Constants
Volume = 0.15
DLM = 1.25

T_medium = 35
T_cold = 20

Cp = 4184

tank_radius = 0.3
tank_height = 1.8
thermal_resistance = 2.0

tank_area = (
    2*np.pi*tank_height*tank_radius
    + 2*np.pi*tank_radius**2
)
T_hot = 55.0
T_medium = np.linspace(15,25,100)

Q_thermal = (
    Volume*1000*Cp*(T_hot-T_medium)
)/3600

hourly_loss = (
    tank_area*(T_hot-T_cold)
)/thermal_resistance

Q_standby = hourly_loss*24

Q_total = Q_standby + DLM*Q_thermal

COP = Q_total/(2.09*3600)

plt.figure(figsize=(8,5))
plt.plot(T_medium,COP,linewidth=2)

plt.xlabel('Inlet Water Temperature (°C)')
plt.ylabel('Energy requirement')
plt.title('Energy req. vs Inlet Water Temperature')
plt.grid(True)

plt.show()