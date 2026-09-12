import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI

# =====================================================
# INPUT PARAMETERS
# =====================================================

T_in = 15.0               # °C
T_out = 55.0              # °C

m_dot_water = 0.03        # kg/s

P_water = 101325          # Pa

collector_area = 4.0      # m²
eta_collector = 0.77

evap_temp = 10.0          # °C
cond_temp = 60.0          # °C

eta_isen = 0.70
eta_motor = 0.85

fluid = 'R134a'

# =====================================================
# WATER PROPERTIES
# =====================================================

h1 = PropsSI(
    'H',
    'T',
    T_in + 273.15,
    'P',
    P_water,
    'Water'
)/1000

h3 = PropsSI(
    'H',
    'T',
    T_out + 273.15,
    'P',
    P_water,
    'Water'
)/1000

# =====================================================
# SOLAR INPUT
# =====================================================

G_t = 800        # W/m²

Q_solar = eta_collector * collector_area * G_t

h2 = h1 + Q_solar/(m_dot_water*1000)

# =====================================================
# R134A STATES
# =====================================================

P_evap = PropsSI(
    'P',
    'T',
    evap_temp + 273.15,
    'Q',
    1,
    fluid
)

P_cond = PropsSI(
    'P',
    'T',
    cond_temp + 273.15,
    'Q',
    0,
    fluid
)

# State 1
h_evap = PropsSI(
    'H',
    'P',
    P_evap,
    'Q',
    1,
    fluid
)/1000

s_evap = PropsSI(
    'S',
    'P',
    P_evap,
    'Q',
    1,
    fluid
)

# Ideal compressor discharge
h2s = PropsSI(
    'H',
    'P',
    P_cond,
    'S',
    s_evap,
    fluid
)/1000

# Actual discharge
h_cond2 = h_evap + (h2s - h_evap)/eta_isen

# Condenser exit
h_cond3 = PropsSI(
    'H',
    'P',
    P_cond,
    'Q',
    0,
    fluid
)/1000

# =====================================================
# ENERGY BALANCE
# =====================================================

Q_required = m_dot_water*(h3-h2)

m_dot_r = Q_required/(h_cond2-h_cond3)

W_comp = m_dot_r*(h_cond2-h_evap)

W_electric = W_comp/eta_motor

COP_system = m_dot_water*(h3-h1)/W_electric

# =====================================================
# OUTPUTS
# =====================================================

print(f"Solar Heat Gain = {Q_solar:.2f} W")
print(f"Refrigerant Flow Rate = {m_dot_r:.4f} kg/s")
print(f"Electrical Power = {W_electric:.2f} kW")
print(f"System COP = {COP_system:.2f}")

irradiance = np.linspace(100,1000,50)

COP = []

for G in irradiance:

    Q_solar = eta_collector*collector_area*G

    h2 = h1 + Q_solar/(m_dot_water*1000)

    Q_required = m_dot_water*(h3-h2)

    m_dot_r = Q_required/(h_cond2-h_cond3)

    W_electric = (
        m_dot_r*(h_cond2-h_evap)
    )/eta_motor

    COP.append((
        m_dot_water*(h3-h1)*0.85*0.7)/W_electric
    )

plt.figure(figsize=(8,5))
plt.plot(irradiance,COP,linewidth=2)
plt.xlabel('Solar Irradiance (W/m²)')
plt.ylabel('System COP')
plt.title('COP vs Solar Irradiance')
plt.grid()
plt.show()

areas = np.linspace(1,10,40)

COP_area = []

for A in areas:

    Q_solar = eta_collector*A*G_t

    h2 = h1 + Q_solar/(m_dot_water*1000)

    Q_required = m_dot_water*(h3-h2)

    m_dot_r = Q_required/(h_cond2-h_cond3)

    W_electric = (
        m_dot_r*(h_cond2-h_evap)
    )/eta_motor

    COP_area.append((
        m_dot_water*(h3-h1)*0.7*0.85)/W_electric)


plt.figure(figsize=(8,5))
plt.plot(areas,COP_area)
plt.xlabel('Collector Area (m²)')
plt.ylabel('System COP')
plt.title('COP vs Collector Area')
plt.grid()
plt.show()

hours = np.arange(6,19)

ambient = np.array([
10,12,15,18,21,24,
26,27,26,24,21,18,15
])

irradiance = np.array([
0,150,350,550,700,
850,950,900,800,
600,350,100,0
])

COP_hourly = []

