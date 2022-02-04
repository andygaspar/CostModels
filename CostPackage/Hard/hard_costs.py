from typing import Callable
import os

import numpy as np
import pandas as pd

# dataframe from deliverable D3.2 Industry  briefing  on updates  to  the  European cost of delay, Beacon Project, 2019
df_hard_reimbursement_rate = pd.read_csv(os.path.join(os.path.dirname(__file__), "reimbursementPaxRate.csv"))
df_hard_waiting_rate = pd.read_csv(os.path.join(os.path.dirname(__file__), "waitingPaxRate.csv"))
df_hard = pd.read_csv(os.path.join(os.path.dirname(__file__), "passengersHardCosts.csv"))

# from The cost of passenger delay to airlines in Europe, consultation document, UOW 2015
# confirmed in deliverable D3.2 Industry  briefing  on updates  to  the  European cost of delay, Beacon Project, 2019
WAITING_RATE = .8
REIMBURSEMENT_RATE = 0.2

# from The cost of passenger delay to airlines in Europe, consultation document, UOW 2015
WAITING_RATE_LOW_COST = .9
REIMBURSEMENT_RATE_LOW_COST = 0.1


def get_cost(cost_type: str, haul: str):
    return df_hard[df_hard.CostType == cost_type][haul]


def get_waiting_rate(cost_type: str, haul: str):
    return df_hard_waiting_rate[df_hard_waiting_rate.CostType == cost_type][haul]


def get_reimbursement_rate(cost_type: str, haul: str):
    return df_hard_reimbursement_rate[df_hard_reimbursement_rate.CostType == cost_type][haul]


def get_interval(delay, costs, delays):
    if delay < delays[0]:
        return 0
    for i in range(delays.shape[0] - 1):
        if delays[i] <= delay < delays[i + 1]:
            return costs[i]
    return costs[-1]


def get_hard_costs(passengers: int, scenario: str, haul: str) -> Callable:
    waiting_pax = passengers * (WAITING_RATE_LOW_COST if scenario == "low" else WAITING_RATE)
    reimbursement_pax = passengers * (REIMBURSEMENT_RATE_LOW_COST if scenario == "low" else REIMBURSEMENT_RATE)

    costs_waiting = ((get_cost("care", haul) * get_waiting_rate("care", haul)).to_numpy() +
                     (get_cost("reimbursement_rebooking", haul) * get_waiting_rate("reimbursement_rebooking",
                                                                                   haul)).to_numpy() +
                     (get_cost("compensation", haul) * get_waiting_rate("compensation", haul)).to_numpy() +
                     (get_cost("accommodation", haul) * get_waiting_rate("accommodation",
                                                                         haul)).to_numpy()
                     ) * waiting_pax

    costs_reimbursement = ((get_cost("care", haul) * get_reimbursement_rate("care", haul)).to_numpy() +
                           (get_cost("reimbursement_rebooking", haul) *
                            get_reimbursement_rate("reimbursement_rebooking", haul)).to_numpy() +
                           (get_cost("compensation", haul) *
                            get_reimbursement_rate("compensation", haul)).to_numpy() +
                           (get_cost("accommodation", haul) *
                            get_reimbursement_rate("accommodation", haul)).to_numpy()
                           ) * reimbursement_pax

    delays = np.array([120, 180, 240, 300, 600])
    costs = costs_waiting + costs_reimbursement

    return lambda d: get_interval(d, costs, delays)
