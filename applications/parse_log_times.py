#!/usr/bin/env python

import sys, os
import glob

# Find the file:
log_file = glob.glob("gen_long*.out")[0]

t2_key = "Start Time:"
t3_key = "End Time:"

# Open the file and find the times:
with open(log_file, 'r') as _f:
    for line in _f:
        if t2_key in line:
            
            keys = line.rstrip('\n').split(t2_key)
            print(keys)
            time_2 = 1.0
        if t3_key in line:
            keys = line.rstrip('\n').split(t3_key)
            print(keys)
            time_3 = 1.0


