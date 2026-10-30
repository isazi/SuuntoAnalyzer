import argparse

import matplotlib
import pytest

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

from suunto_analyzer import plot  # noqa: E402
from suunto_analyzer.__main__ import comparison  # noqa: E402
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


def make_arguments(**flags):
    for name in (
        "snr",
        "gps_error",
        "altitude",
        "cadence",
        "hr",
        "rr",
        "distance",
        "temperature",
        "battery",
        "power",
    ):
        flags.setdefault(name, False)
    return argparse.Namespace(**flags)


def test_comparison_skips_plots_without_data(monkeypatch):
    empty = SuuntoJSON()
    plot_lines = {}
    for name in (
        "compare_gps_snr_plot",
        "compare_gps_error_plot",
        "compare_altitude_plot",
        "compare_cadence_plot",
        "compare_hr_plot",
        "compare_running_distance_plot",
        "compare_temperature_plot",
        "compare_battery_charge_plot",
        "compare_power_plot",
    ):
        monkeypatch.setattr(
            plt,
            "show",
            lambda *args, _name=name, **kwargs: plot_lines.setdefault(_name, plt.gca()),
        )
    arguments = make_arguments(
        snr=True,
        gps_error=True,
        altitude=True,
        cadence=True,
        hr=True,
        distance=True,
        temperature=True,
        battery=True,
        power=True,
    )
    comparison(arguments, [empty])
    assert plot_lines == {}


def test_comparison_plots_once_data_is_present(activity, monkeypatch):
    plotted = []

    def record():
        plotted.append(len(plt.gca().lines))
        plt.close("all")

    monkeypatch.setattr(plt, "show", lambda *args, **kwargs: record())
    arguments = make_arguments(snr=True, battery=True, hr=True)
    comparison(arguments, [activity])
    assert plotted == [1, 1, 1]


def test_comparison_plots_when_at_least_one_activity_has_data(activity):
    empty = SuuntoJSON()
    plot.compare_gps_snr_plot([empty, activity])
    assert len(plt.gca().lines) == 1
