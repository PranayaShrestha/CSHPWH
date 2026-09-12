import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI

# Fixed parameters
m_total = 0.06
m_solar = 0.02
m_hp = 0.04

DLM = 1.25

FR_ta = 0.75
FR_UL = 4.0

Gt = 800
T_ambient = 20

Area_of_tank = 3.95
T_hot_hp = 50
gamma = 0.45

# Variable
T_cold = np.linspace(5, 25, 100)
T_avg = ((T_hot_hp + T_cold)/2) + 273.15
Cp = PropsSI(
    'C',
    'T', T_avg,
    'P', 101325,
    'Water'
)

# Solar efficiency
eta_solar = FR_ta - FR_UL*((T_cold-T_ambient)/Gt)

# Solar outlet temperature
T_hot_solar = (eta_solar/(m_solar*Cp)) + T_cold

# Heat pump COP
COP_hp = gamma*((T_hot_hp+273.15)/(T_hot_hp-T_ambient))

# Tank losses
HLR = (Area_of_tank*(T_hot_hp-T_cold))/2

# Electrical input
W_electrical = (
    (m_hp*Cp*(T_hot_hp-T_cold)*DLM)
    + HLR
)/COP_hp

# Mixed outlet temperature
T_hot = (
    (m_solar*T_hot_solar)
    +(m_hp*T_hot_hp)
)/m_total

# Parallel COP
COP_parallel = (
    (m_total*Cp*(T_hot-T_cold)*DLM)
    + HLR
)/W_electrical

plt.figure(figsize=(8,5))
plt.plot(T_cold,COP_parallel,lw=2)

plt.xlabel("Cold Water Temperature (°C)")
plt.ylabel("System COP")
plt.title("Parallel System COP vs Cold Water Temperature")
plt.grid(True)

plt.show()

T_ambient = np.linspace(0,40,100)

T_cold = 20
Gt = 800

eta_solar = FR_ta - FR_UL*((T_cold-T_ambient)/Gt)

T_hot_solar = (
    eta_solar/(m_solar*Cp)
) + T_cold

COP_hp = gamma*(
    (T_hot_hp+273.15)
    /(T_hot_hp-T_ambient)
)

HLR = (
    Area_of_tank
    *(T_hot_hp-T_cold)
)/2

W_electrical = (
    (m_hp*Cp*(T_hot_hp-T_cold)*DLM)
    + HLR
)/COP_hp

T_hot = (
    (m_solar*T_hot_solar)
    +(m_hp*T_hot_hp)
)/m_total

COP_parallel = (
    (m_total*Cp*(T_hot-T_cold)*DLM)
    + HLR
)/W_electrical

plt.figure(figsize=(8,5))
plt.plot(T_ambient,COP_parallel,lw=2)

plt.xlabel("Ambient Temperature (°C)")
plt.ylabel("System COP")
plt.title("Parallel System COP vs Ambient Temperature")
plt.grid(True)

plt.show()

Gt = np.linspace(200,1200,100)

T_cold = 20
T_ambient = 20

eta_solar = (
    FR_ta
    - FR_UL*((T_cold-T_ambient)/Gt)
)

T_hot_solar = (
    eta_solar/(m_solar*Cp)
) + T_cold

COP_hp = gamma*(
    (T_hot_hp+273.15)
    /(T_hot_hp-T_ambient)
)

HLR = (
    Area_of_tank
    *(T_hot_hp-T_cold)
)/2

W_electrical = (
    (m_hp*Cp*(T_hot_hp-T_cold)*DLM)
    + HLR
)/COP_hp

T_hot = (
    (m_solar*T_hot_solar)
    +(m_hp*T_hot_hp)
)/m_total

COP_parallel = (
    (m_total*Cp*(T_hot-T_cold)*DLM)
    + HLR
)/W_electrical

plt.figure(figsize=(8,5))
plt.plot(Gt,COP_parallel,lw=2)

plt.xlabel("Solar Irradiance (W/m²)")
plt.ylabel("System COP")
plt.title("Parallel System COP vs Solar Irradiance")
plt.grid(True)

plt.show()