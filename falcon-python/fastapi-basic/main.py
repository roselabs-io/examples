"""
Falcon + FastAPI Basic Example

This example shows how to integrate Falcon error tracking
into a FastAPI application.

Run with: FALCON_API_KEY=sk_falcon_... uvicorn main:app --reload
"""

import os
from fastapi import FastAPI, HTTPException
from roselabs_falcon import Falcon
from roselabs_falcon.integrations.fastapi import FalconMiddleware

# Initialize FastAPI
app = FastAPI(
    title="Falcon FastAPI Example",
    description="Example showing Falcon error tracking integration",
)

# Add Falcon middleware
app.add_middleware(
    FalconMiddleware,
    api_key=os.environ.get("FALCON_API_KEY"),
    app_name="fastapi-basic-example",
    environment=os.environ.get("ENVIRONMENT", "development"),
    debug=True,  # Enable debug logging (disable in production)
)

# Get Falcon instance for manual captures
falcon = Falcon.get_instance()


# =============================================================================
# Routes
# =============================================================================


@app.get("/")
async def root():
    """Home route with available endpoints."""
    return {
        "message": "Falcon FastAPI Example",
        "endpoints": {
            "/": "This message",
            "/error": "Triggers an unhandled error (captured by Falcon)",
            "/manual-error": "Manually captures an error",
            "/async-error": "Triggers an async error",
            "/http-error": "Triggers an HTTP exception",
        },
    }


@app.get("/error")
async def trigger_error():
    """Unhandled error - automatically captured by Falcon."""
    raise ValueError("This is a test error!")


@app.get("/manual-error")
async def manual_error():
    """Manual error capture with additional context."""
    try:
        # Simulate some operation that might fail
        result = 1 / 0
    except ZeroDivisionError as e:
        # Manually capture the error with additional context
        falcon.capture_exception(
            e,
            tags={"feature": "calculation"},
            extra={"operation": "division", "numerator": 1, "denominator": 0},
        )
        raise HTTPException(status_code=400, detail="Division by zero")

    return {"result": result}


@app.get("/async-error")
async def async_error():
    """Async error - automatically captured."""
    import asyncio

    await asyncio.sleep(0.1)
    raise RuntimeError("Async error after delay!")


@app.get("/http-error")
async def http_error():
    """HTTP exception with Falcon context."""
    # Set user context
    falcon.set_user({"id": "user-123", "email": "test@example.com"})

    raise HTTPException(status_code=404, detail="Resource not found")


@app.post("/checkout")
async def checkout(user_id: str = None, cart_id: str = None):
    """Endpoint with user context attached to errors."""
    # Add context that will be attached to any errors
    falcon.set_context(
        user={"id": user_id},
        tags={"flow": "checkout"},
        extra={"cart_id": cart_id},
    )

    # Simulate a checkout error
    raise Exception("Payment processing failed")


# =============================================================================
# Startup
# =============================================================================


@app.on_event("startup")
async def startup():
    api_key = os.environ.get("FALCON_API_KEY")
    print(
        f"""
🦅 Falcon FastAPI Example Running!

API Key:    {'✓ Set' if api_key else '✗ Missing (set FALCON_API_KEY)'}

Try these endpoints:
  curl http://localhost:8000/
  curl http://localhost:8000/error
  curl http://localhost:8000/manual-error
  curl http://localhost:8000/async-error
  curl -X POST "http://localhost:8000/checkout?user_id=123&cart_id=abc"
"""
    )
