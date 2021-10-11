import os
from typing import Callable
import pandas as pd

df_crew = pd.read_csv(os.path.join(os.path.dirname(__file__), "2019-TacticalCrewCosts.csv"))
df_maintenance = pd.read_csv(os.path.join(os.path.dirname(__file__), "2019-TacticalMaintenanceCosts.csv"))


def get_maintenance_and_crew_costs(aircraft_cluster: str, scenario: str) -> Callable:
    entry_scenario = 'LowScenario' if scenario== "low" else 'BaseScenario' if scenario == 'base' else 'HighScenario'
    crew_cost = df_crew[(df_crew.Aircraft == aircraft_cluster)][entry_scenario].iloc[0]
    maintenance_cost = df_maintenance[(df_maintenance.Aircraft == aircraft_cluster)][entry_scenario].iloc[0]

    return lambda delay: (crew_cost + maintenance_cost) * delay
