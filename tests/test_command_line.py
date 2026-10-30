import sys

from suunto_analyzer.__main__ import command_line

METRIC_FLAGS = (
    "duration",
    "distance",
    "steps",
    "sensors",
    "apps",
    "gps_error",
    "snr",
    "battery",
    "cadence",
    "temperature",
    "altitude",
    "power",
    "hr",
    "rr",
)


def run(argv):
    old_argv = sys.argv
    sys.argv = ["suunto_analyzer"] + argv
    try:
        return command_line()
    finally:
        sys.argv = old_argv


def test_all_enables_every_metric():
    arguments = run(["-f", "activity.json", "--all"])
    for name in METRIC_FLAGS:
        assert getattr(arguments, name) is True, name


def test_all_does_not_touch_mode_switches():
    arguments = run(["-f", "activity.json", "--all"])
    assert arguments.plot is False
    assert arguments.track is False
    assert arguments.compare is False


def test_without_all_flags_stay_off():
    arguments = run(["-f", "activity.json"])
    for name in METRIC_FLAGS:
        assert getattr(arguments, name) is False, name


def test_single_flag_beats_nothing_else():
    arguments = run(["-f", "activity.json", "--hr"])
    assert arguments.hr is True
    assert arguments.battery is False
