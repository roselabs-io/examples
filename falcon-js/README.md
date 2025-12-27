# Falcon JavaScript SDK

Error tracking for Node.js and browser applications.

## Examples

| Example | Description |
|:--------|:------------|
| [express-basic](./express-basic) | Basic Express.js integration |

## Installation

```bash
npm install @roselabs-io/falcon
```

## Quick Start

```javascript
import { Falcon } from '@roselabs-io/falcon';

Falcon.init({
  apiKey: process.env.FALCON_API_KEY,
  appName: 'my-app',
  environment: process.env.NODE_ENV || 'development',
});

// Errors are automatically captured
// Or capture manually:
Falcon.captureError(new Error('Something went wrong'));
```

## Express.js Middleware

```javascript
import express from 'express';
import { Falcon, falconErrorHandler, falconRequestHandler } from '@roselabs-io/falcon/express';

const app = express();

// Add request handler first (captures request context)
app.use(falconRequestHandler());

// Your routes...
app.get('/', (req, res) => {
  res.send('Hello World');
});

// Add error handler last
app.use(falconErrorHandler());

app.listen(3000);
```

## Links

- [Falcon Dashboard](https://falcon.roselabs.io)
- [GitHub Package](https://github.com/roselabs-io/roselabs/pkgs/npm/falcon-js)
