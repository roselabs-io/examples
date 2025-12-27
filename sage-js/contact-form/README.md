# Sage Contact Form Example

A simple embeddable contact form that creates tickets in your Sage helpdesk.

## Setup

1. Open `index.html` in a text editor
2. Replace `YOUR_TEAM_ID` with your actual Sage team ID
3. Open in a browser

## Get Your Team ID

1. Log in to [Sage](https://sage.roselabs.io)
2. Go to Settings → API Keys
3. Copy your Team ID

## Customization

### Styling

The form uses vanilla CSS that you can easily customize:

```css
/* Change the primary color */
button {
  background: #your-brand-color;
}

/* Make it match your site */
.card {
  border-radius: 0; /* Square corners */
  box-shadow: none; /* No shadow */
}
```

### Fields

Add custom fields by including them in the JSON body:

```javascript
body: JSON.stringify({
  team_id: TEAM_ID,
  subject: 'Support Request',
  message: document.getElementById('message').value,
  customer_email: document.getElementById('email').value,
  customer_name: document.getElementById('name').value,
  // Custom fields
  metadata: {
    order_id: document.getElementById('order-id').value,
    plan: 'pro',
  },
}),
```

## Production Deployment

1. Change the API URL:
   ```javascript
   const SAGE_API_URL = 'https://api.sage.roselabs.io';
   ```

2. Consider adding CAPTCHA (Cloudflare Turnstile recommended)

3. Add rate limiting on your server

## Using the Widget Instead

For an even easier integration, use the Sage widget:

```html
<script src="https://cdn.roselabs.io/sage.js"
        data-sage-team-id="your-team-id"
        data-sage-position="bottom-right">
</script>
```

This adds a floating chat-style button that opens a contact form.
