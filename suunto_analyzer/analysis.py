from datetime import datetime
import numpy
from suunto_analyzer.json_reader import SuuntoJSON
from suunto_analyzer.util import parse_seconds, rr_filter


def gps_snr_analysis(activity: SuuntoJSON):
    snr_values = [i for i in activity.gps_snr.values()]
    if len(snr_values) >= 1:
        snr_values = numpy.array(snr_values)
        print(f"Min GNSS SNR:\t{numpy.min(snr_values)}")
        print(
            f"Avg GNSS SNR:\t{numpy.average(snr_values):.1f} ±{numpy.std(snr_values):.1f}"
        )
        print(f"Max GNNS SNR:\t{numpy.max(snr_values)}")
        print(f"SNR histogram:\t{numpy.histogram(snr_values)[0]}")


def gps_error_analysis(activity: SuuntoJSON):
    ehpe_values = [i for i in activity.ehpe.values()]
    if len(ehpe_values) >= 1:
        ehpe_values = numpy.array(ehpe_values)
        print(f"Min GNSS EHPE:\t{numpy.min(ehpe_values)}")
        print(
            f"Avg GNSS EHPE:\t{numpy.average(ehpe_values):.1f} ±{numpy.std(ehpe_values):.1f}"
        )
        print(f"Max GNNS EHPE:\t{numpy.max(ehpe_values)}")
        print(f"EHPE histogram:\t{numpy.histogram(ehpe_values)[0]}")
    evpe_values = [i for i in activity.evpe.values()]
    if len(evpe_values) >= 1:
        evpe_values = numpy.array(evpe_values)
        print(f"Min GNSS EVPE:\t{numpy.min(evpe_values)}")
        print(
            f"Avg GNSS EVPE:\t{numpy.average(evpe_values):.1f} ±{numpy.std(evpe_values):.1f}"
        )
        print(f"Max GNNS EVPE:\t{numpy.max(evpe_values)}")
        print(f"EVPE histogram:\t{numpy.histogram(evpe_values)[0]}")


def battery_analysis(activity: SuuntoJSON):
    battery_values = [i for i in activity.battery_charge.values()]
    if len(battery_values) >= 1:
        print("Standard analysis")
        battery_values = numpy.array(battery_values)
        max_battery = numpy.max(battery_values)
        min_battery = numpy.min(battery_values)
        print(f"Max battery:\t{max_battery * 100.0}%")
        print(f"Min battery:\t{min_battery * 100.0}%")
        print(
            f"Consumption:\ttotal = {((max_battery - min_battery) * 100.0):.1f}%\thourly = {(((max_battery - min_battery) / (activity.duration / 3600)) * 100.0):.1f}%"
        )
        if (max_battery - min_battery) > 0:
            hours, minutes = parse_seconds(
                activity.duration / (max_battery - min_battery)
            )
            print(f"Estimated life:\t{hours}h {minutes}m")
        if (max_battery - min_battery) > 0.02:
            hours, minutes = parse_seconds(
                activity.duration / ((max_battery - min_battery) + 0.01)
            )
            print(f"\t\t{hours}h {minutes}m (estimated min)")
            hours, minutes = parse_seconds(
                activity.duration / ((max_battery - min_battery) - 0.01)
            )
            print(f"\t\t{hours}h {minutes}m (estimated max)")
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
                steps.append(
                    (
                        datetime.fromisoformat(key) - datetime.fromisoformat(start)
                    ).total_seconds()
                )
                start = key
        if len(steps) >= 3:
            steps = numpy.array(steps)
            # remove min and max
            mask = numpy.logical_or(steps == steps.max(), steps == steps.min())
            steps = numpy.ma.masked_array(steps, mask=mask)
            hours, minutes = parse_seconds(steps.mean() * 100)
            print("Step analysis")
            print(f"Estimated life:\t{hours}h {minutes}m")


def cadence_analysis(activity: SuuntoJSON):
    cadence_values = [i for i in activity.cadence.values()]
    if len(cadence_values) >= 1:
        cadence_values = numpy.array(cadence_values)
        print(f"Min cadence:\t{numpy.min(cadence_values):.2f}")
        print(
            f"Avg cadence:\t{numpy.average(cadence_values):.2f} ±{numpy.std(cadence_values):.2f}"
        )
        print(f"Max cadence:\t{numpy.max(cadence_values):.2f}")


def temperature_analysis(activity: SuuntoJSON):
    temperature_values = [(i - 273.15) for i in activity.temperature.values()]
    if len(temperature_values) >= 1:
        temperature_values = numpy.array(temperature_values)
        print(f"Min temp:\t{numpy.min(temperature_values):.1f}C")
        print(
            f"Avg temp:\t{numpy.average(temperature_values):.1f}C ±{numpy.std(temperature_values):.1f}C"
        )
        print(f"Max temp:\t{numpy.max(temperature_values):.1f}C")


def altitude_analysis(activity: SuuntoJSON):
    altitude_values = [i for i in activity.altitude.values()]
    gps_altitude_values = [i for i in activity.gps_altitude.values()]
    if len(altitude_values) >= 1 and len(gps_altitude_values) >= 1:
        altitude_values = numpy.array(altitude_values)
        gps_altitude_values = numpy.array(gps_altitude_values)
        print(f"AltiBaro:\t{activity.altibaro}")
        if activity.fusedalti:
            print(f"FusedAlti:\tEnabled")
        print(f"Ascent:\t\t{activity.ascent}")
        print(f"Descent:\t{activity.descent}")
        print(
            f"Min altitude:\taltimeter = {numpy.min(altitude_values):.2f}m\tGNSS = {numpy.min(gps_altitude_values):.2f}m"
        )
        print(
            f"Max altitude:\taltimeter = {numpy.max(altitude_values):.2f}m\tGNSS = {numpy.max(gps_altitude_values):.2f}m"
        )


def power_analysis(activity: SuuntoJSON):
    power_values = [i for i in activity.power.values()]
    if len(power_values) >= 1:
        power_values = numpy.array(power_values)
        print(f"Min power:\t{numpy.min(power_values):.2f}")
        print(
            f"Avg power:\t{numpy.average(power_values):.2f} ±{numpy.std(power_values):.2f}"
        )
        print(f"Max power:\t{numpy.max(power_values):.2f}")


def hr_analysis(activity: SuuntoJSON):
    hr_values = [i for i in activity.hr.values()]
    if len(hr_values) >= 1:
        hr_values = numpy.array(hr_values)
        print(f"Min HR:\t\t{numpy.min(hr_values):.2f}")
        print(f"Avg HR:\t\t{numpy.average(hr_values):.2f} ±{numpy.std(hr_values):.2f}")
        print(f"Max HR:\t\t{numpy.max(hr_values):.2f}")
    elif len(activity.rr) >= 1:
        hr_values = rr_filter(activity.rr)
        print(f"Min HR:\t\t{numpy.min(hr_values):.2f}")
        print(f"Avg HR:\t\t{numpy.average(hr_values):.2f} ±{numpy.std(hr_values):.2f}")
        print(f"Max HR:\t\t{numpy.max(hr_values):.2f}")
