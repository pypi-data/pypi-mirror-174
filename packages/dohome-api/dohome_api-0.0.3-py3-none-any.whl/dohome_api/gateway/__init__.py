"""DoHome Gateway"""
from ..constants import API_PORT
from ..datagram import open_broadcast
from ..light import DoHomeLight
from ..commands import (
    REQUEST_PING,
    CMD_GET_IP,
    format_request,
    parse_response
)
from .util import (
    get_discovery_host,
    parse_pong,
)

class DoHomeGateway:
    """DoHome gateway controller"""

    _host = ''
    _broadcast = None

    def __init__(self, host: str = None):
        self._host = host if host is not None else get_discovery_host()
        self._broadcast = None

    async def add_light(self, sid: str) -> DoHomeLight:
        """Creates new light by sid"""
        host = await self.discover_ip(sid)
        return DoHomeLight(sid, host)

    async def discover_ip(self, sid: str) -> str:
        """Discovers DoHome light IP"""
        responses = await self._request(
            format_request([sid], CMD_GET_IP)
        )
        if len(responses) != 1:
            raise IOError
        parts = responses[0].decode("utf-8").split('"')
        return parts[len(parts) - 2]

    async def discover_lights(self, timeout=3.0):
        """Discovers DoHome lights"""
        responses = await self._request(REQUEST_PING, timeout)
        descriptions = []
        for response in responses:
            message = response.decode("utf-8")
            if message.startswith('cmd=pong'):
                descriptions.append(parse_pong(message))
        return descriptions

    async def _request(self, req: str, timeout=0.2) -> list:
        if self._broadcast is None or self._broadcast.closed:
            await self._connect()
        self._broadcast.send(req.encode())
        return await self._broadcast.receive(timeout)

    async def _connect(self):
        self._broadcast = await open_broadcast((self._host, API_PORT))
