from abc import ABC, abstractmethod

from aiohttp import ClientSession

from linkplay.utils import session_call_api, session_call_api_json, session_call_api_ok


class LinkPlayEndpoint(ABC):
    """Represents an abstract LinkPlay endpoint."""

    @abstractmethod
    async def request(self, command: str) -> None:
        """Performs a request on the given command and verifies the result."""

    @abstractmethod
    async def json_request(self, command: str) -> dict[str, str]:
        """Performs a request on the given command and returns the result as a JSON object."""

    @abstractmethod
    async def raw_request(self, command: str, timeout: int | None) -> str:
        """Performs a request and returns a raw, strinigified response"""


class LinkPlayApiEndpoint(LinkPlayEndpoint):
    """Represents a LinkPlay HTTP API endpoint."""

    def __init__(self, *, protocol: str, endpoint: str, session: ClientSession):
        assert protocol in [
            "http",
            "https",
        ], "Protocol must be either 'http' or 'https'"
        self._endpoint: str = f"{protocol}://{endpoint}"
        self._session: ClientSession = session

    async def request(self, command: str) -> None:
        """Performs a GET request on the given command and verifies the result."""
        await session_call_api_ok(self._endpoint, self._session, command)

    async def json_request(self, command: str) -> dict[str, str]:
        """Performs a GET request on the given command and returns the result as a JSON object."""
        return await session_call_api_json(self._endpoint, self._session, command)
    
    async def raw_request(self, command: str, timeout: int | None) -> str:
        """Performs a GET request on the given command and returns the result as is."""
        return await session_call_api(self._endpoint, self._session, command, timeout)


    def __str__(self) -> str:
        return self._endpoint
