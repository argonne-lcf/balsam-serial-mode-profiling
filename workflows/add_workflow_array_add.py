from balsam.launcher import dag
import os
import subprocess
import glob
import sys

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--n-nodes", help="Number of nodes for this workflow", type=int, default=4)
parser.add_argument("-npc", "--node-packing-count", type=int, help="Number of jobs to run on a single node", default=64)

args = parser.parse_args()

n_nodes = args.n_nodes
node_pack_count = args.node_packing_count

print(args)

# -----------------------------
# add_workflow.py
# -----------------------------

# number of files to generate and number of events per file

# populate database
# don't make more jobs than necessary:
n_jobs = int(100*n_nodes*node_pack_count)

# This is the workflow name
workflow = f"array_add_{n_nodes}_node_core_{node_pack_count}"

# loop over files, index used for run number in events so must count from 1
for i_job in range(n_jobs):
   
      empty_job = dag.add_job(
         name = f"array_add_{i_job}_{n_nodes}_{node_pack_count}",                # This will be the name of the job in the database
         workflow = workflow, 
         description = "empty application for serial testing",  # A description of what this job is
         num_nodes = 1,                                     # Number of nodes each job needs
         ranks_per_node = 1,                                # The number of ranks per node
         node_packing_count = node_pack_count,              # This is set to 64
         wall_time_minutes = 2,                             # Wall time of job
         application= "array_add"         # The name of the application
        )

print(f"Loaded {n_jobs} into the database under workflow {workflow}")
print("To launch these jobs, run:")
print(f"balsam submit-launch -n {n_nodes} -t 30 --job-mode serial --wf-filter {workflow} -A datascience -q default")

