
Total_daily_Volume = 0.15 #m3
DLM = 1.25

# temperature for water (desired, medium, ambient)
T_hot = 55.0
T_cold = 20.0
T_medium = 35.0

C_P = 4184  # J/(kg·K)
Q_thermal_Wh = (Total_daily_Volume * 1000 * C_P * (T_hot-T_medium)) / 3600
print(Q_thermal_Wh)

#dimension profiles for the storage tank
tank_radius = 0.3 #m
tank_height = 1.8 #m
thermal_resistance = 2.0
tank_area = (2.0 * 3.1415 * tank_height * tank_radius) + (2 * 3.1415 * tank_radius**2)
print(tank_area)

hourly_loss_rate = (tank_area*(T_hot - T_cold))/thermal_resistance
print(hourly_loss_rate)
Q_standby_Wh = hourly_loss_rate * 24.0
Q_standby_W = Q_standby_Wh/3600
print(Q_standby_W/2009)

Q_total_Wh = Q_standby_Wh + Q_thermal_Wh*DLM
print(Q_total_Wh)

COP = Q_total_Wh/(2.09*3600)
print(COP)