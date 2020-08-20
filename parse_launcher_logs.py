starts, dones, errors = [], [], []

from dateutil.parser import parse
import numpy as np
import sys
from pathlib import Path
import pickle
from collections import Counter
from balsam.core.models import BalsamJob
from django.db import transaction

logfile = Path(sys.argv[1])
if not logfile.is_file():
    raise ValueError(f"{sys.argv[1]} is not a file")

workflow = sys.argv[2]
jobs = BalsamJob.objects.filter(workflow=workflow)
if not jobs.exists():
    raise ValueError(f"No jobs matching workflow {workflow}")

jobs_dict = {(job.id[:8], job.name): job for job in jobs}

def parse_line(line):
    time_str = line.split('|')[0]
    t = parse(time_str)

    line = line[line.index("[")+1:]
    line = line[:line.index("]")]
    name, id = line.split("|")
    return t, name.strip(), id.strip()

with open(logfile) as fp:
    for line in logfile:
        if 'WORKER_START' in line:
            t, name, id = parse_line(line)
            jobs_dict[(id, name)].data["t0"] = t.isoformat()
        elif 'WORKER_DONE' in line:
            t, name, id = parse_line(line)
            jobs_dict[(id, name)].data["t4"] = t.isoformat()
        elif 'WORKER_ERROR' in line:
            t, name, id = parse_line(line)
            jobs_dict[(id, name)].data["t_err"] = t.isoformat()


with transaction.atomic():
    for job in jobs_dict.values():
        job.save(update_fields=["data"])
