# msgtypes.py
# Author: Meghan Clark
#    Edited for python3 by François Wautier

# To Do: Validate that args are within required ranges, types, etc. In particular: Color [0-65535, 0-65535, 0-65535, 2500-9000], Power Level (must be 0 OR 65535)
# Need to look into assert-type frameworks or something, there has to be a tool for that.
# Also need to make custom errors possibly, though tool may have those.

from curses import color_content
from .message import Message, BROADCAST_MAC, HEADER_SIZE_BYTES, little_endian
import bitstring
from enum import Enum
import random
import sys
import struct

##### DEVICE MESSAGES #####


class GetService(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        target_addr = BROADCAST_MAC
        super(GetService, self).__init__(
            MSG_IDS[GetService],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class StateService(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.service = payload["service"]
        self.port = payload["port"]
        super(StateService, self).__init__(
            MSG_IDS[StateService],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Service", self.service))
        self.payload_fields.append(("Port", self.port))
        service = little_endian(bitstring.pack("uint:8", self.service))
        port = little_endian(bitstring.pack("uint:32", self.port))
        payload = service + port
        return payload


class GetHostInfo(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetHostInfo, self).__init__(
            MSG_IDS[GetHostInfo],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class StateHostInfo(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.signal = payload["signal"]
        self.tx = payload["tx"]
        self.rx = payload["rx"]
        self.reserved1 = payload["reserved1"]
        super(StateHostInfo, self).__init__(
            MSG_IDS[StateHostInfo],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Signal (mW)", self.signal))
        self.payload_fields.append(("TX (bytes since on)", self.tx))
        self.payload_fields.append(("RX (bytes since on)", self.rx))
        self.payload_fields.append(("Reserved", self.reserved1))
        signal = little_endian(bitstring.pack("float:32", self.signal))
        tx = little_endian(bitstring.pack("uint:32", self.tx))
        rx = little_endian(bitstring.pack("uint:32", self.rx))
        reserved1 = little_endian(bitstring.pack("int:16", self.reserved1))
        payload = signal + tx + rx + reserved1
        return payload


class GetHostFirmware(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetHostFirmware, self).__init__(
            MSG_IDS[GetHostFirmware],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class StateHostFirmware(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.build = payload["build"]
        self.reserved1 = payload["reserved1"]
        self.version = payload["version"]
        super(StateHostFirmware, self).__init__(
            MSG_IDS[StateHostFirmware],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Timestamp of Build", self.build))
        self.payload_fields.append(("Reserved", self.reserved1))
        self.payload_fields.append(("Version", self.version))
        build = little_endian(bitstring.pack("uint:64", self.build))
        reserved1 = little_endian(bitstring.pack("uint:64", self.reserved1))
        version = little_endian(bitstring.pack("uint:32", self.version))
        payload = build + reserved1 + version
        return payload


class GetWifiInfo(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetWifiInfo, self).__init__(
            MSG_IDS[GetWifiInfo],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class StateWifiInfo(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.signal = payload["signal"]
        self.tx = payload["tx"]
        self.rx = payload["rx"]
        self.reserved1 = payload["reserved1"]
        super(StateWifiInfo, self).__init__(
            MSG_IDS[StateWifiInfo],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Signal (mW)", self.signal))
        self.payload_fields.append(("TX (bytes since on)", self.tx))
        self.payload_fields.append(("RX (bytes since on)", self.rx))
        self.payload_fields.append(("Reserved", self.reserved1))
        signal = little_endian(bitstring.pack("float:32", self.signal))
        tx = little_endian(bitstring.pack("uint:32", self.tx))
        rx = little_endian(bitstring.pack("uint:32", self.rx))
        reserved1 = little_endian(bitstring.pack("int:16", self.reserved1))
        payload = signal + tx + rx + reserved1
        return payload


class GetWifiFirmware(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetWifiFirmware, self).__init__(
            MSG_IDS[GetWifiFirmware],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class StateWifiFirmware(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.build = payload["build"]
        self.reserved1 = payload["reserved1"]
        self.version = payload["version"]
        super(StateWifiFirmware, self).__init__(
            MSG_IDS[StateWifiFirmware],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Timestamp of Build", self.build))
        self.payload_fields.append(("Reserved", self.reserved1))
        self.payload_fields.append(("Version", self.version))
        build = little_endian(bitstring.pack("uint:64", self.build))
        reserved1 = little_endian(bitstring.pack("uint:64", self.reserved1))
        version = little_endian(bitstring.pack("uint:32", self.version))
        payload = build + reserved1 + version
        return payload


class GetPower(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetPower, self).__init__(
            MSG_IDS[GetPower],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class SetPower(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.power_level = payload["power_level"]
        super(SetPower, self).__init__(
            MSG_IDS[SetPower],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Power", self.power_level))
        power_level = little_endian(bitstring.pack("uint:16", self.power_level))
        payload = power_level
        return payload


class StatePower(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.power_level = payload["power_level"]
        super(StatePower, self).__init__(
            MSG_IDS[StatePower],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Power", self.power_level))
        power_level = little_endian(bitstring.pack("uint:16", self.power_level))
        payload = power_level
        return payload


class GetLabel(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetLabel, self).__init__(
            MSG_IDS[GetLabel],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class SetLabel(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.label = payload["label"]
        super(SetLabel, self).__init__(
            MSG_IDS[SetLabel],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Label", self.label))
        field_len_bytes = 32
        label = b"".join(
            little_endian(bitstring.pack("uint:8", ord(c))) for c in self.label
        )
        padding = b"".join(
            little_endian(bitstring.pack("uint:8", 0))
            for i in range(field_len_bytes - len(self.label))
        )
        payload = label + padding
        return payload


class StateLabel(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.label = payload["label"]
        super(StateLabel, self).__init__(
            MSG_IDS[StateLabel],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Label", self.label))
        field_len_bytes = 32
        label = b"".join(little_endian(bitstring.pack("uint:8", c)) for c in self.label)
        padding = b"".join(
            little_endian(bitstring.pack("uint:8", 0))
            for i in range(field_len_bytes - len(self.label))
        )
        payload = label + padding
        return payload


class GetVersion(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetVersion, self).__init__(
            MSG_IDS[GetVersion],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class StateVersion(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.vendor = payload["vendor"]
        self.product = payload["product"]
        self.version = payload["version"]
        super(StateVersion, self).__init__(
            MSG_IDS[StateVersion],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Vendor", self.vendor))
        self.payload_fields.append(("Reserved", self.product))
        self.payload_fields.append(("Version", self.version))
        vendor = little_endian(bitstring.pack("uint:32", self.vendor))
        product = little_endian(bitstring.pack("uint:32", self.product))
        version = little_endian(bitstring.pack("uint:32", self.version))
        payload = vendor + product + version
        return payload


class GetInfo(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetInfo, self).__init__(
            MSG_IDS[GetInfo],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class StateInfo(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.time = payload["time"]
        self.uptime = payload["uptime"]
        self.downtime = payload["downtime"]
        super(StateInfo, self).__init__(
            MSG_IDS[StateInfo],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Current Time", self.time))
        self.payload_fields.append(("Uptime (ns)", self.uptime))
        self.payload_fields.append(
            ("Last Downtime Duration (ns) (5 second error)", self.downtime)
        )
        time = little_endian(bitstring.pack("uint:64", self.time))
        uptime = little_endian(bitstring.pack("uint:64", self.uptime))
        downtime = little_endian(bitstring.pack("uint:64", self.downtime))
        payload = time + uptime + downtime
        return payload


class GetLocation(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetLocation, self).__init__(
            MSG_IDS[GetLocation],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class StateLocation(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.location = payload["location"]
        self.label = payload["label"]
        self.updated_at = payload["updated_at"]
        super(StateLocation, self).__init__(
            MSG_IDS[StateLocation],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Location ", self.location))
        self.payload_fields.append(("Label ", self.label))
        self.payload_fields.append(("Updated At ", self.updated_at))
        location = b"".join(
            little_endian(bitstring.pack("uint:8", b)) for b in self.location
        )
        label = b"".join(little_endian(bitstring.pack("uint:8", c)) for c in self.label)
        label_padding = b"".join(
            little_endian(bitstring.pack("uint:8", 0))
            for i in range(32 - len(self.label))
        )
        label += label_padding
        updated_at = little_endian(bitstring.pack("uint:64", self.updated_at))
        payload = location + label + updated_at
        return payload


class GetGroup(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetGroup, self).__init__(
            MSG_IDS[GetGroup],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class StateGroup(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.group = payload["group"]
        self.label = payload["label"]
        self.updated_at = payload["updated_at"]
        super(StateGroup, self).__init__(
            MSG_IDS[StateGroup],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Group ", self.group))
        self.payload_fields.append(("Label ", self.label))
        self.payload_fields.append(("Updated At ", self.updated_at))
        group = b"".join(little_endian(bitstring.pack("uint:8", b)) for b in self.group)
        label = b"".join(little_endian(bitstring.pack("uint:8", c)) for c in self.label)
        label_padding = b"".join(
            little_endian(bitstring.pack("uint:8", 0))
            for i in range(32 - len(self.label))
        )
        label += label_padding
        updated_at = little_endian(bitstring.pack("uint:64", self.updated_at))
        payload = group + label + updated_at
        return payload


class SetReboot(Message):
    def __init__(
        self,
        target_addr: str,
        source_id: str,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ) -> None:
        """Initialise a SetReboot packet."""
        super(SetReboot, self).__init__(
            MSG_IDS[SetReboot],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class Acknowledgement(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(Acknowledgement, self).__init__(
            MSG_IDS[Acknowledgement],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class EchoRequest(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.byte_array = payload["byte_array"]
        super(EchoRequest, self).__init__(
            MSG_IDS[EchoRequest],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        field_len = 64
        self.payload_fields.append(("Byte Array", self.byte_array))
        byte_array = b"".join(
            little_endian(bitstring.pack("uint:8", b)) for b in self.byte_array
        )
        byte_array_len = len(byte_array)
        if byte_array_len < field_len:
            byte_array += b"".join(
                little_endian(bitstring.pack("uint:8", 0))
                for i in range(field_len - byte_array_len)
            )
        elif byte_array_len > field_len:
            byte_array = byte_array[:field_len]
        payload = byte_array
        return payload


class EchoResponse(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.byte_array = payload["byte_array"]
        super(EchoResponse, self).__init__(
            MSG_IDS[EchoResponse],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Byte Array", self.byte_array))
        byte_array = b"".join(
            little_endian(bitstring.pack("uint:8", b)) for b in self.byte_array
        )
        payload = byte_array
        return payload


##### LIGHT MESSAGES #####


class LightGet(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(LightGet, self).__init__(
            MSG_IDS[LightGet],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class LightSetColor(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.color = payload["color"]
        self.duration = payload["duration"]
        super(LightSetColor, self).__init__(
            MSG_IDS[LightSetColor],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        reserved_8 = little_endian(bitstring.pack("uint:8", self.reserved))
        color = b"".join(
            little_endian(bitstring.pack("uint:16", field)) for field in self.color
        )
        duration = little_endian(bitstring.pack("uint:32", self.duration))
        payload = reserved_8 + color + duration
        payloadUi = " ".join("{:02x}".format(c) for c in payload)
        return payload


class LightSetWaveform(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.transient = payload["transient"]
        self.color = payload["color"]
        self.period = payload["period"]
        self.cycles = payload["cycles"]
        self.skew_ratio = payload["skew_ratio"]
        self.waveform = payload["waveform"]
        super(LightSetWaveform, self).__init__(
            MSG_IDS[LightSetWaveform],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        reserved_8 = little_endian(bitstring.pack("uint:8", self.reserved))
        transient = little_endian(bitstring.pack("uint:8", self.transient))
        color = b"".join(
            little_endian(bitstring.pack("uint:16", field)) for field in self.color
        )
        period = little_endian(bitstring.pack("uint:32", self.period))
        cycles = little_endian(bitstring.pack("float:32", self.cycles))
        skew_ratio = little_endian(bitstring.pack("int:16", self.skew_ratio))
        waveform = little_endian(bitstring.pack("uint:8", self.waveform))
        payload = (
            reserved_8 + transient + color + period + cycles + skew_ratio + waveform
        )

        payloadUi = " ".join("{:02x}".format(c) for c in payload)
        return payload


class LightSetWaveformOptional(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.transient = payload["transient"]
        self.color = payload["color"]
        self.period = payload["period"]
        self.cycles = payload["cycles"]
        self.skew_ratio = payload["skew_ratio"]
        self.waveform = payload["waveform"]
        self.set_hue = payload["set_hue"]
        self.set_saturation = payload["set_saturation"]
        self.set_brightness = payload["set_brightness"]
        self.set_kelvin = payload["set_kelvin"]
        super(LightSetWaveformOptional, self).__init__(
            MSG_IDS[LightSetWaveformOptional],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        reserved_8 = little_endian(bitstring.pack("uint:8", self.reserved))
        transient = little_endian(bitstring.pack("uint:8", self.transient))
        color = b"".join(
            little_endian(bitstring.pack("uint:16", field)) for field in self.color
        )
        period = little_endian(bitstring.pack("uint:32", self.period))
        cycles = little_endian(bitstring.pack("float:32", self.cycles))
        skew_ratio = little_endian(bitstring.pack("int:16", self.skew_ratio))
        waveform = little_endian(bitstring.pack("uint:8", self.waveform))
        set_hue = little_endian(bitstring.pack("uint:8", self.set_hue))
        set_saturation = little_endian(bitstring.pack("uint:8", self.set_saturation))
        set_brightness = little_endian(bitstring.pack("uint:8", self.set_brightness))
        set_kelvin = little_endian(bitstring.pack("uint:8", self.set_kelvin))
        payload = (
            reserved_8
            + transient
            + color
            + period
            + cycles
            + skew_ratio
            + waveform
            + set_hue
            + set_saturation
            + set_brightness
            + set_kelvin
        )

        payloadUi = " ".join("{:02x}".format(c) for c in payload)
        return payload


class LightState(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.color = payload["color"]
        self.reserved1 = payload["reserved1"]
        self.power_level = payload["power_level"]
        self.label = payload["label"]
        self.reserved2 = payload["reserved2"]
        super(LightState, self).__init__(
            MSG_IDS[LightState],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Color (HSBK)", self.color))
        self.payload_fields.append(("Reserved", self.reserved1))
        self.payload_fields.append(("Power Level", self.power_level))
        self.payload_fields.append(("Label", self.label))
        self.payload_fields.append(("Reserved", self.reserved2))
        color = b"".join(
            little_endian(bitstring.pack("uint:16", field)) for field in self.color
        )
        reserved1 = little_endian(bitstring.pack("int:16", self.reserved1))
        power_level = little_endian(bitstring.pack("uint:16", self.power_level))
        label = self.label.ljust(32, b"\0")
        reserved2 = little_endian(bitstring.pack("uint:64", self.reserved1))
        payload = color + reserved1 + power_level + label + reserved2
        return payload


class LightGetPower(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(LightGetPower, self).__init__(
            MSG_IDS[LightGetPower],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class LightSetPower(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.power_level = payload["power_level"]
        self.duration = payload["duration"]
        super(LightSetPower, self).__init__(
            MSG_IDS[LightSetPower],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        power_level = little_endian(bitstring.pack("uint:16", self.power_level))
        duration = little_endian(bitstring.pack("uint:32", self.duration))
        payload = power_level + duration
        return payload


class LightStatePower(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.power_level = payload["power_level"]
        super(LightStatePower, self).__init__(
            MSG_IDS[LightStatePower],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Power Level", self.power_level))
        power_level = little_endian(bitstring.pack("uint:16", self.power_level))
        payload = power_level
        return payload


##### INFRARED MESSAGES #####


class LightGetInfrared(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(LightGetInfrared, self).__init__(
            MSG_IDS[LightGetInfrared],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class LightStateInfrared(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.infrared_brightness = payload["infrared_brightness"]
        super(LightStateInfrared, self).__init__(
            MSG_IDS[LightStateInfrared],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Infrared Brightness", self.infrared_brightness))
        infrared_brightness = little_endian(
            bitstring.pack("uint:16", self.infrared_brightness)
        )
        payload = infrared_brightness
        return payload


class LightSetInfrared(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.infrared_brightness = payload["infrared_brightness"]
        super(LightSetInfrared, self).__init__(
            MSG_IDS[LightSetInfrared],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        infrared_brightness = little_endian(
            bitstring.pack("uint:16", self.infrared_brightness)
        )
        payload = infrared_brightness
        return payload


##### HEV (LIFX Clean) MESSAGES #####
# https://lan.developer.lifx.com/docs/hev-light-control
class GetHevCycle(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetHevCycle, self).__init__(
            MSG_IDS[GetHevCycle],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class SetHevCycle(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.enable = payload["enable"]
        self.duration = payload["duration"]
        super(SetHevCycle, self).__init__(
            MSG_IDS[SetHevCycle],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        enable = little_endian(bitstring.pack("uint:8", self.enable))
        duration = little_endian(bitstring.pack("uint:32", self.duration))
        payload = enable + duration
        return payload


class StateHevCycle(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.duration = payload["duration"]
        self.remaining = payload["remaining"]
        self.last_power = payload["last_power"]
        super(StateHevCycle, self).__init__(
            MSG_IDS[StateHevCycle],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        duration = little_endian(bitstring.pack("uint:32", self.duration))
        remaining = little_endian(bitstring.pack("uint:32", self.remaining))
        last_power = little_endian(bitstring.pack("uint:8", self.last_power))
        payload = duration + remaining + last_power
        return payload


class GetHevCycleConfiguration(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetHevCycleConfiguration, self).__init__(
            MSG_IDS[GetHevCycleConfiguration],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class SetHevCycleConfiguration(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.indication = payload["indication"]
        self.duration = payload["duration"]
        super(SetHevCycleConfiguration, self).__init__(
            MSG_IDS[SetHevCycleConfiguration],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        indication = little_endian(bitstring.pack("uint:8", self.indication))
        duration = little_endian(bitstring.pack("uint:32", self.duration))
        payload = indication + duration
        return payload


class StateHevCycleConfiguration(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.indication = payload["indication"]
        self.duration = payload["duration"]
        super(StateHevCycleConfiguration, self).__init__(
            MSG_IDS[StateHevCycleConfiguration],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        indication = little_endian(bitstring.pack("uint:8", self.indication))
        duration = little_endian(bitstring.pack("uint:32", self.duration))
        payload = indication + duration
        return payload


class GetLastHevCycleResult(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(GetLastHevCycleResult, self).__init__(
            MSG_IDS[GetLastHevCycleResult],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class StateLastHevCycleResult(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.result = payload["result"]
        super(StateLastHevCycleResult, self).__init__(
            MSG_IDS[StateLastHevCycleResult],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        result = little_endian(bitstring.pack("uint:8", self.result))
        return result

    @property
    def result_str(self):
        return LAST_HEV_CYCLE_RESULT.get(self.result, "UNKNOWN")


##### MULTIZONE MESSAGES #####


class MultiZoneStateMultiZone(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.count = payload["count"]
        self.index = payload["index"]
        self.color = payload["color"]
        super(MultiZoneStateMultiZone, self).__init__(
            MSG_IDS[MultiZoneStateMultiZone],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Count", self.count))
        self.payload_fields.append(("Index", self.index))
        self.payload_fields.append(("Color (HSBK)", self.color))
        count = little_endian(bitstring.pack("uint:8", self.count))
        index = little_endian(bitstring.pack("uint:8", self.index))
        payload = count + index
        for color in self.color:
            payload += b"".join(
                little_endian(bitstring.pack("uint:16", field)) for field in color
            )
        return payload


class MultiZoneStateZone(Message):  # 503
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.count = payload["count"]
        self.index = payload["index"]
        self.color = payload["color"]
        super(MultiZoneStateZone, self).__init__(
            MSG_IDS[MultiZoneStateZone],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Count", self.count))
        self.payload_fields.append(("Index", self.index))
        self.payload_fields.append(("Color (HSBK)", self.color))
        count = little_endian(bitstring.pack("uint:8", self.count))
        index = little_endian(bitstring.pack("uint:8", self.index))
        color = b"".join(
            little_endian(bitstring.pack("uint:16", field)) for field in self.color
        )
        payload = count + index + color
        return payload


class MultiZoneSetColorZones(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.start_index = payload["start_index"]
        self.end_index = payload["end_index"]
        self.color = payload["color"]
        self.duration = payload["duration"]
        self.apply = payload["apply"]
        super(MultiZoneSetColorZones, self).__init__(
            MSG_IDS[MultiZoneSetColorZones],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        start_index = little_endian(bitstring.pack("uint:8", self.start_index))
        end_index = little_endian(bitstring.pack("uint:8", self.end_index))
        color = b"".join(
            little_endian(bitstring.pack("uint:16", field)) for field in self.color
        )
        duration = little_endian(bitstring.pack("uint:32", self.duration))
        apply = little_endian(bitstring.pack("uint:8", self.apply))
        payload = start_index + end_index + color + duration + apply
        return payload


class MultiZoneGetColorZones(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.start_index = payload["start_index"]
        self.end_index = payload["end_index"]
        super(MultiZoneGetColorZones, self).__init__(
            MSG_IDS[MultiZoneGetColorZones],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        start_index = little_endian(bitstring.pack("uint:8", self.start_index))
        end_index = little_endian(bitstring.pack("uint:8", self.end_index))
        payload = start_index + end_index
        return payload


class MultiZoneGetMultiZoneEffect(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(MultiZoneGetMultiZoneEffect, self).__init__(
            MSG_IDS[MultiZoneGetMultiZoneEffect],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class MultiZoneSetMultiZoneEffect(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.instanceid = random.randrange(1, 1 << 32)
        self.type = payload["type"]
        self.speed = payload["speed"]
        self.duration = payload["duration"]
        self.direction = payload["direction"]
        super(MultiZoneSetMultiZoneEffect, self).__init__(
            MSG_IDS[MultiZoneSetMultiZoneEffect],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        instanceid = little_endian(bitstring.pack("uint:32", self.instanceid))
        type = little_endian(bitstring.pack("uint:8", self.type))
        reserved6 = little_endian(bitstring.pack("int:16", 2))
        speed = little_endian(bitstring.pack("uint:32", self.speed))
        duration = little_endian(bitstring.pack("uint:64", self.duration))
        reserved7 = little_endian(bitstring.pack("int:32", 4))
        reserved8 = little_endian(bitstring.pack("int:32", 4))
        parameter1 = little_endian(bitstring.pack("uint:32", 4))
        direction = little_endian(bitstring.pack("uint:32", self.direction))
        parameter3 = little_endian(bitstring.pack("uint:32", 4))

        payload = (
            instanceid
            + type
            + reserved6
            + speed
            + duration
            + reserved7
            + reserved8
            + parameter1
            + direction
            + parameter3 * 6
        )
        return payload


class MultiZoneStateMultiZoneEffect(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.instanceid = payload["instanceid"]
        self.effect = payload["effect"]
        self.speed = payload["speed"]
        self.duration = payload["duration"]
        self.direction = payload["direction"]

        super(MultiZoneStateMultiZoneEffect, self).__init__(
            MSG_IDS[MultiZoneStateMultiZoneEffect],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append("Instance ID", self.instanceid)
        self.payload_fields.append("Effect", self.effect)
        self.payload_fields.append("Speed", self.speed)
        self.payload_fields.append("Duration", self.duration)
        self.payload_fields.append("Direction", self.direction)
        instanceid = little_endian(bitstring.pack("uint:32", self.instanceid))
        effect = little_endian(bitstring.pack("uint:8", self.effect))
        speed = little_endian(bitstring.pack("uint:32", self.speed))
        duration = little_endian(bitstring.pack("uint:64", self.duration))
        parameter1 = b"".join(little_endian(bitstring.pack("uint:8", 8)))
        direction = b"".join(
            little_endian(bitstring.pack("uint:8", c)) for c in self.direction
        )
        direction_padding = b"".join(
            little_endian(bitstring.pack("uint:8", 0))
            for i in range(8 - len(self.direction))
        )
        direction += direction_padding
        parameter3 = b"".join(little_endian(bitstring.pack("uint:8", 8)))
        parameter4 = b"".join(little_endian(bitstring.pack("uint:8", 8)))
        payload = (
            instanceid
            + effect
            + speed
            + duration
            + parameter1
            + direction
            + parameter3
            + parameter4
        )

        return payload

    @property
    def effect_str(self):
        return MultiZoneEffectType(self.effect).name.upper()

    @property
    def direction_str(self):
        return MultiZoneDirection(self.direction).name.lower()


class MultiZoneSetExtendedColorZones(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.duration = payload["duration"]
        self.apply = payload["apply"]
        self.zone_index = payload["zone_index"]
        self.colors_count = payload["colors_count"]
        self.colors = payload["colors"]
        super(MultiZoneSetExtendedColorZones, self).__init__(
            MSG_IDS[MultiZoneSetExtendedColorZones],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        duration = little_endian(bitstring.pack("uint:32", self.duration))
        apply = little_endian(bitstring.pack("uint:8", self.apply))
        zone_index = little_endian(bitstring.pack("uint:16", self.zone_index))
        colors_count = little_endian(bitstring.pack("uint:8", self.colors_count))
        payload = duration + apply + zone_index + colors_count
        for color in self.colors:
            payload += b"".join(
                little_endian(bitstring.pack("uint:16", field)) for field in color
            )
        return payload


class MultiZoneGetExtendedColorZones(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(MultiZoneGetExtendedColorZones, self).__init__(
            MSG_IDS[MultiZoneGetExtendedColorZones],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class MultiZoneStateExtendedColorZones(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.zones_count = payload["zones_count"]
        self.zone_index = payload["zone_index"]
        self.colors_count = payload["colors_count"]
        self.colors = payload["colors"]
        super(MultiZoneStateExtendedColorZones, self).__init__(
            MSG_IDS[MultiZoneStateExtendedColorZones],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append(("Zones Count", self.zones_count))
        self.payload_fields.append(("Zone Index", self.zone_index))
        self.payload_fields.append(("Colors count", self.colors_count))
        self.payload_fields.append(("Colors", self.colors))
        zones_count = little_endian(bitstring.pack("uint:16", self.zones_count))
        zone_index = little_endian(bitstring.pack("uint:16", self.zone_index))
        colors_count = little_endian(bitstring.pack("uint:8", self.colors_count))
        payload = zones_count + zone_index + colors_count
        for color in self.colors:
            payload += b"".join(
                little_endian(bitstring.pack("uint:16", field)) for field in color
            )
        return payload


class TileGetTileEffect(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload={},
        ack_requested=False,
        response_requested=False,
    ):
        super(TileGetTileEffect, self).__init__(
            MSG_IDS[TileGetTileEffect],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )


class TileSetTileEffect(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.instanceid = random.randrange(1, 1 << 32)
        self.type = payload["type"]
        self.speed = payload["speed"]
        self.duration = payload["duration"]
        self.palette_count = payload["palette_count"]
        self.palette = payload["palette"]
        super(TileSetTileEffect, self).__init__(
            MSG_IDS[TileSetTileEffect],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        reserved8 = little_endian(bitstring.pack("int:8", 0))
        reserved9 = little_endian(bitstring.pack("int:8", 0))
        instanceid = little_endian(bitstring.pack("uint:32", self.instanceid))
        type = little_endian(bitstring.pack("uint:8", self.type))
        speed = little_endian(bitstring.pack("uint:32", self.speed))
        duration = little_endian(bitstring.pack("uint:64", self.duration))
        reserved6 = little_endian(bitstring.pack("int:32", 0))
        reserved7 = little_endian(bitstring.pack("int:32", 0))
        parameters = little_endian(bitstring.pack("int:32", 0))
        palette_count = little_endian(bitstring.pack("uint:8", self.palette_count))
        payload = (
            reserved8
            + reserved9
            + instanceid
            + type
            + speed
            + duration
            + reserved6
            + reserved7
            + parameters * 8
            + palette_count
        )
        for color in self.palette:
            payload += b"".join(
                little_endian(bitstring.pack("uint:16", field)) for field in color
            )
        return payload


class TileStateTileEffect(Message):
    def __init__(
        self,
        target_addr,
        source_id,
        seq_num,
        payload,
        ack_requested=False,
        response_requested=False,
    ):
        self.instanceid = payload["instanceid"]
        self.effect = payload["effect"]
        self.speed = payload["speed"]
        self.duration = payload["duration"]
        self.palette_count = payload["palette_count"]
        self.palette = payload["palette"]
        super(TileStateTileEffect, self).__init__(
            MSG_IDS[TileStateTileEffect],
            target_addr,
            source_id,
            seq_num,
            ack_requested,
            response_requested,
        )

    def get_payload(self):
        self.payload_fields.append("Instance ID", self.instanceid)
        self.payload_fields.append("Effect", self.effect)
        self.payload_fields.append("Speed", self.speed)
        self.payload_fields.append("Duration", self.duration)
        self.payload_fields.append("Palette Count", self.palette_count)
        self.payload_fields.append("Palette", self.palette)
        instanceid = little_endian(bitstring.pack("uint:32", self.instanceid))
        effect = little_endian(bitstring.pack("uint:8", self.effect))
        speed = little_endian(bitstring.pack("uint:32", self.speed))
        duration = little_endian(bitstring.pack("uint:64", self.duration))
        palette_count = little_endian(bitstring.pack("uint:8", self.palette_count))
        payload = instanceid + effect + speed + duration + palette_count
        for color in self.palette:
            payload += b"".join(
                little_endian(bitstring.pack("uint:16", field)) for field in color
            )
        return payload


MSG_IDS = {
    GetService: 2,
    StateService: 3,
    GetHostInfo: 12,
    StateHostInfo: 13,
    GetHostFirmware: 14,
    StateHostFirmware: 15,
    GetWifiInfo: 16,
    StateWifiInfo: 17,
    GetWifiFirmware: 18,
    StateWifiFirmware: 19,
    GetPower: 20,
    SetPower: 21,
    StatePower: 22,
    GetLabel: 23,
    SetLabel: 24,
    StateLabel: 25,
    GetVersion: 32,
    StateVersion: 33,
    GetInfo: 34,
    StateInfo: 35,
    SetReboot: 38,
    Acknowledgement: 45,
    GetLocation: 48,
    StateLocation: 50,
    GetGroup: 51,
    StateGroup: 53,
    EchoRequest: 58,
    EchoResponse: 59,
    LightGet: 101,
    LightSetColor: 102,
    LightSetWaveform: 103,
    LightState: 107,
    LightGetPower: 116,
    LightSetPower: 117,
    LightStatePower: 118,
    LightSetWaveformOptional: 119,
    LightGetInfrared: 120,
    LightStateInfrared: 121,
    LightSetInfrared: 122,
    GetHevCycle: 142,
    SetHevCycle: 143,
    StateHevCycle: 144,
    GetHevCycleConfiguration: 145,
    SetHevCycleConfiguration: 146,
    StateHevCycleConfiguration: 147,
    GetLastHevCycleResult: 148,
    StateLastHevCycleResult: 149,
    MultiZoneSetColorZones: 501,
    MultiZoneGetColorZones: 502,
    MultiZoneStateZone: 503,
    MultiZoneStateMultiZone: 506,
    MultiZoneGetMultiZoneEffect: 507,
    MultiZoneSetMultiZoneEffect: 508,
    MultiZoneStateMultiZoneEffect: 509,
    MultiZoneSetExtendedColorZones: 510,
    MultiZoneGetExtendedColorZones: 511,
    MultiZoneStateExtendedColorZones: 512,
    TileGetTileEffect: 718,
    TileSetTileEffect: 719,
    TileStateTileEffect: 720,
}

SERVICE_IDS = {1: "UDP", 2: "reserved", 3: "reserved", 4: "reserved"}

STR_MAP = {65535: "On", 0: "Off", None: "Unknown"}

ZONE_MAP = {0: "NO_APPLY", 1: "APPLY", 2: "APPLY_ONLY"}

LAST_HEV_CYCLE_RESULT = {
    0: "SUCCESS",
    1: "BUSY",
    2: "INTERRUPTED_BY_RESET",
    3: "INTERRUPTED_BY_HOMEKIT",
    4: "INTERRUPTED_BY_LAN",
    5: "INTERRUPTED_BY_CLOUD",
    255: "NONE",
}


class MultiZoneEffectType(Enum):
    OFF = 0
    MOVE = 1
    RESERVED1 = 2
    RESERVED2 = 3


class MultiZoneDirection(Enum):
    RIGHT = 0
    LEFT = 1
    BACKWARD = 0
    FORWARD = 1


class TileEffectType(Enum):
    OFF = 0
    RESERVED1 = 1
    MORPH = 2
    FLAME = 3
    RESERVED2 = 4


def str_map(key):
    string_representation = "Unknown"
    if key == None:
        string_representation = "Unknown"
    elif type(key) == type(0):
        if key > 0 and key <= 65535:
            string_representation = "On"
        elif key == 0:
            string_representation = "Off"
    return string_representation
