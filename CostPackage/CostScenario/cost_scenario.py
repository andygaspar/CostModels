import os
from typing import Callable

import pandas as pd
import numpy as np

lcc_airlines = pd.read_csv(os.path.join(os.path.dirname(__file__), "2017-LCC.csv"))

lev_1_airports = pd.read_csv(os.path.join(os.path.dirname(__file__), "airportMore25M.csv"))


def get_cost_scenario(airline: str, destination: str) -> str:
    if airline in lcc_airlines.airline.to_list():
        return "low"
    else:
        if destination in lev_1_airports.Airport.to_list():
            return "high"
    return "base"
