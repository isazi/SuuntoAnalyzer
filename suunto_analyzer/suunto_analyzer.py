import argparse
import datetime
from os import path

import json_reader
import analysis
import plot


def command_line():
    parser = argparse.ArgumentParser()
    # Files
    parser.add_argument("-f", "--filename", help="File to analyze", type=str, required=True)
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--duration", action="store_true")
    parser.add_argument("--distance", action="store_true")
    parser.add_argument("--sensors", action="store_true")
    parser.add_argument("--snr", action="store_true")
    parser.add_argument("--battery", action="store_true")
    parser.add_argument("--cadence", action="store_true")
    parser.add_argument("--altitude", action="store_true")
    parser.add_argument("--power", action="store_true")
    parser.add_argument("--hr", action="store_true")
    parser.add_argument("--compare", action="store_true")
    parser.add_argument("-f2", "--filename2", help="File to compare with.", type=str)
    return parser.parse_args()


def __main__():
    print("Suunto Activity Analyzer (SAA)")
    print()

    arguments = command_line()
    activity = json_reader.SuuntoJSON()
    activity.load_file(arguments.filename)
    # Base functions
    print(f"Filename:\t{path.basename(arguments.filename)}")
    print(f"Device:\t\t{activity.name}")
    print(f"GNSS:\t\t{activity.gnss}")
    print(f"Time:\t\t{activity.datetime}")
    print()
    if arguments.sensors and len(activity.sensors) >= 1:
        print(f"Sensors:\t{activity.sensors}")
        print()
    if arguments.duration:
        print(f"Duration:\t{datetime.timedelta(seconds=activity.duration)}")
        print()
    if arguments.distance:
        print(f"Distance:\t{activity.distance:.2f} km")
        print()
    if arguments.snr:
        analysis.gps_snr_analysis(activity)
        print()
    if arguments.altitude:
        analysis.altitude_analysis(activity)
        print()
    if arguments.battery:
        analysis.battery_analysis(activity)
        print()
    if arguments.cadence:
        analysis.cadence_analysis(activity)
        print()
    if arguments.hr:
        analysis.hr_analysis(activity)
        print()
    if arguments.power:
        analysis.power_analysis(activity)
        print()
    # Plotting
    if arguments.plot:
        if arguments.snr:
            plot.gps_snr_plot(activity)
        if arguments.altitude:
            plot.altitude_plot(activity)
        if arguments.cadence:
            plot.cadence_plot(activity)
        if arguments.hr:
            plot.hr_plot(activity)
        if arguments.battery:
            plot.battery_charge_plot(activity)
    # Comparing with another file
    if arguments.compare and arguments.filename2 is not None:
        other_activity = json_reader.SuuntoJSON()
        other_activity.load_file(arguments.filename2)
        if arguments.snr:
            plot.compare_gps_snr_plot(activity, other_activity)
        if arguments.altitude:
            plot.compare_altitude_plot(activity, other_activity)
        if arguments.cadence:
            plot.compare_cadence_plot(activity, other_activity)
        if arguments.hr:
            plot.compare_hr_plot(activity, other_activity)
        if arguments.distance:
            plot.compare_running_distance_plot(activity, other_activity)


if __name__ == "__main__":
    __main__()
