import numpy as np

from CostPackage.arrival_costs import *
import os
import matplotlib.pyplot as plt

# print(os.getcwd())
cost_fun = get_cost_model(aircraft_type="A320", airline="fhjd", destination="fjfjfj", n_passengers=170)
cost_fun_mc = get_cost_model(aircraft_type="A320", airline="fhjd", destination="fjfjfj", n_passengers=170,
                             missed_connected=[(20, 300), (40, 200), (25, 185)])
cost_fun_mc_1 = get_cost_model(aircraft_type="A320", airline="fhjd", destination="fjfjfj", n_passengers=170,
                               missed_connected=[(20, 300) for _ in range(20)], self_curfew=30)

# print(pippo(20))
# data = get_data_dict()

delays = np.linspace(0, 300)
# print(delays)
plt.plot(delays, [cost_fun(d) for d in delays], label="no mc")
plt.plot(delays, [cost_fun_mc_1(d) for d in delays], label="1 p")

plt.plot(delays, [cost_fun_mc(d) for d in delays], label="3 p")
plt.legend()
plt.show()
# print(data)

'''
XXX = 80.000 EUR for the following aircraft types: 77X, 77W, 772, 388, 343

XXX = 40.000 EUR for all other aircraft types


77X ???? not found



cluster = pd.read_csv("CostPackage/Cluster/aircraftClustering.csv")
cluster_dict = dict(zip(cluster.AircraftType, cluster.AssignedAircraftType))
import numpy as np
vals = list(cluster_dict.values())
v = np.unique(vals)
for i in v:
    print(i)


cluster["extra"] = cluster.AircraftType.apply(lambda name: name[-3:])
p = cluster[cluster.extra.isin(['77X', '77W', '772', '388', '343'])]

TURNAROUND TO BE INCLUDED IN THE CURFEW CSV
EXTEND FIXED COSTS TO OTHER WIDEBODY CLUSTER

'''
