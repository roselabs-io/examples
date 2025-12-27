# Falcon Python SDK

Error tracking for Python applications.

## Examples

| Example | Description |
|:--------|:------------|
| [fastapi-basic](./fastapi-basic) | FastAPI integration |

## Installation

```bash
pip install roselabs-falcon
```

## Quick Start

```python
from roselabs_falcon import Falcon

falcon = Falcon(
    api_key="sk_falcon_...",
    app_name="my-app",
    environment="production",
)

# Capture exceptions
try:
    risky_operation()
except Exception as e:
    falcon.capture_exception(e)

# Or capture messages
falcon.capture_message("User signed up", level="info")
```

## FastAPI Integration

```python
from fastapi import FastAPI
from roselabs_falcon.integrations.fastapi import FalconMiddleware

app = FastAPI()
app.add_middleware(FalconMiddleware, api_key="sk_falcon_...", app_name="my-api")

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## Links

- [Falcon Dashboard](https://falcon.roselabs.io)
- [PyPI Package](https://pypi.org/project/roselabs-falcon/)
