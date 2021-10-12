from CostPackage.arrival_costs import *

pippo = get_cost_model("A320", "fhjd", "fjfjfj", 170)
print(pippo(20))
