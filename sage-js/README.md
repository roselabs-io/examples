# Sage JavaScript SDK

Helpdesk and contact form integration.

## Examples

| Example | Description |
|:--------|:------------|
| [contact-form](./contact-form) | Embeddable contact form widget |

## Installation

```bash
npm install @roselabs-io/sage
```

Or use the CDN:

```html
<script src="https://cdn.roselabs.io/sage.js"></script>
```

## Quick Start (Widget)

```html
<!-- Add the widget script -->
<script src="https://cdn.roselabs.io/sage.js"
        data-sage-team-id="your-team-id"
        data-sage-position="bottom-right">
</script>
```

## Quick Start (JavaScript)

```javascript
import { Sage } from '@roselabs-io/sage';

const sage = new Sage({
  apiKey: process.env.SAGE_API_KEY,
});

// Create a ticket
await sage.createTicket({
  subject: 'Help with my order',
  message: 'I need help tracking my order #12345',
  customer: {
    email: 'customer@example.com',
    name: 'John Doe',
  },
});
```

## Links

- [Sage Dashboard](https://sage.roselabs.io)
- [GitHub Package](https://github.com/roselabs-io/roselabs/pkgs/npm/sage-js)
