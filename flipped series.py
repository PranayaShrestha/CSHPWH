import numpy as np
import matplotlib.pyplot as plt

# Temperatures
T_cold = 20
T_desired = 55

# Solar collector parameters
FrTa = 0.75
FrUl = 4.0

Gt = np.linspace(200,1200,100)

# Assume solar outlet temperature
T_solar_out = 40

# ----------------------------
# CASE 1
# Solar -> Heat Pump
# ----------------------------

eta_solar_case1 = (
    FrTa
    - FrUl*((T_cold-20)/Gt)
)

Q_hp_case1 = (
    T_desired
    - T_solar_out
)

COP_case1 = 4.0 + (T_solar_out-T_cold)/20

# ----------------------------
# CASE 2
# Heat Pump -> Solar
# ----------------------------

T_hp_out = 40

eta_solar_case2 = (
    FrTa
    - FrUl*((T_hp_out-20)/Gt)
)

COP_case2 = 4.0

# ----------------------------
# Plot
# ----------------------------

plt.figure(figsize=(8,5))

plt.plot(
    Gt,
    eta_solar_case1,
    label='Solar → HP'
)

plt.plot(
    Gt,
    eta_solar_case2,
    label='HP → Solar'
)

plt.xlabel('Solar Irradiance (W/m²)')
plt.ylabel('Collector Efficiency')

plt.title(
    'Collector Efficiency Comparison'
)

plt.legend()
plt.grid(True)

plt.show()