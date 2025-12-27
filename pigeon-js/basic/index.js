/**
 * Pigeon Basic Example
 *
 * This example shows how to send emails using Pigeon.
 *
 * Run with: PIGEON_API_KEY=sk_pigeon_... node index.js
 */

import { Pigeon } from '@roselabs-io/pigeon';

const pigeon = new Pigeon({
  apiKey: process.env.PIGEON_API_KEY,
  // baseUrl: 'http://localhost:8001', // For local development
});

async function main() {
  console.log('🐦 Pigeon Email Examples\n');

  // Example 1: Send using a template
  console.log('1. Sending template email...');
  try {
    const result = await pigeon.send({
      to: 'recipient@example.com',
      templateId: 'welcome',
      variables: {
        name: 'John Doe',
        company: 'Acme Inc',
        login_url: 'https://app.example.com/login',
      },
    });
    console.log('   ✓ Template email sent:', result.messageId);
  } catch (error) {
    console.log('   ✗ Error:', error.message);
  }

  // Example 2: Send raw HTML email
  console.log('\n2. Sending HTML email...');
  try {
    const result = await pigeon.send({
      to: 'recipient@example.com',
      subject: 'Welcome to Our Service!',
      html: `
        <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
          <h1 style="color: #333;">Welcome!</h1>
          <p>Thanks for signing up. We're excited to have you.</p>
          <a href="https://example.com/get-started"
             style="display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">
            Get Started
          </a>
        </div>
      `,
    });
    console.log('   ✓ HTML email sent:', result.messageId);
  } catch (error) {
    console.log('   ✗ Error:', error.message);
  }

  // Example 3: Send to multiple recipients
  console.log('\n3. Sending to multiple recipients...');
  try {
    const result = await pigeon.send({
      to: ['user1@example.com', 'user2@example.com'],
      subject: 'Team Update',
      html: '<p>This is a team-wide announcement.</p>',
    });
    console.log('   ✓ Batch email sent:', result.messageId);
  } catch (error) {
    console.log('   ✗ Error:', error.message);
  }

  // Example 4: Send with attachments
  console.log('\n4. Sending with CC and Reply-To...');
  try {
    const result = await pigeon.send({
      to: 'recipient@example.com',
      cc: 'manager@example.com',
      replyTo: 'support@example.com',
      subject: 'Your Invoice',
      html: '<p>Please find your invoice attached.</p>',
    });
    console.log('   ✓ Email with CC sent:', result.messageId);
  } catch (error) {
    console.log('   ✗ Error:', error.message);
  }

  console.log('\n✅ Done! Check your Pigeon dashboard for delivery status.');
}

// Check for API key
if (!process.env.PIGEON_API_KEY) {
  console.error('❌ PIGEON_API_KEY environment variable is required');
  console.log('\nUsage: PIGEON_API_KEY=sk_pigeon_... node index.js');
  process.exit(1);
}

main().catch(console.error);
