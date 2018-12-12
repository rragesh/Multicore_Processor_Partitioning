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
	random.seed() #Random seeding
	n = random.randrange(2,7)  #random in range of 2 and 7
	print("number of tasks",n)

	for i in range(n):    
		task_id = i
		period = random.randrange(9,20) #random period
		WCET = random.randrange(4,8)    #random WCET
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
		print("--------------------------------")
		print("\nCORE  %d"%cores[i].core_id)
		print("\tcore number       ",cores[i].core_id)
		print("\tcore load capacity",cores[i].core_U)
		print("\tcore rem capacity ",cores[i].core_rem_U)
		print("\tTask in core      ",cores[i].task_ID) 
		print("\tTask Utilization  ",cores[i].task_U) 
		print("--------------------------------")
	print("\n\tNumber of processors used for NEXT FIT",m)
	dispaly_metrics(cores)

def FIRST_FIT():
	# 'n' tasks and 'res' processors
	global need
	res = 0
	core_remain = [0]*n			# array to store remaining space in cores
	cores = []  			#instance list of core class
	core_rem = sched_factor #Store remaining U factor of core
	
	for i in range(n):
		need = 0
		# Find the first core that can schedule the task
		for j in range(res):
			if core_remain[j] >= tasks[i].U:
				core_remain[j] = tasks[i].U - core_remain[j] 
				cores.append(core(res,
							sched_factor,
							truncate(tasks[i].U - core_remain[j] ,2),
							i,
							tasks[i].U)) 
				break
			else:
				need = need +1
		
		# If no core can schedule the task add new core
		if need == res:
			core_remain[res] = sched_factor - tasks[i].U
			res = res +1   #task i is added to a new core
			cores.append(core(res,
							sched_factor, 
							truncate(sched_factor - tasks[i].U,2),
							i,
							tasks[i].U)) 
	
	for i in range(len(cores)):
		print("--------------------------------")
		print("\nCORE  %d"%cores[i].core_id)
		print("\tcore number       ",cores[i].core_id)
		print("\tcore load capacity",cores[i].core_U)
		print("\tcore rem capacity ",cores[i].core_rem_U)
		print("\tTask in core      ",cores[i].task_ID) 
		print("\tTask Utilization  ",cores[i].task_U) 
		print("--------------------------------")
	print("\n\tNumber of processors used for FIRST FIT",res)
	dispaly_metrics(cores)

def BEST_FIT():
	# 'n' tasks and 'm' processors
	res = 0
	core_remain = [0]*n	# array to store remaining space in cores
	cores = []  			#instance list of core class
	core_rem = sched_factor #Store remaining U factor of core
	count = sched_factor    

	for i in range(n):
		min = count +1
		for j in range(res):
			if (core_remain[j] >= tasks[i].U 
				and core_remain[j]-tasks[i].U < min):
				min = core_remain[j] - tasks[i].U
				c = j
				break
		
		if min == count+1:
			core_remain[res] = sched_factor - tasks[i].U
			res = res  + 1
			cores.append(core(res,
						sched_factor,
						truncate(sched_factor - tasks[i].U,2),
						i,
						tasks[i].U))
		else:
			core_remain[c] = tasks[i].U - core_remain[c]
			cores.append(core(res,
						sched_factor,
						truncate(tasks[i].U - core_remain[c],2),
						i,
						tasks[i].U))
	
	for i in range(len(cores)):
		print("--------------------------------")
		print("\nCORE  %d"%cores[i].core_id)
		print("\tcore number       ",cores[i].core_id)
		print("\tcore load capacity",cores[i].core_U)
		print("\tcore rem capacity ",cores[i].core_rem_U)
		print("\tTask in core      ",cores[i].task_ID) 
		print("\tTask Utilization  ",cores[i].task_U) 
		print("--------------------------------")
	print("\n\tNumber of processors used for BEST FIT",res)
	dispaly_metrics(cores)

def dispaly_metrics(cores):
	core_buff = []          #Store the utilization of cores
	merged_cores = []       #Store the non-duplicate cores
	id_list = []			#Stores id list of cores
	id_merged = []			#Stores id list of merged cores 
	
	# The cores are sorted based on the core_id
	cores = sorted(cores, key=lambda cores:cores.core_id )	
	for i in range(len(cores)):
		id_list.append(cores[i].core_id)
	# Metrics are calculated here
	
	# Inorder to remove the multiple instances of core
	#  with same core_id they are merged
	id_merged = [i for i, x in enumerate(id_list) 
				if i == len(id_list) - 1 or x != id_list[i + 1]]
	# A merged_core array is created to store the core_id
	for i in id_merged:
		merged_cores.append(cores[i])
	
	# Display of main metrics
	for i in range(len(merged_cores)): #truncate the utilization value
		core_buff.append(truncate(merged_cores[i].core_U 
							- merged_cores[i].core_rem_U,2)) 

	core_buff.sort() #sorting the U list for finding max and min values
	print("Utilization factor of cores		  ", core_buff)
	print("Maximum Utilization factor of cores", core_buff[-1])
	print("Minimum Utilization factor of cores", core_buff[0])

if __name__ == '__main__':
	random_data()		#Random task set generation
	# read_data()			#Reads taskset from user
	# hp = hyperperiod()	#Calculates hyperperiod	
	schedulability()	#Check for feasibility
	print("\n\n\n\n")	
	NEXT_FIT()			#Next fit partitioning
	print("\n\n\n\n")
	FIRST_FIT()			#First fit partitioning
	print("\n\n\n\n")
	BEST_FIT()			#Best fit partitioning
	print("\n\n\n\n")