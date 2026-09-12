# ================================================================
# CSHPWH - BOX-BEHNKEN DESIGN OF EXPERIMENT
# 4 Factors / 3 Levels
# Using pyDOE3
# ================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pyDOE3 import bbdesign
import statsmodels.api as sm
from statsmodels.formula.api import ols


# ================================================================
# 1. SYSTEM PARAMETERS
# ================================================================

# Target hot-water temperature
T_hot = 55.0                         # deg C

# Practical heat-pump performance factor
# COP_HP = gamma * COP_Carnot
gamma = 0.45

# Solar collector efficiency
eta_col = 0.65

# Water properties
Cp_water = 4180                       # J/(kg.K)
rho_water = 1000                      # kg/m^3

# Solar water mass flow rate
# Assumed 0.02 kg/s per m2 of collector
m_dot_per_area = 0.02                 # kg/s/m2

# Solar circulation pump power
P_pump_per_area = 15                  # W/m2

# Approximate tank/piping heat-loss factor
standby_loss = 0.02                   # 2%


# ================================================================
# 2. DOE FACTORS AND THEIR THREE LEVELS
# ================================================================

# Factor:
# G_t     = solar irradiance
# T_amb   = ambient temperature
# T_cold  = cold-water inlet temperature
# A_c     = collector area

factor_levels = {

    "G_t": {
        -1: 600,
         0: 800,
         1: 1000
    },

    "T_amb": {
        -1: 15.0,
         0: 16.5,
         1: 18.0
    },

    "T_cold": {
        -1: 20.0,
         0: 30.0,
         1: 40.0
    },

    "A_c": {
        -1: 2.0,
         0: 5.0,
         1: 8.0
    }
}


# ================================================================
# 3. GENERATE BOX-BEHNKEN DESIGN
# ================================================================

n_factors = 4

# Number of center points
n_center = 5

# Generate Box-Behnken design
# For 4 factors:
# Base BBD runs = 2*k*(k-1) = 24
# + 5 center points = 29 runs

bbd = bbdesign(
    n_factors,
    center=n_center
)

# Convert to DataFrame
doe_coded = pd.DataFrame(
    bbd,
    columns=[
        "G_t_code",
        "T_amb_code",
        "T_cold_code",
        "A_c_code"
    ]
)


# ================================================================
# 4. RANDOMIZE EXPERIMENTAL RUN ORDER
# ================================================================

# Randomization is important for experimental DOE
np.random.seed(42)

doe_coded = doe_coded.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

doe_coded.insert(
    0,
    "Run",
    np.arange(1, len(doe_coded) + 1)
)


# ================================================================
# 5. CONVERT CODED VARIABLES TO ACTUAL VALUES
# ================================================================

def decode_factor(code, levels):
    """
    Convert coded DOE value (-1, 0, +1)
    to actual experimental value.
    """
    return levels[int(code)]


doe = pd.DataFrame()

doe["Run"] = doe_coded["Run"]

doe["G_t"] = doe_coded["G_t_code"].apply(
    lambda x: decode_factor(x, factor_levels["G_t"])
)

doe["T_amb"] = doe_coded["T_amb_code"].apply(
    lambda x: decode_factor(x, factor_levels["T_amb"])
)

doe["T_cold"] = doe_coded["T_cold_code"].apply(
    lambda x: decode_factor(x, factor_levels["T_cold"])
)

doe["A_c"] = doe_coded["A_c_code"].apply(
    lambda x: decode_factor(x, factor_levels["A_c"])
)


# ================================================================
# 6. CSHPWH ANALYTICAL MODEL
# ================================================================

