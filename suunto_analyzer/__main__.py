from __future__ import annotations

import argparse
import datetime
from os import path
import numpy

import suunto_analyzer.json_reader as json_reader
import suunto_analyzer.analysis as analysis
import suunto_analyzer.plot as plot
import suunto_analyzer.track as track
from suunto_analyzer.activity import Activity


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
        "--rr", help="Show inter-beat intervals (R-R)", action="store_true"
    )
    parser.add_argument(
        "--compare",
        help="Compare activities (text; add --plot for comparison plots)",
        action="store_true",
    )
    return parser.parse_args()


def load_activity(filename: str) -> Activity:
    """Load an activity, choosing the reader from the file extension."""
    extension = path.splitext(filename)[1].lower()
    if extension == ".json":
        activity = json_reader.SuuntoJSON()
    elif extension == ".fit":
        from suunto_analyzer import fit_reader

        try:
            fit_reader.require_fitdecode()
        except fit_reader.FitdecodeNotInstalled as error:
            raise SystemExit(str(error)) from None
        activity = fit_reader.SuuntoFIT()
    else:
        raise SystemExit(f"Unsupported activity file: {filename}")
    activity.load_file(filename)
    activity.filename = filename
    return activity


def plotting(arguments: argparse.Namespace, activity: Activity):
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
    if arguments.rr:
        plot.rr_plot(activity)
    if arguments.battery:
        plot.battery_charge_plot(activity)
    if arguments.power:
        plot.power_plot(activity)


MISSING = "–"


def normalize_label(label: str) -> str:
    return label.replace("\t", "").rstrip()


def collect_rows(
    activities: list[Activity], stats_func
) -> list[tuple[str, list[str | None]]]:
    """Turn per-activity stats into comparison rows.

    The row labels are the union of all activities' rows, in order of
    first appearance. An activity without a row gets ``None``.
    """
    rows_per_activity = [
        {normalize_label(label): value for label, value in stats_func(activity)}
        for activity in activities
    ]
    labels: list[str] = []
    for stats in rows_per_activity:
        for label in stats:
            if not label or "histogram" in label:
                continue
            if label not in labels:
                labels.append(label)
    rows = list()
    for label in labels:
        cells = [
            values.get(label, "").replace("\t", "  ").rstrip() or None
            for values in rows_per_activity
        ]
        rows.append((label, cells))
    return rows


def print_table(
    title: str,
    headers: list[str],
    rows: list[tuple[str, list[str | None]]],
):
    cells = [
        [value if value is not None else MISSING for value in row[1]] for row in rows
    ]
    first_width = max(len(label) for label, _ in rows)
    widths = [
        max(len(headers[index]), max(len(row[index]) for row in cells))
        for index in range(len(headers))
    ]
    print(title)
    print(" " * first_width + "  ", end="")
    print("  ".join(header.rjust(width) for header, width in zip(headers, widths)))
    for (label, _), row in zip(rows, cells):
        print(
            label.ljust(first_width)
            + "  "
            + "  ".join(cell.rjust(width) for cell, width in zip(row, widths))
        )


def column_headers(activities: list[Activity]) -> list[str]:
    counts = {}
    for activity in activities:
        counts[activity.name] = counts.get(activity.name, 0) + 1
    headers = list()
    for activity in activities:
        name = activity.name or "Unknown"
        if counts[activity.name] > 1:
            name = f"{name} ({path.basename(activity.filename)})"
        headers.append(name)
    return headers


