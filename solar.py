F_r_tow_alpha = 0.75 #heat removal factor multiplied with transmittence and absorbtance (%)
FrUl = 4.0 #overall heat loss coefficient (W/m2.C)
G_t = 800 #solar irradiance
T_i = 25.0
T_a = 18.0

eff = F_r_tow_alpha - FrUl*((T_i-T_a)/G_t)
print(eff)