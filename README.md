
# Partitioning Strategies using Rate Monotonic Scheduling

simulating the behaviour of several partitioning strategies in periodic tasks with their deadlines equal to their periods. Each processor is scheduled using Rate Monotonic Scheduler.The program will be composed of the following parts:
* **Data acquisition**:The user will specify the number of tasks and for each task, its WCET and period. We will assume that the task set is synchronous to time zero.

* **Partitioning**:This part will focus on the partitioning of the tasks. Simulate BF
(Best Fit), FF (First Fit) and NF (Next Fit). Each strategy will be coded as a function which input is a set of tasks and the outputs are for eac processor, the processor utilization and identity of the tasks assigned to it.

* **Display of metrics**:The number of processors used, highest processor utilization, lowest processor utilization of the task sets are calculated.

## Usage
```
git clone https://github.com/EnigmaRagesh/Multicore_Processor_Partitioning
python3  partitioning.py
```

## sample input 

|        | Period  | WCET |
|:------:|:-------:|:----:|
| Task 1 |    8    |   4  |
| Task 2 |    8    |   2  |
| Task 3 |    8    |   4  |
| Task 4 |    10   |   2  |
