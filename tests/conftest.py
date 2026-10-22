import json

import pytest

HEADER = {
    "Device": {"Name": "Ibiza", "Info": {"SW": "11.2.0"}},
    "DateTime": "2024-05-01T08:00:00.000Z",
    "Settings": {
        "EnabledNavigationSystems": "GPS+GLONASS",
        "AltiBaroProfile": "Auto",
        "BikePodUsed": False,
        "FootPodUsed": True,
        "PowerPodUsed": False,
        "FusedAltiUsed": True,
        "HrUsed": True,
    },
    "Duration": 600.0,
    "Distance": 2000.0,
    "Ascent": 10,
    "Descent": 5,
    "StepCount": 1500,
}

SAMPLES = [
    {
        "TimeISO8601": "2024-05-01T08:00:01.000Z",
        "Latitude": 1.0,
        "Longitude": 2.0,
        "Temperature": 293.15,
        "Altitude": 100.0,
        "GPSAltitude": 98.0,
        "Satellite5BestSNR": 30,
        "EHPE": 3,
        "EVPE": 5,
        "BatteryCharge": 0.9,
        "Cadence": 80,
        "Power": 250,
        "Distance": 10,
        "HR": 70,
    },
    {
        # A sample with empty optional channels: these must be skipped
        # instead of being stored as None.
        "TimeISO8601": "2024-05-01T08:00:02.000Z",
        "Latitude": 1.001,
        "Longitude": 2.001,
        "Temperature": 294.15,
        "Altitude": 101.0,
        "GPSAltitude": 99.0,
        "Satellite5BestSNR": None,
        "EHPE": None,
        "EVPE": None,
        "BatteryCharge": None,
        "Cadence": 82,
        "Power": 255,
        "Distance": 20,
        "HR": 72,
    },
    {
        "TimeISO8601": "2024-05-01T08:00:03.000Z",
        "Latitude": 1.002,
        "Longitude": 2.002,
        "Temperature": 295.15,
        "Altitude": 102.0,
        "GPSAltitude": 100.0,
        "Satellite5BestSNR": 32,
        "EHPE": 4,
        "EVPE": 6,
        "BatteryCharge": 0.88,
        "Cadence": 84,
        "Power": 260,
        "Distance": 30,
        "HR": 74,
    },
]


def build_log(samples=None, header=None, extra=None):
    """Build a synthetic Suunto DeviceLog dictionary."""
    log = {
        "DeviceLog": {
            "Header": dict(HEADER) if header is None else header,
            "Samples": (
                [dict(sample) for sample in SAMPLES] if samples is None else samples
            ),
        }
    }
    if extra:
        log["DeviceLog"].update(extra)
    return log


def write_log(tmp_path, log, name="activity.json"):
    path = tmp_path / name
    path.write_text(json.dumps(log))
    return path


@pytest.fixture
def activity_file(tmp_path):
    """A well-formed activity file with Z-suffixed ISO 8601 timestamps."""
    log = build_log(
        extra={"R-R": {"Data": [800, 810, 795]}, "Zapps": [{"Name": "App1"}]}
    )
    return write_log(tmp_path, log)
