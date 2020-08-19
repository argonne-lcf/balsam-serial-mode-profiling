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
n_files = 25
n_events = 1000

tot_events = n_files*n_events

# This is the workflow name
workflow = f"larsoft_reproducer_{n_nodes}_node_core_{node_pack_count}"

# loop over files, index used for run number in events so must count from 1
for ifile in range(1, n_files + 1):
   
    # print the file
    print("File: ", ifile)


    # loop over events for file, index used for event number so must count from 1
    for ievent in range (1, n_events + 1):
	
	# offset run number by 1 million to avoid overlap with fermigrid production
        irun = ifile + 1000000

        MCP2_0_args  = f"{ifile} {irun} {ievent}" 

        MCP2_0_job = dag.add_job(
            name = f"gen_long_{ifile}_{ievent}",                # This will be the name of the job in the database
            workflow = workflow, 
            description = "cosmics generation stage only",  # A description of what this job is
            num_nodes = 1,                                     # Number of nodes each job needs
            ranks_per_node = 1,                                # The number of ranks per node
            node_packing_count = node_pack_count,              # This is set to 64
            args = MCP2_0_args,                                # The arguments to the application (the bash script being run)
            wall_time_minutes = 2,                            # Wall time of job
            application= "cosmics_gen_stage"         # The name of the application
        )

print("Total number of events to be generated: ", tot_events)
