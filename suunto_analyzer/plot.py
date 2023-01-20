import datetime
import matplotlib
import matplotlib.pyplot as plt
from suunto_analyzer.json_reader import SuuntoJSON


def altitude_plot(activity: SuuntoJSON):
    x_altitude = [datetime.datetime.fromisoformat(i) for i in activity.altitude.keys()]
    x_gps_altitude = [datetime.datetime.fromisoformat(i) for i in activity.gps_altitude.keys()]
    plt.plot(x_altitude, activity.altitude.values(), label="Altitude (altimeter)")
    plt.plot(x_gps_altitude, activity.gps_altitude.values(), label="Altitude (GNSS)")
    plt.ylabel("Altitude (m)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_altitude_plot(activities: list):
    for activity in activities:
        x_altitude = [datetime.datetime.fromisoformat(i) for i in activity.altitude.keys()]
        x_gps_altitude = [datetime.datetime.fromisoformat(i) for i in activity.gps_altitude.keys()]
        plt.plot(x_altitude, activity.altitude.values(), label=f"{activity.name} Altitude (altimeter)")
        plt.plot(x_gps_altitude, activity.gps_altitude.values(), label=f"{activity.name} Altitude (GNSS)")
    plt.ylabel("Altitude (m)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def cadence_plot(activity: SuuntoJSON):
    x_cadence = [datetime.datetime.fromisoformat(i) for i in activity.cadence.keys()]
    plt.plot(x_cadence, activity.cadence.values(), "o")
    plt.ylabel("Cadence (rpm)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_cadence_plot(activities: list):
    for activity in activities:
        x_cadence = [datetime.datetime.fromisoformat(i) for i in activity.cadence.keys()]
        plt.plot(x_cadence, activity.cadence.values(), "o", label=activity.name)
    plt.ylabel("Cadence (rpm)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def gps_snr_plot(activity: SuuntoJSON):
    x_gps_snr = [datetime.datetime.fromisoformat(i) for i in activity.gps_snr.keys()]
    plt.plot(x_gps_snr, activity.gps_snr.values())
    plt.ylabel("GNSS SNR")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_gps_snr_plot(activities: list):
    for activity in activities:
        x_gps_snr = [datetime.datetime.fromisoformat(i) for i in activity.gps_snr.keys()]
        plt.plot(x_gps_snr, activity.gps_snr.values(), label=activity.name)
    plt.ylabel("GNSS SNR")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def gps_error_plot(activity: SuuntoJSON):
    x_gps_error = [datetime.datetime.fromisoformat(i) for i in activity.ehpe.keys()]
    plt.plot(x_gps_error, activity.ehpe.values(), label="Horizontal Error")
    plt.plot(x_gps_error, activity.evpe.values(), label="Vertical Error")
    plt.ylabel("GNSS Error")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def hr_plot(activity: SuuntoJSON):
    if len(activity.hr.values()) >= 1:
        x_hr = [datetime.datetime.fromisoformat(i) for i in activity.hr.keys()]
        plt.plot(x_hr, activity.hr.values())
        plt.ylabel("Heart Rate (bpm)")
        plt.xlabel("Time")
        plt.gcf().autofmt_xdate()
        plt.show()
    elif len(activity.rr) >= 1:
        plt.plot(activity.rr, "o")
        plt.ylabel("Inter-Beat Interval (ms)")
        plt.xlabel("Time")
        plt.gcf().autofmt_xdate()
        plt.show()


def compare_hr_plot(activities: list):
    for activity in activities:
        x_hr = [datetime.datetime.fromisoformat(i) for i in activity.hr.keys()]
        plt.plot(x_hr, activity.hr.values(), label=activity.name)
    plt.ylabel("Heart Rate (bpm)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_running_distance_plot(activities: list):
    for activity in activities:
        x_running_distance = [datetime.datetime.fromisoformat(i) for i in activity.running_distance.keys()]
        plt.plot(x_running_distance, activity.running_distance.values(), label=activity.name)
    plt.ylabel("Distance (m)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def battery_charge_plot(activity: SuuntoJSON):
    x_battery_charge = [datetime.datetime.fromisoformat(i) for i in activity.battery_charge.keys()]
    battery_charge = [i * 100.0 for i in activity.battery_charge.values()]
    plt.plot(x_battery_charge, battery_charge)
    plt.ylabel("Battery Charge (%)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def temperature_plot(activity: SuuntoJSON):
    x_temperature = [datetime.datetime.fromisoformat(i) for i in activity.temperature.keys()]
    y_temperature = [(i - 273.15) for i in activity.temperature.values()]
    plt.plot(x_temperature, y_temperature, "o")
    plt.ylabel("Temperature (C)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_temperature_plot(activities: list):
    for activity in activities:
        x_temperature = [datetime.datetime.fromisoformat(i) for i in activity.temperature.keys()]
        y_temperature = [(i - 273.15) for i in activity.temperature.values()]
        plt.plot(x_temperature, y_temperature, label=activity.name)
    plt.ylabel("Temperature (C)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def power_plot(activity: SuuntoJSON):
    x_power = [datetime.datetime.fromisoformat(i) for i in activity.power.keys()]
    plt.plot(x_power, activity.power.values(), "o")
    plt.ylabel("Power (W)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_power_plot(activities: list):
    for activity in activities:
        x_power = [datetime.datetime.fromisoformat(i) for i in activity.power.keys()]
        plt.plot(x_power, activity.power.values(), label=activity.name)
    plt.ylabel("Power (W)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()