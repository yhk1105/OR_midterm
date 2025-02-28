import pandas as pd
from gurobipy import *
import numpy as np


file_path = '/Users/yhk/Desktop/大二下/作業研究/to students/data'
makespanans = list()
tardinessans = list()
for t in range(5, 6):
    filepath = file_path + '/instance'+f'{t:02d}'+'.csv'
    machine = set()
    data = pd.read_csv(filepath)

    # Count the number of rows in the data
    jobs = data.shape[0]

    data_list = []
    # Iterate through each row and print the values
    for index, row in data.iterrows():
        # print(f"Row {index+1}: {row.values}")
        data_list.append(row.values)

    processing_times_1 = []
    for i in range(jobs):
        processing_time_1 = data_list[i][1]
        processing_times_1.append(processing_time_1)

    # print("processing_times_1:", processing_times_1)

    processing_times_2 = []
    for i in range(jobs):
        processing_time_2 = data_list[i][2]
        processing_times_2.append(processing_time_2)
    # print("processing_times_2:", processing_times_2)

    machines_1 = []
    for i in range(jobs):
        machine_1 = data_list[i][3]
        machines_1.append(machine_1)
    # print(machines_1)

    machines_1_new = []
    for item in machines_1:
        string_list = item.split(',')
        int_list = [int(num) for num in string_list]
        machines_1_new.append(int_list)
        for item in int_list:
            machine.add(item)
    # print("machines_1_new", machines_1_new)

    machines_2 = []
    for i in range(jobs):
        machine_2 = data_list[i][4]
        machines_2.append(machine_2)
    # print(machines_2)

    machines_2_new = []
    for item in machines_2:
        if pd.isna(item):
            machines_2_new.append([0])
        else:
            string_list = item.split(',')
            int_list = [int(num) for num in string_list]
            machines_2_new.append(int_list)
            for item in int_list:
                machine.add(item)
    a = list(machine)
    A = []
    for i in range(len(a)):
        A.append([])
        for j in range(jobs):
            A[i].append([])
            for k in range(2):
                A[i][j].append(0)
    for i in range(jobs):
        for j in range(len(machines_1_new[i])):
            A[machines_1_new[i][j]-1][i][0] = 1
        for j in range(len(machines_2_new[i])):
            if machines_2_new[i][0] == 0:
                for k in range(len(a)):
                    A[k][i][1] = 1
            else:
                A[machines_2_new[i][j]-1][i][1] = 1

    due_list = []
    for i in range(jobs):
        due = data_list[i][5]
        due_list.append(due)
    # print(due_list)

    mintardiness = Model("mintardiness")

    stages = 2

    p = []
    for i in range(jobs):
        p.append([])
        for s in range(stages):
            if s == 0:
                p[i].append(processing_times_1[i])
            else:
                p[i].append(processing_times_2[i])

    M = 0
    for i in range(jobs):
        for s in range(stages):
            M += p[i][s]

    # Variables
    c = []
    for i in range(jobs):
        c.append([])
        for s in range(stages):
            c[i].append(mintardiness.addVar(
                lb=0, vtype=GRB.CONTINUOUS, name=f"c{i}, {s}"))

    y = []
    for m in range(len(a)):
        y.append([])
        for i in range(jobs):
            y[m].append([])
            for s in range(stages):
                y[m][i].append(mintardiness.addVar(
                    lb=0, ub=1, vtype=GRB.BINARY, name=f"y{m}{i}{s}"))
                mintardiness.addConstr(y[m][i][s] <= A[m][i][s])

    z = []
    for m in range(len(a)):
        z.append([])
        for i in range(jobs):
            z[m].append([])
            for s in range(stages):
                z[m][i].append([])
                for j in range(jobs):
                    z[m][i][s].append([])
                    for t in range(stages):
                        z[m][i][s][j].append(mintardiness.addVar(
                            lb=0, ub=1, vtype=GRB.BINARY, name=f"z{m}{i}{s}{j}{t}"))

    T = []
    for i in range(jobs):
        T .append(mintardiness.addVar(
            lb=0, vtype=GRB.CONTINUOUS, name=f"T {i}"))

    # Objective
    mintardiness.setObjective(quicksum(T[i]
                                       for i in range(jobs)), GRB.MINIMIZE)

    # Constraints
    # mintardiness.addConstr(i != j)

    for i in range(jobs):
        mintardiness.addConstr(T[i] >= 0)

    for i in range(jobs):
        mintardiness.addConstr(T[i] >= c[i][1] - due_list[i])
    for i in range(jobs):
        for s in range(stages):
            mintardiness.addConstr(
                quicksum(y[m][i][s] for m in range(len(a))) == 1)
    for m in range(len(a)):  # Fix: Iterate over len(a)
        for i in range(jobs):
            for j in range(jobs):
                for s in range(stages):
                    for t in range(stages):
                        if i != j or s != t:
                            mintardiness.addConstr(
                                y[m][i][s] + y[m][j][t] <= 1 + z[m][i][s][j][t] + z[m][j][t][i][s])
    for m in range(len(a)):
        for i in range(jobs):
            for j in range(jobs):
                for s in range(stages):
                    for t in range(stages):
                        if i != j or s != t:
                            mintardiness.addConstr(
                                c[i][s] - c[j][t] + p[j][t] <= M * (1 - z[m][i][s][j][t]))

    for i in range(jobs):
        mintardiness.addConstr(c[i][1] - p[i][1] >= c[i][0])

    for i in range(jobs):
        mintardiness.addConstr(
            c[i][1] - p[i][1] - c[i][0] <= 1)

    for i in range(jobs):
        for s in range(stages):
            mintardiness.addConstr(c[i][s] >= p[i][s])
    mintardiness.setParam('TimeLimit', 600)
    mintardiness.optimize()

    print("Result:")

    K = []
    L = []
    with open('output.txt', 'w') as f:
        for var in mintardiness.getVars():
            f.write(f"{var.varName} = {var.x}\n")
    for var in mintardiness.getVars():
        print(var.varName, '=', var.x)
        if var.varName[0] == "T":
            K.append(var.x)
        if var.varName[0] == "c" and var.varName[-1] == "1":
            L.append(var.x)
    print(L)

    print("z* =", mintardiness.objVal)
    lastans = mintardiness.objVal

    minmakespan = Model("minmakespan")
    # Variables
    w = minmakespan.addVar(lb=0, vtype=GRB.CONTINUOUS, name="w")

    c = []
    for i in range(jobs):
        c.append([])
        for s in range(stages):
            c[i].append(minmakespan.addVar(
                lb=0, vtype=GRB.CONTINUOUS, name=f"c{i}, {s}"))

    y = []
    for m in range(len(a)):
        y.append([])
        for i in range(jobs):
            y[m].append([])
            for s in range(stages):
                y[m][i].append(minmakespan.addVar(
                    lb=0, ub=1, vtype=GRB.BINARY, name=f"y{m}{i}{s}"))
                minmakespan.addConstr(y[m][i][s] <= A[m][i][s])

    z = []
    for m in range(len(a)):
        z.append([])
        for i in range(jobs):
            z[m].append([])
            for s in range(stages):
                z[m][i].append([])
                for j in range(jobs):
                    z[m][i][s].append([])
                    for t in range(stages):
                        z[m][i][s][j].append(minmakespan.addVar(
                            lb=0, ub=1, vtype=GRB.BINARY, name=f"z{m}{i}{s}{j}{t}"))

    T = []
    for i in range(jobs):
        T .append(minmakespan.addVar(
            lb=0, vtype=GRB.CONTINUOUS, name=f"T {i}"))

    # Objective
    minmakespan.setObjective(w, GRB.MINIMIZE)

    # Constraints

    for i in range(jobs):
        minmakespan.addConstr(w >= c[i][1])
    for i in range(jobs):
        minmakespan.addConstr(T[i] >= 0)

    for i in range(jobs):
        minmakespan.addConstr(T[i] >= c[i][1] - due_list[i])

    minmakespan.addConstr(quicksum(T[i]
                                   for i in range(jobs)) - lastans <= 0.1)
    for m in range(len(a)):
        for i in range(jobs):
            for j in range(jobs):
                for s in range(stages):
                    for t in range(stages):
                        if i != j or s != t:
                            minmakespan.addConstr(
                                c[i][s] - c[j][t] + p[j][t] <= M * (1 - z[m][i][s][j][t]))

    for i in range(jobs):
        minmakespan.addConstr(c[i][1] - p[i][1] >= c[i][0])

    for i in range(jobs):
        for s in range(stages):
            minmakespan.addConstr(
                quicksum(y[m][i][s] for m in range(len(a))) == 1)

    for i in range(jobs):
        minmakespan.addConstr(
            c[i][1] - p[i][1] - c[i][0] <= 1)

    for m in range(len(a)):  # Fix: Iterate over len(a)
        for i in range(jobs):
            for j in range(jobs):
                for s in range(stages):
                    for t in range(stages):
                        if i != j or s != t:
                            minmakespan.addConstr(
                                y[m][i][s] + y[m][j][t] <= 1 + z[m][i][s][j][t] + z[m][j][t][i][s])

    for i in range(jobs):
        for s in range(stages):
            minmakespan.addConstr(c[i][s] >= p[i][s])
    minmakespan.setParam('TimeLimit', 600)
    minmakespan.optimize()
    tardinessans.append(mintardiness.objVal)
    makespanans.append(minmakespan.objVal)

series1 = pd.Series(tardinessans)
series2 = pd.Series(makespanans)

df = pd.DataFrame({'Instance': series1.index+1,
                   'optimize makespan': series2, 'optimize tardiness': series1})

df.to_csv(file_path+'/output.csv', index=False)