def calculate_cshpwh(G_t, T_amb, T_cold, A_c):

    # ------------------------------------------------------------
    # SOLAR COLLECTOR
    # ------------------------------------------------------------

    # Incident solar energy
    Q_solar_incident = G_t * A_c                       # W

    # Useful solar energy
    Q_solar = eta_col * Q_solar_incident               # W

    # Water mass flow rate
    m_dot = m_dot_per_area * A_c                       # kg/s

    # Temperature increase due to collector
    delta_T_solar = Q_solar / (m_dot * Cp_water)

    # Solar outlet / HP inlet temperature
    T_preheat = T_cold + delta_T_solar

    # Prevent preheated temperature from exceeding
    # the final hot-water setpoint
    T_preheat = min(T_preheat, T_hot)


    # ------------------------------------------------------------
    # HEAT PUMP COP
    # ------------------------------------------------------------

    T_hot_K = T_hot + 273.15
    T_amb_K = T_amb + 273.15

    # Ideal Carnot COP
    COP_carnot = (
        T_hot_K /
        (T_hot_K - T_amb_K)
    )

    # Actual/practical COP
    COP_HP = gamma * COP_carnot


    # ------------------------------------------------------------
    # HEAT REQUIRED FROM HEAT PUMP
    # ------------------------------------------------------------

    delta_T_HP = max(
        T_hot - T_preheat,
        0
    )

    Q_HP_ideal = (
        m_dot *
        Cp_water *
        delta_T_HP
    )

    # Include heat losses
    Q_HP = Q_HP_ideal * (1 + standby_loss)

    # HP electrical input
    P_HP = Q_HP / COP_HP


    # ------------------------------------------------------------
    # PUMP POWER
    # ------------------------------------------------------------

    P_pump = P_pump_per_area * A_c

    # Total electrical power
    P_total = P_HP + P_pump


    # ------------------------------------------------------------
    # TOTAL SYSTEM HEAT
    # ------------------------------------------------------------

    # Heat delivered by system
    Q_useful = Q_solar + Q_HP


    # ------------------------------------------------------------
    # SYSTEM COP
    # ------------------------------------------------------------

    if P_total > 0:
        COP_system = Q_useful / P_total
    else:
        COP_system = np.nan


    # ------------------------------------------------------------
    # SOLAR CONTRIBUTION
    # ------------------------------------------------------------

    if Q_useful > 0:
        solar_fraction = (
            Q_solar /
            Q_useful
        )
    else:
        solar_fraction = np.nan


    # Heat-pump contribution
    if Q_useful > 0:
        HP_fraction = Q_HP / Q_useful
    else:
        HP_fraction = np.nan


    # ------------------------------------------------------------
    # RETURN ALL RESPONSES
    # ------------------------------------------------------------

    return {

        "Q_solar_W": Q_solar,

        "T_preheat_C": T_preheat,

        "COP_carnot": COP_carnot,

        "COP_HP": COP_HP,

        "Q_HP_W": Q_HP,

        "P_HP_W": P_HP,

        "P_pump_W": P_pump,

        "P_total_W": P_total,

        "Q_useful_W": Q_useful,

        "COP_system": COP_system,

        "Solar_fraction": solar_fraction,

        "HP_fraction": HP_fraction
    }


# ================================================================
# 7. RUN THE COMPLETE DOE
# ================================================================

results = []

for _, row in doe.iterrows():

    result = calculate_cshpwh(

        G_t=row["G_t"],

        T_amb=row["T_amb"],

        T_cold=row["T_cold"],

        A_c=row["A_c"]
    )

    results.append(result)


results_df = pd.DataFrame(results)


# ================================================================
# 8. COMBINE DOE AND RESPONSES
# ================================================================

final_doe = pd.concat(
    [
        doe,
        results_df
    ],
    axis=1
)


# Add coded values
final_doe["G_t_code"] = doe_coded["G_t_code"]
final_doe["T_amb_code"] = doe_coded["T_amb_code"]
final_doe["T_cold_code"] = doe_coded["T_cold_code"]
final_doe["A_c_code"] = doe_coded["A_c_code"]


# ================================================================
# 9. REORDER COLUMNS
# ================================================================

