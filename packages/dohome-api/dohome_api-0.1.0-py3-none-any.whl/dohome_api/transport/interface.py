"""DoHome transport interface"""

class DoHomeApiTransport:
    """DoHome API transport interface"""

    @property
    def connected(self):
        """Indicates whether the transport is connected."""

    async def send_request(self, request: str) -> list[str]:
        """Sends request to DoHome device"""
