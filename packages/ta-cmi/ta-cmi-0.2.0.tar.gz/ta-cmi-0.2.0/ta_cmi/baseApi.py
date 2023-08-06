import json
from typing import Any, Dict

from aiohttp import BasicAuth, ClientSession, ClientConnectionError

from .const import HTTP_OK, HTTP_UNAUTHORIZED


class BaseAPI:
    """Class to perform CMI API requests"""

    def __init__(self,
                 username: str,
                 password: str,
                 session: ClientSession = None
                 ):
        """Initialize."""
        self.auth = BasicAuth(username, password)
        self.session = session

    async def _make_request(self, url: str) -> Dict[str, Any]:
        """Retrieve data from CMI API."""
        raw_response: str = await self._make_request_no_json(url)
        data = json.loads(raw_response)

        STATUS_CODE = "Status code"

        if data[STATUS_CODE] == 0:
            return data
        elif data[STATUS_CODE] == 1:
            raise ApiError("Node not available")
        elif data[STATUS_CODE] == 2:
            raise ApiError("Failure during the CAN-request/parameter not available for this device")
        elif data[STATUS_CODE] == 4:
            raise RateLimitError("Only one request per minute is permitted")
        elif data[STATUS_CODE] == 5:
            raise ApiError("Device not supported")
        elif data[STATUS_CODE] == 7:
            raise ApiError("CAN Bus is busy")
        else:
            raise ApiError("Unknown error")

    async def _make_request_no_json(self, url: str) -> str:
        """Retrieve data from CMI API that is not valid json."""
        internal_session: bool = False
        if self.session is None:
            internal_session = True
            self.session = ClientSession()

        try:
            async with self.session.get(url, auth=self.auth) as res:
                if res.status == HTTP_UNAUTHORIZED:
                    raise InvalidCredentialsError("Invalid API key")
                elif res.status != HTTP_OK:
                    raise ApiError(f"Invalid response from CMI: {res.status}")

                text = await res.text()
                if internal_session:
                    await self.session.close()
                    self.session = None
                return text
        except ClientConnectionError:
            if internal_session:
                await self.session.close()
                self.session = None
            raise ApiError(f"Could not connect to C.M.I")

    @staticmethod
    def _is_json(to_test: str) -> bool:
        """Test if string is valid json."""
        try:
            json.loads(to_test)
        except ValueError:
            return False
        return True


class ApiError(Exception):
    """Raised when API request ended in error."""

    def __init__(self, status: str):
        """Initialize."""
        super().__init__(status)
        self.status = status


class InvalidCredentialsError(Exception):
    """Triggered when the credentials are invalid."""

    def __init__(self, status: str):
        """Initialize."""
        super().__init__(status)
        self.status = status


class RateLimitError(Exception):
    """Triggered when the rate limit is reached."""

    def __init__(self, status: str):
        """Initialize."""
        super().__init__(status)
        self.status = status
