from . import retries as retries_module
from .response import Response
from .session import Session


async def get(
    url: str = "",
    stream: bool = False,
    follow_redirects: bool = True,
    max_redirects: int = 30,
    decode: bool = True,
    ssl=None,
    timeout=None,
    retries: retries_module.RetryStrategy = None,
    headers: dict = None,
    query: dict = None,
    ignore_prefix: bool = False,
) -> Response:
    return await Session(keep_alive=False).request(
        url=url,
        stream=stream,
        follow_redirects=follow_redirects,
        max_redirects=max_redirects,
        decode=decode,
        ssl=ssl,
        retries=retries,
        headers=headers,
        timeout=timeout,
        method="GET",
        query=query,
        ignore_prefix=ignore_prefix,
    )


async def post(
    url: str = "",
    stream: bool = False,
    follow_redirects: bool = True,
    max_redirects: int = 30,
    decode: bool = True,
    validate_ssl=None,
    timeout=None,
    retries: retries_module.RetryStrategy = None,
    headers: dict = None,
    query: dict = None,
    body=None,
    form=None,
    json=None,
    ignore_prefix: bool = False,
) -> Response:
    return await Session(keep_alive=False).request(
        url=url,
        stream=stream,
        follow_redirects=follow_redirects,
        max_redirects=max_redirects,
        decode=decode,
        ssl=validate_ssl,
        retries=retries,
        headers=headers,
        timeout=timeout,
        method="POST",
        query=query,
        ignore_prefix=ignore_prefix,
        body=body,
        form=form,
        json=json,
    )
