from series import *
from solar import *

#PRIMARY KNOWN PARAMETERS
T_in = 15.0 #inlet temperature
h_in_1 = 62.9 # state 1:enthalpy ---> f(T_in, P_in)
T_out = 55.0 #desired output temperature of the whole system
h_in_3 = 230.2 # state 3: enthalpy ---> f(T_out,P_out)

m_dot_water = 0.03 #considered mass flow rate of the water
T_amb = 20.0 #ambient air temperature

#FOR SOLAR CALCULATIONS
G_t = 0.8
collector_area = 4.0 #m2
eta_solar = 0.77 #calculated value of the solar efficiency for flat plate collector

Q_solar = eta_solar*collector_area*G_t
print("Q_solar",Q_solar)

h_in_2 = h_in_1 + (Q_solar/m_dot_water)
print("h_in_2",h_in_2)

#FOR HEAT PUMP LOOP(R134A)
h_evaporator_1 = 404.5 #evaporator exit, saturated vapor, evaporator temp assumed 10C
h_condensor_3 = 287.4 #condensor exit, saturated liquid, condensor temp assumed 60C
isentropic_eff = 0.7
motor_eff = 0.85
ideal_isen_discharge = 435.0 #kj/kg

Q_thermal_water = m_dot_water*(h_in_3-h_in_2)
print("Q_thermal_water",Q_thermal_water)

h_condensor_2 = h_evaporator_1+((ideal_isen_discharge-h_evaporator_1)/isentropic_eff)
print("h_condensor_2",h_condensor_2)

m_dot_r = Q_thermal_water/(h_condensor_2-h_condensor_3)
print("m_dot_r",m_dot_r)

W_electrical = (m_dot_r*(h_condensor_2-h_evaporator_1))/motor_eff
print("W_electrical",W_electrical)

COP_system_series_en = (m_dot_water*(h_in_3-h_in_1))/W_electrical
print("COP_system_series_en",COP_system_series_en)