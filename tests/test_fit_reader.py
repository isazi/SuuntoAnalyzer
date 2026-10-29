import datetime
import math

import matplotlib
import pytest

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

fitdecode = pytest.importorskip("fitdecode")

from suunto_analyzer import analysis, fit_reader, plot  # noqa: E402
from suunto_analyzer.activity import Activity  # noqa: E402
from suunto_analyzer.fit_reader import (  # noqa: E402
    FitdecodeNotInstalled,
    SuuntoFIT,
)

from fit_writer import FitFile, compute_crc  # noqa: E402

START = datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc)
STEP = datetime.timedelta(seconds=60)
TIMES = [START + STEP * (index + 1) for index in range(3)]


def build_fit(
    records=True,
    session=True,
    file_id=True,
    device_info=True,
    sensor_info=False,
    hrv=True,
):
    """Build a small but complete FIT activity."""
    fit = FitFile()
    if file_id:
        fit.add(
            0,
            type="activity",
            manufacturer=1,
            product=123,
            serial_number=42,
            time_created=START,
            product_name="SyntheticWatch",
        )
    if session:
        fit.add(
            18,
            start_time=START,
            sport="running",
            total_timer_time=600.0,
            total_elapsed_time=610.0,
            total_distance=300.0,
            total_ascent=12,
            total_descent=7,
        )
    if device_info:
        fit.add(
            23,
            timestamp=START,
            device_index=0,
            source_type="local",
            product_name="SyntheticWatch",
            battery_level=88,
        )
    if sensor_info:
        fit.add(
            23,
            timestamp=START,
            device_index=1,
            source_type="antplus",
            product_name="HRM",
            battery_level=21,
        )
    if records:
        for index, timestamp in enumerate(TIMES):
            fit.add(
                20,
                timestamp=timestamp,
                position_lat=1.0 + index * 0.001,
                position_long=2.0 + index * 0.001,
                enhanced_altitude=100.0 + index,
                temperature=20.0 + index,
                distance=10.0 * (index + 1),
                heart_rate=70 + index,
                cadence=80 + index,
                power=250 + index,
                battery_soc=90 - index,
                gps_accuracy=3 + index,
            )
    if hrv:
        fit.add(78, time=(0.8, 0.81, 0.795))
    return fit.to_bytes()


def write_fit(tmp_path, data):
    path = tmp_path / "activity.fit"
    path.write_bytes(data)
    return path


def load(tmp_path, **kwargs):
    activity = SuuntoFIT()
    activity.load_file(write_fit(tmp_path, build_fit(**kwargs)))
    return activity


@pytest.fixture
def activity(tmp_path):
    return load(tmp_path)


def test_header(activity):
    assert activity.name == "SyntheticWatch"
    assert activity.sport == "running"
    assert activity.datetime == START
    assert activity.duration == 600.0
    assert activity.distance == 0.3
    assert activity.ascent == 12
    assert activity.descent == 7


def test_sample_keys_are_timezone_aware_datetimes(activity):
    for series in (
        activity.temperature,
        activity.altitude,
        activity.battery_charge,
        activity.cadence,
        activity.power,
        activity.running_distance,
        activity.hr,
        activity.ehpe,
    ):
        assert len(series) >= 1
        for key in series.keys():
            assert isinstance(key, datetime.datetime)
            assert key.tzinfo is not None
            assert key.utcoffset() == datetime.timedelta(0)


def test_coordinates_are_converted_to_radians(activity):
    assert len(activity.coordinates) == 3
    latitude, longitude = activity.coordinates[0]
    assert latitude == pytest.approx(math.radians(1.0))
    assert longitude == pytest.approx(math.radians(2.0))


def test_altitude(activity):
    assert list(activity.altitude.values()) == [100.0, 101.0, 102.0]


def test_altitude_falls_back_to_the_plain_field(tmp_path):
    fit = FitFile()
    fit.add(20, timestamp=START, altitude=150.0)
    loaded = SuuntoFIT()
    loaded.load_file(write_fit(tmp_path, fit.to_bytes()))
    assert list(loaded.altitude.values()) == [150.0]


def test_temperature_is_converted_to_kelvin(activity):
    assert list(activity.temperature.values()) == [293.15, 294.15, 295.15]


def test_running_distance_is_converted_to_metres(activity):
    assert list(activity.running_distance.values()) == [10.0, 20.0, 30.0]


def test_heart_rate_cadence_and_power(activity):
    assert list(activity.hr.values()) == [70.0, 71.0, 72.0]
    assert list(activity.cadence.values()) == [80.0, 81.0, 82.0]
    assert list(activity.power.values()) == [250.0, 251.0, 252.0]


def test_battery_is_converted_to_a_fraction(activity):
    # device_info battery at the start of the activity.
    assert activity.battery_charge[START] == 0.88
    # Per-record battery.
    assert [activity.battery_charge[timestamp] for timestamp in TIMES] == [
        0.9,
        0.89,
        0.88,
    ]


def test_gps_accuracy_is_used_as_ehpe(activity):
    assert list(activity.ehpe.values()) == [3.0, 4.0, 5.0]


