import matplotlib
import pytest

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

from suunto_analyzer import plot  # noqa: E402
from suunto_analyzer.json_reader import SuuntoJSON  # noqa: E402


@pytest.fixture(autouse=True)
def close_figures():
    """matplotlib keeps figures around between tests, which would make
    the line counts accumulate."""
    yield
    plt.close("all")


@pytest.fixture(autouse=True)
def no_show(monkeypatch):
    monkeypatch.setattr(plt, "show", lambda *args, **kwargs: None)


@pytest.fixture
def activity(activity_file):
    loaded = SuuntoJSON()
    loaded.load_file(activity_file)
    return loaded


def test_altitude_plot(activity):
    plot.altitude_plot(activity)
    assert len(plt.gca().lines) == 2


def test_cadence_plot(activity):
    plot.cadence_plot(activity)
    assert len(plt.gca().lines) == 1


def test_gps_snr_plot(activity):
    plot.gps_snr_plot(activity)
    assert len(plt.gca().lines) == 1


def test_gps_error_plot(activity):
    plot.gps_error_plot(activity)
    assert len(plt.gca().lines) == 2


def test_hr_plot(activity):
    plot.hr_plot(activity)
    assert len(plt.gca().lines) == 1


def test_rr_plot(activity):
    plot.rr_plot(activity)
    assert len(plt.gca().lines) == 1


def test_hr_plot_does_not_fall_back_to_rr(activity):
    activity.hr = {}  # simulate a monitor without HR
    plot.hr_plot(activity)
    assert len(plt.gca().lines) == 0
    plot.rr_plot(activity)
    assert len(plt.gca().lines) == 1


def test_battery_charge_plot(activity):
    plot.battery_charge_plot(activity)
    assert len(plt.gca().lines) == 1


def test_temperature_plot(activity):
    plot.temperature_plot(activity)
    assert len(plt.gca().lines) == 1


def test_power_plot(activity):
    plot.power_plot(activity)
    assert len(plt.gca().lines) == 1


def test_plots_use_datetime_axis(activity):
    plot.altitude_plot(activity)
    line = plt.gca().lines[0]
    xdata = line.get_xdata()
    assert len(xdata) == 3
    assert xdata[0].tzinfo is not None


def test_compare_plots(activity):
    activities = [activity, activity]
    plot.compare_altitude_plot(activities)
    assert len(plt.gca().lines) == 4
    plt.close("all")
    plot.compare_cadence_plot(activities)
    assert len(plt.gca().lines) == 2
    plt.close("all")
    plot.compare_gps_snr_plot(activities)
    assert len(plt.gca().lines) == 2
    plt.close("all")
    plot.compare_hr_plot(activities)
    assert len(plt.gca().lines) == 2
    plt.close("all")
    plot.compare_rr_plot(activities)
    assert len(plt.gca().lines) == 2
    plt.close("all")
    plot.compare_running_distance_plot(activities)
    assert len(plt.gca().lines) == 2
    plt.close("all")
    plot.compare_temperature_plot(activities)
    assert len(plt.gca().lines) == 2
    plt.close("all")
    plot.compare_power_plot(activities)
    assert len(plt.gca().lines) == 2
    plt.close("all")
    plot.compare_battery_charge_plot(activities)
    assert len(plt.gca().lines) == 2
    plt.close("all")
    plot.compare_gps_error_plot(activities)
    assert len(plt.gca().lines) == 4


def test_track_plot_without_map_tiles(activity, monkeypatch):
    from suunto_analyzer import track

    monkeypatch.setitem(__import__("sys").modules, "contextily", None)
    monkeypatch.setattr(track, "contextily", None, raising=False)
    track.plot_track([activity])
    assert len(plt.gca().lines) == 1
