# Falcon Python Examples

Error tracking examples for Python applications.

## Examples

| Example | Description |
|:--------|:------------|
| [fastapi-basic](./fastapi-basic) | FastAPI integration |
| [flask-basic](./flask-basic) | Flask integration |

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

## Flask Integration

```python
from flask import Flask
from roselabs_falcon.integrations.flask import init_falcon

app = Flask(__name__)
init_falcon(app, api_key="sk_falcon_...", app_name="my-app")

@app.route("/")
def hello():
    return "Hello World"
```

## Links

- [Full Documentation](https://docs.roselabs.io/falcon/python)
- [API Reference](https://docs.roselabs.io/falcon/api)
- [PyPI Package](https://pypi.org/project/roselabs-falcon/)
