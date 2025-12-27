# Falcon + FastAPI Basic Example

Error tracking integration with FastAPI.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
FALCON_API_KEY=sk_falcon_... uvicorn main:app --reload
```

## Test Endpoints

```bash
# Home (shows available endpoints)
curl http://localhost:8000/

# Trigger an unhandled error
curl http://localhost:8000/error

# Manual error capture
curl http://localhost:8000/manual-error

# Async error
curl http://localhost:8000/async-error

# Error with user context
curl -X POST "http://localhost:8000/checkout?user_id=123&cart_id=abc"
```

## Interactive Docs

FastAPI provides automatic API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## What This Example Shows

1. **Middleware integration** - `FalconMiddleware` captures all unhandled exceptions
2. **Manual capture** - Use `falcon.capture_exception()` for handled errors
3. **User context** - Use `falcon.set_user()` to attach user info
4. **Custom context** - Use `falcon.set_context()` for additional metadata
5. **Async support** - Works with async/await

## Next Steps

- View errors in your [Falcon Dashboard](https://falcon.roselabs.io)
- Configure alerts for critical errors
- Add source maps for better stack traces
