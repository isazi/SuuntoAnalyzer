import pytest

from suunto_analyzer import analysis
from suunto_analyzer.json_reader import SuuntoJSON


@pytest.fixture
def activity(activity_file):
    loaded = SuuntoJSON()
    loaded.load_file(activity_file)
    return loaded


def test_gps_snr_analysis(activity, capsys):
    analysis.gps_snr_analysis(activity)
    out = capsys.readouterr().out
    assert "Min GNSS SNR:\t30" in out
    assert "Max GNNS SNR:\t32" in out


def test_gps_error_analysis(activity, capsys):
    analysis.gps_error_analysis(activity)
    out = capsys.readouterr().out
    assert "Min GNSS EHPE:\t3" in out
    assert "Min GNSS EVPE:\t5" in out


def test_battery_analysis(activity, capsys):
    analysis.battery_analysis(activity)
    out = capsys.readouterr().out
    assert "Max battery:\t90.0%" in out
    assert "Min battery:\t88.0%" in out
    assert "Consumption:" in out


def test_cadence_analysis(activity, capsys):
    analysis.cadence_analysis(activity)
    out = capsys.readouterr().out
    assert "Min cadence:\t4800.00" in out
    assert "Max cadence:\t5040.00" in out


def test_temperature_analysis(activity, capsys):
    analysis.temperature_analysis(activity)
    out = capsys.readouterr().out
    assert "Min temp:\t20.0C" in out
    assert "Max temp:\t22.0C" in out


def test_altitude_analysis(activity, capsys):
    analysis.altitude_analysis(activity)
    out = capsys.readouterr().out
    assert "AltiBaro:\tAuto" in out
    assert "FusedAlti:\tEnabled" in out
    assert "Ascent:\t\t10" in out
    assert "Descent:\t5" in out


def test_power_analysis(activity, capsys):
    analysis.power_analysis(activity)
    out = capsys.readouterr().out
    assert "Min power:\t250.00" in out
    assert "Max power:\t260.00" in out


def test_hr_analysis(activity, capsys):
    analysis.hr_analysis(activity)
    out = capsys.readouterr().out
    assert "Min HR:\t\t4200.00" in out
    assert "Max HR:\t\t4440.00" in out


def test_hr_analysis_falls_back_to_rr(activity, capsys):
    activity.hr = {}
    analysis.hr_analysis(activity)
    out = capsys.readouterr().out
    assert "Min HR:" in out


def test_analyses_tolerate_empty_activity(tmp_path, capsys):
    activity = SuuntoJSON()
    # None of the analyses may raise on an activity without samples.
    analysis.gps_snr_analysis(activity)
    analysis.gps_error_analysis(activity)
    analysis.battery_analysis(activity)
    analysis.cadence_analysis(activity)
    analysis.temperature_analysis(activity)
    analysis.altitude_analysis(activity)
    analysis.power_analysis(activity)
    analysis.hr_analysis(activity)
    assert capsys.readouterr().out == ""
