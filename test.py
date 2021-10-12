from CostPackage.arrival_costs import *
import os

print(os.getcwd())
pippo = get_cost_model("A320", "fhjd", "fjfjfj", 170)
print(pippo(20))
data = get_data_dict()
print(data)
