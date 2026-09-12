import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI



# COMBINED SOLAR + HEAT PUMP WATER HEATER
# Dynamic gamma model based on catalog data




# 1. SYSTEM / CATALOG PARAMETERS

# Heat pump catalog data
COP_rated = 4.1                    # Rated COP
T_hot_rated = 55                  # Rated outlet temperature [°C]

# Maximum allowable outlet temperature
T_hot_max = 60                    # [°C]

# Catalog ambient operating range
T_ambient_min_catalog = 0         # [°C]
T_ambient_max_catalog = 46        # [°C]

# User's operating water temperatures
T_cold = 20                       # Water inlet temperature [°C]
T_hot = 60                        # Desired final outlet temperature [°C]

# Standby heat loss parameter
standby_R = 2.0

# Additional heating/load factor from your original model
heating_factor = 1.25


# 2. WATER PROPERTIES

Cp = PropsSI(
    'C',
    'T', T_cold + 273.15,
    'P', 101325,
    'Water'
)


# 3. GAMMA LIMITS FROM CATALOG

T_hot_rated_K = T_hot_rated + 273.15

T_ambient_min_K = T_ambient_min_catalog + 273.15
T_ambient_max_K = T_ambient_max_catalog + 273.15


# Carnot COP at minimum ambient temperature
COP_carnot_max = (
    T_hot_rated_K /
    (T_hot_rated_K - T_ambient_min_K)
)

# Carnot COP at maximum ambient temperature
COP_carnot_min = (
    T_hot_rated_K /
    (T_hot_rated_K - T_ambient_max_K)
)


# Corresponding gamma limits
gamma_max = COP_rated / COP_carnot_max
gamma_min = COP_rated / COP_carnot_min


print("=" * 65)
print("CATALOG-BASED GAMMA RANGE")
print("=" * 65)

print(f"Rated COP                 : {COP_rated:.2f}")
print(f"Rated hot water temp.     : {T_hot_rated:.1f} °C")
print(f"Ambient operating range   : "
      f"{T_ambient_min_catalog}–{T_ambient_max_catalog} °C")

print(f"\nGamma at {T_ambient_min_catalog} °C ambient : "
      f"{gamma_max:.4f}")

print(f"Gamma at {T_ambient_max_catalog} °C ambient : "
      f"{gamma_min:.4f}")

print(f"\nGamma range = "
      f"{gamma_min:.4f} – {gamma_max:.4f}")


# ============================================================
# 4. DYNAMIC GAMMA FUNCTION
# ============================================================

def calculate_gamma(T_ambient):
    """
    Calculate gamma dynamically from ambient temperature.

    gamma = COP_rated / COP_Carnot

    COP_Carnot = T_hot_rated /
                 (T_hot_rated - T_ambient)

    The catalog ambient range is 0–46 °C.
    """

    T_ambient = np.asarray(T_ambient)

    # Convert to Kelvin
    T_ambient_K = T_ambient + 273.15

    # Carnot COP based on catalog rated hot-water temperature
    COP_carnot = (
        T_hot_rated_K /
        (T_hot_rated_K - T_ambient_K)
    )

    gamma = COP_rated / COP_carnot

    return gamma


# ============================================================
# 5. DYNAMIC HEAT PUMP COP
# ============================================================

def calculate_COP_hp(T_ambient):
    """
    Calculate heat-pump COP using dynamic gamma.

    gamma is calculated from the catalog.
    Actual COP is then evaluated at the specified
    operating hot-water temperature.
    """

    gamma = calculate_gamma(T_ambient)

    T_hot_K = T_hot + 273.15
    T_ambient_K = np.asarray(T_ambient) + 273.15

    delta_T = T_hot_K - T_ambient_K

    COP_carnot_actual = T_hot_K / delta_T

    COP_hp = gamma * COP_carnot_actual

    return COP_hp


# ============================================================
# 6. SYSTEM MODEL
# ============================================================

