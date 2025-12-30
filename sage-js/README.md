# Sage JavaScript SDK

Helpdesk, contact form, and live chat integration.

## Examples

| Example | Description |
|:--------|:------------|
| [contact-form](./contact-form) | Embeddable contact form widget |
| [live-chat](./live-chat) | AI-powered live chat widget |

## Installation

```bash
npm install @roselabs-io/sage
```

Or use the CDN for the live chat widget:

```html
<script src="https://cdn.roselabs.io/sage-chat.min.js"></script>
```

## Quick Start (Live Chat Widget)

```html
<!-- Add the live chat widget script -->
<script src="https://cdn.roselabs.io/sage-chat.min.js"
        data-sage-api-key="sk_sage_..."
        data-sage-position="bottom-right">
</script>
```

## Quick Start (JavaScript)

```javascript
import { SageChat } from '@roselabs-io/sage/chat';

// Initialize the chat widget
const chat = SageChat.init({
  apiKey: 'sk_sage_...',
  primaryColor: '#6366f1',
  visitor: {
    email: 'user@example.com',
    name: 'John Doe',
  },
});

// Control programmatically
chat.open();
chat.send('Hello!');
chat.identify({ email: 'new@email.com' });
chat.close();
```

## Links

- [Sage Dashboard](https://sage.roselabs.io)
- [GitHub Package](https://github.com/roselabs-io/roselabs/pkgs/npm/sage-js)
