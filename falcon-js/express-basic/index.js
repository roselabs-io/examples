/**
 * Falcon + Express.js Basic Example
 *
 * This example shows how to integrate Falcon error tracking
 * into a basic Express.js application.
 *
 * Run with: FALCON_API_KEY=sk_falcon_... npm start
 */

import express from 'express';
import { Falcon, falconErrorHandler, falconRequestHandler } from '@roselabs-io/falcon/express';

// Initialize Falcon
Falcon.init({
  apiKey: process.env.FALCON_API_KEY,
  appName: 'express-basic-example',
  environment: process.env.NODE_ENV || 'development',
  debug: true, // Enable debug logging (disable in production)
});

const app = express();
const PORT = process.env.PORT || 3000;

// Add Falcon request handler (captures request context for errors)
app.use(falconRequestHandler());

// Parse JSON bodies
app.use(express.json());

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
    Falcon.captureError(error, {
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

// Custom error with context
app.post('/checkout', (req, res) => {
  const { userId, cartId } = req.body || {};

  // Add context that will be attached to any errors
  Falcon.setContext({
    user: { id: userId },
    extra: { cartId },
  });

  // Simulate a checkout error
  throw new Error('Payment processing failed');
});

// =============================================================================
// Error Handler (must be last)
// =============================================================================

app.use(falconErrorHandler());

// =============================================================================
// Start Server
// =============================================================================

app.listen(PORT, () => {
  console.log(`
🦅 Falcon Express Example Running!

Server:     http://localhost:${PORT}
API Key:    ${process.env.FALCON_API_KEY ? '✓ Set' : '✗ Missing (set FALCON_API_KEY)'}

Try these endpoints:
  curl http://localhost:${PORT}/
  curl http://localhost:${PORT}/error
  curl http://localhost:${PORT}/manual-error
  curl http://localhost:${PORT}/async-error
  curl -X POST http://localhost:${PORT}/checkout -H "Content-Type: application/json" -d '{"userId": "123", "cartId": "abc"}'
  `);
});
