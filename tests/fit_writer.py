"""Minimal FIT encoder used to build binary fixtures for the tests.

It supports only the handful of messages and fields that the reader
uses, so the test suite does not need Garmin's encoder SDK. Values are
given in FIT profile units (metres, seconds, bpm, ...) and the profile
scale/offset of each field is applied while encoding, exactly as a
device or the official encoder would do.
"""

import datetime
import struct

FIT_EPOCH = datetime.datetime(1989, 12, 31, tzinfo=datetime.timezone.utc)
PROFILE_VERSION = 2140

# FIT base types: name -> (base type code, struct format or None)
BASE_TYPES = {
    "enum": (0x00, "B"),
    "sint8": (0x01, "b"),
    "uint8": (0x02, "B"),
    "uint16": (0x84, "H"),
    "sint32": (0x85, "i"),
    "uint32": (0x86, "I"),
    "uint32z": (0x8C, "I"),
    "date_time": (0x86, "I"),
    "string": (0x07, None),
}

ENUMS = {
    "type": {"activity": 4},
    "sport": {"generic": 0, "running": 1, "cycling": 2, "swimming": 5},
    "source_type": {
        "ant": 0,
        "antplus": 1,
        "bluetooth": 2,
        "bluetooth_low_energy": 3,
        "wifi": 4,
        "local": 5,
    },
}

# (field num, base type, scale, offset, converter, is_array)
FIELDS = {
    0: {  # file_id
        "type": (0, "enum", 1, 0, None, False),
        "manufacturer": (1, "uint16", 1, 0, None, False),
        "product": (2, "uint16", 1, 0, None, False),
        "serial_number": (3, "uint32z", 1, 0, None, False),
        "time_created": (4, "date_time", 1, 0, None, False),
        "product_name": (8, "string", 1, 0, None, False),
    },
    18: {  # session
        "start_time": (2, "date_time", 1, 0, None, False),
        "sport": (5, "enum", 1, 0, None, False),
        "total_elapsed_time": (7, "uint32", 1000, 0, None, False),
        "total_timer_time": (8, "uint32", 1000, 0, None, False),
        "total_distance": (9, "uint32", 100, 0, None, False),
        "total_strides": (10, "uint32", 1, 0, None, False),
        "total_ascent": (22, "uint16", 1, 0, None, False),
        "total_descent": (23, "uint16", 1, 0, None, False),
    },
    20: {  # record
        "position_lat": (0, "sint32", 1, 0, "semicircles", False),
        "position_long": (1, "sint32", 1, 0, "semicircles", False),
        "altitude": (2, "uint16", 5, 500, None, False),
        "heart_rate": (3, "uint8", 1, 0, None, False),
        "cadence": (4, "uint8", 1, 0, None, False),
        "distance": (5, "uint32", 100, 0, None, False),
        "power": (7, "uint16", 1, 0, None, False),
        "temperature": (13, "sint8", 1, 0, None, False),
        "gps_accuracy": (31, "uint8", 1, 0, None, False),
        "enhanced_altitude": (78, "uint32", 5, 500, None, False),
        "battery_soc": (81, "uint8", 2, 0, None, False),
        "timestamp": (253, "date_time", 1, 0, None, False),
    },
    23: {  # device_info
        "device_index": (0, "uint8", 1, 0, None, False),
        "device_type": (1, "uint8", 1, 0, None, False),
        "manufacturer": (2, "uint16", 1, 0, None, False),
        "serial_number": (3, "uint32z", 1, 0, None, False),
        "product": (4, "uint16", 1, 0, None, False),
        "software_version": (5, "uint16", 100, 0, None, False),
        "source_type": (25, "enum", 1, 0, None, False),
        "product_name": (27, "string", 1, 0, None, False),
        "battery_level": (32, "uint8", 1, 0, None, False),
        "timestamp": (253, "date_time", 1, 0, None, False),
    },
    78: {  # hrv
        "time": (0, "uint16", 1000, 0, None, True),
    },
}


