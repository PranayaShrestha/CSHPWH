import program
from program import C_P, T_hot
from solar import G_t
from solar import eff

#Solar system constants
Collector_Area = 4 #m2
m_dot = 0.02 * Collector_Area #mass flow rate, assumed constant for both solar and heat pump

#Temperature
T_cold = 20 # celcius
T_ambient = 18 #celcius

Q_solar = Collector_Area*G_t*eff
T_hp_inlet = T_cold + (Q_solar/(m_dot*C_P)) # T_hp_inlet = T_solar_outlet
print("Inlet temperature: ", T_hp_inlet)

Q_thermal = m_dot*C_P*(T_hot - T_hp_inlet)
print("Thermal q: ", Q_thermal, "W")
Q_standby = (3.95*(T_hot-T_hp_inlet))/2.0
print("Standby q: ", Q_standby, "W")
Q_total = (Q_thermal*1.25) + Q_standby
print("Total q: ", Q_total, "W")

gamma = 0.45
COP_hp = gamma * (T_hot + 273.15) / ((T_hot + 273.15) - (T_ambient + 273.15))
print("COP h: ", COP_hp)

W_electrical = Q_total/COP_hp
print("W: ", W_electrical, "W")
COP_system_series = ((m_dot*C_P*(T_hot-T_cold)*1.25)+Q_standby)/W_electrical
print("System COP: ", COP_system_series)
