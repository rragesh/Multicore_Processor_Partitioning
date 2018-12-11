#!/usr/bin/env python3
# ------------------------------------------
# partitioning.py : Partitioning strategies: 
			# Best fist, First fit, Next fit
# Author: Ragesh RAMACHANDRAN
# -----------------------------------------
import json
import copy
import operator
import random
from sys import *
from math import gcd
import math
import numpy as np

# Data structure to store the task sets
class task:
	def __init__(self,task_id=None, period=None, WCET=None, U=None):
		self.task_id = task_id
		self.period = period
		self.WCET = WCET
		self.U = U
	
# Data structure to store the processor data
class core:
	def __init__(self,core_id=None,core_U=None,core_rem_U=None, task_ID=None,task_U=None):
		self.core_id = core_id
		self.core_U = core_U
		self.core_rem_U = core_rem_U
		self.task_ID =	task_ID
		self.task_U = task_U


def truncate(f, n):
	return math.floor(f * 10 ** n) / 10 ** n

def hyperperiod():
	temp = []
	for i in range(n):
		temp.append(tasks[i].period)
	HP = temp[0]
	for i in temp[1:]:
		HP = HP*i//gcd(HP, i)
	print ("\n\tHyperperiod:",HP)
	return HP

def random_data():
	global n     # Number of tasks to be partitioned
	global tasks # List that stores the instances of tasks
	tasks = []
	random.seed()
	n = random.randrange(2,7)
	print("number of tasks",n)

	for i in range(n):    
		task_id = i
		period = random.randrange(9,20)
		WCET = random.randrange(4,8)
		u =  WCET/period
		# Limit U by 2 decimal places without rounding off
		U = truncate(u,2)
		tasks.append(task(task_id,period,WCET,U))

	# Tasks are sorted based on their period and displayed
	tasks = sorted(tasks, key=lambda tasks:tasks.period)
	for i in range(n):
		print("-----------------")
		print("TASK  %d"%(i+1))
		print("-----------------")
		print("Period     ",tasks[i].period)
		print("WCET       ",tasks[i].WCET)
		print("Utilization",tasks[i].U)
		print("-----------------")
		print("\n\n")

def read_data():
	global n     # Number of tasks to be partitioned
	global tasks # List that stores the instances of tasks
	tasks = []
	n = int(input("\n \t\tEnter number of tasks:"))
	# Read data from user
	for i in range(n):    
		task_id = i
		print("\nEnter Period of task T",i,":")
		period = int(input())
		print("Enter the WCET of task C",i,":")
		WCET = int(input()) 
		u =  WCET/period
		# Limit U by 2 decimal places without rounding off
		U = truncate(u,2)
		tasks.append(task(task_id,period,WCET,U))

	# Tasks are sorted based on their period and displayed
	tasks = sorted(tasks, key=lambda tasks:tasks.period)
	for i in range(n):
		print("-----------------")
		print("TASK  %d"%(i+1))
		print("-----------------")
		print("Period     ",tasks[i].period)
		print("WCET       ",tasks[i].WCET)
		print("Utilization",tasks[i].U)
		print("-----------------")
		print("\n\n")

def schedulability():
	global sched_factor
	# Schedulability test for RM scheduling
	sched_fac = n*(2**(1/n)-1)
	# to limit only 2 decimal places without rounding off
	sched_factor = truncate(sched_fac, 2)
	print("\tsched_factor", sched_factor)
 