def calculate_system(
        T_ambient,
        G_t,
        Collector_Area,
        eff):

    # --------------------------------------------------------
    # Solar collector mass flow rate
    # --------------------------------------------------------

    m_dot = 0.02 * Collector_Area

    # --------------------------------------------------------
    # Solar thermal energy supplied
    # --------------------------------------------------------

    Q_solar = Collector_Area * G_t * eff

    # --------------------------------------------------------
    # Temperature rise produced by solar collector
    # --------------------------------------------------------

    delta_T_solar = Q_solar / (m_dot * Cp)

    T_hp_inlet_raw = T_cold + delta_T_solar

    # HP inlet cannot exceed desired outlet temperature
    # Otherwise the heat pump would have negative heating load.
    T_hp_inlet = min(T_hp_inlet_raw, T_hot)

    # --------------------------------------------------------
    # Remaining thermal load for heat pump
    # --------------------------------------------------------

    Q_thermal = (
        m_dot * Cp *
        max(T_hot - T_hp_inlet, 0)
    )

    # --------------------------------------------------------
    # Standby heat loss
    # --------------------------------------------------------

    Q_standby = (
        3.95 *
        max(T_hot - T_hp_inlet, 0)
        / standby_R
    )

    # --------------------------------------------------------
    # Total heat-pump thermal requirement
    # --------------------------------------------------------

    Q_total = (
        heating_factor * Q_thermal
        + Q_standby
    )

    # --------------------------------------------------------
    # Dynamic COP
    # --------------------------------------------------------

    COP_hp = calculate_COP_hp(T_ambient)

    # --------------------------------------------------------
    # Electrical power consumption
    # --------------------------------------------------------

    W_electrical = Q_total / COP_hp

    # --------------------------------------------------------
    # Overall system COP
    # --------------------------------------------------------

    useful_heat = (
        m_dot * Cp *
        (T_hot - T_cold)
        * heating_factor
        + Q_standby
    )

    if W_electrical > 0:
        COP_system = useful_heat / W_electrical
    else:
        COP_system = np.nan


    # Solar fraction

    total_available_heat = Q_solar + max(Q_thermal, 0)

    if total_available_heat > 0:

        Solar_fraction = (
            Q_solar /
            total_available_heat
        )

    else:

        Solar_fraction = 0

    return (
        T_hp_inlet,
        Q_solar,
        Q_thermal,
        Q_standby,
        COP_hp,
        W_electrical,
        COP_system,
        Solar_fraction
    )


# 7. VARIABLE PARAMETERS

T_ambient_range = np.linspace(
    15, 18, 100
)

G_t_range = np.linspace(
    600, 1000, 100
)

Collector_area_range = np.linspace(
    2, 8, 100
)

eff_range = np.linspace(
    0.50, 0.75, 100
)


# 8. PLOT: GAMMA VS AMBIENT TEMPERATURE

T_ambient_gamma = np.linspace(
    T_ambient_min_catalog,
    T_ambient_max_catalog,
    300
)

gamma_values = calculate_gamma(
    T_ambient_gamma
)

plt.figure(figsize=(8, 5))

plt.plot(
    T_ambient_gamma,
    gamma_values,
    linewidth=2
)

plt.scatter(
    [T_ambient_min_catalog,
     T_ambient_max_catalog],
    [gamma_max, gamma_min]
)

plt.xlabel("Ambient Temperature (°C)")
plt.ylabel("Gamma (γ)")
plt.title("Dynamic γ Based on Heat Pump Catalog")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# 9. PLOT: GAMMA VS TEMPERATURE LIFT

T_hot_gamma = T_hot_rated_K

T_lift = (
    T_hot_gamma -
    (T_ambient_gamma + 273.15)
)

plt.figure(figsize=(8, 5))

plt.plot(
    T_lift,
    gamma_values,
    linewidth=2
)

plt.xlabel(
    "Temperature Lift, ΔT = T_hot − T_ambient (K)"
)

plt.ylabel("Gamma (γ)")

plt.title(
    "γ vs Temperature Lift"
)

plt.grid(True, alpha=0.3)

plt.gca().invert_xaxis()

plt.tight_layout()
plt.show()


# 10. SOLAR IRRADIANCE VS HP INLET TEMPERATURE

T_inlet = []

for G in G_t_range:

    result = calculate_system(
        T_ambient=18,
        G_t=G,
        Collector_Area=4,
        eff=0.65
    )

    T_inlet.append(result[0])


plt.figure(figsize=(8, 5))

plt.plot(
    G_t_range,
    T_inlet,
    linewidth=2
)

plt.xlabel("Solar Irradiance (W/m²)")
plt.ylabel("HP Inlet Temperature (°C)")
plt.title("Solar Irradiance vs HP Inlet Temperature")

plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# 11. COLLECTOR AREA VS HP INLET TEMPERATURE

T_inlet = []

for A in Collector_area_range:

    result = calculate_system(
        T_ambient=18,
        G_t=800,
        Collector_Area=A,
        eff=0.65
    )

    T_inlet.append(result[0])


plt.figure(figsize=(8, 5))

plt.plot(
    Collector_area_range,
    T_inlet,
    linewidth=2
)

