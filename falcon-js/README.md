# Falcon JavaScript SDK

Error tracking and uptime monitoring for Node.js applications.

## Examples

| Example | Description |
|:--------|:------------|
| [express-basic](./express-basic) | Express.js integration with auto-registration |

## Installation

```bash
npm install @roselabs-io/falcon
```

## Quick Start

```javascript
import { Falcon, captureError } from '@roselabs-io/falcon';

// Initialize Falcon
Falcon.init({
  apiKey: process.env.FALCON_API_KEY,
  appName: 'my-app',
  environment: process.env.NODE_ENV || 'development',
});

// Capture exceptions
try {
  riskyOperation();
} catch (error) {
  captureError(error);
}
```

## Express.js Integration

The recommended way to integrate Falcon with Express:

```javascript
import express from 'express';
import { Falcon } from '@roselabs-io/falcon';
import { instrumentExpress } from '@roselabs-io/falcon/express';

const app = express();

// Initialize Falcon
Falcon.init({
  apiKey: process.env.FALCON_API_KEY,
  appName: 'my-api',
});

// Instrument the app (adds error tracking, health check, and metrics)
instrumentExpress(app, {
  autoUptime: true,   // Creates /__falcon/health endpoint
  autoMetrics: true,  // Creates /__falcon/metrics endpoint
});

app.get('/', (req, res) => {
  res.json({ message: 'Hello World' });
});

app.listen(3000);
```

## Auto-Registration

When you use `instrumentExpress()`, your app automatically registers with Falcon on startup. The SDK manages:

| SDK Manages | User Configures (in Dashboard) |
|:------------|:-------------------------------|
| `health_url` | Alert email recipients |
| `metrics_url` | Error rate thresholds |
| `sdk_version` | Ping intervals |
| `sdk_last_seen_at` | Alert environments |

### URL Detection Priority

For `instrumentExpress()`, the SDK detects your app's public URL in this order:

1. **Explicit `baseUrl` option** - Best for production
   ```javascript
   instrumentExpress(app, { baseUrl: 'https://api.example.com' });
   ```

2. **`FALCON_PUBLIC_URL` environment variable** - Good for Docker/K8s
   ```bash
   FALCON_PUBLIC_URL=https://api.example.com
   ```

3. **Auto-detect from first request** - Convenient for development
   Uses the `Host` header (or `X-Forwarded-Host` behind a proxy)

## Cron Job Monitoring

Monitor scheduled tasks:

```javascript
import { cronHeartbeat, cronJob } from '@roselabs-io/falcon';

// Simple heartbeat
cronHeartbeat('daily-backup');

// With timing
cronHeartbeat('hourly-sync', { durationMs: 1234, status: 'ok' });

// As a wrapper function
const cleanup = cronJob('nightly-cleanup', async () => {
  // Your job logic here
});
```

## Links

- [Falcon Dashboard](https://falcon.roselabs.io)
- [GitHub Package](https://github.com/roselabs-io/roselabs/pkgs/npm/falcon-js)