def NEXT_FIT():
	# 'n' tasks and 'm' processors
	m = 1      				#core counter
	c = 1                   #initial core count
	cores = []              #instance list of core class
	core_rem = sched_factor #Store remaining U factor of core
	core_buff = []          #Store the utilization of cores
	merged_cores = []       #Store the non-duplicate cores
	id_list = []			#Stores id list of cores
	id_merged = []			#Stores id list of merged cores
	for i in range(n):
		# if a task cannot fit into same core
		if(tasks[i].U > core_rem):   #task does not fit into same core
			c = c + 1                #task i is added to a new core 
			core_rem = sched_factor - tasks[i].U    #calculate rem capacity
			core_rem = truncate(core_rem,2)
			cores.append(core(c, sched_factor, core_rem,i,tasks[i].U)) 
		 # If a task fit into a same core 
		else:
			core_rem = core_rem - tasks[i].U #task run on same core
			core_rem = truncate(core_rem,2)
			cores.append(core(c, sched_factor, core_rem,i,tasks[i].U)) 
	# if there are no new cores added then default value = 1
	if(c>m):
			m = c
	# sorting the processors based on core_id
	cores = sorted(cores, key=lambda cores:cores.core_id )
	for i in range(len(cores)):
		id_list.append(cores[i].core_id)
		print("------------------------")
		print("\nCORE  %d"%cores[i].core_id)
		print("\tcore number       ",cores[i].core_id)
		print("\tcore load capacity",cores[i].core_U)
		print("\tcore rem capacity ",cores[i].core_rem_U)
		print("\tTask in core      ",cores[i].task_ID) 
		print("\tTask Utilization  ",cores[i].task_U) 
		print("------------------------")
	# Metrics are calculated here
	# Inorder to remove the multiple instances of core with same core_id they are merged
	# Check the next index in the id_list. If an element is not equal to the element in the 
	# next index, it is the last duplicate
	id_merged = [i for i, x in enumerate(id_list) if i == len(id_list) - 1 or x != id_list[i + 1]]
	for i in id_merged:
		merged_cores.append(cores[i])
	
	print("\n\tNumber of processors used for NEXT FIT",m)
	for i in range(len(merged_cores)):
		print("\n------------------------")
		print("\nCORE  %d"%merged_cores[i].core_id)
		print("\tcore number       ",merged_cores[i].core_id)
		print("\tcore total load   ",merged_cores[i].core_U - merged_cores[i].core_rem_U)
		print("\tcore remaing U    ",merged_cores[i].core_rem_U)
		print("------------------------")

	# Display of main metrics
	for i in range(len(merged_cores)): #truncate the utilization value
		core_buff.append(truncate(merged_cores[i].core_U - merged_cores[i].core_rem_U,2)) 
	core_buff.sort() #sorting the U list for finding max and min values
	print("Utilization factor of cores		  ", core_buff)
	print("Maximum Utilization factor of cores", core_buff[-1])
	print("Minimum Utilization factor of cores", core_buff[0])

def FIRST_FIT():
	# 'n' tasks and 'm' processors
	m = 1       #core counter
	c = 1       #initial core count
	cores = []  #instance list of core class
	core_rem = sched_factor #Store remaining U factor of core
	merged_cores = []  
	cores.append(core(1,sched_factor,sched_factor,0,0))
	for i in range(n):
		for j in range(c):
			# if a task  fit into same core
			if(tasks[i].U < core_rem):   #task does not fit into same core
				core_rem = core_rem - tasks[i].U #task run on same core
				core_rem = truncate(core_rem,2)
				cores.append(core(c, sched_factor, core_rem,i,tasks[i].U))				 
			else:
				c = c + 1                #task i is added to a new core 
				core_rem = sched_factor - tasks[i].U    #calculate rem capacity
				core_rem = truncate(core_rem,2)
				cores.append(core(c, sched_factor, core_rem,i,tasks[i].U))
		# if there are no new cores added then default value = 1
		if(c>m):
				m = c
	cores.pop(0)
	# sorting the processors based on core_id
	cores = sorted(cores, key=lambda cores:cores.core_id )
	# Display the result
	for i in range(len(cores)):
		print("--------------------------------")
		print("\nCORE  %d"%cores[i].core_id)
		print("\tcore number       ",cores[i].core_id)
		print("\tcore load capacity",cores[i].core_U)
		print("\tcore rem capacity ",cores[i].core_rem_U)
		print("\tTask in core      ",cores[i].task_ID) 
		print("\tTask Utilization  ",cores[i].task_U) 
		print("--------------------------------")
	print("\n\tNumber of processors used for FIRST FIT",m)
  
def BEST_FIT():
	pass	

if __name__ == '__main__':
	random_data()
	# read_data()
	# hp = hyperperiod()
	schedulability()
	NEXT_FIT()
	# FIRST_FIT()
	# BEST_FIT()