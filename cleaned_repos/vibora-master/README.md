
# Vibora is a **fast, asynchronous and elegant** Python 3.6+ http client/server framework.

> Before you ask, Vibora means Viper in Portuguese :)


Server Features
---------------
* Performance.
* Schemas Engine.
* Nested Blueprints / Domain Based Routes / Components
* Connection Reaper / Self-Healing Workers
* Sessions Engine
* Streaming
* Websockets
* Caching tools
* Async Template Engine (hot-reloading, deep inheritance)
* Complete flow customization
* Static Files (Smart Cache, Range, LastModified, ETags)
* Testing Framework
* Type hints, type hints, type hints everywhere.


Client Features
---------------
* Streaming MultipartForms
* Rate Limiting / Retries mechanisms
* Websockets
* Keep-Alive & Connection Pooling
* Sessions with cookies persistence
* Basic/digest Authentication
* Transparent Content Decoding

## Server Example
--------------
```python
from vibora import Vibora, Request
from vibora.responses import JsonResponse

app = Vibora()


@app.route('/')
async def home(request: Request):
    return JsonResponse({'hello': 'world'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
```

Client Example
--------------

```python
import asyncio
from vibora import client


async def hello_world():
    response = await client.get('https://google.com/')
    print(f'Content: {response.content}')
    print(f'Status code: {response.status_code}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hello_world())
```