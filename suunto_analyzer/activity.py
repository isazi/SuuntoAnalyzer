"""Device-agnostic activity model shared by every reader.

The readers (Suunto JSON, FIT, ...) fill an :class:`Activity` and the
analysis, plotting and track modules only depend on this interface.
The units are part of the contract:

* ``datetime``: timezone-aware UTC
* sample keys: timezone-aware UTC ``datetime`` objects
* ``duration``: seconds
* ``distance``: kilometres
* ``running_distance``: metres
* ``temperature``: Kelvin
* ``battery_charge``: fraction (0..1)
* ``cadence``: rpm
* ``hr``: bpm
* ``rr``: milliseconds
* ``coordinates``: ``(latitude, longitude)`` in radians
* ``altitude``, ``gps_altitude``, ``ascent``, ``descent``, ``ehpe``,
  ``evpe``: metres
"""

from collections import OrderedDict


class Activity:
    def __init__(self):
        self.name = None
        self.filename = ""
        self.datetime = None
        self.sport = None
        self.gnss = str()
        self.altibaro = str()
        self.fusedalti = False
        self.steps = 0
        self.duration = 0
        self.distance = 0
        self.running_distance = OrderedDict()
        self.ascent = 0
        self.descent = 0
        self.sensors = []
        self.apps = []
        self.coordinates = []
        self.temperature = OrderedDict()
        self.altitude = OrderedDict()
        self.gps_altitude = OrderedDict()
        self.gps_snr = OrderedDict()
        self.ehpe = OrderedDict()
        self.evpe = OrderedDict()
        self.battery_charge = OrderedDict()
        self.cadence = OrderedDict()
        self.hr = OrderedDict()
        self.rr = []
        self.power = OrderedDict()
