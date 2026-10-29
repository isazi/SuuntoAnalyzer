
# Suunto Activity Analyzer (SAA)

Simple tool to analyze activities recorded with [Suunto](https://www.suunto.com) watches.
The idea of the tool is to be able to check some statistics extracted from the native JSON activity files, to help in testing watches.
[FIT](https://developer.garmin.com/fit/overview/) files (the binary format used by Garmin and many other sport devices) are supported too.

## Install

You can download and install the latest version of this package with `pip`:

```shell
python -m pip install -U git+https://github.com/isazi/SuuntoAnalyzer 
```

To plot tracks (`--track`) on top of real map tiles, install the optional `map` extra (map tiles are downloaded at runtime, so network access is required):

```shell
python -m pip install -U "suunto_analyzer[map] @ git+https://github.com/isazi/SuuntoAnalyzer"
```

Without it, tracks are plotted as plain latitude/longitude lines.

FIT files are read through the optional `fit` extra:

```shell
python -m pip install -U "suunto_analyzer[fit] @ git+https://github.com/isazi/SuuntoAnalyzer"
```

Without it only Suunto JSON files can be loaded.

## Usage

To visualize the helper it is possible to use the `-h` command line argument:

```shell
python -m suunto_analyzer -h
```

Following is the output of this command:

```
Suunto Activity Analyzer (SAA)

usage: __main__.py [-h] -f FILES [FILES ...] [--plot] [--duration] [--distance] [--steps] [--sensors] [--apps] [--gps_error] [--snr] [--battery] [--cadence] [--temperature] [--altitude] [--power] [--hr]
                   [--compare]

options:
  -h, --help            show this help message and exit
  -f FILES [FILES ...], --files FILES [FILES ...]
                        Files to analyze
  --plot                Enable plotting
  --duration            Show duration
  --distance            Show distance
  --steps               Show the number of steps
  --sensors             Show the used sensors
  --apps                Show the enabled S+ apps
  --gps_error           Shows the GPS horizontal/vertical error.
  --snr                 Show SNR of 5 best GNSS satellites
  --battery             Show battery consumption
  --cadence             Show cadence
  --temperature         Show temperature
  --altitude            Show ascent, descent, and altitude
  --power               Show power
  --hr                  Show heart rate
  --compare             Enable comparison between activities
```

The reader is chosen from the file extension: `.json` files are parsed as Suunto activity logs and `.fit` files as FIT activities (both can be mixed on the same command line).
FIT files do not carry some Suunto-specific channels (satellite SNR, GNSS altitude, FusedAlti, S+ apps, steps), so those analyses and plots print nothing for them; however, `--altitude` still reports the ascent, descent and altimeter altitude found in the FIT file, and the horizontal GPS accuracy is reported as `EHPE`.

## Development

Install the package in editable mode together with the test dependencies:

```shell
python -m pip install -e ".[dev]"
```

Run the test suite:

```shell
python -m pytest
```