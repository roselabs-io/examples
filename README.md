# Rose Labs Examples

Official examples for integrating Rose Labs products into your applications.

## Products

| Product | Description | Examples |
|:--------|:------------|:---------|
| [Falcon](https://falcon.roselabs.io) | Error tracking & uptime monitoring | [falcon-js](./falcon-js), [falcon-python](./falcon-python) |
| [Pigeon](https://pigeon.roselabs.io) | Transactional email API | [pigeon-js](./pigeon-js), [pigeon-python](./pigeon-python) |
| [Sage](https://sage.roselabs.io) | Helpdesk & customer support | [sage-js](./sage-js) |
| [Canary](https://canary.roselabs.io) | Dependency vulnerability scanning | Coming soon |

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
PIGEON_API_KEY=pk_pigeon_... node index.js
```

**Python:**
```bash
cd pigeon-python/basic
pip install -r requirements.txt
PIGEON_API_KEY=pk_pigeon_... python main.py
```

### Sage (Helpdesk)

**Contact Form:**
```bash
cd sage-js/contact-form
# Open index.html in browser
```

## Getting API Keys

1. Sign up at the product dashboard (e.g., [falcon.roselabs.io](https://falcon.roselabs.io))
2. Create a team for your project
3. Go to Settings → API Keys
4. Copy your API key

## Support

- [GitHub Issues](https://github.com/roselabs-io/examples/issues)
- [Email](mailto:support@roselabs.io)

## License

MIT
