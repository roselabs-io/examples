# Falcon SDK - Breadcrumbs Example

Demonstrates automatic breadcrumb capture for debugging context.

## What are Breadcrumbs?

Breadcrumbs are a trail of events leading up to an error. When an exception occurs, Falcon captures these breadcrumbs along with the error, giving you context about what the user did before the crash.

## Features Demonstrated

### HTTP Request Tracking

Automatically captures HTTP requests from:

- **httpx** - Modern async/sync HTTP client
- **requests** - Popular synchronous HTTP library
- **aiohttp** - Async HTTP client
- **urllib3** - Low-level HTTP library

### Database Query Tracking

Captures SQLAlchemy queries including:

- Query type (SELECT, INSERT, UPDATE, DELETE)
- Execution duration
- Truncated SQL for context

### Logging Integration

Captures log messages as breadcrumbs:

- INFO and above by default
- Includes logger name, level, and source location

### Context Managers

Use `breadcrumb_scope` to track code blocks:

```python
from falcon_sdk import breadcrumb_scope

# Sync
with breadcrumb_scope("checkout", category="business"):
    process_payment()

# Async
async with breadcrumb_scope("api_call", data={"endpoint": "/users"}):
    await fetch_users()
```

### Custom Breadcrumbs

Add manual breadcrumbs for user actions:

```python
from falcon_sdk import add_breadcrumb

add_breadcrumb(
    type="click",
    message="User clicked 'Buy Now'",
    category="ui",
    data={"product_id": "123"},
)
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
# Set your API key
export FALCON_API_KEY=sk_falcon_xxx

# Run the example
python main.py
```

## Configuration

```python
from falcon_sdk import init, install_breadcrumb_integrations

falcon = init(
    api_key="sk_falcon_xxx",
    app_name="my-app",
)

install_breadcrumb_integrations(
    http=True,           # httpx, requests, aiohttp, urllib3
    logging_handler=True,
    logging_level=logging.INFO,
    sqlalchemy=True,     # Database query tracking
)
```

## Selective Instrumentation

You can also instrument libraries individually:

```python
from falcon_sdk import (
    instrument_aiohttp,
    instrument_urllib3,
    instrument_sqlalchemy,
)

# Only instrument what you need
instrument_aiohttp()
instrument_sqlalchemy()
```

## Breadcrumb Types

| Type | Use Case |
|------|----------|
| `http` | HTTP requests (auto-captured) |
| `console` | Log messages (auto-captured) |
| `navigation` | Page/route changes, scope entry/exit |
| `click` | User interactions |
| `custom` | Any other events |

## Best Practices

1. **Keep breadcrumbs lightweight** - Don't include large payloads in `data`
2. **Use meaningful messages** - They should be human-readable
3. **Add context at boundaries** - User actions, API calls, state changes
4. **Use scopes for operations** - Wrap multi-step processes
