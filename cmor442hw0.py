import gurobipy as gp
import os
import itertools
import csv
import time

cut_params = ["GomoryPasses", "MIRCuts", "FlowCoverCuts", "CliqueCuts"]

param_values = [-1, 0, 1]

param_combinations = list(itertools.product(param_values, repeat=4))

time_limit = 120

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
mps_list_path = os.path.join(BASE_DIR, "instance_list.txt")

with open(mps_list_path, "r") as f:
    mps_files = [os.path.join(BASE_DIR, line.strip()) for line in f if line.strip()]

output_file = os.path.join(BASE_DIR, "results.csv")
with open(output_file, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Instance"] + cut_params + ["Runtime_sec", "NodeCount"])

for instance_path in mps_files:
    instance_name = os.path.basename(instance_path)
    print(f"Solving instance: {instance_name}")
    
    for combo in param_combinations:
        model = gp.read(instance_path)

        for i, param in enumerate(cut_params):
            model.setParam(param, combo[i])

        model.setParam("TimeLimit", time_limit)

        start_time = time.time()
        model.optimize()
        end_time = time.time()
        
        runtime = end_time - start_time
        nodes = model.NodeCount

        with open(output_file, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([instance_name] + list(combo) + [runtime, nodes])
        
        print(f"  Combo {combo} -> Runtime: {runtime:.2f}s, Nodes: {nodes}")

