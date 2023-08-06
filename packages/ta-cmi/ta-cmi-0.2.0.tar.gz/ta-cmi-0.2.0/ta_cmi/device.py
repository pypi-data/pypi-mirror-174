from typing import Dict, Any, List

from aiohttp import ClientSession

from .baseApi import BaseAPI
from .channel import Channel

from .const import DEVICES, ReadOnlyClass, ChannelMode


class Device(BaseAPI, metaclass=ReadOnlyClass):
    """Class to interact with a device"""

    def __init__(self, node_id: str, host: str, username: str, password: str, session: ClientSession = None):
        """Initialize."""
        super().__init__(username, password, session)
        self.id: str = node_id
        self.host: str = host

        self.apiVersion: int = 0
        self.deviceType: str = "00"

        self.inputs: Dict[int, Channel] = {}
        self.outputs: Dict[int, Channel] = {}
        self.analog_logging: Dict[int, Channel] = {}
        self.digital_logging: Dict[int, Channel] = {}

    def _extract_device_info(self, json: Dict[str, Any]):
        """Extract device info from request response."""
        self.apiVersion: int = json["Header"]["Version"]
        self.deviceType: str = json["Header"]["Device"]

    @staticmethod
    def _extract_channels(mode: ChannelMode, raw_channels: List[Dict[str, Any]]) -> Dict[int, Channel]:
        """Extract channel info from data array from request."""
        list_of_channels: Dict[int, Channel] = {}
        for channel_raw in raw_channels:
            ch: Channel = Channel(mode, channel_raw)
            list_of_channels[ch.index] = ch

        return list_of_channels

    def _get_json_params(self):
        params = "I,O"

        if self.getDeviceType().endswith("x2"):
            params += ",La,Ld"

        return params

    async def update(self):
        """Update data."""
        url: str = f"{self.host}/INCLUDE/api.cgi?jsonparam={self._get_json_params()}&jsonnode={self.id}"
        res: Dict[str, Any] = await self._make_request(url)

        self._extract_device_info(res)
        if "Inputs" in res["Data"]:
            self.inputs: Dict[int, Channel] = self._extract_channels(ChannelMode.INPUT, res["Data"]["Inputs"])
        if "Outputs" in res["Data"]:
            self.outputs: Dict[int, Channel] = self._extract_channels(ChannelMode.OUTPUT, res["Data"]["Outputs"])
        if "Logging Analog" in res["Data"]:
            self.analog_logging: Dict[int, Channel] = self._extract_channels(ChannelMode.ANALOG_LOGGING,
                                                                             res["Data"]["Logging Analog"])
        if "Logging Digital" in res["Data"]:
            self.digital_logging: Dict[int, Channel] = self._extract_channels(ChannelMode.DIGITAL_LOGGING,
                                                                              res["Data"]["Logging Digital"])

    def set_device_type(self, device_name: str):
        type_id = [i for i in DEVICES if DEVICES[i] == device_name]

        if len(type_id) != 1:
            raise InvalidDeviceError(f"Invalid device name: {device_name}")

        self.deviceType = type_id[0]

    def getDeviceType(self) -> str:
        return DEVICES.get(self.deviceType, "Unknown")

    def __repr__(self) -> str:
        return f"Node {self.id}: Type: {self.getDeviceType()}, Inputs: {len(self.inputs)}, " \
               f"Outputs: {len(self.outputs)}, Analog Logging: {len(self.analog_logging)}, " \
               f"Digital Logging: {len(self.digital_logging)} "


class InvalidDeviceError(Exception):
    """Triggered when an invalid device type is set."""

    def __init__(self, status: str):
        """Initialize."""
        super().__init__(status)
        self.status = status
