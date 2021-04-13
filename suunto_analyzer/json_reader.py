import json
import numpy


class SuuntoJSON:
    def __init__(self):
        self.altitude = list()
        self.gps_altitude = list()

    def load_file(self, filename: str):
        with open(filename) as file:
            temp = json.load(file)
        for sample in temp["DeviceLog"]["Samples"]:
            # Altitude
            try:
                self.altitude.append(sample["Altitude"])
            except KeyError:
                pass
            # GPS altitude
            try:
                self.gps_altitude.append(sample["GPSAltitude"])
            except KeyError:
                pass
