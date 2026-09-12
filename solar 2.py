import numpy as np
import matplotlib.pyplot as plt

F_r_tow_alpha = 0.75
FrUl = 4.0

Ti = 40
Ta = 20

Gt = np.linspace(200,1200,100)

eff = F_r_tow_alpha - FrUl*((Ti-Ta)/Gt)

plt.figure(figsize=(8,5))
plt.plot(Gt, eff, linewidth=2)

plt.xlabel('Solar Irradiance Gt (W/m²)')
plt.ylabel('Collector Efficiency')
plt.title('Efficiency vs Solar Irradiance')
plt.grid(True)

plt.show()