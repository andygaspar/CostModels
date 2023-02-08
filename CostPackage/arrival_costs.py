import pandas as pd
import os
from typing import Callable, List, Tuple, Union

from matplotlib import pyplot as plt

from CostPackage.Hard.hard_costs import get_hard_costs
from CostPackage.Cluster.cluster import get_aircraft_cluster, ClusterError
from CostPackage.Haul.haul import get_haul
from CostPackage.MaintenanceCrew.maintenance_crew_costs import get_maintenance_and_crew_costs
from CostPackage.CostScenario.cost_scenario import get_cost_scenario
from CostPackage.Soft.soft_costs import get_soft_costs
from CostPackage.Passengers.passengers import get_passengers
from CostPackage.Curfew.curfew import get_curfew_value


def get_cost_model(aircraft_type: str, airline: str, destination: str, length: float, n_passengers: int,
                   missed_connected: List[Tuple] = None,
                   curfew: Union[tuple[float, int], float] = None) -> Callable:
    """Generate cost function of a given flight according to the specifics

    Parameters:
    aircraft_type (str):
        name of the aircraft type
    airline (str):
        airline's acronym (three letters), used to determine soft costs and maintenance costs
    destination (str)
        destination airport name
    length (float):
        length of the flight. Used to compute the Haul scenario Long >=3500km, 3500km > Medium >= 1500km, 1500km >= Short
    n_passengers (int):
        number of passengers
   missed_connected List[Tuple] default None,
        list of tuples. Each tuple represents one passenger and its composition is (delay threshold, delay perceived).
        The delay threshold is the time at which the passenger misses the connection.
        The delay perceived is the delay at the passenger final destination, generally computed considering the next
        available flight of the same airline which carries the pax to its final destination
    curfew: Tuple[curfew_time: float, n_passenger: int] or float, default None,
       react_curfew: Union[tuple[float, str], tuple[float, int]] = None

    Returns:
    lambda function

   """

    haul = get_haul(length=length)

    try:
        aircraft_cluster = get_aircraft_cluster(aircraft_type=aircraft_type)
        cost_scenario = get_cost_scenario(airline=airline, destination=destination)

        n_missed_connected = 0 if missed_connected is None else len(missed_connected)
        n_passengers -= n_missed_connected

        hard_costs = get_hard_costs(passengers=n_passengers, scenario=cost_scenario, haul=haul)

        soft_costs = get_soft_costs(passengers=n_passengers, scenario=cost_scenario)

        maintenance_crew_costs = get_maintenance_and_crew_costs(aircraft_cluster=aircraft_cluster,
                                                                scenario=cost_scenario)

        if n_missed_connected > 0:
            hard_costs_mc = get_hard_costs(passengers=1, scenario=cost_scenario, haul=haul)
            soft_costs_mc = get_soft_costs(passengers=1, scenario=cost_scenario)
            #  set only care if delay < pax_connection_th
            hc_mp = lambda delay, passenger: hard_costs_mc(delay) if delay < passenger[0] else hard_costs_mc(
                passenger[1])
            #  set 0 if delay < pax_connection_th
            sc_mp = lambda delay, passenger: soft_costs_mc(delay) if delay < passenger[0] else soft_costs_mc(
                passenger[1])
            cost_fun = lambda delay: hard_costs(delay) + soft_costs(delay) + maintenance_crew_costs(delay) + sum(
                hc_mp(delay, passenger) for passenger in missed_connected) + sum(
                sc_mp(delay, passenger) for passenger in missed_connected)

        else:
            cost_fun = lambda delay: hard_costs(delay) + soft_costs(delay) + maintenance_crew_costs(delay)

        if curfew is None:
            return cost_fun
        else:
            curfew_threshold = curfew[0] if type(curfew) == tuple else curfew
            curfew_passengers = curfew[1] if type(curfew) == tuple else n_passengers + n_missed_connected

        return lambda delay: cost_fun(delay) if delay < curfew_threshold \
            else cost_fun(delay) + get_curfew_value(aircraft_cluster, cost_scenario, curfew_passengers)

    except ClusterError as cl_error:
        print(cl_error.message)


def get_data_dict():
    data_dict = {
        "aircraft": pd.read_csv(os.path.join(os.path.dirname(__file__), "Cluster/aircraftClustering.csv")),
        "aircraft_seats": pd.read_csv(os.path.join(os.path.dirname(__file__), "Passengers/2019-AircraftSeats.csv")),
        "airports": pd.read_csv(os.path.join(os.path.dirname(__file__), "CostScenario/airportMore25M.csv")),
        "hard": pd.read_csv(os.path.join(os.path.dirname(__file__),
                                         "Hard/2019-PassengerHardCostsBaseScenarioAverage.csv")),
        "crew": pd.read_csv(os.path.join(os.path.dirname(__file__), "MaintenanceCrew/2019-TacticalCrewCosts.csv")),
        "maintenance": pd.read_csv(os.path.join(os.path.dirname(__file__),
                                                "MaintenanceCrew/2019-TacticalMaintenanceCosts.csv")),
        "soft": pd.read_csv(os.path.join(os.path.dirname(__file__), "Soft/2019-PassengerSoftCosts.csv"))
    }
    return data_dict


def get_pax_number(airline: str, destination: str, aircraft_type: str):
    aircraft_cluster = get_aircraft_cluster(aircraft_type=aircraft_type)
    cost_scenario = get_cost_scenario(airline=airline, destination=destination)
    return get_passengers(aircraft_cluster, cost_scenario)


def get_pax_number_from_load_factor(aircraft_type: str, load_factor: float):
    aircraft_cluster = get_aircraft_cluster(aircraft_type=aircraft_type)
    df_aircraft_seats = pd.read_csv(os.path.join(os.path.dirname(__file__), "Passengers/2019-AircraftSeats.csv"))
    n_passengers = int(load_factor * df_aircraft_seats[df_aircraft_seats.Aircraft == aircraft_cluster].SeatsLow.iloc[0])
    return n_passengers
