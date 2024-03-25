import asyncio

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass
from .request import Request
from .responses import *
from .server import *
from .tests import *
