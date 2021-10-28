import os
from typing import Callable
import pandas as pd
import numpy as np

df_soft = pd.read_csv(os.path.join(os.path.dirname(__file__), "2019-PassengerSoftCosts.csv"))


def get_interpolated_value(delay, costs, delays):
    if delay < delays[0]:
        return (delay) * (costs[0]) / (delays[0])
    for i in range(delays.shape[0] - 1):
        if delays[i] <= delay < delays[i + 1]:
            return (delay - delays[i]) * (costs[i + 1] - costs[i]) / (delays[i + 1] - delays[i]) + costs[i]
    return costs[-1]


def get_soft_costs(passengers: int, scenario: str) -> Callable:
    entry_scenario = 'LowScenario' if scenario == "low" else 'BaseScenario' if scenario == 'base' else 'HighScenario'

    costs = df_soft[entry_scenario].to_numpy()
    delays = df_soft.Delay.to_numpy()
    discount_factor = 0.1

    return lambda d: get_interpolated_value(d, costs, delays) * passengers * d * discount_factor
