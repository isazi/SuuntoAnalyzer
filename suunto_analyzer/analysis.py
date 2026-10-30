import numpy
from suunto_analyzer.activity import Activity
from suunto_analyzer.util import parse_seconds, rr_filter

Row = tuple[str, str]


def print_rows(rows: list[Row]):
    """Print rows labelled for direct printing, e.g. ``"Min HR:\\t\\t4200"``.

    An empty label marks a section header and is printed verbatim.
    """
    for label, value in rows:
        if not label:
            print(value)
        else:
            print(f"{label}{value}")


def gps_snr_stats(activity: Activity) -> list[Row]:
    snr_values = [i for i in activity.gps_snr.values()]
    rows = list()
    if len(snr_values) >= 1:
        snr_values = numpy.array(snr_values)
        rows.append(("Min GNSS SNR:\t", f"{numpy.min(snr_values)}"))
        rows.append(
            (
                "Avg GNSS SNR:\t",
                f"{numpy.average(snr_values):.1f} ±{numpy.std(snr_values):.1f}",
            )
        )
        rows.append(("Max GNNS SNR:\t", f"{numpy.max(snr_values)}"))
        rows.append(("SNR histogram:\t", f"{numpy.histogram(snr_values)[0]}"))
    return rows


def gps_snr_analysis(activity: Activity):
    print_rows(gps_snr_stats(activity))


def gps_error_stats(activity: Activity) -> list[Row]:
    ehpe_values = [i for i in activity.ehpe.values()]
    evpe_values = [i for i in activity.evpe.values()]
    rows = list()
    if len(ehpe_values) >= 1:
        ehpe_values = numpy.array(ehpe_values)
        rows.append(("Min GNSS EHPE:\t", f"{numpy.min(ehpe_values)}"))
        rows.append(
            (
                "Avg GNSS EHPE:\t",
                f"{numpy.average(ehpe_values):.1f} ±{numpy.std(ehpe_values):.1f}",
            )
        )
        rows.append(("Max GNNS EHPE:\t", f"{numpy.max(ehpe_values)}"))
        rows.append(("EHPE histogram:\t", f"{numpy.histogram(ehpe_values)[0]}"))
    if len(evpe_values) >= 1:
        evpe_values = numpy.array(evpe_values)
        rows.append(("Min GNSS EVPE:\t", f"{numpy.min(evpe_values)}"))
        rows.append(
            (
                "Avg GNSS EVPE:\t",
                f"{numpy.average(evpe_values):.1f} ±{numpy.std(evpe_values):.1f}",
            )
        )
        rows.append(("Max GNNS EVPE:\t", f"{numpy.max(evpe_values)}"))
        rows.append(("EVPE histogram:\t", f"{numpy.histogram(evpe_values)[0]}"))
    return rows


def gps_error_analysis(activity: Activity):
    print_rows(gps_error_stats(activity))


def battery_stats(activity: Activity) -> list[Row]:
    battery_values = [i for i in activity.battery_charge.values()]
    rows = list()
    if len(battery_values) >= 1:
        rows.append(("", "Standard analysis"))
        battery_values = numpy.array(battery_values)
        max_battery = numpy.max(battery_values)
        min_battery = numpy.min(battery_values)
        rows.append(("Max battery:\t", f"{max_battery * 100.0}%"))
        rows.append(("Min battery:\t", f"{min_battery * 100.0}%"))
        rows.append(
            (
                "Consumption:\t",
                f"total = {((max_battery - min_battery) * 100.0):.1f}%\thourly = {(((max_battery - min_battery) / (activity.duration / 3600)) * 100.0):.1f}%",
            )
        )
        if (max_battery - min_battery) > 0:
            hours, minutes = parse_seconds(
                activity.duration / (max_battery - min_battery)
            )
            rows.append(("Estimated life:\t", f"{hours}h {minutes}m"))
        if (max_battery - min_battery) > 0.02:
            hours, minutes = parse_seconds(
                activity.duration / ((max_battery - min_battery) + 0.01)
            )
            rows.append(
                ("Estimated life (min):\t", f"{hours}h {minutes}m (estimated min)")
            )
            hours, minutes = parse_seconds(
                activity.duration / ((max_battery - min_battery) - 0.01)
            )
            rows.append(
                ("Estimated life (max):\t", f"{hours}h {minutes}m (estimated max)")
            )
        old_value = -1
        start = None
        steps = list()
        for key, value in activity.battery_charge.items():
            if old_value == -1:
                old_value = int(value * 100)
                start = key
                continue
            if old_value > int(value * 100):
                old_value = int(value * 100)
                steps.append((key - start).total_seconds())
                start = key
        if len(steps) >= 3:
            steps = numpy.array(steps)
            # remove min and max
            mask = numpy.logical_or(steps == steps.max(), steps == steps.min())
            steps = numpy.ma.masked_array(steps, mask=mask)
            hours, minutes = parse_seconds(steps.mean() * 100)
            rows.append(("", "Step analysis"))
            rows.append(("Step analysis life:\t", f"{hours}h {minutes}m"))
    return rows


def battery_analysis(activity: Activity):
    for label, value in battery_stats(activity):
        if not label:
            print(value)
        elif label == "Step analysis life:\t":
            print(f"Estimated life:\t{value}")
        elif label in ("Estimated life (min):\t", "Estimated life (max):\t"):
            print(f"\t\t{value}")
        else:
            print(f"{label}{value}")


