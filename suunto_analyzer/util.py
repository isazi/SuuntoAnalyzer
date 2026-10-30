from __future__ import annotations

import math
import datetime
import numpy


def parse_seconds(seconds: float) -> tuple[int, int]:
    hours = int(seconds // 3600)
    minutes = int((seconds - (hours * 3600)) // 60)
    return hours, minutes


def parse_timestamp(value: str) -> datetime.datetime:
    """Parse an ISO 8601 timestamp into a timezone-aware datetime.

    datetime.fromisoformat() only accepts the "Z" (UTC) designator from
    Python 3.11 onwards, so it is rewritten as an explicit offset, which
    every supported version understands.
    """
    if value and value[-1:] in ("Z", "z"):
        value = value[:-1] + "+00:00"
    return datetime.datetime.fromisoformat(value)


def rr_filter(rr: list[float]) -> list[float]:
    sigma = 2.25
    rr_mean = numpy.average(rr)
    rr_std = numpy.std(rr)
    hr_values = [
        (1000 / i) * 60.0 for i in rr if (math.fabs(i - rr_mean) < (sigma * rr_std))
    ]
    return hr_values
