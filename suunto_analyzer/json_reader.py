import json
import numpy


class SuuntoJSON:
    def __init__(self):
        self.altitude = list()

    def load_file(self, filename: str):
        with open(filename) as file:
            temp = json.load(file)
        for sample in temp["DeviceLog"]["Samples"]:
            try:
                self.altitude.append(sample["Altitude"])
            except KeyError:
                continue

    def altitude_statistics(self):
        print(f"Min ({numpy.min(self.altitude)})")
        print(f"Median ({numpy.median(self.altitude)})")
        print(f"Max ({numpy.max(self.altitude)})")
