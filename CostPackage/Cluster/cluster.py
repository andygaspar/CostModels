import os

import pandas as pd
import numpy as np


class ClusterError(Exception):
    def __init__(self, flight: str):
        self.flight = flight
        self.message = "Aircraft " + self.flight + " not found"

    def __repr__(self):
        return "Aircraft " + self.flight + " not found"


cluster = pd.read_csv(os.path.join(os.path.dirname(__file__), "aircraftClustering.csv"))
cluster_dict = dict(zip(cluster.AircraftType, cluster.AssignedAircraftType))


def get_aircraft_cluster(aircraft_type: str):
    if aircraft_type in list(cluster_dict.keys()):
        return cluster_dict[aircraft_type]
    else:
        raise ClusterError(aircraft_type)