def cadence_stats(activity: Activity) -> list[Row]:
    cadence_values = [i for i in activity.cadence.values()]
    rows = list()
    if len(cadence_values) >= 1:
        cadence_values = numpy.array(cadence_values)
        rows.append(("Min cadence:\t", f"{numpy.min(cadence_values):.2f}"))
        rows.append(
            (
                "Avg cadence:\t",
                f"{numpy.average(cadence_values):.2f} ±{numpy.std(cadence_values):.2f}",
            )
        )
        rows.append(("Max cadence:\t", f"{numpy.max(cadence_values):.2f}"))
    return rows


def cadence_analysis(activity: Activity):
    print_rows(cadence_stats(activity))


def temperature_stats(activity: Activity) -> list[Row]:
    temperature_values = [(i - 273.15) for i in activity.temperature.values()]
    rows = list()
    if len(temperature_values) >= 1:
        temperature_values = numpy.array(temperature_values)
        rows.append(("Min temp:\t", f"{numpy.min(temperature_values):.1f}C"))
        rows.append(
            (
                "Avg temp:\t",
                f"{numpy.average(temperature_values):.1f}C ±{numpy.std(temperature_values):.1f}C",
            )
        )
        rows.append(("Max temp:\t", f"{numpy.max(temperature_values):.1f}C"))
    return rows


def temperature_analysis(activity: Activity):
    print_rows(temperature_stats(activity))


def altitude_stats(activity: Activity) -> list[Row]:
    altitude_values = [i for i in activity.altitude.values()]
    gps_altitude_values = [i for i in activity.gps_altitude.values()]
    rows = list()
    if len(altitude_values) < 1 and len(gps_altitude_values) < 1:
        return rows
    rows.append(("AltiBaro:\t", activity.altibaro))
    if activity.fusedalti:
        rows.append(("FusedAlti:\t", "Enabled"))
    rows.append(("Ascent:\t\t", f"{activity.ascent}"))
    rows.append(("Descent:\t", f"{activity.descent}"))
    altitude_values = numpy.array(altitude_values)
    gps_altitude_values = numpy.array(gps_altitude_values)
    if len(altitude_values) >= 1 and len(gps_altitude_values) >= 1:
        rows.append(
            (
                "Min altitude:\t",
                f"altimeter = {numpy.min(altitude_values):.2f}m\tGNSS = {numpy.min(gps_altitude_values):.2f}m",
            )
        )
        rows.append(
            (
                "Max altitude:\t",
                f"altimeter = {numpy.max(altitude_values):.2f}m\tGNSS = {numpy.max(gps_altitude_values):.2f}m",
            )
        )
    elif len(altitude_values) >= 1:
        rows.append(
            ("Min altitude:\t", f"altimeter = {numpy.min(altitude_values):.2f}m")
        )
        rows.append(
            ("Max altitude:\t", f"altimeter = {numpy.max(altitude_values):.2f}m")
        )
    else:
        rows.append(
            ("Min altitude:\t", f"GNSS = {numpy.min(gps_altitude_values):.2f}m")
        )
        rows.append(
            ("Max altitude:\t", f"GNSS = {numpy.max(gps_altitude_values):.2f}m")
        )
    return rows


def altitude_analysis(activity: Activity):
    print_rows(altitude_stats(activity))


def power_stats(activity: Activity) -> list[Row]:
    power_values = [i for i in activity.power.values()]
    rows = list()
    if len(power_values) >= 1:
        power_values = numpy.array(power_values)
        rows.append(("Min power:\t", f"{numpy.min(power_values):.2f}"))
        rows.append(
            (
                "Avg power:\t",
                f"{numpy.average(power_values):.2f} ±{numpy.std(power_values):.2f}",
            )
        )
        rows.append(("Max power:\t", f"{numpy.max(power_values):.2f}"))
    return rows


def power_analysis(activity: Activity):
    print_rows(power_stats(activity))


def hr_stats(activity: Activity) -> list[Row]:
    hr_values = [i for i in activity.hr.values()]
    rows = list()
    if len(hr_values) >= 1:
        hr_values = numpy.array(hr_values)
        rows.append(("Min HR:\t\t", f"{numpy.min(hr_values):.2f}"))
        rows.append(
            (
                "Avg HR:\t\t",
                f"{numpy.average(hr_values):.2f} ±{numpy.std(hr_values):.2f}",
            )
        )
        rows.append(("Max HR:\t\t", f"{numpy.max(hr_values):.2f}"))
    elif len(activity.rr) >= 1:
        hr_values = rr_filter(activity.rr)
        rows.append(("Min HR:\t\t", f"{numpy.min(hr_values):.2f}"))
        rows.append(
            (
                "Avg HR:\t\t",
                f"{numpy.average(hr_values):.2f} ±{numpy.std(hr_values):.2f}",
            )
        )
        rows.append(("Max HR:\t\t", f"{numpy.max(hr_values):.2f}"))
    return rows


def hr_analysis(activity: Activity):
    print_rows(hr_stats(activity))


def rr_stats(activity: Activity) -> list[Row]:
    rows = list()
    if len(activity.rr) >= 1:
        rows.append(("RR samples:\t", f"{len(activity.rr)}"))
        hr_values = numpy.array(rr_filter(activity.rr))
        rows.append(("Min HR (R-R):\t", f"{numpy.min(hr_values):.2f}"))
        rows.append(
            (
                "Avg HR (R-R):\t",
                f"{numpy.average(hr_values):.2f} ±{numpy.std(hr_values):.2f}",
            )
        )
        rows.append(("Max HR (R-R):\t", f"{numpy.max(hr_values):.2f}"))
    return rows
