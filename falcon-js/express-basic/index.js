/**
 * Falcon + Express.js Basic Example
 *
 * This example shows how to integrate Falcon error tracking
 * into an Express.js application using the recommended instrumentExpress() approach.
 *
 * Run with: FALCON_API_KEY=sk_falcon_... npm start
 */

import express from 'express';
import { Falcon, captureError, setContext, setUser } from '@roselabs-io/falcon';
import { instrumentExpress } from '@roselabs-io/falcon/express';

// Initialize Falcon SDK
Falcon.init({
  apiKey: process.env.FALCON_API_KEY,
  appName: 'express-basic-example',
  environment: process.env.NODE_ENV || 'development',
  debug: true, // Enable debug logging (disable in production)
});

const app = express();
const PORT = process.env.PORT || 3000;

// Parse JSON bodies
app.use(express.json());

// Instrument the app with auto-registration
// This automatically:
// - Adds error tracking middleware
// - Creates /__falcon/health endpoint for uptime monitoring
// - Creates /__falcon/metrics endpoint for performance metrics
// - Auto-registers the app with Falcon on first request
instrumentExpress(app, {
  autoUptime: true,   // Creates health endpoint
  autoMetrics: true,  // Creates metrics endpoint
  // baseUrl: 'https://api.example.com',  // Optional: explicit URL for production
});

// =============================================================================
// Routes
// =============================================================================

// Home route
app.get('/', (req, res) => {
  res.json({
    message: 'Falcon Express Example',
    endpoints: {
      '/': 'This message',
      '/error': 'Triggers an unhandled error (captured by Falcon)',
      '/manual-error': 'Manually captures an error',
      '/async-error': 'Triggers an async error',
      '/__falcon/health': 'Health check endpoint (auto-created)',
      '/__falcon/metrics': 'Metrics endpoint (auto-created)',
    },
  });
});

// Unhandled error (automatically captured by Falcon)
app.get('/error', (req, res) => {
  throw new Error('This is a test error!');
});

// Manual error capture
app.get('/manual-error', (req, res) => {
  try {
    // Simulate some operation that might fail
    JSON.parse('invalid json');
  } catch (error) {
    // Manually capture the error with additional context
    captureError(error, {
      tags: { feature: 'json-parsing' },
      extra: { input: 'invalid json' },
    });

    res.status(400).json({ error: 'Invalid JSON provided' });
  }
});

// Async error (automatically captured)
app.get('/async-error', async (req, res) => {
  await new Promise((resolve) => setTimeout(resolve, 100));
  throw new Error('Async error after delay!');
});

// Custom error with user context
app.get('/user-error', (req, res) => {
  // Set user context
  setUser({ id: 'user-123', email: 'test@example.com' });

  throw new Error('Error with user context attached');
});

// Custom error with context
app.post('/checkout', (req, res) => {
  const { userId, cartId } = req.body || {};

  // Add context that will be attached to any errors
  setContext({
    user: { id: userId },
    extra: { cartId },
  });

  // Simulate a checkout error
  throw new Error('Payment processing failed');
});

// =============================================================================
// Start Server
// =============================================================================

app.listen(PORT, () => {
  console.log(`
🦅 Falcon Express Example Running!

Server:     http://localhost:${PORT}
API Key:    ${process.env.FALCON_API_KEY ? '✓ Set' : '✗ Missing (set FALCON_API_KEY)'}

Auto-registration enabled:
  - Health endpoint: /__falcon/health
  - Metrics endpoint: /__falcon/metrics

Try these endpoints:
  curl http://localhost:${PORT}/
  curl http://localhost:${PORT}/error
  curl http://localhost:${PORT}/manual-error
  curl http://localhost:${PORT}/async-error
  curl http://localhost:${PORT}/__falcon/health
  curl http://localhost:${PORT}/__falcon/metrics
  curl -X POST http://localhost:${PORT}/checkout -H "Content-Type: application/json" -d '{"userId": "123", "cartId": "abc"}'
  `);
});
