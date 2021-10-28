import numpy as np

from CostPackage.arrival_costs import *
import os
import matplotlib.pyplot as plt

# print(os.getcwd())
cost_fun = get_cost_model(aircraft_type="A320", airline="fhjd", destination="fjfjfj", n_passengers=170)
cost_fun_mc = get_cost_model(aircraft_type="A320", airline="fhjd", destination="fjfjfj", n_passengers=170,
                             missed_connected=[(20, 300), (40, 200), (25, 185)])
cost_fun_mc_1 = get_cost_model(aircraft_type="A320", airline="fhjd", destination="fjfjfj", n_passengers=170,
                               missed_connected=[(20, 300) for _ in range(20)])

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
