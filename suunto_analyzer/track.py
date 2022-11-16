import matplotlib.pyplot as plt
from suunto_analyzer.json_reader import SuuntoJSON

def plot_track(activity: SuuntoJSON):
    lat, lon = zip(*activity.coordinates)
    plt.plot(lon, lat)
    plt.show()