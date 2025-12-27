# Falcon JavaScript Examples

Error tracking examples for Node.js and browser applications.

## Examples

| Example | Description |
|:--------|:------------|
| [express-basic](./express-basic) | Basic Express.js integration |
| [express-typescript](./express-typescript) | TypeScript Express.js app |
| [browser](./browser) | Browser-only error tracking |

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

- [Full Documentation](https://docs.roselabs.io/falcon/javascript)
- [API Reference](https://docs.roselabs.io/falcon/api)
- [npm Package](https://www.npmjs.com/package/@roselabs-io/falcon)
