import math
import numpy


def parse_seconds(seconds: int):
    hours = int(seconds // 3600)
    minutes = int((seconds - (hours * 3600)) // 60)
    return hours, minutes


def rr_filter(rr: list) -> list:
    sigma = 2.25
    rr_mean = numpy.average(rr)
    rr_std = numpy.std(rr)
    hr_values = [
        (1000 / i) * 60.0 for i in rr if (math.fabs(i - rr_mean) < (sigma * rr_std))
    ]
    return hr_values
