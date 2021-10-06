import argparse
import datetime
from os import path

import json_reader
import analysis
import plot


def command_line():
    parser = argparse.ArgumentParser()
    # Files
    parser.add_argument("-f", "--filename", type=str, required=True)
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--duration", action="store_true")
    parser.add_argument("--distance", action="store_true")
    parser.add_argument("--snr", action="store_true")
    parser.add_argument("--battery", action="store_true")
    parser.add_argument("--cadence", action="store_true")
    parser.add_argument("--altitude", action="store_true")
    return parser.parse_args()


def __main__():
    print("Suunto Activity Analyzer (SAA)")
    print()

    arguments = command_line()
    activity = json_reader.SuuntoJSON()
    activity.load_file(arguments.filename)
    print(f"Filename:\t{path.basename(arguments.filename)}")
    print(f"Device:\t\t{activity.name}")
    print(f"GNSS:\t\t{activity.gnss}")
    print(f"Time:\t\t{activity.datetime}")
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
    if arguments.plot:
        if arguments.altitude:
            plot.altitude_plot(activity)
        if arguments.cadence:
            plot.cadence_plot(activity)
    return 0


if __name__ == "__main__":
    __main__()
