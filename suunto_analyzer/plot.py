from __future__ import annotations

import matplotlib.pyplot as plt
from suunto_analyzer.activity import Activity


def altitude_plot(activity: Activity):
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


def compare_altitude_plot(activities: list[Activity]):
    for activity in activities:
        if len(activity.altitude) >= 1:
            plt.plot(
                activity.altitude.keys(),
                activity.altitude.values(),
                label=f"{activity.name} Altitude (altimeter)",
            )
        if len(activity.gps_altitude) >= 1:
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


def cadence_plot(activity: Activity):
    plt.plot(activity.cadence.keys(), activity.cadence.values())
    plt.ylabel("Cadence (rpm)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_cadence_plot(activities: list[Activity]):
    for activity in activities:
        if len(activity.cadence) >= 1:
            plt.plot(
                activity.cadence.keys(),
                activity.cadence.values(),
                label=activity.name,
            )
    plt.ylabel("Cadence (rpm)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def gps_snr_plot(activity: Activity):
    plt.plot(activity.gps_snr.keys(), activity.gps_snr.values())
    plt.ylabel("GNSS SNR")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_gps_snr_plot(activities: list[Activity]):
    for activity in activities:
        if len(activity.gps_snr) >= 1:
            plt.plot(
                activity.gps_snr.keys(),
                activity.gps_snr.values(),
                label=activity.name,
            )
    plt.ylabel("GNSS SNR")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def gps_error_plot(activity: Activity):
    plt.plot(activity.ehpe.keys(), activity.ehpe.values(), label="Horizontal Error")
    plt.plot(activity.evpe.keys(), activity.evpe.values(), label="Vertical Error")
    plt.ylabel("GNSS Error")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def hr_plot(activity: Activity):
    if len(activity.hr.values()) >= 1:
        plt.plot(activity.hr.keys(), activity.hr.values())
        plt.ylabel("Heart Rate (bpm)")
        plt.xlabel("Time")
        plt.gcf().autofmt_xdate()
        plt.show()


def rr_plot(activity: Activity):
    if len(activity.rr) >= 1:
        plt.plot(activity.rr, "o")
        plt.ylabel("Inter-Beat Interval (ms)")
        plt.xlabel("Time")
        plt.gcf().autofmt_xdate()
        plt.show()


def compare_hr_plot(activities: list[Activity]):
    for activity in activities:
        if len(activity.hr) >= 1:
            plt.plot(activity.hr.keys(), activity.hr.values(), label=activity.name)
    plt.ylabel("Heart Rate (bpm)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_rr_plot(activities: list[Activity]):
    for activity in activities:
        if len(activity.rr) >= 1:
            plt.plot(activity.rr, "o", label=activity.name)
    plt.ylabel("Inter-Beat Interval (ms)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_running_distance_plot(activities: list[Activity]):
    for activity in activities:
        if len(activity.running_distance) >= 1:
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


def battery_charge_plot(activity: Activity):
    battery_charge = [i * 100.0 for i in activity.battery_charge.values()]
    plt.plot(activity.battery_charge.keys(), battery_charge)
    plt.ylabel("Battery Charge (%)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def temperature_plot(activity: Activity):
    y_temperature = [(i - 273.15) for i in activity.temperature.values()]
    plt.plot(activity.temperature.keys(), y_temperature, "o")
    plt.ylabel("Temperature (C)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_temperature_plot(activities: list[Activity]):
    for activity in activities:
        if len(activity.temperature) >= 1:
            y_temperature = [(i - 273.15) for i in activity.temperature.values()]
            plt.plot(
                activity.temperature.keys(),
                y_temperature,
                label=activity.name,
            )
    plt.ylabel("Temperature (C)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def power_plot(activity: Activity):
    plt.plot(activity.power.keys(), activity.power.values(), "o")
    plt.ylabel("Power (W)")
    plt.xlabel("Time")
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_power_plot(activities: list[Activity]):
    for activity in activities:
        if len(activity.power) >= 1:
            plt.plot(
                activity.power.keys(),
                activity.power.values(),
                label=activity.name,
            )
    plt.ylabel("Power (W)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_battery_charge_plot(activities: list[Activity]):
    for activity in activities:
        if len(activity.battery_charge) >= 1:
            battery_charge = [i * 100.0 for i in activity.battery_charge.values()]
            plt.plot(
                activity.battery_charge.keys(),
                battery_charge,
                label=activity.name,
            )
    plt.ylabel("Battery Charge (%)")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def compare_gps_error_plot(activities: list[Activity]):
    for activity in activities:
        if len(activity.ehpe) >= 1:
            plt.plot(
                activity.ehpe.keys(),
                activity.ehpe.values(),
                label=f"{activity.name} Horizontal Error",
            )
        if len(activity.evpe) >= 1:
            plt.plot(
                activity.evpe.keys(),
                activity.evpe.values(),
                label=f"{activity.name} Vertical Error",
            )
    plt.ylabel("GNSS Error")
    plt.xlabel("Time")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()
