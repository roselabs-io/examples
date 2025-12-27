# Pigeon JavaScript SDK

Transactional email sending for Node.js applications.

## Examples

| Example | Description |
|:--------|:------------|
| [basic](./basic) | Send emails, manage templates, view email history |

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
  templateName: 'welcome',
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

## API Reference

### Sending Emails

```javascript
// Send with template name
const result = await pigeon.send({
  to: 'user@example.com',
  templateName: 'welcome',
  variables: { name: 'John' },
});

// Send with template ID
const result = await pigeon.send({
  to: 'user@example.com',
  templateId: '123e4567-e89b-12d3-a456-426614174000',
  variables: { name: 'John' },
});

// Send raw HTML
const result = await pigeon.send({
  to: 'user@example.com',
  subject: 'Hello!',
  html: '<h1>Welcome</h1>',
  text: 'Welcome', // optional plain text version
});

// Send with options
const result = await pigeon.send({
  to: ['user1@example.com', 'user2@example.com'],
  subject: 'Update',
  html: '<p>News...</p>',
  fromName: 'Support Team',
  replyTo: 'support@example.com',
  scheduledFor: '2024-12-31T00:00:00Z', // schedule for later
});
```

### Templates

```javascript
// List all templates
const templates = await pigeon.listTemplates();

// Get template by ID
const template = await pigeon.getTemplate('template-id');

// Get template by name
const template = await pigeon.getTemplateByName('welcome');
```

### Email History

```javascript
// List sent emails
const emails = await pigeon.listEmails({
  page: 1,
  pageSize: 50,
  status: 'sent', // optional filter
});

// Get email by ID
const email = await pigeon.getEmail('email-id');
```

## Links

- [Pigeon Dashboard](https://pigeon.roselabs.io)
- [GitHub Package](https://github.com/roselabs-io/roselabs/pkgs/npm/pigeon-js)
