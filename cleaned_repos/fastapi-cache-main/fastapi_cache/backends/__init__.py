from fastapi_cache.backends import inmemory
from fastapi_cache.types import Backend

__all__ = ["Backend", "inmemory"]

try:
    from fastapi_cache.backends import dynamodb
except ImportError:
    pass
else:
    __all__ += ["dynamodb"]

try:
    from fastapi_cache.backends import memcached
except ImportError:
    pass
else:
    __all__ += ["memcached"]

try:
    from fastapi_cache.backends import redis
except ImportError:
    pass
else:
    __all__ += ["redis"]
