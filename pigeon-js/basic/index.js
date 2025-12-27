/**
 * Pigeon Basic Example
 *
 * This example shows how to use all Pigeon SDK methods.
 *
 * Run with: PIGEON_API_KEY=pk_pigeon_... node index.js
 */

import { Pigeon } from '@roselabs-io/pigeon';

const pigeon = new Pigeon({
  apiKey: process.env.PIGEON_API_KEY,
  // baseUrl: 'http://localhost:8001', // For local development
});

async function main() {
  console.log('🐦 Pigeon SDK Examples\n');

  // =========================================================================
  // Templates
  // =========================================================================
  console.log('📋 TEMPLATES\n');

  // List all templates
  console.log('1. Listing templates...');
  try {
    const templates = await pigeon.listTemplates();
    console.log(`   ✓ Found ${templates.length} template(s)`);
    templates.forEach((t) => console.log(`     - ${t.name} (${t.id})`));
  } catch (error) {
    console.log('   ✗ Error:', error.message);
  }

  // Get template by name
  console.log('\n2. Getting template by name...');
  try {
    const template = await pigeon.getTemplateByName('welcome');
    console.log(`   ✓ Template: ${template.name}`);
    console.log(`     Subject: ${template.subject}`);
    console.log(`     Variables: ${template.variables?.map((v) => v.name || v).join(', ') || 'none'}`);
  } catch (error) {
    console.log('   ✗ Error:', error.message);
  }

  // =========================================================================
  // Sending Emails
  // =========================================================================
  console.log('\n\n📧 SENDING EMAILS\n');

  // Send using a template name
  console.log('3. Sending email with template name...');
  let sentEmailId;
  try {
    const result = await pigeon.send({
      to: 'recipient@example.com',
      templateName: 'welcome',
      variables: {
        name: 'John Doe',
        company: 'Acme Inc',
      },
    });
    sentEmailId = result.id;
    console.log(`   ✓ Email queued: ${result.id}`);
    console.log(`     Status: ${result.status}`);
    console.log(`     Subject: ${result.subject}`);
  } catch (error) {
    console.log('   ✗ Error:', error.message);
  }

  // Send raw HTML email
  console.log('\n4. Sending HTML email...');
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
    console.log(`   ✓ Email queued: ${result.id}`);
    console.log(`     Status: ${result.status}`);
  } catch (error) {
    console.log('   ✗ Error:', error.message);
  }

  // Send with reply-to
  console.log('\n5. Sending with reply-to...');
  try {
    const result = await pigeon.send({
      to: 'recipient@example.com',
      replyTo: 'support@example.com',
      subject: 'Your Invoice',
      html: '<p>Please find your invoice details below.</p>',
    });
    console.log(`   ✓ Email queued: ${result.id}`);
  } catch (error) {
    console.log('   ✗ Error:', error.message);
  }

  // =========================================================================
  // Email History
  // =========================================================================
  console.log('\n\n📊 EMAIL HISTORY\n');

  // List sent emails
  console.log('6. Listing sent emails...');
  try {
    const emails = await pigeon.listEmails({ page: 1, pageSize: 5 });
    console.log(`   ✓ Found ${emails.total} email(s) (showing ${emails.emails.length})`);
    emails.emails.forEach((e) => {
      console.log(`     - ${e.subject} → ${e.to.join(', ')} [${e.status}]`);
    });
  } catch (error) {
    console.log('   ✗ Error:', error.message);
  }

  // Get specific email
  if (sentEmailId) {
    console.log('\n7. Getting email details...');
    try {
      const email = await pigeon.getEmail(sentEmailId);
      console.log(`   ✓ Email: ${email.id}`);
      console.log(`     To: ${email.to.join(', ')}`);
      console.log(`     Subject: ${email.subject}`);
      console.log(`     Status: ${email.status}`);
      console.log(`     Template: ${email.templateName || 'none'}`);
    } catch (error) {
      console.log('   ✗ Error:', error.message);
    }
  }

  console.log('\n\n✅ Done! Check your Pigeon dashboard for delivery status.');
}

// Check for API key
if (!process.env.PIGEON_API_KEY) {
  console.error('❌ PIGEON_API_KEY environment variable is required');
  console.log('\nUsage: PIGEON_API_KEY=pk_pigeon_... node index.js');
  process.exit(1);
}

main().catch(console.error);
