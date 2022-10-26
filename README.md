
# Suunto Activity Analyzer (SAA)

Simple tool to analyze activities recorded with [Suunto](https://www.suunto.com) watches.
The idea of the tool is to be able to check some statistics extracted from the native JSON activity files, to help in testing watches.

## Install

You can download and install the latest version of this package with `pip`:

```shell
python -m pip install -U git+https://github.com/isazi/SuuntoAnalyzer 
```

## Usage

To visualize the helper it is possible to use the `-h` command line argument:

```shell
python -m suunto_analyzer -h
```

Following is the output of this command:

```shell
Suunto Activity Analyzer (SAA)

usage: suunto_analyzer.py [-h] -f FILENAME [--plot] [--duration] [--distance] [--steps] [--sensors] [--apps] [--gps_error] [--snr] [--battery] [--cadence] [--temperature] [--altitude] [--power] [--hr]
                          [--compare] [-f2 FILENAME2]

options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        File to analyze
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
  --compare             Enable comparison with a second activity file
  -f2 FILENAME2, --filename2 FILENAME2
                        File to compare with
```