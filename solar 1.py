import numpy as np
import matplotlib.pyplot as plt

# Constants
F_r_tow_alpha = 0.75
FrUl = 4.0

Ta = 20
Gt = np.linspace(600, 1200, 100)

Ti = np.linspace(20,100,100)

eff = F_r_tow_alpha - FrUl*((Ti-Ta)/Gt)

plt.figure(figsize=(8,5))
plt.plot(Ti, eff, linewidth=2)

plt.xlabel('Inlet Temperature Ti (°C)')
plt.ylabel('Collector Efficiency')
plt.title('Efficiency vs Inlet Temperature')
plt.grid(True)

plt.show()

