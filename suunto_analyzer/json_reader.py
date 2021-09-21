import json
import datetime
from collections import OrderedDict


class SuuntoJSON:
    def __init__(self):
        self.name = None
        self.datetime = None
        self.duration = 0
        self.distance = 0
        self.altitude = OrderedDict()
        self.gps_altitude = OrderedDict()
        self.gps_snr = OrderedDict()
        self.battery_charge = OrderedDict()

    def load_file(self, filename: str):
        with open(filename) as file:
            temp = json.load(file)
        # Header
        try:
            self.name = f"{temp['DeviceLog']['Header']['Device']['Name']} {temp['DeviceLog']['Header']['Device']['Info']['SW']}"
        except KeyError:
            pass
        try:
            self.datetime = datetime.datetime.fromisoformat(temp["DeviceLog"]["Header"]["DateTime"])
        except KeyError:
            pass
        try:
            self.duration = float(temp["DeviceLog"]["Header"]["Duration"])
        except KeyError:
            pass
        try:
            self.distance = float(temp["DeviceLog"]["Header"]["Duration"]) / 1000
        except KeyError:
            pass
        # Samples
        for sample in temp["DeviceLog"]["Samples"]:
            timestamp = sample["TimeISO8601"]
            # Altitude
            try:
                self.altitude[timestamp] = sample["Altitude"]
            except KeyError:
                pass
            # GPS altitude
            try:
                self.gps_altitude[timestamp] = sample["GPSAltitude"]
            except KeyError:
                pass
            # SNR 5 best satellites
            try:
                self.gps_snr[timestamp] = sample["Satellite5BestSNR"]
            except KeyError:
                pass
            # Battery charge
            try:
                self.battery_charge[timestamp] = sample["BatteryCharge"]
            except KeyError:
                pass
        file.close()
