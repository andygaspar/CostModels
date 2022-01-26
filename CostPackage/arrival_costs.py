import pandas as pd
import os
from typing import Callable, List, Tuple, Union
from CostPackage.Hard.hard_costs import get_hard_costs
from CostPackage.Cluster.cluster import get_aircraft_cluster, ClusterError
from CostPackage.MaintenanceCrew.maintenance_crew_costs import get_maintenance_and_crew_costs
from CostPackage.CostScenario.cost_scenario import get_cost_scenario
from CostPackage.Soft.soft_costs import get_soft_costs
from CostPackage.Passengers.passengers import get_passengers
from CostPackage.Curfew.curfew import get_curfew_value


def get_cost_model(aircraft_type: str, airline: str, destination: str, n_passengers: int = None,
                   missed_connected: List[Tuple] = None, length: float = None, self_curfew: float = None,
                   react_curfew: Union[tuple[float, str], tuple[float, int]] = None) -> Callable:
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
            cost_fun = lambda delay: hard_costs(delay) + soft_costs(delay) + maintenance_crew_costs(delay) + sum(
                hc_mp(delay, passenger) for passenger in missed_connected) + sum(
                sc_mp(delay, passenger) for passenger in missed_connected)

        else:
            cost_fun = lambda delay: hard_costs(delay) + soft_costs(delay) + maintenance_crew_costs(delay)

        if self_curfew is None and react_curfew is None:
            return cost_fun

        else:
            if self_curfew is not None:
                curfew_threshold = self_curfew
                curfew_passengers = n_passengers if missed_connected is None else n_passengers + len(missed_connected)
            else:
                curfew_threshold = react_curfew[0]
                curfew_passengers = get_passengers(aircraft_cluster, get_cost_scenario(airline, react_curfew[1])) \
                    if type(react_curfew[1]) == str else react_curfew[1]

            return lambda delay: cost_fun(delay) if delay < curfew_threshold \
                else get_curfew_value(aircraft_cluster, cost_scenario, curfew_passengers)

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
