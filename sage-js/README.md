# Sage JavaScript Examples

Helpdesk and contact form examples.

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

- [Full Documentation](https://docs.roselabs.io/sage/javascript)
- [Widget Customization](https://docs.roselabs.io/sage/widget)
- [npm Package](https://www.npmjs.com/package/@roselabs-io/sage)
