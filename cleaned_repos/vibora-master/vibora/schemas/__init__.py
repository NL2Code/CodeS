from .extensions import fields
from .extensions.schemas import Schema as CythonSchema
from .schemas import *

locals()["Schema"] = CythonSchema
