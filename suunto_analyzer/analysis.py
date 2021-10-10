import numpy
import datetime
from json_reader import SuuntoJSON


def gps_snr_analysis(activity: SuuntoJSON):
    snr_values = [i for i in activity.gps_snr.values()]
    if len(snr_values) >= 1:
        snr_values = numpy.array(snr_values)
        print(f"Min GNSS SNR:\t{numpy.min(snr_values)}")
        print(f"Avg GNSS SNR:\t{numpy.average(snr_values):.1f} ±{numpy.std(snr_values):.1f}")
        print(f"Max GNNS SNR:\t{numpy.max(snr_values)}")
        print(f"SNR histogram:\t{numpy.histogram(snr_values)[0]}")


def battery_analysis(activity: SuuntoJSON):
    battery_values = [i for i in activity.battery_charge.values()]
    if len(battery_values) >= 1:
        battery_values = numpy.array(battery_values)
        max_battery = numpy.max(battery_values)
        min_battery = numpy.min(battery_values)
        print(f"Max battery:\t{max_battery * 100.0}%")
        print(f"Min battery:\t{min_battery * 100.0}%")
        print(f"Consumption:\t{((max_battery - min_battery) * 100.0):.1f}%")
        print(f"Estimated life:\t{datetime.timedelta(seconds=(activity.duration / (max_battery - min_battery)))}")


def cadence_analysis(activity: SuuntoJSON):
    cadence_values = [i for i in activity.cadence.values()]
    if len(cadence_values) >= 1:
        cadence_values = numpy.array(cadence_values)
        print(f"Min cadence:\t{numpy.min(cadence_values):.2f}")
        print(f"Avg cadence:\t{numpy.average(cadence_values):.2f} ±{numpy.std(cadence_values):.2f}")
        print(f"Max cadence:\t{numpy.max(cadence_values):.2f}")


def altitude_analysis(activity: SuuntoJSON):
    altitude_values = [i for i in activity.altitude.values()]
    gps_altitude_values = [i for i in activity.gps_altitude.values()]
    if len(altitude_values) >= 1 and len(gps_altitude_values) >= 1:
        altitude_values = numpy.array(altitude_values)
        gps_altitude_values = numpy.array(gps_altitude_values)
        print(f"Ascent:\t\t{activity.ascent}")
        print(f"Descent:\t{activity.descent}")
        print(f"Min altitude:\taltimeter = {numpy.min(altitude_values):.2f}m\tGNSS = {numpy.min(gps_altitude_values):.2f}m")
        print(f"Max altitude:\taltimeter = {numpy.max(altitude_values):.2f}m\tGNSS = {numpy.max(gps_altitude_values):.2f}m")


def power_analysis(activity: SuuntoJSON):
    power_values = [i for i in activity.power.values()]
    if len(power_values) >= 1:
        power_values = numpy.array(power_values)
        print(f"Min power:\t{numpy.min(power_values):.2f}")
        print(f"Avg power:\t{numpy.average(power_values):.2f} ±{numpy.std(power_values):.2f}")
        print(f"Max power:\t{numpy.max(power_values):.2f}")


def hr_analysis(activity: SuuntoJSON):
    hr_values = [i for i in activity.hr.values()]
    if len(hr_values) >= 1:
        hr_values = numpy.array(hr_values)
        print(f"Min HR:\t\t{numpy.min(hr_values):.2f}")
        print(f"Avg HR:\t\t{numpy.average(hr_values):.2f} ±{numpy.std(hr_values):.2f}")
        print(f"Max HR:\t\t{numpy.max(hr_values):.2f}")
