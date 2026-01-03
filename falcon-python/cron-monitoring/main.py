"""
Falcon Cron Monitoring Example

This example shows how to monitor scheduled jobs using Falcon's cron monitoring feature.
Falcon will alert you if your scheduled jobs don't run on time or fail.

Run with: FALCON_API_KEY=sk_falcon_... python main.py
"""

import asyncio
import os
import random
import time

from falcon_sdk import init
from falcon_sdk.cron import cron_heartbeat, cron_heartbeat_async, cron_job


# Initialize Falcon SDK
falcon = init(
    api_key=os.environ.get("FALCON_API_KEY", ""),
    app_name="cron-monitoring-example",
    environment=os.environ.get("ENVIRONMENT", "development"),
    api_url=os.environ.get("FALCON_API_URL", "https://api.falcon.roselabs.io"),
    debug=True,
)


# =============================================================================
# Example 1: Simple heartbeat
# =============================================================================

def simple_backup():
    """
    Simple job that sends a heartbeat when complete.

    First, create a monitor in Falcon with slug "daily-backup" and set the expected schedule.
    """
    print("Starting daily backup...")
    time.sleep(1)  # Simulate backup work
    print("Backup complete!")

    # Send heartbeat - Falcon will alert if this doesn't arrive on schedule
    cron_heartbeat(
        "daily-backup",
        status="ok",
        metadata={"files_backed_up": 150, "size_mb": 2048},
    )


# =============================================================================
# Example 2: Using the @cron_job decorator
# =============================================================================

@cron_job("hourly-sync")
def sync_data():
    """
    Job decorated with @cron_job automatically:
    - Sends heartbeat when complete
    - Records duration
    - Reports errors if the job fails

    Create a monitor in Falcon with slug "hourly-sync".
    """
    print("Syncing data from external API...")
    time.sleep(random.uniform(0.5, 2.0))  # Simulate variable work

    records = random.randint(100, 500)
    print(f"Synced {records} records")

    return {"records_synced": records}


@cron_job("nightly-cleanup")
def cleanup_old_data():
    """
    Job that might fail - Falcon will capture the error.
    """
    print("Cleaning up old data...")

    # Simulate occasional failures
    if random.random() < 0.3:
        raise Exception("Database connection timeout")

    deleted = random.randint(50, 200)
    print(f"Deleted {deleted} old records")
    return {"deleted": deleted}


# =============================================================================
# Example 3: Async cron jobs
# =============================================================================

@cron_job("async-report-generation")
async def generate_reports():
    """
    Async job - also works with the decorator.
    """
    print("Generating reports...")
    await asyncio.sleep(1)  # Simulate async work

    reports = ["daily-summary", "user-activity", "error-stats"]
    print(f"Generated {len(reports)} reports")
    return {"reports": reports}


# =============================================================================
# Example 4: Manual heartbeat with timing
# =============================================================================

async def process_queue():
    """
    Manual heartbeat with explicit timing for jobs where you want more control.
    """
    print("Processing message queue...")

    start_time = time.time()
    messages_processed = 0

    try:
        # Simulate processing messages
        for i in range(10):
            await asyncio.sleep(0.1)
            messages_processed += 1

        duration_ms = int((time.time() - start_time) * 1000)

        # Send success heartbeat with timing
        await cron_heartbeat_async(
            "queue-processor",
            status="ok",
            duration_ms=duration_ms,
            metadata={
                "messages_processed": messages_processed,
                "queue_size_remaining": random.randint(0, 50),
            },
        )
        print(f"Processed {messages_processed} messages in {duration_ms}ms")

    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)

        # Send error heartbeat
        await cron_heartbeat_async(
            "queue-processor",
            status="error",
            duration_ms=duration_ms,
            metadata={
                "error": str(e),
                "messages_processed": messages_processed,
            },
        )
        raise


# =============================================================================
# Example 5: Context manager for more control
# =============================================================================

def complex_etl_job():
    """
    Using cron_job as a context manager for multi-step jobs.
    """
    with cron_job("etl-pipeline") as job:
        print("Step 1: Extracting data...")
        time.sleep(0.5)
        job.metadata["extract_count"] = 1000

        print("Step 2: Transforming data...")
        time.sleep(0.5)
        job.metadata["transform_count"] = 950

        print("Step 3: Loading data...")
        time.sleep(0.5)
        job.metadata["load_count"] = 950

        print("ETL pipeline complete!")


# =============================================================================
# Main
# =============================================================================

async def main():
    api_key = os.environ.get("FALCON_API_KEY")

    print(f"""
🦅 Falcon Cron Monitoring Example

API Key: {'✓ Set' if api_key else '✗ Missing (set FALCON_API_KEY)'}

Prerequisites:
  Create these monitors in your Falcon dashboard:
  - daily-backup (expected: daily)
  - hourly-sync (expected: hourly)
  - nightly-cleanup (expected: daily)
  - async-report-generation (expected: hourly)
  - queue-processor (expected: every 5 minutes)
  - etl-pipeline (expected: daily)

Running examples...
""")

    if not api_key:
        print("⚠️  Set FALCON_API_KEY to send heartbeats to Falcon")
        print("    Running in demo mode (no actual heartbeats sent)\n")

    # Run examples
    print("=" * 50)
    print("Example 1: Simple heartbeat")
    print("=" * 50)
    simple_backup()
    print()

    print("=" * 50)
    print("Example 2: @cron_job decorator")
    print("=" * 50)
    try:
        result = sync_data()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Job failed: {e}")
    print()

    print("=" * 50)
    print("Example 3: Job that might fail")
    print("=" * 50)
    try:
        result = cleanup_old_data()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Job failed (expected occasionally): {e}")
    print()

    print("=" * 50)
    print("Example 4: Async cron job")
    print("=" * 50)
    result = await generate_reports()
    print(f"Result: {result}")
    print()

    print("=" * 50)
    print("Example 5: Manual async heartbeat")
    print("=" * 50)
    await process_queue()
    print()

    print("=" * 50)
    print("Example 6: Context manager")
    print("=" * 50)
    complex_etl_job()
    print()

    print("""
✅ Examples complete!

Check your Falcon dashboard to see:
  - Heartbeat history for each monitor
  - Duration trends
  - Any failures captured

To simulate missed heartbeats, comment out the cron_heartbeat calls
and Falcon will alert you when jobs don't run on schedule.
""")


if __name__ == "__main__":
    asyncio.run(main())
