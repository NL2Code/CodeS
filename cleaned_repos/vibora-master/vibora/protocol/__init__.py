from . import cprotocol
from .definitions import *

locals()["Connection"] = cprotocol.Connection
locals()["update_current_time"] = cprotocol.update_current_time
