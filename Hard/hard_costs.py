from typing import Callable

import pandas as pd
import numpy as np

df_hard_base = pd.read_csv("Hard/2019-PassengerHardCostsBaseScenario.csv")

"""
to integrate with the new tables
"""
df_hard_low = pd.read_csv("Hard/2019-PassengerHardCostsBaseScenario.csv")
df_hard_high = pd.read_csv("Hard/2019-PassengerHardCostsBaseScenario.csv")

wide_body_list = ['B763', 'B744', 'A332']


def get_interval(delay, costs, delays):
    if delay < delays[0]:
        return 0
    for i in range(delays.shape[0] - 1):
        if delays[i] < delay < delays[i + 1]:
            return costs[i]
    return costs[-1]


def get_hard_costs(passengers: int, aircraft: str, scenario: str, length: float) -> Callable:
    if scenario == "high":
        df_hard = df_hard_high
    elif scenario == "base":
        df_hard = df_hard_base
    else:
        df_hard = df_hard_low

    if length is None:
        delays = df_hard.Delay.to_numpy()
        if aircraft in wide_body_list:
            costs = df_hard.LongHaul.to_numpy()
            return lambda d: get_interval(d, costs, delays) * passengers

        else:
            costs = df_hard.MediumHaul.to_numpy()
            return lambda d: get_interval(d, costs, delays) * passengers

    else:
        delays = df_hard.Delay.to_numpy()
        if length <= 1500:
            costs = df_hard.ShortHaul.to_numpy()
            return lambda d: get_interval(d, costs, delays) * passengers
        if length <= 3500:
            costs = df_hard.MediumHaul.to_numpy()
            return lambda d: get_interval(d, costs, delays) * passengers

        costs = df_hard.LongHaul.to_numpy()
        return lambda d: get_interval(d, costs, delays) * passengers
