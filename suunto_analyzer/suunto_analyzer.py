import argparse
import json_reader
import gps


def command_line():
    parser = argparse.ArgumentParser()
    # Files
    parser.add_argument("-f", "--filename", type=str, required=True)
    parser.add_argument("--snr", action="store_true")
    return parser.parse_args()


def __main__():
    print("Suunto Analyzer")
    print()

    arguments = command_line()
    activity = json_reader.SuuntoJSON()
    activity.load_file(arguments.filename)
    if arguments.snr:
        gps.gps_snr_analysis(activity)

    print()
    return 0


if __name__ == "__main__":
    __main__()