final_doe = final_doe[
    [

        "Run",

        # Coded factors
        "G_t_code",
        "T_amb_code",
        "T_cold_code",
        "A_c_code",

        # Actual factors
        "G_t",
        "T_amb",
        "T_cold",
        "A_c",

        # Responses
        "Q_solar_W",
        "T_preheat_C",
        "COP_carnot",
        "COP_HP",
        "Q_HP_W",
        "P_HP_W",
        "P_pump_W",
        "P_total_W",
        "Q_useful_W",
        "COP_system",
        "Solar_fraction",
        "HP_fraction"
    ]
]


# ================================================================
# 10. ROUND DATA
# ================================================================

final_doe = final_doe.round(4)


# ================================================================
# 11. PRINT DOE
# ================================================================

pd.set_option(
    "display.max_columns",
    None
)

pd.set_option(
    "display.width",
    250
)

print("\n")
print("=" * 80)
print("CSHPWH BOX-BEHNKEN DESIGN")
print("=" * 80)

print(
    f"Number of factors       : {n_factors}"
)

print(
    f"Center points           : {n_center}"
)

print(
    f"Total experimental runs : {len(final_doe)}"
)

print("\nDOE MATRIX:\n")

print(final_doe.to_string(index=False))


# ================================================================
# 12. SAVE COMPLETE DOE TO EXCEL
# ================================================================

excel_filename = "CSHPWH_Box_Behnken_DOE_pyDOE3.xlsx"

final_doe.to_excel(
    excel_filename,
    index=False
)

print("\n")
print(f"DOE saved to: {excel_filename}")


# ================================================================
# 13. RESPONSE-SURFACE ANALYSIS
# ================================================================

print("\n")
print("=" * 80)
print("SECOND-ORDER RESPONSE SURFACE ANALYSIS")
print("=" * 80)


# ---------------------------------------------------------------
# Create formula terms
# ---------------------------------------------------------------

# We use coded factors for response-surface analysis because
# the coefficients then correspond directly to normalized factors.

formula_terms = """
Q_solar_W ~
G_t_code +
T_amb_code +
T_cold_code +
A_c_code +
I(G_t_code**2) +
I(T_amb_code**2) +
I(T_cold_code**2) +
I(A_c_code**2) +
G_t_code:T_amb_code +
G_t_code:T_cold_code +
G_t_code:A_c_code +
T_amb_code:T_cold_code +
T_amb_code:A_c_code +
T_cold_code:A_c_code
"""


# ---------------------------------------------------------------
# Fit models for important responses
# ---------------------------------------------------------------

responses_for_model = [

    "Q_solar_W",

    "T_preheat_C",

    "COP_HP",

    "P_total_W",

    "COP_system",

    "Solar_fraction"
]


for response in responses_for_model:

    formula = formula_terms.replace(
        "Q_solar_W",
        response
    )

    model = ols(
        formula,
        data=final_doe
    ).fit()

    print("\n")
    print("-" * 80)
    print(f"RESPONSE: {response}")
    print("-" * 80)

    print(model.summary())


# ================================================================
# 14. ANOVA FOR SYSTEM COP
# ================================================================

print("\n")
print("=" * 80)
print("ANOVA - SYSTEM COP")
print("=" * 80)


model_cop = ols(
    """
    COP_system ~
    G_t_code +
    T_amb_code +
    T_cold_code +
    A_c_code +
    I(G_t_code**2) +
    I(T_amb_code**2) +
    I(T_cold_code**2) +
    I(A_c_code**2) +
    G_t_code:T_amb_code +
    G_t_code:T_cold_code +
    G_t_code:A_c_code +
    T_amb_code:T_cold_code +
    T_amb_code:A_c_code +
    T_cold_code:A_c_code
    """,
    data=final_doe
).fit()


anova_cop = sm.stats.anova_lm(
    model_cop,
    typ=2
)

print(anova_cop)


# ================================================================
# 15. ANOVA FOR SOLAR FRACTION
# ================================================================

print("\n")
print("=" * 80)
print("ANOVA - SOLAR FRACTION")
print("=" * 80)


