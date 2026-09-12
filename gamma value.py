import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# COMBINED SOLAR + HEAT PUMP WATER HEATER
# Calculation of Carnot COP and gamma
# ============================================================

# -----------------------------
# Given system specifications
# -----------------------------

COP_rated = 4.1                 # Rated COP
T_hot_C = 55                    # Rated hot water outlet temperature [°C]
T_ambient_min_C = 0             # Minimum ambient temperature [°C]
T_ambient_max_C = 46            # Maximum ambient temperature [°C]

# -----------------------------
# Convert temperatures to Kelvin
# -----------------------------

T_hot_K = T_hot_C + 273.15

T_ambient_C = np.linspace(
    T_ambient_min_C,
    T_ambient_max_C,
    200
)

T_ambient_K = T_ambient_C + 273.15

# -----------------------------
# Temperature lift
# -----------------------------

Delta_T = T_hot_K - T_ambient_K

# -----------------------------
# Carnot COP for heat pump
# COP_Carnot = Th / (Th - Tc)
# -----------------------------

COP_carnot = T_hot_K / Delta_T

# -----------------------------
# Gamma
# gamma = COP_rated / COP_carnot
# -----------------------------

gamma = COP_rated / COP_carnot

# ============================================================
# Display important values
# ============================================================

print("=" * 60)
print("COMBINED SOLAR + HEAT PUMP WATER HEATER")
print("=" * 60)

print(f"Rated COP              = {COP_rated:.2f}")
print(f"Hot water temperature  = {T_hot_C:.1f} °C")
print(f"Hot water temperature  = {T_hot_K:.2f} K")
print(f"Ambient range          = {T_ambient_min_C} to "
      f"{T_ambient_max_C} °C")
print()

print(f"Maximum gamma = {gamma.max():.4f}")
print(f"Minimum gamma = {gamma.min():.4f}")

# ============================================================
# Calculate values at important ambient temperatures
# ============================================================

selected_temperatures = [0, 5, 10, 15, 20, 25, 30, 35, 40, 46]

results = []

for T_C in selected_temperatures:

    T_K = T_C + 273.15

    delta_T = T_hot_K - T_K

    COP_c = T_hot_K / delta_T

    gamma_value = COP_rated / COP_c

    results.append([
        T_C,
        delta_T,
        COP_c,
        COP_rated,
        gamma_value
    ])

# Create dataframe
df = pd.DataFrame(
    results,
    columns=[
        "Ambient Temperature (°C)",
        "Temperature Lift (K)",
        "Carnot COP",
        "Rated COP",
        "Gamma"
    ]
)

print("\nSelected operating points:\n")
print(df.to_string(index=False))

# ============================================================
# Plot 1: Gamma vs Temperature Lift
# ============================================================

plt.figure(figsize=(9, 6))

plt.plot(
    Delta_T,
    gamma,
    linewidth=2
)

plt.xlabel("Temperature Lift, ΔT = T_hot − T_ambient (K)")
plt.ylabel("γ = COP_rated / COP_Carnot")
plt.title("Gamma vs Temperature Lift")
plt.grid(True, alpha=0.3)

# Reverse x-axis so increasing ambient temperature
# corresponds to movement from left to right
plt.gca().invert_xaxis()

plt.tight_layout()
plt.show()

# ============================================================
# Plot 2: Gamma vs Ambient Temperature
# ============================================================

plt.figure(figsize=(9, 6))

plt.plot(
    T_ambient_C,
    gamma,
    linewidth=2
)

plt.xlabel("Ambient Temperature (°C)")
plt.ylabel("γ = COP_rated / COP_Carnot")
plt.title("Gamma vs Ambient Temperature")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================================
# Plot 3: Carnot COP vs Temperature Lift
# ============================================================

plt.figure(figsize=(9, 6))

plt.plot(
    Delta_T,
    COP_carnot,
    linewidth=2
)

plt.xlabel("Temperature Lift, ΔT (K)")
plt.ylabel("Carnot COP")
plt.title("Carnot COP vs Temperature Lift")
plt.grid(True, alpha=0.3)

plt.gca().invert_xaxis()

plt.tight_layout()
plt.show()