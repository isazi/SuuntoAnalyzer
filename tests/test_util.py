import datetime

import pytest

from suunto_analyzer.util import parse_seconds, parse_timestamp, rr_filter


def test_parse_timestamp_with_zulu_designator():
    parsed = parse_timestamp("2024-05-01T08:00:01.000Z")
    assert parsed == datetime.datetime(
        2024, 5, 1, 8, 0, 1, tzinfo=datetime.timezone.utc
    )
    assert parsed.tzinfo is not None
    assert parsed.utcoffset() == datetime.timedelta(0)


def test_parse_timestamp_with_lowercase_zulu_designator():
    parsed = parse_timestamp("2024-05-01T08:00:01.000z")
    assert parsed.utcoffset() == datetime.timedelta(0)


def test_parse_timestamp_without_timezone_stays_naive():
    parsed = parse_timestamp("2024-05-01T08:00:01.000")
    assert parsed == datetime.datetime(2024, 5, 1, 8, 0, 1)
    assert parsed.tzinfo is None


def test_parse_timestamp_with_explicit_offset():
    parsed = parse_timestamp("2024-05-01T10:00:01.000+02:00")
    assert parsed.utcoffset() == datetime.timedelta(hours=2)


def test_parse_timestamp_rejects_garbage():
    with pytest.raises(ValueError):
        parse_timestamp("not-a-timestamp")


def test_parse_timestamp_of_empty_string():
    with pytest.raises(ValueError):
        parse_timestamp("")


def test_parse_seconds():
    assert parse_seconds(3660) == (1, 1)
    assert parse_seconds(0) == (0, 0)


def test_rr_filter_removes_outliers():
    # A single gross outlier in a short series inflates the standard
    # deviation enough to survive the filter, so a longer series is
    # needed to exercise the rejection path.
    rr = [800, 802, 798, 801, 799, 803, 797, 805, 804, 1200]
    filtered = rr_filter(rr)
    assert len(filtered) == len(rr) - 1
    # The surviving values are the heart rates of the inlier intervals.
    assert min(filtered) == pytest.approx((1000 / 805) * 60.0)
    assert max(filtered) == pytest.approx((1000 / 797) * 60.0)


def test_rr_filter_keeps_clean_data():
    rr = [800, 802, 798, 801, 799, 803, 797, 805, 804, 806]
    assert len(rr_filter(rr)) == len(rr)
