# Falcon Source Maps Upload Example

Upload source maps to Falcon to get readable stack traces for minified JavaScript.

## Why Source Maps?

When your JavaScript is minified for production, stack traces look like:

```
Error: Something went wrong
    at a.b (main.abc123.js:1:12345)
    at c.d (main.abc123.js:1:67890)
```

With source maps uploaded, Falcon shows the original source:

```
Error: Something went wrong
    at processPayment (src/services/payment.ts:42:15)
    at handleCheckout (src/pages/Checkout.tsx:128:23)
```

## Usage

### 1. Configure your build to generate source maps

**Vite (vite.config.ts):**
```ts
export default defineConfig({
  build: {
    sourcemap: true,
  },
});
```

**Webpack:**
```js
module.exports = {
  devtool: 'source-map',
};
```

**Next.js (next.config.js):**
```js
module.exports = {
  productionBrowserSourceMaps: true,
};
```

### 2. Set environment variables

```bash
export FALCON_API_KEY=sk_falcon_...
export FALCON_APP_ID=your-app-id
export BUILD_VERSION=1.0.0  # or use npm_package_version
```

### 3. Upload after build

```bash
npm run build
node upload-sourcemaps.js
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Build
  run: npm run build

- name: Upload source maps
  env:
    FALCON_API_KEY: ${{ secrets.FALCON_API_KEY }}
    FALCON_APP_ID: your-app-id
    BUILD_VERSION: ${{ github.sha }}
  run: node upload-sourcemaps.js
```

### Using the SDK directly

```ts
import { uploadSourceMaps } from '@roselabs-io/falcon/sourcemaps';
import glob from 'glob';
import path from 'path';

const maps = glob.sync('./dist/**/*.map').map(p => ({
  path: p,
  filename: path.basename(p),
  originalFilename: path.basename(p).replace('.map', ''),
}));

await uploadSourceMaps({
  apiKey: process.env.FALCON_API_KEY,
  appId: process.env.FALCON_APP_ID,
  release: process.env.BUILD_VERSION,
  sourceMaps: maps,
});
```

## Important Notes

1. **Set release version in your app** - The release must match between your app and uploaded source maps:

   ```ts
   const falcon = new Falcon({
     apiKey: 'sk_falcon_...',
     appName: 'my-app',
     release: '1.0.0',  // Must match uploaded source maps
   });
   ```

2. **Don't expose source maps publicly** - Source maps contain your original source code. Only upload them to Falcon, don't serve them from your CDN.

3. **Upload for each release** - Source maps are versioned by release. Upload new maps whenever you deploy.
