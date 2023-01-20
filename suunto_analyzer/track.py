import matplotlib.pyplot as plt
from suunto_analyzer.json_reader import SuuntoJSON

def plot_track(activities: list):
    for activity in activities:
        lat, lon = zip(*activity.coordinates)
        plt.plot(lon, lat, label=activity.name)
    plt.ylabel("Longitude")
    plt.xlabel("Latitude")
    plt.legend()
    plt.show()