from balsam.core.models import BalsamJob
from collections import Counter
import numpy as np
from dateutil.parser import isoparse
from math import floor

def fetch_by_workflow(workflow):
    """
    Get times_list for a particular workflow string
    """
    jobs = BalsamJob.objects.filter(workflow=workflow)
    times_list = list(jobs.values_list("data", flat=True))
    for d in times_list:
        for key in d:
            try:
                d[key] = isoparse(d[key])
            except ValueError:
                print(f"WARNING: failed to isoparse time stamp {d[key]}")
    return times_list

def get_inner_app_runtimes(times_list):
    """
    Generates a sequence of [ (t2, t3-t2) ]
    Where t2 is application start time and t3-t2 is the inner app runtime
    """
    for d in times_list:
        if "t2" in d and "t3" in d:
            yield (d["t2"], d["t3"] - d["t2"])

def get_start_delays(times_list):
    """
    Generates a sequence of [ (t0, t2-t0) ]
    Where t0 is worker start time and t2-t0 is the Popen startup delay
    """
    for d in times_list:
        if "t2" in d and "t0" in d:
            yield (d["t0"], d["t2"] - d["t0"])

def get_end_delays(times_list):
    """
    Generates a sequence of [ (t3, t4-t3) ]
    Where t3 is application end time and t4-t3 is the Popen end delay
    """
    for d in times_list:
        if "t3" in d and "t4" in d:
            yield (d["t3"], d["t4"] - d["t3"])


def generate_percentiles(times, time_deltas, num_bins=100, percentiles=[25, 50, 75]):
    """
    From a list of times and corresponding time_deltas, generate percentiles
    of the time_deltas binned according to time.

    Returns a tuple of equal-length lists:
        bin_centers, percentile1, percentile2, ...
    """
    t_min = min(times)
    t_max = max(times)

    bin_width = (t_max - t_min).total_seconds() / num_bins
    times = [(t - t_min).total_seconds() for t in times]
    time_deltas = [td.total_seconds() for td in time_deltas]

    bin_centers = [(i+1)*bin_width/2 for i in range(num_bins)]
    bins = [[] for i in range(num_bins)]

    for t, td in zip(times, time_deltas):
        i = floor(t / bin_width)
        bins[i].append(td)

    bin_centers = [center for (center, bin) in zip(bin_centers, bins) if bin]
    bins = [np.array(bin) for bin in bins if bin]
    results = [
        [np.percentile(bin, percentile) for bin in bins]
        for percentile in percentiles
    ]
    return (bin_centers, *results)



def plot_end_delays(workflow):
    time_dat = fetch_by_workflow(workflow)
    T2, Tdelay = zip(*get_end_delays(time_dat))
    from matplotlib import pyplot as plt
    plt.scatter(T2, Tdelay)
