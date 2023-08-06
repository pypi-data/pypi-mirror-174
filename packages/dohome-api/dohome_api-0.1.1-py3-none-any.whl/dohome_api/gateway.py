"""DoHome Gateway"""
from typing import Final, Tuple
from .commands import (
    CMD_GET_IP,
    format_request,
)
from .transport import DoHomeBroadcastTransport
from .light import DoHomeLight

REQUEST_PING: Final[str] = 'cmd=ping\r\n'

def parse_pong(message: str) -> dict:
    """Parses DoHome pong response"""
    records = list(map(lambda x: x.split('='), message.split('&')))
    descr = {
        record[0]: record[1].strip() for record in records
    }
    name = descr["device_name"]
    descr["sid"] = name[len(name) - 4:]
    return descr

class DoHomeGateway:
    """DoHome gateway controller"""

    _broadcast: DoHomeBroadcastTransport = None

    def __init__(self, broadcast: DoHomeBroadcastTransport):
        self._broadcast = broadcast

    async def add_light(self, sid: str) -> DoHomeLight:
        """Creates new light by sid"""
        host = await self.discover_ip(sid)
        return DoHomeLight(sid, host)

    async def discover_ip(self, sid: str) -> str:
        """Discovers DoHome light IP"""
        responses = await self._broadcast.send_request(
            format_request([sid], CMD_GET_IP)
        )
        if len(responses) != 1:
            raise Exception("Not found")
        parts = responses[0].decode("utf-8").split('"')
        return parts[len(parts) - 2]

    async def discover_devices(self, timeout=3.0):
        """Discovers DoHome devices"""
        responses = await self._broadcast.send_request(REQUEST_PING, timeout)
        descriptions = []
        for response in responses:
            if response.startswith('cmd=pong'):
                descriptions.append(parse_pong(response))
        return descriptions

def create_gateway(host: str=None) -> Tuple[DoHomeGateway, DoHomeBroadcastTransport]:
    """Creates DoHome gateway"""
    broadcast = DoHomeBroadcastTransport(host)
    gateway = DoHomeGateway(broadcast)
    return (gateway, broadcast)