for Ta,G in zip(ambient,irradiance):

    evap_temp = Ta - 5

    P_evap = PropsSI(
        'P',
        'T',
        evap_temp+273.15,
        'Q',
        1,
        fluid
    )

    h_evap = PropsSI(
        'H',
        'P',
        P_evap,
        'Q',
        1,
        fluid
    )/1000

    s_evap = PropsSI(
        'S',
        'P',
        P_evap,
        'Q',
        1,
        fluid
    )

    h2s = PropsSI(
        'H',
        'P',
        P_cond,
        'S',
        s_evap,
        fluid
    )/1000

    h_cond2 = h_evap + (
        h2s-h_evap
    )/eta_isen

    Q_solar = eta_collector*collector_area*G

    h2 = h1 + Q_solar/(m_dot_water*1000)

    Q_required = m_dot_water*(h3-h2)

    m_dot_r = Q_required/(h_cond2-h_cond3)

    W_electric = (
        m_dot_r*(h_cond2-h_evap)
    )/eta_motor

    COP = (
        m_dot_water*(h3-h1)
    )/W_electric

    COP_hourly.append(COP)

plt.figure(figsize=(10,5))
plt.plot(hours,COP_hourly,marker='o')
plt.xlabel('Hour of Day')
plt.ylabel('System COP')
plt.title('Kathmandu Hourly COP Variation')
plt.grid()
plt.show()

from CoolProp.CoolProp import PropsSI

def calculate_COP(G_t, T_amb,
                  collector_area=4.0,
                  eta_collector=0.77,
                  T_in=15.0,
                  T_out=55.0,
                  m_dot_water=0.03,
                  eta_isen=0.70,
                  eta_motor=0.85):

    fluid = "R134a"

    # -------------------------
    # Water Side
    # -------------------------
    h1 = PropsSI(
        'H',
        'T',
        T_in + 273.15,
        'P',
        101325,
        'Water'
    )/1000

    h3 = PropsSI(
        'H',
        'T',
        T_out + 273.15,
        'P',
        101325,
        'Water'
    )/1000

    # -------------------------
    # Solar Collector
    # -------------------------
    Q_solar = eta_collector * collector_area * G_t

    h2 = h1 + Q_solar/(m_dot_water*1000)

    # -------------------------
    # Heat Pump
    # -------------------------

    evap_temp = T_amb - 5
    cond_temp = 60

    P_evap = PropsSI(
        'P',
        'T',
        evap_temp + 273.15,
        'Q',
        1,
        fluid
    )

    P_cond = PropsSI(
        'P',
        'T',
        cond_temp + 273.15,
        'Q',
        0,
        fluid
    )

    h_evap = PropsSI(
        'H',
        'P',
        P_evap,
        'Q',
        1,
        fluid
    )/1000

    s_evap = PropsSI(
        'S',
        'P',
        P_evap,
        'Q',
        1,
        fluid
    )

    h2s = PropsSI(
        'H',
        'P',
        P_cond,
        'S',
        s_evap,
        fluid
    )/1000

    h_cond2 = h_evap + (h2s-h_evap)/eta_isen

    h_cond3 = PropsSI(
        'H',
        'P',
        P_cond,
        'Q',
        0,
        fluid
    )/1000

    # -------------------------
    # Energy Balance
    # -------------------------

    Q_required = m_dot_water*(h3-h2)

    if Q_required <= 0:
        return np.nan

    m_dot_r = Q_required/(h_cond2-h_cond3)

    W_elec = (
        m_dot_r*(h_cond2-h_evap)
    )/eta_motor

    COP = (
        m_dot_water*(h3-h1)
    *0.7*0.85)/W_elec

    return COP

G_range = np.linspace(100,1000,40)
Ta_range = np.linspace(5,35,40)

G_mesh, Ta_mesh = np.meshgrid(
    G_range,
    Ta_range
)

COP_map = np.zeros_like(G_mesh)

for i in range(len(Ta_range)):
    for j in range(len(G_range)):

        COP_map[i,j] = calculate_COP(
            G_mesh[i,j],
            Ta_mesh[i,j]
        )

plt.figure(figsize=(10,6))

contour = plt.contourf(
    G_mesh,
    Ta_mesh,
    COP_map,
    levels=20
)

plt.colorbar(contour,label="COP")

plt.xlabel("Solar Irradiance (W/m²)")
plt.ylabel("Ambient Temperature (°C)")
plt.title("Solar-Assisted Heat Pump COP Map")

plt.show()