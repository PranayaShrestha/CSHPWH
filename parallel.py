import numpy as np

from series import Q_solar

# =====================================================
# SYSTEM INPUTS
# =====================================================

# Total daily hot water demand
m_total = 0.06          # m³/day
m_solar = 0.02
m_hp = 0.04

# Temperatures (°C)
T_cold = 20.0
T_hot = 55.0
T_ambient = 20.0

# Specific heat
Cp = 4184.0             # J/kg-K

# Demand Load Multiplier
DLM = 1.25

# =====================================================
# SOLAR COLLECTOR PARAMETERS

Ac = 4.0                # m²

FR_ta = 0.75
FR_UL = 4.0

Gt = 800.0              # W/m²

# =====================================================
# HEAT PUMP PARAMETERS
# =====================================================

gamma = 0.45            # heat pump effectiveness factor

# =====================================================
# STORAGE TANK PARAMETERS
# =====================================================

tank_radius = 0.30
tank_height = 1.80
thermal_resistance = 2.0

Area_of_tank = 3.95
HLR = (Area_of_tank*(T_hot-T_cold))/2
Q_solar = FR_ta - FR_UL*((T_cold-T_ambient)/Gt)
print("Q_solar: ", Q_solar)

T_hot_solar = (Q_solar/(m_solar*Cp))+T_cold
print("T_hot_solar: ", T_hot_solar)

T_hot_hp = 50.0
COP_hp = gamma*((T_hot_hp+273.15)/(T_hot_hp-T_ambient))
print("COP_hp: ", COP_hp)

W_electrical = ((m_hp*Cp*(T_hot_hp-T_cold)*DLM)+HLR)/COP_hp
print("W_electrical: ", W_electrical)

T_hot = ((m_solar*T_hot_solar)+(m_hp*T_hot_hp))/m_total
print("T_hot: ", T_hot)

COP_parallel = ((m_total*Cp*(T_hot-T_cold)*DLM)+HLR)/W_electrical
print("COP_parallel: ", COP_parallel)