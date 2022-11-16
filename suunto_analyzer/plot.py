import datetime
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


def compare_altitude_plot(activity_one: SuuntoJSON, activity_two: SuuntoJSON):
    x_altitude_one = [datetime.datetime.fromisoformat(i) for i in activity_one.altitude.keys()]
    x_gps_altitude_one = [datetime.datetime.fromisoformat(i) for i in activity_one.gps_altitude.keys()]
    x_altitude_two = [datetime.datetime.fromisoformat(i) for i in activity_two.altitude.keys()]
    x_gps_altitude_two = [datetime.datetime.fromisoformat(i) for i in activity_two.gps_altitude.keys()]
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
    plt.plot(x_cadence, activity.cadence.values(), "bo")
    plt.ylabel("Cadence (rpm)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_cadence_plot(activity_one: SuuntoJSON, activity_two: SuuntoJSON):
    x_cadence_one = [datetime.datetime.fromisoformat(i) for i in activity_one.cadence.keys()]
    x_cadence_two = [datetime.datetime.fromisoformat(i) for i in activity_two.cadence.keys()]
    plt.plot(x_cadence_one, activity_one.cadence.values(), "bo", label=activity_one.name)
    plt.plot(x_cadence_two, activity_two.cadence.values(), "ro", label=activity_two.name)
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


def compare_gps_snr_plot(activity_one: SuuntoJSON, activity_two: SuuntoJSON):
    x_gps_snr_one = [datetime.datetime.fromisoformat(i) for i in activity_one.gps_snr.keys()]
    x_gps_snr_two = [datetime.datetime.fromisoformat(i) for i in activity_two.gps_snr.keys()]
    plt.plot(x_gps_snr_one, activity_one.gps_snr.values(), label=activity_one.name)
    plt.plot(x_gps_snr_two, activity_two.gps_snr.values(), label=activity_two.name)
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
        plt.plot(activity.rr, "ro")
        plt.ylabel("Inter-Beat Interval (ms)")
        plt.xlabel("Time")
        plt.gcf().autofmt_xdate()
        plt.show()


def compare_hr_plot(activity_one: SuuntoJSON, activity_two: SuuntoJSON):
    x_hr_one = [datetime.datetime.fromisoformat(i) for i in activity_one.hr.keys()]
    x_hr_two = [datetime.datetime.fromisoformat(i) for i in activity_two.hr.keys()]
    plt.plot(x_hr_one, activity_one.hr.values(), label=activity_one.name)
    plt.plot(x_hr_two, activity_two.hr.values(), label=activity_two.name)
    plt.ylabel("Heart Rate (bpm)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_running_distance_plot(activity_one: SuuntoJSON, activity_two: SuuntoJSON):
    x_running_distance_one = [datetime.datetime.fromisoformat(i) for i in activity_one.running_distance.keys()]
    x_running_distance_two = [datetime.datetime.fromisoformat(i) for i in activity_two.running_distance.keys()]
    plt.plot(x_running_distance_one, activity_one.running_distance.values(), label=activity_one.name)
    plt.plot(x_running_distance_two, activity_two.running_distance.values(), label=activity_two.name)
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
    plt.plot(x_temperature, y_temperature, "bo")
    plt.ylabel("Temperature (C)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_temperature_plot(activity_one: SuuntoJSON, activity_two: SuuntoJSON):
    x_temperature_one = [datetime.datetime.fromisoformat(i) for i in activity_one.temperature.keys()]
    y_temperature_one = [(i - 273.15) for i in activity_one.temperature.values()]
    x_temperature_two = [datetime.datetime.fromisoformat(i) for i in activity_two.temperature.keys()]
    y_temperature_two = [(i - 273.15) for i in activity_two.temperature.values()]
    plt.plot(x_temperature_one, y_temperature_one, label=activity_one.name)
    plt.plot(x_temperature_two, y_temperature_two, label=activity_two.name)
    plt.ylabel("Temperature (C)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def power_plot(activity: SuuntoJSON):
    x_power = [datetime.datetime.fromisoformat(i) for i in activity.power.keys()]
    plt.plot(x_power, activity.power.values(), "bo")
    plt.ylabel("Power (W)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_power_plot(activity_one: SuuntoJSON, activity_two: SuuntoJSON):
    x_power_one = [datetime.datetime.fromisoformat(i) for i in activity_one.power.keys()]
    x_power_two = [datetime.datetime.fromisoformat(i) for i in activity_two.power.keys()]
    plt.plot(x_power_one, activity_one.power.values(), label=activity_one.name)
    plt.plot(x_power_two, activity_two.power.values(), label=activity_two.name)
    plt.ylabel("Power (W)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()