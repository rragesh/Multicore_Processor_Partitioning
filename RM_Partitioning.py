#!/usr/bin/env python3
# ------------------------------------------
# RM_scheduling.py: Partitioning strategies: Best fist, First fit, Next fit
# Author: Ragesh RAMACHANDRAN
# ------------------------------------------
import json
import copy
from sys import *
from math import gcd
import math
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# stores set of tasks read form user
tasks = dict()
# store the processor number
processor = []
#  store task id in each processor
task_alloc = []  
# To store task_id, Period, Utilization and WCET of sorted tasks
T = []
C = []
U = []
task_id = []
def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

def read_data():
    """
    Reading the details of the tasks to be scheduled from the user 
    as number of tasks, Period, and WCET 
    """ 
    global n
    global hp
    global tasks

    n = int(input("\n \t\tEnter number of tasks:"))
    #  Storing data in a dictionary
    for i in range(n):
        tasks[i] = {}
        print("\n\n\n Enter Period of task T",i,":")
        p = input()
        tasks[i]["Period"] = int(p)
        print("Enter the WCET of task C",i,":")
        w = input()
        tasks[i]["WCET"] = int(w)
    # Writing the dictionary into a JSON file
    with open('tasks.json','w') as outfile:
        json.dump(tasks,outfile,indent = 4)
    return tasks

def hyper_period():
    """
    Calculates the hyper period of the tasks to be scheduled
    """
    temp = []
    for i in range(n):
        temp.append(tasks[i]["Period"])
    HP = temp[0]
    for i in temp[1:]:
        HP = HP*i//gcd(HP, i)
    print ("\n hyperperiod:",HP)
    return HP

def sort_task():
    """
    The task sets are sorted in the increasing order of their Periods.
    """
    global T
    global C
    global U
    global task_id
    global sched_factor

    # Schedulability test for RM scheduling
    sched_fac = n*(2**(1/n)-1)
    # to limit only 2 decimal places without rounding off
    sched_factor = truncate(sched_fac, 2)

    # sorting the list of tasks in increasing order of their period
    for sorted_tasks_id in OrderedDict(sorted(tasks.items(), key=lambda k_v: k_v[1]['Period'])):  
        
        task_id.append(sorted_tasks_id)
        T.append(tasks[sorted_tasks_id]['Period'])
        C.append(tasks[sorted_tasks_id]['WCET'])

    for i in range(len(task_id)):
        
        U.append(truncate(int(C[i])/int(T[i]),3))

    print("\nTask_id",task_id)
    print("\nPeriod", T)
    print("\nWCET",C)
    print("\nSchedulability_factor",sched_factor)


def plot_graph():

    # plot Utilization percentage in x axis
    x_axis = [x * 100 for x in U]
    #  plot percentage in y axis
    y_axis = np.ones(len(U))
    # different colors for different processors
    colors = ['red','green','blue','orange','yellow','magenta','cyan']
    x = np.arange(n)
    fig, ax = plt.subplots()
    # for percentage in y axis
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    for i in range(n):

        plt.bar(x[i], x_axis[i], color = colors[i])

    plt.xticks(x, x_axis)
    # show the result
    plt.show()

def next_fit(tasks):
    sort_task()
    #  initially task 1 is allocated to processor 1 
    processor_id = 1
    Util_factor = 0
    temp = []

    # Starts partitioning based on next fit

    for i in range(len(task_id)):   
        # sum of each utilization factor
        if U[i] <= 1:
            # processor.append(task_id)
            Util_factor = Util_factor + U[i]
            
            if Util_factor < sched_factor:
                print("same processor")
                temp.append(Util_factor)

            else:
                Util_factor = U[i]
                temp.append(Util_factor)
                processor_id = processor_id + 1
                # processor.append(task_id)
                print("processor change")

    if processor_id >= n:
        processor_id = n
            
    print("\nUtilization factor",U)
    print("\nTemp Util factor",temp)
    print("\nNumber of tasks:", n)
    print("\nNumber of Processors used:",processor_id)
    # for task_id in tasks.keys():
    # plot_graph()

def first_fit():
    pass

def best_fit():
    pass

if __name__ == '__main__':

    TASKS = read_data()
    next_fit(TASKS)
    hp = hyper_period()
    