plt.xlabel("Collector Area (m²)")
plt.ylabel("HP Inlet Temperature (°C)")
plt.title("Collector Area Effect")

plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# 12. AMBIENT TEMPERATURE VS HEAT PUMP COP

COPs = []

for Ta in T_ambient_range:

    result = calculate_system(
        T_ambient=Ta,
        G_t=800,
        Collector_Area=4,
        eff=0.65
    )

    COPs.append(result[4])


plt.figure(figsize=(8, 5))

plt.plot(
    T_ambient_range,
    COPs,
    linewidth=2
)

plt.xlabel("Ambient Temperature (°C)")
plt.ylabel("Heat Pump COP")
plt.title("Ambient Temperature Effect on Dynamic COP")

plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# 13. SOLAR IRRADIANCE VS ELECTRICAL CONSUMPTION

W = []

for G in G_t_range:

    result = calculate_system(
        T_ambient=18,
        G_t=G,
        Collector_Area=4,
        eff=0.65
    )

    W.append(result[5])


plt.figure(figsize=(8, 5))

plt.plot(
    G_t_range,
    W,
    linewidth=2
)

plt.xlabel("Solar Irradiance (W/m²)")
plt.ylabel("Electrical Power (W)")
plt.title("Solar Irradiance vs Electrical Consumption")

plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# 14. COLLECTOR AREA VS OVERALL SYSTEM COP

COP_sys = []

for A in Collector_area_range:

    result = calculate_system(
        T_ambient=18,
        G_t=800,
        Collector_Area=A,
        eff=0.65
    )

    COP_sys.append(result[6])


plt.figure(figsize=(8, 5))

plt.plot(
    Collector_area_range,
    COP_sys,
    linewidth=2
)

plt.xlabel("Collector Area (m²)")
plt.ylabel("Overall System COP")
plt.title("Collector Area vs Overall System COP")

plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# 15. SOLAR FRACTION VS COLLECTOR AREA

Solar_fractions = []

for A in Collector_area_range:

    result = calculate_system(
        T_ambient=18,
        G_t=800,
        Collector_Area=A,
        eff=0.65
    )

    Solar_fractions.append(result[7])


plt.figure(figsize=(8, 5))

plt.plot(
    Collector_area_range,
    Solar_fractions,
    linewidth=2
)

plt.xlabel("Collector Area (m²)")
plt.ylabel("Solar Fraction")
plt.title("Collector Area vs Solar Fraction")

plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# 16. EFFICIENCY VS SYSTEM COP

COP_efficiency = []

for eff in eff_range:

    result = calculate_system(
        T_ambient=18,
        G_t=800,
        Collector_Area=4,
        eff=eff
    )

    COP_efficiency.append(result[6])


plt.figure(figsize=(8, 5))

plt.plot(
    eff_range,
    COP_efficiency,
    linewidth=2
)

plt.xlabel("Solar Collector Efficiency")
plt.ylabel("Overall System COP")
plt.title("Collector Efficiency vs System COP")

plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# 17. PRINT REPRESENTATIVE OPERATING POINT

Ta_test = 18
G_test = 800
A_test = 4
eff_test = 0.65

result = calculate_system(
    T_ambient=Ta_test,
    G_t=G_test,
    Collector_Area=A_test,
    eff=eff_test
)

(
    T_hp_inlet,
    Q_solar,
    Q_thermal,
    Q_standby,
    COP_hp,
    W_electrical,
    COP_system,
    Solar_fraction
) = result

gamma_test = calculate_gamma(Ta_test)

print("\n" + "=" * 65)
print("REPRESENTATIVE SYSTEM OPERATING POINT")
print("=" * 65)

print(f"Ambient temperature       : {Ta_test:.2f} °C")
print(f"Solar irradiance          : {G_test:.1f} W/m²")
print(f"Collector area            : {A_test:.2f} m²")
print(f"Collector efficiency      : {eff_test:.3f}")

print(f"\nDynamic gamma             : {gamma_test:.4f}")
print(f"HP inlet temperature      : {T_hp_inlet:.2f} °C")
print(f"Solar thermal input       : {Q_solar:.2f} W")
print(f"Heat pump thermal load    : {Q_thermal:.2f} W")
print(f"Standby heat loss         : {Q_standby:.2f} W")
print(f"Heat pump COP             : {COP_hp:.3f}")
print(f"Electrical power          : {W_electrical:.2f} W")
print(f"Overall system COP        : {COP_system:.3f}")
print(f"Solar fraction            : {Solar_fraction:.3f}")