model_solar = ols(
    """
    Solar_fraction ~
    G_t_code +
    T_amb_code +
    T_cold_code +
    A_c_code +
    I(G_t_code**2) +
    I(T_amb_code**2) +
    I(T_cold_code**2) +
    I(A_c_code**2) +
    G_t_code:T_amb_code +
    G_t_code:T_cold_code +
    G_t_code:A_c_code +
    T_amb_code:T_cold_code +
    T_amb_code:A_c_code +
    T_cold_code:A_c_code
    """,
    data=final_doe
).fit()


anova_solar = sm.stats.anova_lm(
    model_solar,
    typ=2
)

print(anova_solar)


# ================================================================
# 16. FIND OPTIMUM EXPERIMENTAL RUN
# ================================================================

print("\n")
print("=" * 80)
print("OPTIMUM DOE CONDITIONS")
print("=" * 80)


# Maximum system COP
best_cop_index = final_doe[
    "COP_system"
].idxmax()

best_cop = final_doe.loc[
    best_cop_index
]


print("\nMaximum System COP:")
print(
    best_cop[
        [
            "Run",
            "G_t",
            "T_amb",
            "T_cold",
            "A_c",
            "COP_system",
            "P_total_W",
            "Solar_fraction"
        ]
    ]
)


# Maximum solar fraction
best_solar_index = final_doe[
    "Solar_fraction"
].idxmax()

best_solar = final_doe.loc[
    best_solar_index
]


print("\nMaximum Solar Fraction:")

print(
    best_solar[
        [
            "Run",
            "G_t",
            "T_amb",
            "T_cold",
            "A_c",
            "Solar_fraction",
            "T_preheat_C"
        ]
    ]
)


# Minimum electrical power
best_power_index = final_doe[
    "P_total_W"
].idxmin()

best_power = final_doe.loc[
    best_power_index
]


print("\nMinimum Total Electrical Power:")

print(
    best_power[
        [
            "Run",
            "G_t",
            "T_amb",
            "T_cold",
            "A_c",
            "P_total_W",
            "COP_system"
        ]
    ]
)


# ================================================================
# 17. RESPONSE PLOTS
# ================================================================

# ---------------------------------------------------------------
# System COP
# ---------------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.scatter(
    final_doe["Run"],
    final_doe["COP_system"]
)

plt.xlabel("Experimental Run")
plt.ylabel("System COP")

plt.title(
    "CSHPWH System COP - Box-Behnken Design"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ---------------------------------------------------------------
# Solar fraction
# ---------------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.scatter(
    final_doe["Run"],
    final_doe["Solar_fraction"]
)

plt.xlabel("Experimental Run")

plt.ylabel(
    "Solar Contribution Fraction"
)

plt.title(
    "Solar Contribution - Box-Behnken Design"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ---------------------------------------------------------------
# Solar preheating temperature
# ---------------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.scatter(
    final_doe["Run"],
    final_doe["T_preheat_C"]
)

plt.xlabel("Experimental Run")

plt.ylabel(
    "Preheated Water Temperature (°C)"
)

plt.title(
    "Solar Preheating Temperature"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ---------------------------------------------------------------
# Total electrical power
# ---------------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.scatter(
    final_doe["Run"],
    final_doe["P_total_W"]
)

plt.xlabel("Experimental Run")

plt.ylabel(
    "Total Electrical Power (W)"
)

plt.title(
    "CSHPWH Electrical Power Consumption"
)

plt.grid(True)

plt.tight_layout()

plt.show()


# ================================================================
# 18. DESCRIPTIVE STATISTICS
# ================================================================

print("\n")
print("=" * 80)
print("RESPONSE STATISTICS")
print("=" * 80)

response_columns = [

    "Q_solar_W",

    "T_preheat_C",

    "COP_carnot",

    "COP_HP",

    "Q_HP_W",

    "P_HP_W",

    "P_pump_W",

    "P_total_W",

    "Q_useful_W",

    "COP_system",

    "Solar_fraction",

    "HP_fraction"
]


print(
    final_doe[
        response_columns
    ].describe().round(4)
)


# ================================================================
# 19. END
# ================================================================

print("\n")
print("=" * 80)
print("CSHPWH DOE ANALYSIS COMPLETE")
print("=" * 80)