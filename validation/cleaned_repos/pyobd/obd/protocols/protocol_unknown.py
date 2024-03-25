from .protocol import *


class UnknownProtocol(Protocol):
    """
    Class representing an unknown protocol.

    Used for when a connection to the ELM has
    been made, but the car hasn't responded.
    """

    def parse_frame(self, frame):
        return True  # pass everything

    def parse_message(self, message):
        return True  # pass everything
