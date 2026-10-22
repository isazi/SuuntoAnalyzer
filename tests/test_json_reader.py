import datetime

from suunto_analyzer.json_reader import SuuntoJSON

from conftest import build_log, write_log


def load(tmp_path, log):
    activity = SuuntoJSON()
    activity.load_file(write_log(tmp_path, log))
    return activity


def test_header_is_parsed(activity_file):
    activity = SuuntoJSON()
    activity.load_file(activity_file)
    assert activity.name == "Ibiza 11.2.0"
    assert activity.gnss == "GPS+GLONASS"
    assert activity.altibaro == "Auto"
    assert activity.fusedalti is True
    assert activity.duration == 600.0
    assert activity.steps == 1500
    assert activity.ascent == 10
    assert activity.descent == 5


def test_header_datetime_is_timezone_aware(activity_file):
    activity = SuuntoJSON()
    activity.load_file(activity_file)
    assert activity.datetime == datetime.datetime(
        2024, 5, 1, 8, 0, 0, tzinfo=datetime.timezone.utc
    )
    assert activity.datetime.tzinfo is not None


def test_distance_is_converted_to_kilometres(activity_file):
    activity = SuuntoJSON()
    activity.load_file(activity_file)
    assert activity.distance == 2.0


def test_sensors_and_apps(activity_file):
    activity = SuuntoJSON()
    activity.load_file(activity_file)
    assert "Foot Pod" in activity.sensors
    assert "Heart Rate" in activity.sensors
    assert "Bike Pod" not in activity.sensors
    assert activity.apps == ["App1"]


def test_rr_intervals(activity_file):
    activity = SuuntoJSON()
    activity.load_file(activity_file)
    assert activity.rr == [800, 810, 795]


def test_sample_keys_are_timezone_aware_datetimes(activity_file):
    activity = SuuntoJSON()
    activity.load_file(activity_file)
    for series in (
        activity.temperature,
        activity.altitude,
        activity.gps_altitude,
        activity.gps_snr,
        activity.ehpe,
        activity.evpe,
        activity.battery_charge,
        activity.cadence,
        activity.power,
        activity.running_distance,
        activity.hr,
    ):
        assert len(series) >= 1
        for key in series.keys():
            assert isinstance(key, datetime.datetime)
            assert key.tzinfo is not None
            assert key.utcoffset() == datetime.timedelta(0)


def test_sample_values(activity_file):
    activity = SuuntoJSON()
    activity.load_file(activity_file)
    assert list(activity.altitude.values()) == [100.0, 101.0, 102.0]
    assert list(activity.gps_altitude.values()) == [98.0, 99.0, 100.0]
    # Cadence and heart rate are scaled to rpm and bpm.
    assert list(activity.cadence.values()) == [4800.0, 4920.0, 5040.0]
    assert list(activity.hr.values()) == [4200.0, 4320.0, 4440.0]
    assert list(activity.temperature.values()) == [293.15, 294.15, 295.15]


def test_none_values_are_not_stored(activity_file):
    activity = SuuntoJSON()
    activity.load_file(activity_file)
    # The middle sample has empty SNR/EHPE/EVPE/battery channels: they
    # must be absent rather than stored as None.
    assert len(activity.gps_snr) == 2
    assert len(activity.ehpe) == 2
    assert len(activity.evpe) == 2
    assert len(activity.battery_charge) == 2
    for series in (
        activity.gps_snr,
        activity.ehpe,
        activity.evpe,
        activity.battery_charge,
        activity.temperature,
        activity.altitude,
    ):
        assert all(value is not None for value in series.values())


def test_coordinates_are_collected_for_every_sample(activity_file):
    activity = SuuntoJSON()
    activity.load_file(activity_file)
    assert len(activity.coordinates) == 3
    assert activity.coordinates[0] == (1.0, 2.0)


def test_file_without_samples(tmp_path):
    activity = load(tmp_path, build_log(samples=[]))
    assert activity.altitude == {}
    assert activity.coordinates == []
    assert activity.name == "Ibiza 11.2.0"


def test_file_with_missing_optional_header_fields(tmp_path):
    header = {"Device": {"Name": "Ibiza", "Info": {"SW": "11.2.0"}}}
    activity = load(tmp_path, build_log(samples=[], header=header))
    assert activity.name == "Ibiza 11.2.0"
    assert activity.datetime is None
    assert activity.gnss == ""
    assert activity.duration == 0
    assert activity.sensors == []
    assert activity.apps == []


def test_file_with_malformed_header_datetime(tmp_path):
    header = dict(build_log()["DeviceLog"]["Header"])
    header["DateTime"] = "not-a-timestamp"
    activity = load(tmp_path, build_log(samples=[], header=header))
    # A malformed timestamp must not abort the whole file.
    assert activity.datetime is None
    assert activity.name == "Ibiza 11.2.0"


def test_sample_with_malformed_timestamp_is_skipped(tmp_path):
    samples = [
        {
            "TimeISO8601": "not-a-timestamp",
            "Latitude": 1.0,
            "Longitude": 2.0,
            "Altitude": 100.0,
        }
    ]
    activity = load(tmp_path, build_log(samples=samples))
    assert activity.altitude == {}
    # Coordinates are still usable for the track plot.
    assert len(activity.coordinates) == 1
