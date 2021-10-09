import json
import datetime
from collections import OrderedDict


class SuuntoJSON:
    def __init__(self):
        self.name = None
        self.datetime = None
        self.gnss = str()
        self.duration = 0
        self.distance = 0
        self.ascent = 0
        self.descent = 0
        self.altitude = OrderedDict()
        self.gps_altitude = OrderedDict()
        self.gps_snr = OrderedDict()
        self.battery_charge = OrderedDict()
        self.cadence = OrderedDict()

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
            self.gnss = temp["DeviceLog"]["Header"]["Settings"]["EnabledNavigationSystems"]
        except KeyError:
            pass
        try:
            self.duration = float(temp["DeviceLog"]["Header"]["Duration"])
        except KeyError:
            pass
        try:
            self.distance = float(temp["DeviceLog"]["Header"]["Distance"]) / 1000
        except KeyError:
            pass
        try:
            if temp["DeviceLog"]["Header"]["Ascent"] is not None:
                self.ascent = temp["DeviceLog"]["Header"]["Ascent"]
        except KeyError:
            pass
        try:
            if temp["DeviceLog"]["Header"]["Descent"] is not None:
                self.descent = temp["DeviceLog"]["Header"]["Descent"]
        except KeyError:
            pass
        # Samples
        for sample in temp["DeviceLog"]["Samples"]:
            timestamp = sample["TimeISO8601"]
            # Altitude
            try:
                if sample["Altitude"] is not None:
                    self.altitude[timestamp] = sample["Altitude"]
            except KeyError:
                pass
            # GPS altitude
            try:
                if sample["GPSAltitude"] is not None:
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
            # Cadence
            try:
                if sample["Cadence"] is not None:
                    self.cadence[timestamp] = 60.0 * sample["Cadence"]
            except KeyError:
                pass
        file.close()