def test_rr_intervals_are_milliseconds(activity):
    assert activity.rr == [800, 810, 795]


def test_channels_without_fit_equivalent_are_empty(activity):
    assert activity.gps_snr == {}
    assert activity.gps_altitude == {}
    assert activity.evpe == {}
    assert activity.gnss == ""
    assert activity.altibaro == ""
    assert activity.fusedalti is False
    assert activity.steps == 0
    assert activity.apps == []
    assert activity.sensors == []


def test_sensor_device_info_is_ignored(tmp_path):
    activity = load(tmp_path, sensor_info=True)
    # The sensor reports 21% battery: only the watch itself may feed the
    # battery series and the device name.
    assert all(value > 0.5 for value in activity.battery_charge.values())
    assert activity.name == "SyntheticWatch"


def test_device_info_without_source_type_uses_device_index(tmp_path):
    fit = FitFile()
    fit.add(23, timestamp=START, device_index=0, product_name="Watch", battery_level=50)
    activity = SuuntoFIT()
    activity.load_file(write_fit(tmp_path, fit.to_bytes()))
    assert activity.name == "Watch"
    assert activity.battery_charge[START] == 0.5


def test_name_falls_back_to_the_sport(tmp_path):
    activity = load(tmp_path, file_id=False, device_info=False)
    assert activity.name == "Running"


def test_file_without_session_keeps_defaults(tmp_path):
    activity = load(tmp_path, session=False)
    assert activity.duration == 0
    assert activity.distance == 0
    assert activity.ascent == 0
    assert activity.descent == 0


def test_loading_fit_without_the_optional_dependency(tmp_path, monkeypatch):
    path = write_fit(tmp_path, build_fit())
    monkeypatch.setattr(fit_reader, "fitdecode", None)
    with pytest.raises(FitdecodeNotInstalled, match="fit"):
        SuuntoFIT().load_file(path)


def test_fixture_has_a_valid_crc(tmp_path):
    path = write_fit(tmp_path, build_fit())
    with fitdecode.FitReader(path, check_crc=fitdecode.CrcCheck.RAISE) as reader:
        assert len(list(reader)) >= 1


def test_crc_matches_fitdecode():
    from fitdecode.utils import compute_crc as reference

    assert compute_crc(b"123456789") == reference(b"123456789")


def test_fit_activity_works_with_the_analyses(activity, capsys):
    analysis.gps_error_analysis(activity)
    analysis.battery_analysis(activity)
    analysis.cadence_analysis(activity)
    analysis.temperature_analysis(activity)
    analysis.altitude_analysis(activity)
    analysis.power_analysis(activity)
    analysis.hr_analysis(activity)
    out = capsys.readouterr().out
    assert "Min GNSS EHPE:\t3" in out
    assert "Max battery:\t90.0%" in out
    assert "Min battery:\t88.0%" in out
    assert "Min cadence:\t80.00" in out
    assert "Min temp:\t20.0C" in out
    assert "Min power:\t250.00" in out
    assert "Min HR:\t\t70.00" in out


def test_altitude_analysis_reports_only_what_fit_has(activity, capsys):
    # FIT has ascent/descent and the altimeter altitude, but no GNSS
    # altitude: the analysis must print the former two channels alone.
    analysis.altitude_analysis(activity)
    out = capsys.readouterr().out
    assert "Ascent:\t\t12" in out
    assert "Descent:\t7" in out
    assert "Min altitude:\taltimeter = 100.00m" in out
    assert "Max altitude:\taltimeter = 102.00m" in out
    assert "GNSS =" not in out


def test_altitude_analysis_tolerates_a_fit_file_without_altitude(tmp_path, capsys):
    loaded = load(tmp_path, records=False)
    analysis.altitude_analysis(loaded)
    assert capsys.readouterr().out == ""


def test_fit_activity_works_with_the_plots(activity, monkeypatch):
    monkeypatch.setattr(plt, "show", lambda *args, **kwargs: None)
    plot.hr_plot(activity)
    assert len(plt.gca().lines) == 1
    plt.close("all")
    plot.battery_charge_plot(activity)
    assert len(plt.gca().lines) == 1
    plt.close("all")


def test_json_reader_uses_the_canonical_model():
    from suunto_analyzer.json_reader import SuuntoJSON

    assert isinstance(SuuntoJSON(), Activity)


def test_cli_dispatches_fit_files(tmp_path):
    from suunto_analyzer.__main__ import load_activity

    activity = load_activity(write_fit(tmp_path, build_fit()))
    assert isinstance(activity, SuuntoFIT)


def test_cli_rejects_unknown_extensions(tmp_path):
    from suunto_analyzer.__main__ import load_activity

    unknown = tmp_path / "activity.txt"
    unknown.write_text("")
    with pytest.raises(SystemExit, match="Unsupported"):
        load_activity(unknown)


def test_cli_explains_the_missing_optional_dependency(tmp_path, monkeypatch):
    from suunto_analyzer.__main__ import load_activity

    monkeypatch.setattr(fit_reader, "fitdecode", None)
    path = write_fit(tmp_path, build_fit())
    with pytest.raises(SystemExit, match="fit"):
        load_activity(path)
