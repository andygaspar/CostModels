from typing import Callable
from CostPackage.Hard.hard_costs import get_hard_costs
from CostPackage.Cluster.cluster import get_aircraft_cluster, ClusterError
from CostPackage.MaintenanceCrew.maintenance_crew_costs import get_maintenance_and_crew_costs
from CostPackage.CostScenario.cost_scenario import get_cost_scenario
from CostPackage.SoftCosts.soft_costs import get_soft_costs


def get_cost_model(aircraft_type: str, airline: str, n_passengers: int = None, destination: str = None,
                   length: float = None) -> Callable:
    try:
        aircraft_cluster = get_aircraft_cluster(aircraft_type=aircraft_type)
        cost_scenario = get_cost_scenario(airline=airline, destination=destination)

        hard_costs = get_hard_costs(passengers=n_passengers, aircraft=aircraft_cluster, scenario=cost_scenario,
                                    length=length)
        soft_costs = get_soft_costs(passengers=n_passengers, scenario=cost_scenario)
        maintenance_crew_costs = get_maintenance_and_crew_costs(aircraft_cluster=aircraft_cluster,
                                                                scenario=cost_scenario)

        return lambda delay: hard_costs(delay) + soft_costs(delay) + maintenance_crew_costs(delay)

    except ClusterError as cl_error:
        print(cl_error.message)


