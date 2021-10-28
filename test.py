import numpy as np

from CostPackage.arrival_costs import *
import os
import matplotlib.pyplot as plt

print(os.getcwd())
cost_fun = get_cost_model(aircraft_type="A320", airline="fhjd", destination="fjfjfj", n_passengers=170)
cost_fun_mc = get_cost_model(aircraft_type="A320", airline="fhjd", destination="fjfjfj", n_passengers=170, missed_connected=[(20, 300)])

# print(pippo(20))
# data = get_data_dict()

delays = np.linspace(0,100)
print(delays)
plt.plot(delays, [cost_fun(d) for d in delays], label="no mc")
plt.plot(delays, [cost_fun_mc(d) for d in delays])
plt.legend()
plt.show()
# print(data)
