import datetime
import matplotlib
import matplotlib.pyplot as plt
from json_reader import SuuntoJSON


def altitude_plot(activity: SuuntoJSON):
    x_altitude = [datetime.datetime.fromisoformat(i) for i in activity.altitude.keys()]
    x_gps_altitude = [datetime.datetime.fromisoformat(i) for i in activity.gps_altitude.keys()]
    matplotlib.use("GTK3Cairo")
    plt.plot(x_altitude, activity.altitude.values(), label="Altitude (altimeter)")
    plt.plot(x_gps_altitude, activity.gps_altitude.values(), label="Altitude (GNSS)")
    plt.ylabel("Altitude (m)")
    plt.xlabel("Time")
    plt.xticks([])
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def cadence_plot(activity: SuuntoJSON):
    x_cadence = [datetime.datetime.fromisoformat(i) for i in activity.cadence.keys()]
    matplotlib.use("GTK3Cairo")
    plt.plot(x_cadence, activity.cadence.values(), "bo")
    plt.ylabel("Cadence (rpm)")
    plt.xlabel("Time")
    plt.xticks([])
    plt.gcf().autofmt_xdate()
    plt.show()
