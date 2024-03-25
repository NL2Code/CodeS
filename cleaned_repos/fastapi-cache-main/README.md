# fastapi-cache

## Introduction

`fastapi-cache` is a tool to cache FastAPI endpoint and function results, with
backends supporting Redis, Memcached, and Amazon DynamoDB.

## Features

- Supports `redis`, `memcache`, `dynamodb`, and `in-memory` backends.
- Easy integration with [FastAPI](https://fastapi.tiangolo.com/).
- Support for HTTP cache headers like `ETag` and `Cache-Control`, as well as conditional `If-Match-None` requests.

## Usage

### Quick Start

```python
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

app = FastAPI()


@cache()
async def get_cache():
    return 1


@app.get("/")
@cache(expire=60)
async def index():
    return dict(hello="world")


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

```