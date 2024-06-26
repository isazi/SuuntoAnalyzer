import argparse
import datetime
from os import path
import numpy

import suunto_analyzer.json_reader as json_reader
import suunto_analyzer.analysis as analysis
import suunto_analyzer.plot as plot
import suunto_analyzer.track as track


def command_line():
    parser = argparse.ArgumentParser()
    # Files
    parser.add_argument(
        "-f", "--files", help="Files to analyze", type=str, required=True, nargs="+"
    )
    parser.add_argument("--plot", help="Enable plotting", action="store_true")
    parser.add_argument("--duration", help="Show duration", action="store_true")
    parser.add_argument("--distance", help="Show distance", action="store_true")
    parser.add_argument("--steps", help="Show the number of steps", action="store_true")
    parser.add_argument("--sensors", help="Show the used sensors", action="store_true")
    parser.add_argument("--apps", help="Show the enabled S+ apps", action="store_true")
    parser.add_argument(
        "--gps_error",
        help="Shows the GPS horizontal/vertical error.",
        action="store_true",
    )
    parser.add_argument(
        "--snr", help="Show SNR of 5 best GNSS satellites", action="store_true"
    )
    parser.add_argument(
        "--battery", help="Show battery consumption", action="store_true"
    )
    parser.add_argument("--cadence", help="Show cadence", action="store_true")
    parser.add_argument("--temperature", help="Show temperature", action="store_true")
    parser.add_argument(
        "--altitude", help="Show ascent, descent, and altitude", action="store_true"
    )
    parser.add_argument("--track", help="Plot GNSS track", action="store_true")
    parser.add_argument("--power", help="Show power", action="store_true")
    parser.add_argument("--hr", help="Show heart rate", action="store_true")
    parser.add_argument(
        "--compare", help="Enable comparison between activities", action="store_true"
    )
    return parser.parse_args()


def plotting(arguments: argparse.Namespace, activity: json_reader.SuuntoJSON):
    if arguments.snr:
        plot.gps_snr_plot(activity)
    if arguments.gps_error:
        plot.gps_error_plot(activity)
    if arguments.temperature:
        plot.temperature_plot(activity)
    if arguments.altitude:
        plot.altitude_plot(activity)
    if arguments.cadence:
        plot.cadence_plot(activity)
    if arguments.hr:
        plot.hr_plot(activity)
    if arguments.battery:
        plot.battery_charge_plot(activity)
    if arguments.power:
        plot.power_plot(activity)


def comparison(arguments: argparse.Namespace, activities: list):
    if arguments.snr:
        plot.compare_gps_snr_plot(activities)
    if arguments.altitude:
        plot.compare_altitude_plot(activities)
    if arguments.cadence:
        plot.compare_cadence_plot(activities)
    if arguments.hr:
        plot.compare_hr_plot(activities)
    if arguments.distance:
        plot.compare_running_distance_plot(activities)
    if arguments.temperature:
        plot.compare_temperature_plot(activities)
    if arguments.power:
        plot.compare_power_plot(activities)


def __main__():
    print("Suunto Activity Analyzer (SAA)")
    print()
    arguments = command_line()
    activities = []
    for file in arguments.files:
        print(f"Loading:\t{path.basename(file)}")
        activity = json_reader.SuuntoJSON()
        activity.load_file(file)
        activities.append(activity)
    print()
    # Activity loop
    for activity in activities:
        # Base functions
        print(f"Device:\t\t{activity.name}")
        print(f"GNSS:\t\t{activity.gnss}")
        print(f"Time:\t\t{activity.datetime}")
        print()
        if arguments.sensors and len(activity.sensors) >= 1:
            print(f"Sensors:\t{activity.sensors}")
            print()
        if arguments.apps and len(activity.apps) >= 1:
            print(f"S+ Apps:\t{activity.apps}")
            print()
        if arguments.duration:
            print(f"Duration:\t{datetime.timedelta(seconds=activity.duration)}")
            print()
        if arguments.distance:
            print(f"Distance:\t{activity.distance:.2f} km")
            print()
        if arguments.steps:
            print(f"Steps:\t\t{activity.steps}")
            if arguments.cadence:
                cadence_values = [i for i in activity.cadence.values()]
                ref_steps = int(numpy.average(cadence_values) * 2) * int(
                    activity.duration / 60
                )
                print(f"Ref steps:\t{ref_steps}")
                print(
                    f"Difference:\t{((activity.steps - ref_steps) * 100.0) / ref_steps:.2f}%"
                )
            print()
        if arguments.snr:
            analysis.gps_snr_analysis(activity)
            print()
        if arguments.gps_error:
            analysis.gps_error_analysis(activity)
            print()
        if arguments.temperature:
            analysis.temperature_analysis(activity)
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
            plotting(arguments, activity)
    if arguments.track:
        track.plot_track(activities)
    # Comparing metrics
    if arguments.compare:
        comparison(arguments, activities)


if __name__ == "__main__":
    __main__()
