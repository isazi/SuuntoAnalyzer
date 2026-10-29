import json

from suunto_analyzer.activity import Activity
from suunto_analyzer.util import parse_timestamp


class SuuntoJSON(Activity):
    def load_file(self, filename: str):
        with open(filename) as file:
            temp = json.load(file)
        # Header
        try:
            self.name = f"{temp['DeviceLog']['Header']['Device']['Name']} {temp['DeviceLog']['Header']['Device']['Info']['SW']}"
        except KeyError:
            pass
        try:
            self.datetime = parse_timestamp(temp["DeviceLog"]["Header"]["DateTime"])
        except (KeyError, ValueError):
            pass
        try:
            self.gnss = temp["DeviceLog"]["Header"]["Settings"][
                "EnabledNavigationSystems"
            ]
        except KeyError:
            pass
        try:
            self.altibaro = temp["DeviceLog"]["Header"]["Settings"]["AltiBaroProfile"]
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
        try:
            if temp["DeviceLog"]["Header"]["Settings"]["BikePodUsed"] is True:
                self.sensors.append("Bike Pod")
        except KeyError:
            pass
        try:
            if temp["DeviceLog"]["Header"]["Settings"]["FootPodUsed"] is True:
                self.sensors.append("Foot Pod")
        except KeyError:
            pass
        try:
            if temp["DeviceLog"]["Header"]["Settings"]["PowerPodUsed"] is True:
                self.sensors.append("Power Pod")
        except KeyError:
            pass
        try:
            if temp["DeviceLog"]["Header"]["Settings"]["FusedAltiUsed"] is True:
                self.fusedalti = True
        except KeyError:
            pass
        try:
            if temp["DeviceLog"]["Header"]["Settings"]["HrUsed"] is True:
                self.sensors.append("Heart Rate")
        except KeyError:
            pass
        try:
            if temp["DeviceLog"]["Header"]["StepCount"] is not None:
                self.steps = temp["DeviceLog"]["Header"]["StepCount"]
        except KeyError:
            pass
        # Samples
        for sample in temp["DeviceLog"].get("Samples", []):
            try:
                timestamp = parse_timestamp(sample["TimeISO8601"])
            except (KeyError, ValueError):
                timestamp = None
            try:
                if sample["Latitude"] is not None and sample["Longitude"] is not None:
                    self.coordinates.append((sample["Latitude"], sample["Longitude"]))
            except KeyError:
                pass
            if timestamp is None:
                continue
            try:
                if sample["Temperature"] is not None:
                    self.temperature[timestamp] = sample["Temperature"]
            except KeyError:
                pass
            try:
                if sample["Altitude"] is not None:
                    self.altitude[timestamp] = sample["Altitude"]
            except KeyError:
                pass
            try:
                if sample["GPSAltitude"] is not None:
                    self.gps_altitude[timestamp] = sample["GPSAltitude"]
            except KeyError:
                pass
            try:
                if sample["Satellite5BestSNR"] is not None:
                    self.gps_snr[timestamp] = sample["Satellite5BestSNR"]
            except KeyError:
                pass
            try:
                if sample["EHPE"] is not None:
                    self.ehpe[timestamp] = sample["EHPE"]
            except KeyError:
                pass
            try:
                if sample["EVPE"] is not None:
                    self.evpe[timestamp] = sample["EVPE"]
            except KeyError:
                pass
            try:
                if sample["BatteryCharge"] is not None:
                    self.battery_charge[timestamp] = sample["BatteryCharge"]
            except KeyError:
                pass
            try:
                if sample["Cadence"] is not None:
                    self.cadence[timestamp] = sample["Cadence"] * 60.0
            except KeyError:
                pass
            try:
                if sample["Power"] is not None:
                    self.power[timestamp] = sample["Power"]
            except KeyError:
                pass
            try:
                if sample["Distance"] is not None:
                    self.running_distance[timestamp] = sample["Distance"]
            except KeyError:
                pass
            try:
                if sample["HR"] is not None:
                    self.hr[timestamp] = sample["HR"] * 60.0
            except KeyError:
                pass
        # External HR
        try:
            for value in temp["DeviceLog"]["R-R"]["Data"]:
                self.rr.append(value)
        except KeyError:
            pass
        # S+ apps
        try:
            for app in temp["DeviceLog"]["Zapps"]:
                self.apps.append(app["Name"])
        except KeyError:
            pass
