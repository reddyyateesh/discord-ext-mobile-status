import logging

from discord.gateway import DiscordWebSocket

from .core import SimulatedMobileWebSocket

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


def init():
    _log.info("Initializing mobile status")
    DiscordWebSocket.identify = SimulatedMobileWebSocket.identify
