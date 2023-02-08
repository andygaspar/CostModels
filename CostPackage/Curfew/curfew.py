from typing import Callable
import os
import pandas as pd

df_curfew = pd.read_csv(os.path.join(os.path.dirname(__file__), "curfew.csv"))

wide_body_list = ['B763', 'B744', 'A332']

# def get_curfew_value(air_cluster: str, cost_scenario: str, curfew_passengers: int) -> float:
#     if air_cluster in wide_body_list:
#         return curfew_passengers * 254 + 19230
#     elif cost_scenario == "low":
#         return curfew_passengers * 102.75
#     else:
#         return curfew_passengers * 136.59


# to improve
def get_curfew_value(air_cluster: str, cost_scenario: str, curfew_passengers: int) -> float:
    return curfew_passengers * 300 + df_curfew[df_curfew.AirCluster == air_cluster].Cost.iloc[0]
