import argparse
import matplotlib.pyplot
import json_reader


def command_line():
    parser = argparse.ArgumentParser()
    # Files
    parser.add_argument("-f", "--filename", type=str, required=True)
    return parser.parse_args()


def __main__():
    arguments = command_line()
    activity = json_reader.SuuntoJSON()
    activity.load_file(arguments.filename)
    print(len(activity.altitude))
    matplotlib.pyplot.plot(activity.altitude)
    matplotlib.pyplot.ylabel("Altitude")
    matplotlib.pyplot.xticks()
    matplotlib.pyplot.plot(activity.gps_altitude)
    matplotlib.pyplot.savefig("./altitude.png")
    print(len(activity.gps_altitude))
    return 0


if __name__ == "__main__":
    __main__()
