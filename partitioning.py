#!/usr/bin/env python3
# ------------------------------------------
# partitioning.py : Partitioning strategies: 
			# Best fist, First fit, Next fit
# Author: Ragesh RAMACHANDRAN
# -----------------------------------------
import json
import copy
import operator
from sys import *
from math import gcd
import math
import numpy as np

class task:
	def __init__(self,task_id=None, period=None, WCET=None, U=None, core_ID=None):
		self.task_id = task_id
		self.period = period
		self.WCET = WCET
		self.U = U
		self.core_ID = core_ID

class core:
	def __init__(self,core_id = None,core_U = None,core_rem_U = None):
		self.core_id = core_id
		self.core_U = core_U
		self.core_rem_U = core_rem_U


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
	m = 1       #core counter
	c = 1       #initial core count
	cores = []  #instance list of core class
	core_rem = sched_factor #Store remaining U factor of core
	merged_cores = []  

	for i in range(n):
		# if a task cannot fit into same core
		if(tasks[i].U > core_rem):   #task does not fit into same core
			c = c + 1                #task i is added to a new core 
			core_rem = sched_factor - tasks[i].U    #calculate rem capacity
			core_rem = truncate(core_rem,2)
			cores.append(core(c, sched_factor, core_rem)) 
		 # If a task fit into a same core 
		else:
			core_rem = core_rem - tasks[i].U #task run on same core
			core_rem = truncate(core_rem,2)
			cores.append(core(c, sched_factor, core_rem)) 
	# if there are no new cores added then default value = 1
	if(c>m):
			m = c
	# sorting the processors based on core_id
	cores = sorted(cores, key=lambda cores:cores.core_id )
	#prints resultant data
	for i in range(len(cores)):
		print("------------------------")
		print("\nCORE  %d"%cores[i].core_id)
		print("\tcore number       ",cores[i].core_id)
		print("\tcore load capacity",cores[i].core_U)
		print("\tcore rem capacity ",cores[i].core_rem_U)
		print("------------------------")
	print("\n\tNumber of processors used for NEXT FIT",m)
	
	# Metrics are calculated here
	# Inorder to remove the multiple instances 
	# of core with same core_id they are merged
	for i in range(len(cores)-1):
		core_len = len(cores)
		# To merge the last object of the cores
		if i+1 == core_len-1:
			if merged_cores[len(merged_cores)-1].core_id == cores[i+1].core_id:
				merged_cores.pop()
				merged_cores.append(cores[i+1])
			else:
				merged_cores.append(cores[i+1])	
		# To merge the  cores having same core_id into a single instance 
		else:
			# If the core_id of two successive instances are same then second instance is merged
			if cores[i].core_id == cores[i+1].core_id:
				merged_cores.append(cores[i+1])	
			else:
				# 
				if merged_cores[len(merged_cores)-1].core_id == cores[i].core_id :
					merged_cores.pop()
					merged_cores.append(cores[i])
				elif merged_cores[len(merged_cores)-1].core_id != cores[i].core_id:
					merged_cores.append(cores[i])

	for i in range(len(merged_cores)):
		print("------------------------")
		print("\nCORE  %d"%merged_cores[i].core_id)
		print("\tcore number       ",merged_cores[i].core_id)
		print("\tcore load capacity",merged_cores[i].core_U)
		print("\tcore rem capacity ",merged_cores[i].core_rem_U)
		print("------------------------")

	# for i in range(len(cores)):
	# 	core_buff.append(truncate(cores[i].core_U - cores[i].core_rem_U,2)) 
	
	# core_buff.sort()
	# print("Utilization factor of cores		  ", core_buff)
	# print("Maximum Utilization factor of cores", core_buff[0])
	# print("Minimum Utilization factor of cores", core_buff[-1])

def FIRST_FIT():
	m = 1
	c = 1
	cores = []
	core_rem = sched_factor
	
	for i in range(n):

		if(tasks[i].U > core_rem):   #task does not fit into same core
			c = c + 1                #add new core  
			core_rem = sched_factor - tasks[i].U    #calculate rem capacity
			core_rem = truncate(core_rem,2)
			cores.append(core(c, sched_factor, core_rem)) 
			print("\tcore change", core_rem)
			# for j in range(len(cores)):

			# 	if(tasks[i].U > cores[j].core_rem_U):
			# 		c = c+1
			# 		core_rem = sched_factor-tasks[i].U
			# 		cores.append(core(m, sched_factor, core_rem)) 
			# 		print(tasks[i].U,"\tchange core inside",core_rem)
			# 		core_rem = sched_factor
			# 	else:
			# 		core_rem = cores[j].core_rem_U - tasks[i].U
			# 		core_rem = truncate(core_rem,2)
			# 		cores.append(core(j, sched_factor, core_rem)) 
			# 		print(tasks[i].U,"\tsame core inside",core_rem)
		else:   #task does not fit into same core
			core_rem = core_rem - tasks[i].U   #task run on same core
			core_rem = truncate(core_rem,2)
			cores.append(core(m, sched_factor, core_rem)) 
			print(tasks[i].U, "\tsame core",core_rem)

		if(c>m):
			m = c
	
	for i in range(len(cores)):
		print("------------------------")
		print("\nCORE  %d"%cores[i].core_id)
		print("\tcore number       ",cores[i].core_id)
		print("\tcore load capacity",cores[i].core_U)
		print("\tcore rem capacity ",cores[i].core_rem_U) 
		print("------------------------")
	print("\n\tNumber of processors used for FIRST FIT",m)
  
	

if __name__ == '__main__':
	read_data()
	hp = hyperperiod()
	schedulability()
	NEXT_FIT()
	# FIRST_FIT()