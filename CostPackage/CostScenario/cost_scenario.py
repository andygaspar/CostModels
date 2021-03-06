import os
import pandas as pd

lcc_airlines = pd.read_csv(os.path.join(os.path.dirname(__file__), "2017-LCC.csv"))
group_1_airports = pd.read_csv(os.path.join(os.path.dirname(__file__), "airportMore25M.csv"))


def get_cost_scenario(airline: str, destination: str) -> str:
    if airline in lcc_airlines.airline.to_list():
        return "low"
    else:
        if destination in group_1_airports.Airport.to_list():
            return "high"
    return "base"
