import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI

# CONSTANTS
T_cold = 20                   # Inlet water temperature (°C)
Cp = PropsSI(
    'C',
    'T', (T_cold + 273.15),
    'P', 101325,
    'Water'
)                             # J/kgK
T_hot = 60                    # Desired outlet temperature (°C)


gamma = 0.45
standby_R = 2.0


# VARIABLE PARAMETERS
T_ambient_range = np.linspace(15,18,10)
G_t_range = np.linspace(600,1000,20)
Collector_area_range = np.linspace(2,8,20)
eff_range = np.linspace(0.50,0.75,10)


def calculate_system(
        T_ambient,
        G_t,
        Collector_Area,
        eff):

    m_dot = 0.02 * Collector_Area

    h_cold = PropsSI(
        'H',
        'T', T_cold+273.15,
        'P', 101325,
        'Water'
    )

    Q_solar = Collector_Area*G_t*eff

    h_hp_in = h_cold + Q_solar/m_dot

    T_hp_inlet = (
        PropsSI(
            'T',
            'H', h_hp_in,
            'P', 101325,
            'Water'
        )
        -273.15
    )

    h_hot = PropsSI(
        'H',
        'T', T_hot+273.15,
        'P', 101325,
        'Water'
    )

    Q_thermal = m_dot*(h_hot - h_hp_in)

    Q_standby = (
        3.95*(T_hot-T_hp_inlet)
    )/2

    Q_total = 1.25*Q_thermal + Q_standby

    COP_hp = (
        gamma*(T_hot+273.15)
        /
        ((T_hot+273.15)
        -(T_ambient+273.15))
    )

    W_electrical = Q_total/COP_hp

    COP_system = (
        (Q_thermal+Q_solar)
        /
        W_electrical
    )

    return (
        T_hp_inlet,
        Q_thermal,
        COP_hp,
        W_electrical,
        COP_system
    )

T_inlet = []

for G in G_t_range:

    result = calculate_system(
        T_ambient=18,
        G_t=G,
        Collector_Area=4,
        eff=0.65)

    T_inlet.append(result[0])

plt.figure(figsize=(8,5))
plt.plot(G_t_range,T_inlet)
plt.xlabel("Solar Irradiance (W/m²)")
plt.ylabel("HP Inlet Temperature (°C)")
plt.grid()
plt.title("Solar Irradiance vs HP Inlet Temperature")
plt.show()

T_inlet = []

for A in Collector_area_range:

    result = calculate_system(
        T_ambient=18,
        G_t=800,
        Collector_Area=A,
        eff=0.65)

    T_inlet.append(result[0])

plt.figure(figsize=(8,5))
plt.plot(Collector_area_range,T_inlet)
plt.xlabel("Collector Area (m²)")
plt.ylabel("HP Inlet Temperature (°C)")
plt.grid()
plt.title("Collector Area Effect")
plt.show()

COPs = []

for Ta in T_ambient_range:

    result = calculate_system(
        T_ambient=Ta,
        G_t=800,
        Collector_Area=4,
        eff=0.65)

    COPs.append(result[2])

plt.figure(figsize=(8,5))
plt.plot(T_ambient_range,COPs)
plt.xlabel("Ambient Temperature (°C)")
plt.ylabel("Heat Pump COP")
plt.grid()
plt.title("Ambient Temperature Effect on COP")
plt.show()

W = []

for G in G_t_range:

    result = calculate_system(
        T_ambient=18,
        G_t=G,
        Collector_Area=4,
        eff=0.65)

    W.append(result[3])

plt.figure(figsize=(8,5))
plt.plot(G_t_range,W)
plt.xlabel("Solar Irradiance (W/m²)")
plt.ylabel("Electrical Power (W)")
plt.grid()
plt.title("Electrical Consumption Reduction")
plt.show()

COP_sys = []

for A in Collector_area_range:

    result = calculate_system(
        T_ambient=18,
        G_t=800,
        Collector_Area=A,
        eff=0.65)

    COP_sys.append(result[4])

plt.figure(figsize=(8,5))
plt.plot(Collector_area_range,COP_sys)
plt.xlabel("Collector Area (m²)")
plt.ylabel("Overall System COP")
plt.grid()
plt.title("Collector Area vs System COP")
plt.show()