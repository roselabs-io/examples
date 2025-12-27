# Pigeon JavaScript Examples

Email sending examples for Node.js applications.

## Examples

| Example | Description |
|:--------|:------------|
| [basic](./basic) | Basic email sending |

## Installation

```bash
npm install @roselabs-io/pigeon
```

## Quick Start

```javascript
import { Pigeon } from '@roselabs-io/pigeon';

const pigeon = new Pigeon({
  apiKey: process.env.PIGEON_API_KEY,
});

// Send using a template
await pigeon.send({
  to: 'user@example.com',
  templateId: 'welcome',
  variables: {
    name: 'John',
    company: 'Acme Inc',
  },
});

// Send raw HTML
await pigeon.send({
  to: 'user@example.com',
  subject: 'Hello!',
  html: '<h1>Welcome!</h1><p>Thanks for signing up.</p>',
});
```

## Links

- [Full Documentation](https://docs.roselabs.io/pigeon/javascript)
- [API Reference](https://docs.roselabs.io/pigeon/api)
- [npm Package](https://www.npmjs.com/package/@roselabs-io/pigeon)
