# Falcon Python SDK

Error tracking and uptime monitoring for Python applications.

## Examples

| Example | Description |
|:--------|:------------|
| [fastapi-basic](./fastapi-basic) | FastAPI integration with auto-registration |
| [cron-monitoring](./cron-monitoring) | Cron job heartbeat monitoring |
| [breadcrumbs](./breadcrumbs) | Breadcrumb capture (HTTP, SQLAlchemy, context managers) |

## Installation

```bash
pip install roselabs-falcon
```

## Quick Start

```python
from falcon_sdk import init, capture_exception

# Initialize Falcon
falcon = init(
    api_key="sk_falcon_...",
    app_name="my-app",
    environment="production",
)

# Capture exceptions
try:
    risky_operation()
except Exception as e:
    capture_exception(e)
```

## FastAPI Integration

The recommended way to integrate Falcon with FastAPI:

```python
from fastapi import FastAPI
from falcon_sdk import init
from falcon_sdk.fastapi import instrument_fastapi

app = FastAPI()

# Initialize Falcon
falcon = init(api_key="sk_falcon_...", app_name="my-api")

# Instrument the app (adds error tracking, health check, and metrics)
instrument_fastapi(
    app,
    falcon,
    auto_uptime=True,   # Creates /__falcon/health endpoint
    auto_metrics=True,  # Creates /__falcon/metrics endpoint
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## Celery Integration

For Celery workers:

```python
from celery import Celery
from falcon_sdk import init
from falcon_sdk.celery import instrument_celery

celery_app = Celery("tasks")
falcon = init(api_key="sk_falcon_...", app_name="my-worker")

# Instrument Celery (auto-registers worker, captures task errors)
instrument_celery(celery_app, falcon)
```

## Auto-Registration

When you use `instrument_fastapi()` or `instrument_celery()`, your app automatically registers with Falcon on startup. The SDK manages:

| SDK Manages | User Configures (in Dashboard) |
|:------------|:-------------------------------|
| `health_url` | Alert email recipients |
| `metrics_url` | Error rate thresholds |
| `sdk_version` | Ping intervals |
| `sdk_last_seen_at` | Alert environments |

### URL Detection Priority

For `instrument_fastapi()`, the SDK detects your app's public URL in this order:

1. **Explicit `base_url` parameter** - Best for production
   ```python
   instrument_fastapi(app, falcon, base_url="https://api.example.com")
   ```

2. **`FALCON_PUBLIC_URL` environment variable** - Good for Docker/K8s
   ```bash
   FALCON_PUBLIC_URL=https://api.example.com
   ```

3. **Auto-detect from first request** - Convenient for development
   Uses the `Host` header (or `X-Forwarded-Host` behind a proxy)

## Cron Job Monitoring

Monitor scheduled tasks:

```python
from falcon_sdk import cron_heartbeat

# Simple heartbeat
cron_heartbeat("daily-backup")

# With timing
cron_heartbeat("hourly-sync", duration_ms=1234, status="ok")

# As a decorator
from falcon_sdk import cron_job

@cron_job("nightly-cleanup")
def cleanup():
    # Your job logic here
    pass
```

## Breadcrumbs

Capture a trail of events leading up to errors:

```python
from falcon_sdk import (
    install_breadcrumb_integrations,
    add_breadcrumb,
    breadcrumb_scope,
)

# Auto-capture HTTP requests, logs, and DB queries
install_breadcrumb_integrations(
    http=True,       # httpx, requests, aiohttp, urllib3
    logging_handler=True,
    sqlalchemy=True,  # Database query breadcrumbs
)

# Manual breadcrumbs
add_breadcrumb(
    type="click",
    message="User clicked checkout",
    data={"product_id": "123"},
)

# Scope breadcrumbs with context managers
with breadcrumb_scope("checkout", category="business"):
    process_payment()
    update_inventory()
```

## Links

- [Falcon Dashboard](https://falcon.roselabs.io)
- [PyPI Package](https://pypi.org/project/roselabs-falcon/)
