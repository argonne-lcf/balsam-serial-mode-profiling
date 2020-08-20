#!/usr/bin/env python

import sys, os
import glob
import balsam.launcher.dag as dag
from pathlib import Path
from datetime import datetime
from dateutil.parser import parse

current_job = dag.current_job

# Find the file:
log_file = glob.glob("*.out")[0]

t2_key = "Start Time: "
t3_key = "End Time: "

output_file = Path(current_job.working_directory) / Path(current_job.name + ".out")

# Open the file and find the times:
with open(output_file, 'r') as _f:
    for line in _f:
        if t2_key in line:
            
            keys = line.rstrip('\n').split(t2_key)
            time_2 = keys[-1].strip()
            time_2 = parse(time_2).isoformat()
        if t3_key in line:
            keys = line.rstrip('\n').split(t3_key)
            time_3 = keys[-1].strip()
            time_3 = parse(time_3).isoformat()

# dt.isoformat()
current_job.data["t2"] = time_2
current_job.data["t3"] = time_3
current_job.save()
print(time_2)
print(time_3)
