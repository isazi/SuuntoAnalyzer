# Quantify the median SNR of different Suunto watches
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
from suunto_analyzer.json_reader import SuuntoJSON


def command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="*", required=True, type=str)
    return parser.parse_args()


used_devices = ["Ibiza", "Nagano", "Qingdao", "Sapporo"]
data = dict()
arguments = command_line()

for filename in arguments.files:
    activity = SuuntoJSON()
    activity.load_file(filename)
    device = activity.name.split()[0]
    if device not in used_devices:
        continue
    try:
        data[device]
    except KeyError:
        data[device] = []
    median_of_medians = np.median(list(activity.gps_snr.values()))
    if math.isfinite(median_of_medians):
        data[device].append(median_of_medians)

for device in data.keys():
    print(f"{device} median SNR: {np.median(data[device])}")
    plt.violinplot(data[device], showmedians=True, showextrema=True)
    plt.title(device)
    plt.show()
