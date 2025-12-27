# Canary Action - Basic Example

This example shows how to add Canary security scanning to your GitHub Actions workflow.

## Setup

1. Get your API key from [Canary Dashboard](https://canary.roselabs.io/settings/api-keys)

2. Add it as a repository secret:
   - Go to your repo → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `CANARY_API_KEY`
   - Value: Your API key (`sk_canary_...`)

3. Copy the workflow file to your project:
   ```bash
   mkdir -p .github/workflows
   cp .github/workflows/security.yml your-project/.github/workflows/
   ```

4. Push to trigger the scan

## Example Output

```
🔍 Canary Security Scan
======================

📦 Scanning package-lock.json (npm)...
   Dependencies: 125
   Vulnerabilities: 3 (critical: 0, high: 1, medium: 2, low: 0)

   ⚠️  HIGH: express@4.18.0 - Denial of Service (CVE-2022-12345)
   ⚠️  MEDIUM: lodash@4.17.20 - Prototype Pollution (CVE-2021-23337)
   ⚠️  MEDIUM: axios@0.21.0 - Server-Side Request Forgery (CVE-2021-3749)

======================
📊 Total: 3 vulnerabilities
   Critical: 0
   High: 1
   Medium: 2
   Low: 0

::error::Security scan failed: Found vulnerabilities at or above 'high' severity
```

## Configuration Options

### Fail only on critical

```yaml
- uses: roselabs-io/canary-action@v1
  with:
    api-key: ${{ secrets.CANARY_API_KEY }}
    fail-on: critical
```

### Report only (never fail)

```yaml
- uses: roselabs-io/canary-action@v1
  with:
    api-key: ${{ secrets.CANARY_API_KEY }}
    fail-on: none
```

### Scan specific files

```yaml
- uses: roselabs-io/canary-action@v1
  with:
    api-key: ${{ secrets.CANARY_API_KEY }}
    lockfiles: 'backend/requirements.txt, frontend/yarn.lock'
```
