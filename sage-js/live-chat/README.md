# Sage Live Chat Widget Example

This example demonstrates how to add the Sage live chat widget to your website for AI-powered customer support.

## Features

- **AI-Powered Responses**: Uses your team's knowledge base to provide instant, accurate answers
- **Real-time Chat**: WebSocket-based for instant message delivery
- **Ticket Conversion**: Seamlessly convert chats to support tickets
- **Customizable**: Match your brand colors and positioning
- **Mobile Responsive**: Works great on all device sizes
- **Visitor Identification**: Pre-fill visitor info for authenticated users

## Quick Start

### Script Tag (Simplest)

Add this to your HTML, just before `</body>`:

```html
<script
  src="https://cdn.roselabs.io/sage-chat.min.js"
  data-sage-api-key="sk_sage_..."
></script>
```

### With Customization

```html
<script
  src="https://cdn.roselabs.io/sage-chat.min.js"
  data-sage-api-key="sk_sage_..."
  data-sage-color="#6366f1"
  data-sage-position="bottom-right"
></script>
```

### ES Module (React, Vue, etc.)

```bash
npm install @roselabs-io/sage
```

```typescript
import { SageChat } from '@roselabs-io/sage/chat';

// Initialize
const chat = SageChat.init({
  apiKey: 'sk_sage_...',
  primaryColor: '#6366f1',
  position: 'bottom-right',
  visitor: {
    email: 'user@example.com',
    name: 'John Doe',
  },
});

// Control programmatically
chat.open();           // Open the chat window
chat.close();          // Close the chat window
chat.toggle();         // Toggle open/closed
chat.send('Hello!');   // Send a message
chat.identify({        // Update visitor info
  email: 'new@email.com',
  name: 'Jane Doe',
});
chat.destroy();        // Remove widget completely
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `apiKey` | string | required | Your Sage API key (`sk_sage_...`) |
| `primaryColor` | string | `#6366f1` | Primary color for the widget |
| `position` | string | `bottom-right` | Widget position (`bottom-right` or `bottom-left`) |
| `visitor` | object | `{}` | Pre-identified visitor info (`email`, `name`) |
| `metadata` | object | `{}` | Additional metadata to attach to sessions |

## Events

Listen for widget events:

```javascript
// Widget opened
document.addEventListener('sage:open', () => {
  console.log('Chat opened');
});

// Widget closed
document.addEventListener('sage:close', () => {
  console.log('Chat closed');
});

// Message received
document.addEventListener('sage:message', (event) => {
  console.log('New message:', event.detail);
});
```

## Getting Your API Key

1. Sign up at [sage.roselabs.io](https://sage.roselabs.io)
2. Create or select a team
3. Go to **Settings → API Keys**
4. Create or copy your Sage API key (starts with `sk_sage_`)

## Running This Example

1. Replace `YOUR_API_KEY` in `index.html` with your actual Sage API key
2. Open `index.html` in a browser
3. Click the chat bubble to start chatting!

## Support

- [Documentation](https://sage.roselabs.io/docs)
- [API Reference](https://sage.roselabs.io/docs/api)
- [GitHub Issues](https://github.com/roselabs-io/sage-js/issues)
