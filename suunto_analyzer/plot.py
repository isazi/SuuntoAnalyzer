import matplotlib.pyplot as plt
from suunto_analyzer.json_reader import SuuntoJSON


def altitude_plot(activity: SuuntoJSON):
    plt.plot(
        activity.altitude.keys(),
        activity.altitude.values(),
        label="Altitude (altimeter)",
    )
    plt.plot(
        activity.gps_altitude.keys(),
        activity.gps_altitude.values(),
        label="Altitude (GNSS)",
    )
    plt.ylabel("Altitude (m)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_altitude_plot(activities: list):
    for activity in activities:
        plt.plot(
            activity.altitude.keys(),
            activity.altitude.values(),
            label=f"{activity.name} Altitude (altimeter)",
        )
        plt.plot(
            activity.gps_altitude.keys(),
            activity.gps_altitude.values(),
            label=f"{activity.name} Altitude (GNSS)",
        )
    plt.ylabel("Altitude (m)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def cadence_plot(activity: SuuntoJSON):
    plt.plot(activity.cadence.keys(), activity.cadence.values())
    plt.ylabel("Cadence (rpm)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_cadence_plot(activities: list):
    for activity in activities:
        plt.plot(
            activity.cadence.keys(), activity.cadence.values(), label=activity.name
        )
    plt.ylabel("Cadence (rpm)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def gps_snr_plot(activity: SuuntoJSON):
    plt.plot(activity.gps_snr.keys(), activity.gps_snr.values())
    plt.ylabel("GNSS SNR")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_gps_snr_plot(activities: list):
    for activity in activities:
        plt.plot(
            activity.gps_snr.keys(), activity.gps_snr.values(), label=activity.name
        )
    plt.ylabel("GNSS SNR")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def gps_error_plot(activity: SuuntoJSON):
    plt.plot(activity.ehpe.keys(), activity.ehpe.values(), label="Horizontal Error")
    plt.plot(activity.evpe.keys(), activity.evpe.values(), label="Vertical Error")
    plt.ylabel("GNSS Error")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def hr_plot(activity: SuuntoJSON):
    if len(activity.hr.values()) >= 1:
        plt.plot(activity.hr.keys(), activity.hr.values())
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
        plt.plot(activity.hr.keys(), activity.hr.values(), label=activity.name)
    plt.ylabel("Heart Rate (bpm)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_running_distance_plot(activities: list):
    for activity in activities:
        plt.plot(
            activity.running_distance.keys(),
            activity.running_distance.values(),
            label=activity.name,
        )
    plt.ylabel("Distance (m)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def battery_charge_plot(activity: SuuntoJSON):
    battery_charge = [i * 100.0 for i in activity.battery_charge.values()]
    plt.plot(activity.battery_charge.keys(), battery_charge)
    plt.ylabel("Battery Charge (%)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def temperature_plot(activity: SuuntoJSON):
    y_temperature = [(i - 273.15) for i in activity.temperature.values()]
    plt.plot(activity.temperature.keys(), y_temperature, "o")
    plt.ylabel("Temperature (C)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_temperature_plot(activities: list):
    for activity in activities:
        y_temperature = [(i - 273.15) for i in activity.temperature.values()]
        plt.plot(activity.temperature.keys(), y_temperature, label=activity.name)
    plt.ylabel("Temperature (C)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def power_plot(activity: SuuntoJSON):
    plt.plot(activity.power.keys(), activity.power.values(), "o")
    plt.ylabel("Power (W)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_power_plot(activities: list):
    for activity in activities:
        plt.plot(activity.power.keys(), activity.power.values(), label=activity.name)
    plt.ylabel("Power (W)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()
