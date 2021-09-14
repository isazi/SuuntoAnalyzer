import numpy
from json_reader import SuuntoJSON


def gps_snr_analysis(activity: SuuntoJSON):
    snr_values = []
    for snr in activity.gps_snr.values():
        snr_values.append(snr)
    snr_values = numpy.array(snr_values)
    print(f"Mininum SNR: {numpy.min(snr_values)}")
    print(f"Average SNR: {numpy.average(snr_values)} ±{numpy.std(snr_values)}")
    print(f"\tHistogram: {numpy.histogram(snr_values)[0]}")
    print(f"Maximum SNR: {numpy.max(snr_values)}")
