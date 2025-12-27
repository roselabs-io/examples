# Falcon + Express.js Basic Example

Basic error tracking integration with Express.js.

## Setup

```bash
npm install
```

## Run

```bash
FALCON_API_KEY=sk_falcon_... npm start
```

## Test Endpoints

```bash
# Home (shows available endpoints)
curl http://localhost:3000/

# Trigger an unhandled error (automatically captured)
curl http://localhost:3000/error

# Manual error capture with context
curl http://localhost:3000/manual-error

# Async error
curl http://localhost:3000/async-error

# Error with user context
curl -X POST http://localhost:3000/checkout \
  -H "Content-Type: application/json" \
  -d '{"userId": "123", "cartId": "abc"}'
```

## What This Example Shows

1. **Automatic error capture** - Unhandled errors are automatically sent to Falcon
2. **Manual capture** - Use `Falcon.captureError()` for handled errors
3. **Request context** - `falconRequestHandler()` captures request details
4. **User context** - Use `Falcon.setContext()` to attach user info
5. **Error handler** - `falconErrorHandler()` sends errors and responds with 500

## Key Files

- `index.js` - Main application with Falcon integration
- `package.json` - Dependencies

## Next Steps

- View errors in your [Falcon Dashboard](https://falcon.roselabs.io)
- Add source maps for better stack traces
- Configure alerts for critical errors
