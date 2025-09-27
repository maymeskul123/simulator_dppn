# Настройки симуляции
SIMULATION_CONFIG = {
    "population_size": 1000,
    "simulation_days": 365,
    "initial_pp_supply": 100000,
    "basic_income_amount": 100,
    "education_voucher_value": 50,
    "healthcare_cost": 30,
    "tax_rate": 0.1,
    "inflation_target": 0.02
}

AGENT_TYPES = {
    "worker": {"base_income": 150, "risk_aversion": 0.7},
    "entrepreneur": {"base_income": 200, "risk_aversion": 0.3},
    "student": {"base_income": 80, "risk_aversion": 0.5},
    "retiree": {"base_income": 120, "risk_aversion": 0.9}
}