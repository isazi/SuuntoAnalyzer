"""Reader for FIT files, Garmin's binary activity format."""

import math

try:
    import fitdecode
except ImportError:  # pragma: no cover - depends on the installed extras
    fitdecode = None

from suunto_analyzer.activity import Activity

INSTALL_HINT = (
    'Reading FIT files requires the optional "fit" extra. Install it with: '
    'python -m pip install "suunto_analyzer[fit]"'
)


class FitdecodeNotInstalled(RuntimeError):
    """Raised when a FIT file is loaded without the optional dependency."""


def require_fitdecode():
    if fitdecode is None:
        raise FitdecodeNotInstalled(INSTALL_HINT)


class SuuntoFIT(Activity):
    """A FIT activity adapted to the canonical :class:`Activity` model.

    ``fitdecode``'s ``StandardUnitsDataProcessor`` already converts
    semicircles to degrees, applies the FIT scale/offset of numeric
    fields (distance in km, timer time in s, ...) and turns FIT
    date-times into timezone-aware UTC datetimes. Only the remaining
    conversions to the canonical units happen here.

    FIT has no equivalent of some Suunto channels (SNR, GNSS altitude,
    FusedAlti/S+ apps, steps): those attributes are simply left empty.
    The horizontal GPS accuracy is used as the EHPE series.
    """

    def load_file(self, filename: str):
        require_fitdecode()
        with fitdecode.FitReader(
            filename, processor=fitdecode.StandardUnitsDataProcessor()
        ) as reader:
            for frame in reader:
                if not isinstance(frame, fitdecode.FitDataMessage):
                    continue
                if frame.name == "record":
                    self._add_record(frame)
                elif frame.name == "session":
                    self._add_session(frame)
                elif frame.name == "file_id":
                    self._add_file_id(frame)
                elif frame.name == "device_info":
                    self._add_device_info(frame)
                elif frame.name == "hrv":
                    self._add_hrv(frame)
        if self.name is None and self.sport is not None:
            self.name = str(self.sport).capitalize()

    @staticmethod
    def _values(frame) -> dict:
        return {
            field.name: field.value for field in frame.fields if field.name is not None
        }

    def _add_record(self, frame):
        values = self._values(frame)
        timestamp = values.get("timestamp")
        if timestamp is None:
            return
        latitude = values.get("position_lat")
        longitude = values.get("position_long")
        if latitude is not None and longitude is not None:
            # fitdecode reports degrees, the canonical model uses radians.
            self.coordinates.append((math.radians(latitude), math.radians(longitude)))
        altitude = values.get("enhanced_altitude")
        if altitude is None:
            altitude = values.get("altitude")
        if altitude is not None:
            self.altitude[timestamp] = float(altitude)
        temperature = values.get("temperature")
        if temperature is not None:
            self.temperature[timestamp] = float(temperature) + 273.15
        distance = values.get("distance")
        if distance is not None:
            # fitdecode reports distance in km, the canonical model uses m.
            self.running_distance[timestamp] = float(distance) * 1000.0
        heart_rate = values.get("heart_rate")
        if heart_rate is not None:
            self.hr[timestamp] = float(heart_rate)
        cadence = values.get("cadence")
        if cadence is not None:
            self.cadence[timestamp] = float(cadence)
        power = values.get("power")
        if power is not None:
            self.power[timestamp] = float(power)
        battery = values.get("battery_soc")
        if battery is not None:
            self.battery_charge[timestamp] = float(battery) / 100.0
        accuracy = values.get("gps_accuracy")
        if accuracy is not None:
            self.ehpe[timestamp] = float(accuracy)

    def _add_session(self, frame):
        values = self._values(frame)
        start_time = values.get("start_time")
        if start_time is not None and self.datetime is None:
            self.datetime = start_time
        duration = values.get("total_timer_time")
        if duration is None:
            duration = values.get("total_elapsed_time")
        if duration is not None:
            self.duration = float(duration)
        distance = values.get("total_distance")
        if distance is not None:
            # fitdecode reports km, which is already the canonical unit.
            self.distance = float(distance)
        ascent = values.get("total_ascent")
        if ascent is not None:
            self.ascent = ascent
        descent = values.get("total_descent")
        if descent is not None:
            self.descent = descent
        steps = values.get("total_strides")
        if steps is not None:
            # Suunto fills this field with the same number the JSON
            # export reports as StepCount (verified against a paired
            # export of the same activity), despite the "strides" name.
            self.steps = int(round(steps))
        sport = values.get("sport")
        if sport is not None:
            self.sport = sport

    def _add_file_id(self, frame):
        values = self._values(frame)
        product_name = values.get("product_name")
        if product_name:
            self.name = product_name
        if self.datetime is None:
            created = values.get("time_created")
            if created is not None:
                self.datetime = created

    def _add_device_info(self, frame):
        values = self._values(frame)
        # device_info also describes connected sensors; only the watch
        # itself describes the activity: source_type "local" (the FIT
        # default), or the creator device. Some producers omit both
        # fields entirely for the watch; the defaults are then local.
        source_type = values.get("source_type")
        device_index = values.get("device_index")
        local = source_type == "local" or (
            source_type is None and device_index in (0, "creator", None)
        )
        if not local:
            return
        product_name = values.get("product_name")
        if self.name is None and product_name:
            self.name = product_name
        battery = values.get("battery_level")
        timestamp = values.get("timestamp")
        if battery is not None and timestamp is not None:
            self.battery_charge[timestamp] = float(battery) / 100.0

    def _add_hrv(self, frame):
        values = self._values(frame)
        intervals = values.get("time")
        if intervals is None:
            return
        if not isinstance(intervals, (tuple, list)):
            intervals = (intervals,)
        for interval in intervals:
            # fitdecode reports seconds, the canonical rr series uses ms.
            self.rr.append(int(round(float(interval) * 1000)))
