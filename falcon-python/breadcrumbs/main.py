"""
Falcon SDK Breadcrumbs Example

Demonstrates automatic breadcrumb capture for:
- HTTP requests (aiohttp, httpx, requests, urllib3)
- Database queries (SQLAlchemy)
- Logging
- Custom scopes with context managers
"""

import asyncio
import logging

from falcon_sdk import (
    init,
    capture_exception,
    add_breadcrumb,
    install_breadcrumb_integrations,
    breadcrumb_scope,
    instrument_sqlalchemy,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_falcon():
    """Initialize Falcon with breadcrumb integrations."""
    falcon = init(
        api_key="sk_falcon_xxx",  # Replace with your API key
        app_name="breadcrumbs-demo",
        environment="development",
        debug=True,
    )

    # Install all HTTP + logging breadcrumb integrations
    install_breadcrumb_integrations(
        http=True,  # Instruments httpx, requests, aiohttp, urllib3
        logging_handler=True,
        logging_level=logging.INFO,
        sqlalchemy=True,  # Enable SQLAlchemy query tracking
    )

    return falcon


# =============================================================================
# HTTP Examples
# =============================================================================


def example_requests():
    """Show requests library breadcrumbs."""
    import requests

    logger.info("Making request with requests library...")

    with breadcrumb_scope("fetch_users", category="api"):
        response = requests.get("https://jsonplaceholder.typicode.com/users/1")
        print(f"Got user: {response.json()['name']}")


def example_urllib3():
    """Show urllib3 breadcrumbs."""
    import urllib3

    logger.info("Making request with urllib3...")

    http = urllib3.PoolManager()
    response = http.request("GET", "https://httpbin.org/get")
    print(f"urllib3 status: {response.status}")


async def example_aiohttp():
    """Show aiohttp breadcrumbs."""
    import aiohttp

    logger.info("Making async request with aiohttp...")

    async with breadcrumb_scope("async_fetch", category="api"):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://httpbin.org/json") as response:
                data = await response.json()
                print(f"aiohttp got: {list(data.keys())}")


async def example_httpx_async():
    """Show async httpx breadcrumbs."""
    import httpx

    logger.info("Making async request with httpx...")

    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/uuid")
        print(f"httpx uuid: {response.json()['uuid']}")


# =============================================================================
# SQLAlchemy Example
# =============================================================================


def example_sqlalchemy():
    """Show SQLAlchemy query breadcrumbs."""
    from sqlalchemy import create_engine, text

    logger.info("Running SQLAlchemy queries...")

    # Create in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", echo=False)

    with engine.connect() as conn:
        # These queries will be captured as breadcrumbs
        conn.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"))
        conn.execute(text("INSERT INTO users (name) VALUES ('Alice')"))
        conn.execute(text("INSERT INTO users (name) VALUES ('Bob')"))

        result = conn.execute(text("SELECT * FROM users"))
        users = result.fetchall()
        print(f"Found {len(users)} users in database")

        conn.commit()


# =============================================================================
# Context Manager Examples
# =============================================================================


def example_breadcrumb_scope():
    """Show breadcrumb_scope context manager."""
    import time

    logger.info("Demonstrating breadcrumb_scope...")

    # Sync context manager
    with breadcrumb_scope("checkout_process", category="business", data={"cart_id": "abc123"}):
        print("Processing payment...")
        time.sleep(0.1)

        with breadcrumb_scope("payment_validation", category="business"):
            print("Validating card...")
            time.sleep(0.05)

        with breadcrumb_scope("inventory_update", category="business"):
            print("Updating inventory...")
            time.sleep(0.05)


async def example_async_scope():
    """Show async breadcrumb_scope."""
    import time

    logger.info("Demonstrating async breadcrumb_scope...")

    async with breadcrumb_scope("async_operation", category="async", data={"task": "demo"}):
        await asyncio.sleep(0.1)
        print("Async operation complete")


def example_scope_with_error():
    """Show how breadcrumb_scope captures errors."""
    logger.info("Demonstrating scope with error...")

    try:
        with breadcrumb_scope("risky_operation", category="business"):
            print("About to fail...")
            raise ValueError("Something went wrong!")
    except ValueError:
        pass  # Error is captured in the exit breadcrumb


# =============================================================================
# Custom Breadcrumbs
# =============================================================================


def example_custom_breadcrumbs():
    """Show manual breadcrumb addition."""
    logger.info("Adding custom breadcrumbs...")

    # User action
    add_breadcrumb(
        type="click",
        message="User clicked 'Buy Now' button",
        category="ui.click",
        data={"button_id": "buy-now", "product_id": "prod_123"},
    )

    # Navigation
    add_breadcrumb(
        type="navigation",
        message="Navigated to /checkout",
        category="router",
        data={"from": "/cart", "to": "/checkout"},
    )

    # Custom event
    add_breadcrumb(
        type="custom",
        message="Cart total calculated",
        category="business",
        data={"total": 99.99, "items": 3, "discount": 10.0},
    )


# =============================================================================
# Simulate Error with Breadcrumb Trail
# =============================================================================


async def simulate_error_with_trail():
    """Simulate an error with a rich breadcrumb trail."""
    import httpx

    logger.info("=== Simulating error with breadcrumb trail ===")

    # Build up breadcrumb trail
    add_breadcrumb(type="navigation", message="User landed on homepage", category="router")

    logger.info("User browsing products...")

    add_breadcrumb(
        type="click",
        message="Clicked 'Add to Cart'",
        category="ui",
        data={"product": "Widget Pro"},
    )

    # Make some HTTP requests
    async with httpx.AsyncClient() as client:
        await client.get("https://httpbin.org/status/200")

    with breadcrumb_scope("checkout", category="business"):
        logger.info("Starting checkout...")

        # Simulate the error
        try:
            with breadcrumb_scope("payment_processing", category="payment"):
                raise RuntimeError("Payment gateway timeout")
        except RuntimeError as e:
            # This will send the error along with all breadcrumbs
            capture_exception(
                e,
                context={"order_id": "ord_123", "amount": 99.99},
                tags={"payment_provider": "stripe"},
            )
            print(f"Captured error with breadcrumb trail: {e}")


# =============================================================================
# Main
# =============================================================================


async def main():
    setup_falcon()

    print("\n=== HTTP Breadcrumbs ===\n")
    example_requests()
    example_urllib3()
    await example_aiohttp()
    await example_httpx_async()

    print("\n=== SQLAlchemy Breadcrumbs ===\n")
    example_sqlalchemy()

    print("\n=== Context Manager Breadcrumbs ===\n")
    example_breadcrumb_scope()
    await example_async_scope()
    example_scope_with_error()

    print("\n=== Custom Breadcrumbs ===\n")
    example_custom_breadcrumbs()

    print("\n=== Error with Breadcrumb Trail ===\n")
    await simulate_error_with_trail()

    print("\n=== Done! ===")
    print("Check your Falcon dashboard to see the captured breadcrumbs.")


if __name__ == "__main__":
    asyncio.run(main())
