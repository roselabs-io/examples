# Canary GitHub Action

Scan dependencies for vulnerabilities in CI/CD pipelines.

## Examples

| Example | Description |
|:--------|:------------|
| [basic](./basic) | Basic workflow setup |

## Quick Start

Add to your GitHub workflow:

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan dependencies
        uses: roselabs-io/canary-action@v1
        with:
          api-key: ${{ secrets.CANARY_API_KEY }}
```

## Configuration

| Input | Description | Default |
|-------|-------------|---------|
| `api-key` | Canary API key | Required |
| `fail-on` | Severity threshold: `critical`, `high`, `medium`, `low`, `none` | `high` |
| `lockfiles` | Comma-separated paths (auto-detected if empty) | Auto |

## Supported Lockfiles

- **npm**: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- **Python**: `requirements.txt`, `Pipfile.lock`, `poetry.lock`, `uv.lock`
- **Go**: `go.sum`
- **Rust**: `Cargo.lock`

## Links

- [Canary Dashboard](https://canary.roselabs.io)
- [Action Repository](https://github.com/roselabs-io/canary-action)
