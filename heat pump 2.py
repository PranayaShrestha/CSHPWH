import numpy as np
import matplotlib.pyplot as plt

DLM = 1.25

T_hot = 55
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

Volume = np.linspace(0.05,0.30,100)

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
plt.plot(Volume*1000,COP,linewidth=2)

plt.xlabel('Daily Hot Water Consumption (L/day)')
plt.ylabel('COP')
plt.title('COP vs Daily Water Volume')
plt.grid(True)

plt.show()