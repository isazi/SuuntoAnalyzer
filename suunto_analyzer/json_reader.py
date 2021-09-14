import json
from collections import OrderedDict


class SuuntoJSON:
    def __init__(self):
        self.altitude = OrderedDict()
        self.gps_altitude = OrderedDict()
        self.gps_snr = OrderedDict()

    def load_file(self, filename: str):
        with open(filename) as file:
            temp = json.load(file)
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
        file.close()

