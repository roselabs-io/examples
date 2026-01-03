# Falcon Cron Monitoring Example

Monitor your scheduled jobs and background tasks with Falcon. Get alerts when jobs don't run on time or fail.

## Features

- **Missed job alerts** - Get notified when scheduled jobs don't run
- **Duration tracking** - Monitor how long jobs take over time
- **Error capture** - Automatically capture and track job failures
- **Rich metadata** - Attach context like records processed, queue sizes, etc.

## Setup

1. Install the SDK:
   ```bash
   pip install roselabs-falcon
   ```

2. Create monitors in your Falcon dashboard for each job:
   - Go to your app → Cron Monitors → Create Monitor
   - Set the expected schedule (e.g., "every hour", "daily at 2am")
   - Copy the slug (e.g., `daily-backup`)

3. Run the example:
   ```bash
   export FALCON_API_KEY=sk_falcon_...
   python main.py
   ```

## Usage Patterns

### Simple Heartbeat

```python
from falcon_sdk.cron import cron_heartbeat

def my_job():
    # Do work...
    cron_heartbeat("my-job-slug", status="ok")
```

### Decorator (Recommended)

```python
from falcon_sdk.cron import cron_job

@cron_job("my-job-slug")
def my_job():
    # Automatically sends heartbeat on completion
    # Automatically tracks duration
    # Automatically reports errors
    return {"records": 100}
```

### With Metadata

```python
@cron_job("data-sync")
def sync_data():
    records = fetch_and_sync()
    return {
        "records_synced": len(records),
        "source": "external-api",
    }
```

### Async Jobs

```python
@cron_job("async-processor")
async def process_queue():
    await async_work()
    return {"processed": 50}
```

### Context Manager

```python
from falcon_sdk.cron import cron_job

def complex_etl():
    with cron_job("etl-pipeline") as job:
        # Step 1
        job.metadata["extracted"] = extract()

        # Step 2
        job.metadata["transformed"] = transform()

        # Step 3
        job.metadata["loaded"] = load()
```

### Manual Timing

```python
from falcon_sdk.cron import cron_heartbeat
import time

def manual_job():
    start = time.time()
    try:
        do_work()
        cron_heartbeat(
            "manual-job",
            status="ok",
            duration_ms=int((time.time() - start) * 1000),
            metadata={"result": "success"},
        )
    except Exception as e:
        cron_heartbeat(
            "manual-job",
            status="error",
            duration_ms=int((time.time() - start) * 1000),
            metadata={"error": str(e)},
        )
        raise
```

## Integration with Celery

```python
from celery import Celery
from falcon_sdk.cron import cron_job

app = Celery('tasks')

@app.task
@cron_job("celery-cleanup")
def cleanup_old_data():
    # Celery task with Falcon monitoring
    deleted = OldRecord.objects.filter(created__lt=cutoff).delete()
    return {"deleted": deleted}
```

## Integration with APScheduler

```python
from apscheduler.schedulers.background import BackgroundScheduler
from falcon_sdk.cron import cron_job

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('cron', hour=2)
@cron_job("nightly-backup")
def backup():
    # Runs at 2 AM, monitored by Falcon
    perform_backup()
```

## Dashboard Features

Once heartbeats are flowing, your Falcon dashboard shows:

- **Status** - Last heartbeat status (ok/error)
- **Last seen** - When the job last ran
- **Next expected** - When the job should run next
- **Duration trend** - Graph of job durations over time
- **Failure rate** - Percentage of failed runs
- **Metadata history** - All metadata from recent runs

## Alerting

Configure alerts in your Falcon dashboard:

- **Missed heartbeat** - Job didn't run when expected
- **Job failure** - Job sent error status
- **Duration anomaly** - Job took unusually long
