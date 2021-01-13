#Mini TF2 Unbox Simulator Demo

#Import dependencies
from collections import Counter
import numpy as np
from numpy import random
from matplotlib import pyplot as plt

def unbox_simulator(number_of_cases_to_unbox, number_of_simulations_to_run):
    p = 0.0065 # p = assumed probability of unusual based on wiki and other simulators

    lst = []

    for simulation in range(int(number_of_simulations_to_run)):
        n_unusual_uncrated = random.binomial(n=number_of_cases_to_unbox, p=p)
        lst.append(n_unusual_uncrated)
    print("Unboxing Results based on your ", number_of_simulations_to_run, " Unboxing Simulation with ", str(number_of_cases_to_unbox), " Cases: ")
    print("Unusual Occurence Count: ",Counter(lst))
    print("Chance to end up with 0 unusual from your ",number_of_cases_to_unbox," unboxes is",round((Counter(lst)[0]/number_of_simulations_to_run)*100.0,2),"%")
    print("Average Number of Unusuals Unboxed: ",round(np.mean(lst),2)," out of ", str(number_of_cases_to_unbox), " cases")
    print("Minimum Number of Unusuals Unboxed: ",np.min(lst)," out of ", str(number_of_cases_to_unbox), " cases")
    print("Maximum Number of Unusuals Unboxed: ",np.max(lst)," out of ", str(number_of_cases_to_unbox), " cases")
    print("See the full distribution in the below chart: ")
    print("==================================================================================================================================================================================================================================================================================")

    #Plot histogram 
    plt.figure(figsize=(9,6))
    plt.xlim([min(lst), max(lst)])

    plt.hist(lst, bins = len(Counter(lst)), alpha=0.7, edgecolor='black', linewidth=1.2)
    plt.title('Number of unusuals obtained in each simulation run unboxing ' + str(number_of_cases_to_unbox) + ' cases', fontsize=12)
    plt.xlabel('Number of unusuals obtained', fontsize=11)
    plt.ylabel('Number of simulation runs', fontsize=11)

    plt.show()