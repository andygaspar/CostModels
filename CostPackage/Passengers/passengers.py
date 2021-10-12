import os
import pandas as pd

df_seats = pd.read_csv(os.path.join(os.path.dirname(__file__), "2019-AircraftSeats.csv"))

wide_body_list = ['B763', 'B744', 'A332']


def get_passengers(aircraft_cluster: str, scenario: str) -> int:
    entry_scenario = 'SeatsLow' if scenario == "low" else 'SeatsBase' if scenario == 'base' else 'SeatsHigh'

    seats = df_seats[(df_seats.Aircraft == aircraft_cluster)][entry_scenario].iloc[0]

    if scenario == "low":
        return round(seats * .65)
    elif scenario == "high":
        return round(seats * .95)
    elif aircraft_cluster in wide_body_list:
        return round(seats * .85)
    return round(seats * .80)