def text_comparison(arguments: argparse.Namespace, activities: list[Activity]) -> bool:
    """Print a text based side-by-side comparison of the activities.

    Returns True when anything was printed.
    """
    headers = column_headers(activities)
    blocks: list[tuple[str, list[tuple[str, list[str | None]]]]] = list()
    summary: list[tuple[str, list[str | None]]] = list()
    if arguments.duration:
        summary.append(
            (
                "Duration",
                [
                    str(datetime.timedelta(seconds=activity.duration))
                    for activity in activities
                ],
            )
        )
    if arguments.distance:
        summary.append(
            ("Distance", [f"{activity.distance:.2f} km" for activity in activities])
        )
    if arguments.steps:
        summary.append(("Steps", [str(activity.steps) for activity in activities]))
    if summary:
        blocks.append(("Summary", summary))
    if arguments.snr and any(activity.gps_snr for activity in activities):
        blocks.append(("GNSS SNR", collect_rows(activities, analysis.gps_snr_stats)))
    if arguments.gps_error and any(
        activity.ehpe or activity.evpe for activity in activities
    ):
        blocks.append(
            ("GNSS error", collect_rows(activities, analysis.gps_error_stats))
        )
    if arguments.altitude and any(
        activity.altitude or activity.gps_altitude for activity in activities
    ):
        blocks.append(("Altitude", collect_rows(activities, analysis.altitude_stats)))
    if arguments.cadence and any(activity.cadence for activity in activities):
        blocks.append(("Cadence", collect_rows(activities, analysis.cadence_stats)))
    if arguments.hr and any(activity.hr for activity in activities):
        blocks.append(("Heart rate", collect_rows(activities, analysis.hr_stats)))
    if arguments.rr and any(activity.rr for activity in activities):
        blocks.append(("R-R", collect_rows(activities, analysis.rr_stats)))
    if arguments.distance and any(activity.running_distance for activity in activities):
        blocks.append(
            (
                "Running distance",
                collect_rows(activities, analysis.running_distance_stats),
            )
        )
    if arguments.temperature and any(activity.temperature for activity in activities):
        blocks.append(
            ("Temperature", collect_rows(activities, analysis.temperature_stats))
        )
    if arguments.battery and any(activity.battery_charge for activity in activities):
        blocks.append(("Battery", collect_rows(activities, analysis.battery_stats)))
    if arguments.power and any(activity.power for activity in activities):
        blocks.append(("Power", collect_rows(activities, analysis.power_stats)))
    printed_any = False
    for title, rows in blocks:
        if not rows:
            continue
        if printed_any:
            print()
        print_table(title, headers, rows)
        printed_any = True
    return printed_any


def comparison(arguments: argparse.Namespace, activities: list[Activity]):
    # Only compare what at least one activity carries samples for:
    # empty output would be confusing.
    if text_comparison(arguments, activities):
        print()
    # Only draw comparison plots when at least one activity carries
    # samples for the metric: empty charts would be confusing.
    if arguments.plot:
        plot_comparison(arguments, activities)


def plot_comparison(arguments: argparse.Namespace, activities: list[Activity]):
    if arguments.snr and any(activity.gps_snr for activity in activities):
        plot.compare_gps_snr_plot(activities)
    if arguments.gps_error and any(
        activity.ehpe or activity.evpe for activity in activities
    ):
        plot.compare_gps_error_plot(activities)
    if arguments.altitude and any(
        activity.altitude or activity.gps_altitude for activity in activities
    ):
        plot.compare_altitude_plot(activities)
    if arguments.cadence and any(activity.cadence for activity in activities):
        plot.compare_cadence_plot(activities)
    if arguments.hr and any(activity.hr for activity in activities):
        plot.compare_hr_plot(activities)
    if arguments.rr and any(activity.rr for activity in activities):
        plot.compare_rr_plot(activities)
    if arguments.distance and any(activity.running_distance for activity in activities):
        plot.compare_running_distance_plot(activities)
    if arguments.temperature and any(activity.temperature for activity in activities):
        plot.compare_temperature_plot(activities)
    if arguments.battery and any(activity.battery_charge for activity in activities):
        plot.compare_battery_charge_plot(activities)
    if arguments.power and any(activity.power for activity in activities):
        plot.compare_power_plot(activities)


def __main__():
    print("Suunto Activity Analyzer (SAA)")
    print()
    arguments = command_line()
    activities = []
    for file in arguments.files:
        print(f"Loading:\t{path.basename(file)}")
        activity = load_activity(file)
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
                if len(cadence_values) >= 1:
                    ref_steps = int(numpy.average(cadence_values) * 2) * int(
                        activity.duration / 60
                    )
                    print(f"Ref steps:\t{ref_steps}")
                    if ref_steps > 0:
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
