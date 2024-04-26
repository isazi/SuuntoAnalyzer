import argparse
import numpy as np
import matplotlib.pyplot as plt
from suunto_analyzer.json_reader import SuuntoJSON

parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, nargs="+", help="Suunto JSON files to process")
args = parser.parse_args()

data = dict()
data["Suunto 9 Baro"] = list()
data["Suunto 9 Peak"] = list()
data["Suunto 5 Peak"] = list()

for file in args.file:
    activity = SuuntoJSON()
    try:
        activity.load_file(file)
    except Exception:
        continue
    battery_values = [i for i in activity.battery_charge.values()]
    if len(battery_values) == 0:
        continue
    battery_values = np.array(battery_values)
    max_battery = np.max(battery_values)
    min_battery = np.min(battery_values)
    if (max_battery - min_battery) == 0:
        continue
    if "Ibiza" in activity.name:
        data["Suunto 9 Baro"].append(
            (activity.duration / (max_battery - min_battery)) / 3600.0
        )
    elif "Nagano" in activity.name:
        data["Suunto 9 Peak"].append(
            (activity.duration / (max_battery - min_battery)) / 3600.0
        )
    elif "Qingdao" in activity.name:
        data["Suunto 5 Peak"].append(
            (activity.duration / (max_battery - min_battery)) / 3600.0
        )
    else:
        print(f"Unknown device: {activity.name}")

# Stats
data["Suunto 9 Baro"] = np.array(data["Suunto 9 Baro"])
data["Suunto 9 Peak"] = np.array(data["Suunto 9 Peak"])
data["Suunto 5 Peak"] = np.array(data["Suunto 5 Peak"])
print(
    f"Avg battery life (in hours) S9B: {np.average(data['Suunto 9 Baro']):.2f} ±{np.std(data['Suunto 9 Baro']):.1f}"
)
print(
    f"Avg battery life (in hours) S9P: {np.average(data['Suunto 9 Peak']):.2f} ±{np.std(data['Suunto 9 Peak']):.1f}"
)
print(
    f"Avg battery life (in hours) S5P: {np.average(data['Suunto 5 Peak']):.2f} ±{np.std(data['Suunto 5 Peak']):.1f}"
)
# Plotting
plt.plot(data["Suunto 9 Baro"], label="Suunto 9 Baro")
plt.plot(data["Suunto 9 Peak"], label="Suunto 9 Peak")
plt.plot(data["Suunto 5 Peak"], label="Suunto 5 Peak")
plt.ylabel("Estimated Battery Life (hours)")
plt.legend()
plt.show()
