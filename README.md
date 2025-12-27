# Rose Labs Examples

Official examples for integrating Rose Labs products into your applications.

## Products

| Product | Description | Examples |
|:--------|:------------|:---------|
| [Falcon](https://roselabs.io/falcon) | Error tracking & uptime monitoring | [falcon-js](./falcon-js), [falcon-python](./falcon-python), [falcon-react](./falcon-react), [falcon-nextjs](./falcon-nextjs) |
| [Pigeon](https://roselabs.io/pigeon) | Transactional email API | [pigeon-js](./pigeon-js), [pigeon-python](./pigeon-python) |
| [Sage](https://roselabs.io/sage) | Helpdesk & customer support | [sage-js](./sage-js), [sage-python](./sage-python) |

## Quick Start

### Falcon (Error Tracking)

**JavaScript/Node.js:**
```bash
cd falcon-js/express-basic
npm install
FALCON_API_KEY=sk_falcon_... npm start
```

**Python:**
```bash
cd falcon-python/fastapi-basic
pip install -r requirements.txt
FALCON_API_KEY=sk_falcon_... uvicorn main:app
```

### Pigeon (Email)

**Node.js:**
```bash
cd pigeon-js/basic
npm install
PIGEON_API_KEY=sk_pigeon_... node index.js
```

### Sage (Helpdesk)

**Contact Form:**
```bash
cd sage-js/contact-form
# Open index.html in browser
```

## Getting API Keys

1. Sign up at [roselabs.io](https://roselabs.io)
2. Create a team for your product
3. Go to Settings → API Keys
4. Copy your API key (starts with `sk_`)

## Documentation

- [Falcon Docs](https://docs.roselabs.io/falcon)
- [Pigeon Docs](https://docs.roselabs.io/pigeon)
- [Sage Docs](https://docs.roselabs.io/sage)

## Support

- [Discord](https://discord.gg/roselabs)
- [GitHub Issues](https://github.com/roselabs-io/examples/issues)
- [Email](mailto:support@roselabs.io)

## License

MIT
