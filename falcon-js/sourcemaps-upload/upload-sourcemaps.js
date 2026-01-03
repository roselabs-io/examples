#!/usr/bin/env node
/**
 * Falcon Source Maps Upload Example
 *
 * This script shows how to upload source maps to Falcon after a build.
 * Source maps enable Falcon to show original source code in stack traces
 * instead of minified code.
 *
 * Usage:
 *   FALCON_API_KEY=sk_falcon_... FALCON_APP_ID=your-app-id node upload-sourcemaps.js
 *
 * In your CI/CD pipeline:
 *   npm run build
 *   node upload-sourcemaps.js
 */

const fs = require('fs');
const path = require('path');

// In a real project, you'd import from the SDK:
// const { uploadSourceMaps } = require('@roselabs-io/falcon/sourcemaps');

// For this example, we'll simulate the upload process
async function uploadSourceMaps(options) {
  const {
    apiKey,
    appId,
    release,
    sourceMaps,
    apiUrl = 'https://api.falcon.roselabs.io',
    debug = false,
  } = options;

  const log = debug ? (msg, data) => console.log(`[Falcon] ${msg}`, data || '') : () => {};

  const results = [];

  for (const sourceMap of sourceMaps) {
    const filename = sourceMap.filename || path.basename(sourceMap.path);

    try {
      log(`Uploading ${filename}...`);

      // Step 1: Get presigned upload URL
      const uploadUrlResponse = await fetch(
        `${apiUrl}/apps/${appId}/source-maps/upload-url`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`,
          },
          body: JSON.stringify({
            release,
            filename,
            original_filename: sourceMap.originalFilename || filename.replace(/\.map$/, ''),
            content_type: 'application/json',
          }),
        }
      );

      if (!uploadUrlResponse.ok) {
        const error = await uploadUrlResponse.text();
        throw new Error(`Failed to get upload URL: ${uploadUrlResponse.status} ${error}`);
      }

      const uploadData = await uploadUrlResponse.json();
      log(`Got presigned URL for ${filename}`, { sourceMapId: uploadData.source_map_id });

      // Step 2: Upload to S3
      const fileContent = fs.readFileSync(sourceMap.path);
      const formData = new FormData();

      for (const [key, value] of Object.entries(uploadData.fields)) {
        formData.append(key, value);
      }
      formData.append('file', new Blob([fileContent], { type: 'application/json' }), filename);

      const s3Response = await fetch(uploadData.upload_url, {
        method: 'POST',
        body: formData,
      });

      if (!s3Response.ok && s3Response.status !== 204) {
        throw new Error(`Failed to upload to S3: ${s3Response.status}`);
      }

      log(`Uploaded ${filename} to S3`);

      // Step 3: Confirm upload
      const confirmResponse = await fetch(
        `${apiUrl}/apps/${appId}/source-maps/confirm`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`,
          },
          body: JSON.stringify({
            source_map_id: uploadData.source_map_id,
            file_size_bytes: fileContent.length,
          }),
        }
      );

      if (!confirmResponse.ok) {
        throw new Error(`Failed to confirm upload: ${confirmResponse.status}`);
      }

      log(`Confirmed upload for ${filename}`);

      results.push({
        success: true,
        filename,
        sourceMapId: uploadData.source_map_id,
      });
    } catch (err) {
      log(`Failed to upload ${filename}`, err.message);
      results.push({
        success: false,
        filename,
        error: err.message,
      });
    }
  }

  return {
    total: results.length,
    successful: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length,
    results,
  };
}

// =============================================================================
// Main
// =============================================================================

async function main() {
  const apiKey = process.env.FALCON_API_KEY;
  const appId = process.env.FALCON_APP_ID;
  const release = process.env.BUILD_VERSION || process.env.npm_package_version || 'dev';
  const distDir = process.env.DIST_DIR || './dist';
  const apiUrl = process.env.FALCON_API_URL || 'https://api.falcon.roselabs.io';

  console.log(`
🦅 Falcon Source Maps Upload

Configuration:
  API Key:  ${apiKey ? '✓ Set' : '✗ Missing (set FALCON_API_KEY)'}
  App ID:   ${appId || '✗ Missing (set FALCON_APP_ID)'}
  Release:  ${release}
  Dist Dir: ${distDir}
  API URL:  ${apiUrl}
`);

  if (!apiKey || !appId) {
    console.error('Error: FALCON_API_KEY and FALCON_APP_ID are required');
    process.exit(1);
  }

  // Find all source maps in the dist directory
  const sourceMaps = [];

  function findSourceMaps(dir) {
    if (!fs.existsSync(dir)) {
      console.log(`Warning: Directory ${dir} does not exist`);
      return;
    }

    const files = fs.readdirSync(dir);
    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory()) {
        findSourceMaps(filePath);
      } else if (file.endsWith('.map')) {
        sourceMaps.push({
          path: filePath,
          filename: file,
          originalFilename: file.replace(/\.map$/, ''),
        });
      }
    }
  }

  findSourceMaps(distDir);

  if (sourceMaps.length === 0) {
    console.log('No source maps found in', distDir);
    console.log('Make sure your build generates source maps (e.g., "sourcemap: true" in your bundler config)');
    process.exit(0);
  }

  console.log(`Found ${sourceMaps.length} source map(s):`);
  sourceMaps.forEach(sm => console.log(`  - ${sm.filename}`));
  console.log();

  // Upload source maps
  console.log('Uploading source maps...\n');

  const result = await uploadSourceMaps({
    apiKey,
    appId,
    release,
    sourceMaps,
    apiUrl,
    debug: true,
  });

  console.log(`
Upload complete!
  Total:      ${result.total}
  Successful: ${result.successful}
  Failed:     ${result.failed}
`);

  if (result.failed > 0) {
    console.log('Failed uploads:');
    result.results
      .filter(r => !r.success)
      .forEach(r => console.log(`  - ${r.filename}: ${r.error}`));
    process.exit(1);
  }

  console.log(`
✅ Source maps uploaded for release "${release}"

Stack traces in Falcon will now show original source code instead of minified code.
`);
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
