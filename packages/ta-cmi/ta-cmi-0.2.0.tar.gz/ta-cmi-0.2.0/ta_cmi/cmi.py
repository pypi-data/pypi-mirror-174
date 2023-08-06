from typing import List

from aiohttp import ClientSession

from .baseApi import BaseAPI
from .device import Device, ReadOnlyClass


class CMI(BaseAPI, metaclass=ReadOnlyClass):
    """Main class to interact with CMI"""

    def __init__(self, host: str, username: str, password: str, session: ClientSession = None):
        """Initialize."""
        super().__init__(username, password, session)
        self.host = host
        self.username = username
        self.password = password

    async def getDevices(self) -> List[Device]:
        """List connected devices."""
        url: str = f"{self.host}/INCLUDE/can_nodes.cgi?_=1"
        data: str = await self._make_request_no_json(url)

        node_ids: List[str] = data.split(";")

        devices: List[Device] = []

        for node_id in node_ids:
            if len(node_id) == 0:
                continue
            devices.append(Device(node_id, self.host, self.username, self.password, self.session))

        return devices
