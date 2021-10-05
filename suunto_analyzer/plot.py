import matplotlib
import matplotlib.pyplot as plt
from json_reader import SuuntoJSON


def altitude_plot(activity: SuuntoJSON):
    matplotlib.use("GTK3Cairo")
    plt.plot([i for i in range(0, len(activity.altitude.keys()))], activity.altitude.values(),
             label="Altitude (altimeter)")
    plt.plot([i for i in range(0, len(activity.gps_altitude.keys()))], activity.gps_altitude.values(),
             label="Altitude (GNSS)")
    plt.ylabel("Altitude (m)")
    plt.xlabel("Time")
    plt.xticks([])
    plt.legend()
    plt.show()
