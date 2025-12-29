"""
Pigeon Basic Example

This example shows how to use all Pigeon SDK methods.

Run with: PIGEON_API_KEY=pk_pigeon_... python main.py
"""

import asyncio
import os

from pigeon import Pigeon


async def main():
    api_key = os.environ.get("PIGEON_API_KEY")
    if not api_key:
        print("❌ PIGEON_API_KEY environment variable is required")
        print("\nUsage: PIGEON_API_KEY=pk_pigeon_... python main.py")
        return

    pigeon = Pigeon(
        api_key=api_key,
        # base_url="http://localhost:8001",  # For local development
    )

    print("🐦 Pigeon SDK Examples\n")

    # =========================================================================
    # Templates
    # =========================================================================
    print("📋 TEMPLATES\n")

    # List all templates
    print("1. Listing templates...")
    try:
        templates = await pigeon.list_templates()
        print(f"   ✓ Found {len(templates)} template(s)")
        for t in templates:
            print(f"     - {t.name} ({t.id})")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Get template by name
    print("\n2. Getting template by name...")
    try:
        template = await pigeon.get_template_by_name("welcome")
        print(f"   ✓ Template: {template.name}")
        print(f"     Subject: {template.subject}")
        vars_str = ", ".join(
            v.get("name", str(v)) if isinstance(v, dict) else str(v)
            for v in (template.variables or [])
        )
        print(f"     Variables: {vars_str or 'none'}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # =========================================================================
    # Sending Emails
    # =========================================================================
    print("\n\n📧 SENDING EMAILS\n")

    # Send using a template name
    print("3. Sending email with template name...")
    sent_email_id = None
    try:
        result = await pigeon.send(
            to="recipient@example.com",
            template_name="welcome",
            variables={
                "name": "John Doe",
                "company": "Acme Inc",
            },
        )
        sent_email_id = result.id
        print(f"   ✓ Email queued: {result.id}")
        print(f"     Status: {result.status}")
        print(f"     Subject: {result.subject}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Send raw HTML email
    print("\n4. Sending HTML email...")
    try:
        result = await pigeon.send(
            to="recipient@example.com",
            subject="Welcome to Our Service!",
            html="""
                <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
                    <h1 style="color: #333;">Welcome!</h1>
                    <p>Thanks for signing up. We're excited to have you.</p>
                    <a href="https://example.com/get-started"
                       style="display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">
                        Get Started
                    </a>
                </div>
            """,
        )
        print(f"   ✓ Email queued: {result.id}")
        print(f"     Status: {result.status}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Send with reply-to
    print("\n5. Sending with reply-to...")
    try:
        result = await pigeon.send(
            to="recipient@example.com",
            reply_to="support@example.com",
            subject="Your Invoice",
            html="<p>Please find your invoice details below.</p>",
        )
        print(f"   ✓ Email queued: {result.id}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # =========================================================================
    # Batch Sending
    # =========================================================================
    print("\n\n📦 BATCH SENDING\n")

    # Send batch with template (personalized for each recipient)
    print("6. Sending batch with template...")
    try:
        batch_result = await pigeon.send_batch(
            recipients=[
                {"to": "user1@example.com", "variables": {"name": "Alice"}},
                {"to": "user2@example.com", "variables": {"name": "Bob"}},
                {"to": "user3@example.com", "variables": {"name": "Charlie"}},
            ],
            template_name="welcome",
        )
        print(f"   ✓ Batch complete: {batch_result.queued}/{batch_result.total} queued")
        if batch_result.suppressed > 0:
            print(f"     Suppressed: {batch_result.suppressed}")
        if batch_result.failed > 0:
            print(f"     Failed: {batch_result.failed}")
        for r in batch_result.results:
            status_icon = "✓" if r.status == "queued" else "✗"
            print(f"     {status_icon} {r.to}: {r.status}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Send batch with raw HTML
    print("\n7. Sending batch with raw HTML...")
    try:
        batch_result = await pigeon.send_batch(
            recipients=[
                {"to": "newsletter1@example.com"},
                {"to": "newsletter2@example.com"},
            ],
            subject="Monthly Newsletter",
            html="""
                <div style="font-family: sans-serif;">
                    <h1>December Newsletter</h1>
                    <p>Here's what's new this month...</p>
                </div>
            """,
        )
        print(f"   ✓ Batch complete: {batch_result.queued}/{batch_result.total} queued")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Send transactional batch (bypasses suppression list)
    print("\n8. Sending transactional batch...")
    try:
        batch_result = await pigeon.send_batch(
            recipients=[
                {"to": "user@example.com", "variables": {"code": "ABC123"}},
            ],
            template_name="password-reset",
            transactional=True,  # Bypasses suppression, no unsubscribe footer
        )
        print(f"   ✓ Transactional batch: {batch_result.queued}/{batch_result.total} queued")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # =========================================================================
    # Email History
    # =========================================================================
    print("\n\n📊 EMAIL HISTORY\n")

    # List sent emails
    print("9. Listing sent emails...")
    try:
        email_list = await pigeon.list_emails(page=1, page_size=5)
        print(f"   ✓ Found {email_list.total} email(s) (showing {len(email_list.emails)})")
        for e in email_list.emails:
            to_str = ", ".join(e.to)
            print(f"     - {e.subject} → {to_str} [{e.status}]")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Get specific email
    if sent_email_id:
        print("\n10. Getting email details...")
        try:
            email = await pigeon.get_email(sent_email_id)
            print(f"   ✓ Email: {email.id}")
            print(f"     To: {', '.join(email.to)}")
            print(f"     Subject: {email.subject}")
            print(f"     Status: {email.status}")
            print(f"     Template: {email.template_name or 'none'}")
        except Exception as e:
            print(f"   ✗ Error: {e}")

    print("\n\n✅ Done! Check your Pigeon dashboard for delivery status.")


if __name__ == "__main__":
    asyncio.run(main())
