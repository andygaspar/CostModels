from typing import Callable
import os
import pandas as pd

df_curfew = pd.read_csv(os.path.join(os.path.dirname(__file__), "curfew.csv"))


def get_curfew_value(air_cluster: str, n_pax_last_aircraft_rotation: int = None) -> float:

    if n_pax_last_aircraft_rotation is None:
        fixed_costs = df_curfew[df_curfew.AirCluster == air_cluster].Fixed.iloc[0]
        return fixed_costs

    else:
        compensation = 300
        fixed_costs = df_curfew[df_curfew.AirCluster == air_cluster].Cost.iloc[0]
        return fixed_costs + n_pax_last_aircraft_rotation * compensation