def fit_timestamp(value: datetime.datetime) -> int:
    """Convert a datetime to FIT seconds (since 1989-12-31T00:00:00Z)."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.timezone.utc)
    return int((value.astimezone(datetime.timezone.utc) - FIT_EPOCH).total_seconds())


def _crc_table():
    table = []
    for index in range(256):
        crc = index
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
        table.append(crc)
    return tuple(table)


CRC_TABLE = _crc_table()


def compute_crc(data: bytes, crc: int = 0) -> int:
    """FIT's CRC-16 (poly 0xA001, init 0)."""
    for byte in data:
        crc = (crc >> 8) ^ CRC_TABLE[(crc ^ byte) & 0xFF]
    return crc


def _scalar_size(base: str) -> int:
    return struct.calcsize("<" + BASE_TYPES[base][1])


def _field_size(name: str, spec: tuple, value) -> int:
    *_, is_array = spec
    if spec[1] == "string":
        return len(str(value).encode("utf-8")) + 1
    if is_array:
        return _scalar_size(spec[1]) * len(value)
    return _scalar_size(spec[1])


def _encode_scalar(name: str, base: str, scale, offset, converter, value) -> bytes:
    if converter == "semicircles":
        raw = int(round(value * (2**31) / 180.0))
    elif base == "date_time":
        raw = fit_timestamp(value)
    else:
        if isinstance(value, str):
            value = ENUMS[name][value]
        raw = int(round((value + offset) * scale))
    return struct.pack("<" + BASE_TYPES[base][1], raw)


def _encode_value(name: str, spec: tuple, size: int, value) -> bytes:
    _, base, scale, offset, converter, is_array = spec
    if base == "string":
        encoded = str(value).encode("utf-8")
        return encoded[: size - 1].ljust(size, b"\x00")
    if is_array:
        return b"".join(
            _encode_scalar(name, base, scale, offset, converter, item) for item in value
        )
    return _encode_scalar(name, base, scale, offset, converter, value)


class FitFile:
    """Incrementally build a FIT file; call :meth:`to_bytes` at the end."""

    def __init__(self):
        self._data = bytearray()
        self._definitions = {}

    def add(self, mesg_num: int, **values) -> "FitFile":
        values = {name: value for name, value in values.items() if value is not None}
        if mesg_num not in self._definitions:
            local_num = len(self._definitions)
            fields, definition = self._build_definition(local_num, mesg_num, values)
            self._definitions[mesg_num] = (local_num, fields)
            self._data += definition
        else:
            local_num, fields = self._definitions[mesg_num]
        expected = {name for _, _, name in fields}
        if set(values) != expected:
            raise ValueError(f"inconsistent fields for FIT message {mesg_num}")
        self._data.append(local_num)
        for spec, size, name in fields:
            self._data += _encode_value(name, spec, size, values[name])
        return self

    def _build_definition(self, local_num: int, mesg_num: int, values):
        fields = sorted(
            ((FIELDS[mesg_num][name], name) for name in values),
            key=lambda item: item[0][0],
        )
        out = bytearray([0x40 | local_num, 0, 0])
        out += struct.pack("<H", mesg_num)
        out.append(len(fields))
        encoded = []
        for spec, name in fields:
            size = _field_size(name, spec, values[name])
            out += bytes([spec[0], size, BASE_TYPES[spec[1]][0]])
            encoded.append((spec, size, name))
        return encoded, bytes(out)

    def to_bytes(self) -> bytes:
        data = bytes(self._data)
        header = bytearray(
            struct.pack("<BBHI4s", 14, 0x10, PROFILE_VERSION, len(data), b".FIT")
        )
        header += struct.pack("<H", compute_crc(header))
        payload = bytes(header) + data
        return payload + struct.pack("<H", compute_crc(payload))
