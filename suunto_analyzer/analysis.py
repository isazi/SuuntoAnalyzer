import numpy
import datetime
from json_reader import SuuntoJSON


def gps_snr_analysis(activity: SuuntoJSON):
    snr_values = []
    for snr in activity.gps_snr.values():
        snr_values.append(snr)
    snr_values = numpy.array(snr_values)
    print(f"Mininum SNR:\t{numpy.min(snr_values)}")
    print(f"Average SNR:\t{numpy.average(snr_values)} ±{numpy.std(snr_values)}")
    print(f"Maximum SNR:\t{numpy.max(snr_values)}")
    print(f"SNR histogram:\t{numpy.histogram(snr_values)[0]}")


def battery_analysis(activity: SuuntoJSON):
    battery_values = []
    for value in activity.battery_charge.values():
        battery_values.append(value)
    battery_values = numpy.array(battery_values)
    max_battery = numpy.max(battery_values)
    min_battery = numpy.min(battery_values)
    print(f"Max battery:\t{max_battery * 100.0}%")
    print(f"Min battery:\t{min_battery * 100.0}%")
    print(f"Consumption:\t{(max_battery - min_battery) * 100.0}%")
    print(f"Estimated life:\t{datetime.timedelta(seconds=(activity.duration / (max_battery - min_battery)))}")


def cadence_analysis(activity: SuuntoJSON):
    cadence_values = []
    for value in activity.cadence.values():
        cadence_values.append(value)
    cadence_values = numpy.array(cadence_values)
    print(f"Min cadence:\t{numpy.min(cadence_values)}")
    print(f"Avg cadence:\t{numpy.average(cadence_values)} ±{numpy.std(cadence_values)}")
    print(f"Max cadence:\t{numpy.max(cadence_values)}")


def altitude_analysis(activity: SuuntoJSON):
    altitude_values = []
    gps_altitude_values = []
    for value in activity.altitude.values():
        altitude_values.append(value)
    for value in activity.gps_altitude.values():
        gps_altitude_values.append(value)
    altitude_values = numpy.array(altitude_values)
    gps_altitude_values = numpy.array(gps_altitude_values)
    print(f"Min altitude:\t{numpy.min(altitude_values)}m (altimeter) {numpy.min(gps_altitude_values)}m (GPS)")
    print(f"Max altitude:\t{numpy.max(altitude_values)}m (altimeter) {numpy.max(gps_altitude_values)}m (GPS)")
