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
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_altitude_plot(activity_one: SuuntoJSON, activity_two: SuuntoJSON):
    x_altitude_one = [datetime.datetime.fromisoformat(i) for i in activity_one.altitude.keys()]
    x_gps_altitude_one = [datetime.datetime.fromisoformat(i) for i in activity_one.gps_altitude.keys()]
    x_altitude_two = [datetime.datetime.fromisoformat(i) for i in activity_two.altitude.keys()]
    x_gps_altitude_two = [datetime.datetime.fromisoformat(i) for i in activity_two.gps_altitude.keys()]
    matplotlib.use("GTK3Cairo")
    plt.plot(x_altitude_one, activity_one.altitude.values(), label=f"{activity_one.name} Altitude (altimeter)")
    plt.plot(x_gps_altitude_one, activity_one.gps_altitude.values(), label=f"{activity_one.name} Altitude (GNSS)")
    plt.plot(x_altitude_two, activity_two.altitude.values(), label=f"{activity_two.name} Altitude (altimeter)")
    plt.plot(x_gps_altitude_two, activity_two.gps_altitude.values(), label=f"{activity_two.name} Altitude (GNSS)")
    plt.ylabel("Altitude (m)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def cadence_plot(activity: SuuntoJSON):
    x_cadence = [datetime.datetime.fromisoformat(i) for i in activity.cadence.keys()]
    matplotlib.use("GTK3Cairo")
    plt.plot(x_cadence, activity.cadence.values(), "bo")
    plt.ylabel("Cadence (rpm)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_cadence_plot(activity_one: SuuntoJSON, activity_two: SuuntoJSON):
    x_cadence_one = [datetime.datetime.fromisoformat(i) for i in activity_one.cadence.keys()]
    x_cadence_two = [datetime.datetime.fromisoformat(i) for i in activity_two.cadence.keys()]
    matplotlib.use("GTK3Cairo")
    plt.plot(x_cadence_one, activity_one.cadence.values(), "bo", label=activity_one.name)
    plt.plot(x_cadence_two, activity_two.cadence.values(), "ro", label=activity_two.name)
    plt.ylabel("Cadence (rpm)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def gps_snr_plot(activity: SuuntoJSON):
    x_gps_snr = [datetime.datetime.fromisoformat(i) for i in activity.gps_snr.keys()]
    matplotlib.use("GTK3Cairo")
    plt.plot(x_gps_snr, activity.gps_snr.values())
    plt.ylabel("GNSS SNR")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_gps_snr_plot(activity_one: SuuntoJSON, activity_two: SuuntoJSON):
    x_gps_snr_one = [datetime.datetime.fromisoformat(i) for i in activity_one.gps_snr.keys()]
    x_gps_snr_two = [datetime.datetime.fromisoformat(i) for i in activity_two.gps_snr.keys()]
    matplotlib.use("GTK3Cairo")
    plt.plot(x_gps_snr_one, activity_one.gps_snr.values(), label=activity_one.name)
    plt.plot(x_gps_snr_two, activity_two.gps_snr.values(), label=activity_two.name)
    plt.ylabel("GNSS SNR")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def hr_plot(activity: SuuntoJSON):
    x_hr = [datetime.datetime.fromisoformat(i) for i in activity.hr.keys()]
    matplotlib.use("GTK3Cairo")
    plt.plot(x_hr, activity.hr.values())
    plt.ylabel("Heart Rate (bpm)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_hr_plot(activity_one: SuuntoJSON, activity_two: SuuntoJSON):
    x_hr_one = [datetime.datetime.fromisoformat(i) for i in activity_one.hr.keys()]
    x_hr_two = [datetime.datetime.fromisoformat(i) for i in activity_two.hr.keys()]
    matplotlib.use("GTK3Cairo")
    plt.plot(x_hr_one, activity_one.hr.values(), label=activity_one.name)
    plt.plot(x_hr_two, activity_two.hr.values(), label=activity_two.name)
    plt.ylabel("Heart Rate (bpm)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()
