# Pigeon Python SDK

Transactional email sending for Python applications.

## Examples

| Example | Description |
|:--------|:------------|
| [basic](./basic) | Send emails, manage templates, view email history |

## Installation

```bash
pip install roselabs-pigeon
```

## Quick Start

```python
import asyncio
from pigeon import Pigeon

pigeon = Pigeon(api_key="pk_pigeon_...")

async def main():
    # Send using a template
    result = await pigeon.send(
        to="user@example.com",
        template_name="welcome",
        variables={
            "name": "John",
            "company": "Acme Inc",
        },
    )

    # Send raw HTML
    result = await pigeon.send(
        to="user@example.com",
        subject="Hello!",
        html="<h1>Welcome!</h1><p>Thanks for signing up.</p>",
    )

asyncio.run(main())
```

## API Reference

### Sending Emails

```python
# Send with template name
result = await pigeon.send(
    to="user@example.com",
    template_name="welcome",
    variables={"name": "John"},
)

# Send with template ID
result = await pigeon.send(
    to="user@example.com",
    template_id="123e4567-e89b-12d3-a456-426614174000",
    variables={"name": "John"},
)

# Send raw HTML
result = await pigeon.send(
    to="user@example.com",
    subject="Hello!",
    html="<h1>Welcome</h1>",
    text="Welcome",  # optional plain text version
)

# Send with options
result = await pigeon.send(
    to=["user1@example.com", "user2@example.com"],
    subject="Update",
    html="<p>News...</p>",
    from_name="Support Team",
    reply_to="support@example.com",
    scheduled_for="2024-12-31T00:00:00Z",  # schedule for later
)
```

### Templates

```python
# List all templates
templates = await pigeon.list_templates()

# Get template by ID
template = await pigeon.get_template("template-id")

# Get template by name
template = await pigeon.get_template_by_name("welcome")
```

### Email History

```python
# List sent emails
emails = await pigeon.list_emails(
    page=1,
    page_size=50,
    status="sent",  # optional filter
)

# Get email by ID
email = await pigeon.get_email("email-id")
```

## Links

- [Pigeon Dashboard](https://pigeon.roselabs.io)
- [PyPI Package](https://pypi.org/project/roselabs-pigeon/)
