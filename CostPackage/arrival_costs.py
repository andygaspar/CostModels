import copy

import pandas as pd
import os
from typing import Callable, List, Tuple
from CostPackage.Hard.hard_costs import get_hard_costs
from CostPackage.Cluster.cluster import get_aircraft_cluster, ClusterError
from CostPackage.MaintenanceCrew.maintenance_crew_costs import get_maintenance_and_crew_costs
from CostPackage.CostScenario.cost_scenario import get_cost_scenario
from CostPackage.Soft.soft_costs import get_soft_costs
from CostPackage.Passengers.passengers import get_passengers


def get_cost_model(aircraft_type: str, airline: str, destination: str, n_passengers: int = None,
                   missed_connected: List[Tuple] = None, length: float = None) -> Callable:
    try:
        aircraft_cluster = get_aircraft_cluster(aircraft_type=aircraft_type)
        cost_scenario = get_cost_scenario(airline=airline, destination=destination)

        if n_passengers is None:
            n_passengers = get_passengers(aircraft_cluster, cost_scenario)

        if missed_connected is not None:
            n_missed_connected = len(missed_connected)
            n_passengers -= n_missed_connected

        hard_costs = get_hard_costs(passengers=n_passengers, aircraft=aircraft_cluster, scenario=cost_scenario,
                                    length=length)
        soft_costs = get_soft_costs(passengers=n_passengers, scenario=cost_scenario)
        maintenance_crew_costs = get_maintenance_and_crew_costs(aircraft_cluster=aircraft_cluster,
                                                                scenario=cost_scenario)

        if missed_connected is not None:
            hard_costs_mc = get_hard_costs(passengers=1, aircraft=aircraft_cluster, scenario=cost_scenario,
                                           length=length)
            soft_costs_mc = get_soft_costs(passengers=1, scenario=cost_scenario)
            hc_mp = lambda delay, passenger: hard_costs_mc(delay) if delay < passenger[0] else hard_costs_mc(
                passenger[1])

            sc_mp = lambda delay, passenger: soft_costs_mc(delay) if delay < passenger[0] else soft_costs_mc(
                passenger[1])
            return lambda delay: hard_costs(delay) + soft_costs(delay) + maintenance_crew_costs(delay) + sum(
                hc_mp(delay, passenger) for passenger in missed_connected) + sum(
                sc_mp(delay, passenger) for passenger in missed_connected)

        return lambda delay: hard_costs(delay) + soft_costs(delay) + maintenance_crew_costs(delay)

    except ClusterError as cl_error:
        print(cl_error.message)


def get_data_dict():
    data_dict = {
        "aircraft": pd.read_csv(os.path.join(os.path.dirname(__file__), "Cluster/aircraftClustering.csv")),
        "aircraft_seats": pd.read_csv(os.path.join(os.path.dirname(__file__), "Passengers/2019-AircraftSeats.csv")),
        "airports": pd.read_csv(os.path.join(os.path.dirname(__file__), "CostScenario/airportMore25M.csv")),
        "hard": pd.read_csv(os.path.join(os.path.dirname(__file__), "Hard/2019-PassengerHardCostsBaseScenario.csv")),
        "crew": pd.read_csv(os.path.join(os.path.dirname(__file__), "MaintenanceCrew/2019-TacticalCrewCosts.csv")),
        "maintenance": pd.read_csv(os.path.join(os.path.dirname(__file__),
                                                "MaintenanceCrew/2019-TacticalMaintenanceCosts.csv")),
        "soft": pd.read_csv(os.path.join(os.path.dirname(__file__), "Soft/2019-PassengerSoftCosts.csv"))
    }
    return data_dict
