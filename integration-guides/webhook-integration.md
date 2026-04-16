# Webhook Integration Guide

This guide covers setting up and handling webhooks to receive real-time notifications about screening events.

## Overview

Webhooks provide real-time notifications when important events occur, eliminating the need to poll the API for status updates.

## Benefits of Webhooks

| Approach | Pros | Cons |
|----------|------|------|
| **Polling** | Simple to implement | Wastes resources, delayed updates |
| **Webhooks** | Real-time, efficient | Requires public endpoint |

## Setting Up Webhooks

### Step 1: Configure Your Webhook URL

Set your webhook URL in the **Partner Portal** under API settings. All webhook notifications for your account are sent to this URL.

### Step 2: Set Up a Handshake Token (Recommended)

In your Partner Portal, configure a **Handshake Token**. SingleKey will include it in the headers of every webhook so you can verify authenticity:

```
Handshake-Token: your_handshake_token
```

### Step 3: Create Your Endpoint

Create a publicly accessible HTTPS endpoint that:
- Accepts POST requests with a JSON body
- Returns a `200` status code within 30 seconds
- Verifies the `Handshake-Token` header (if configured)

### Step 4: Implement Your Handler

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

HANDSHAKE_TOKEN = "your_handshake_token"

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    # Verify handshake token
    token = request.headers.get('Handshake-Token', '')
    if token != HANDSHAKE_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Parse webhook
    data = request.json
    detail = data.get('detail')
    purchase_token = data.get('purchase_token')

    # Route to handler based on detail value
    if detail == 'Report Complete':
        handle_report_complete(data)
    elif detail == 'Report in Progress':
        handle_report_in_progress(data)
    elif detail == 'Partial Report Complete':
        handle_partial_report(data)
    elif detail == 'Request sent to tenant':
        handle_request_sent(data)
    elif detail == 'Tenant email opened':
        handle_email_opened(data)

    return jsonify({"received": True}), 200
```

---

## Webhook Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           WEBHOOK FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────┐      ┌────────────┐      ┌────────────┐      ┌────────────┐
│ Screening  │      │ SingleKey  │      │   Your     │      │   Your     │
│ Event      │─────►│ Webhook    │─────►│ Endpoint   │─────►│ Handler    │
│ Occurs     │      │ Dispatch   │      │            │      │            │
└────────────┘      └────────────┘      └────────────┘      └────────────┘
                                             │
                                       ┌─────▼─────┐
                                       │ Return    │
                                       │ 200 OK    │
                                       └───────────┘
```

### Typical Event Sequence

```
1. "Request sent to tenant"      → Invitation emailed to tenant
2. "Tenant email opened"         → Tenant opened email / started application
3. "Report in Progress"          → Tenant submitted, screening processing
4. "Partial Report Complete"     → Credit data ready (not always sent)
5. "Report Complete"             → Full report ready to fetch
```

---

## Event Handlers

### Report Complete

The most important webhook — the full report is ready.

```python
def handle_report_complete(data):
    """Handle completed screening report."""
    purchase_token = data['purchase_token']
    external_tenant_id = data['external_tenant_id']
    external_customer_id = data['external_customer_id']

    # Update your database
    screening = Screening.objects.get(purchase_token=purchase_token)
    screening.status = 'completed'
    screening.completed_at = timezone.now()
    screening.save()

    # Fetch full report from SingleKey
    report = fetch_report(purchase_token)

    # Notify landlord
    send_landlord_notification(external_customer_id, external_tenant_id)

    logger.info(f"Report complete: {purchase_token}")
```

### Report in Progress

Tenant has submitted their application — screening is processing.

```python
def handle_report_in_progress(data):
    """Handle tenant submission."""
    purchase_token = data['purchase_token']

    screening = Screening.objects.get(purchase_token=purchase_token)
    screening.status = 'processing'
    screening.submitted_at = timezone.now()
    screening.save()

    logger.info(f"Report in progress: {purchase_token}")
```

### Partial Report Complete

Credit bureau data is ready, but the full report is still pending.

```python
def handle_partial_report(data):
    """Handle partial report availability."""
    purchase_token = data['purchase_token']

    screening = Screening.objects.get(purchase_token=purchase_token)
    screening.status = 'partial'
    screening.save()

    # Optionally fetch partial report
    report = fetch_report(purchase_token)

    logger.info(f"Partial report ready: {purchase_token}")
```

### Request Sent to Tenant

Invitation email has been sent to the tenant.

```python
def handle_request_sent(data):
    """Handle invitation sent."""
    purchase_token = data['purchase_token']

    screening = Screening.objects.get(purchase_token=purchase_token)
    screening.invite_sent_at = timezone.now()
    screening.save()

    logger.info(f"Request sent to tenant: {purchase_token}")
```

### Tenant Email Opened

Tenant has opened the invitation email and started the application.

```python
def handle_email_opened(data):
    """Handle tenant opening the application."""
    purchase_token = data['purchase_token']

    screening = Screening.objects.get(purchase_token=purchase_token)
    screening.form_opened_at = timezone.now()
    screening.save()

    logger.info(f"Tenant email opened: {purchase_token}")
```

---

## Security

### Handshake Token Verification

If you've configured a Handshake Token in your Partner Portal, verify it on every incoming request:

**Python:**

```python
HANDSHAKE_TOKEN = "your_handshake_token"

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    token = request.headers.get('Handshake-Token', '')
    if token != HANDSHAKE_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Process webhook...
    return jsonify({"received": True}), 200
```

**Node.js:**

```javascript
const HANDSHAKE_TOKEN = 'your_handshake_token';

app.post('/webhooks/singlekey', (req, res) => {
  if (req.headers['handshake-token'] !== HANDSHAKE_TOKEN) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  // Process webhook...
  res.json({ received: true });
});
```

---

## Reliability

### Idempotent Handlers

Webhooks may be delivered more than once. Design your handlers to be idempotent:

```python
def handle_report_complete(data):
    """Idempotent handler for completed report."""
    purchase_token = data['purchase_token']

    screening = Screening.objects.get(purchase_token=purchase_token)

    # Check if already processed
    if screening.status == 'completed':
        logger.info(f"Already processed: {purchase_token}")
        return

    screening.status = 'completed'
    screening.save()

    # Trigger side effects
    notify_landlord(screening)
```

### Async Processing

For long-running tasks, acknowledge immediately and process in the background:

```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    # Verify handshake token
    token = request.headers.get('Handshake-Token', '')
    if token != HANDSHAKE_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Queue for async processing
    process_webhook.delay(request.json)

    # Return immediately
    return jsonify({"received": True}), 200

@celery.task
def process_webhook(data):
    detail = data.get('detail')
    if detail == 'Report Complete':
        handle_report_complete(data)
    elif detail == 'Report in Progress':
        handle_report_in_progress(data)
    # ... other handlers
```

### Error Handling

Always return 200 to acknowledge receipt, even if your processing fails:

```python
@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    try:
        process_event(request.json)
    except Exception as e:
        # Log error for debugging
        logger.error(f"Webhook processing error: {e}")
        # Still return 200 — we received it, processing failed
        # Fix your code and reprocess from logs

    return jsonify({"received": True}), 200
```

---

## Retry Behavior

The **Report Complete** webhook is retried once automatically if your endpoint returns a non-success status code. Other webhook types are not retried.

To avoid missed events:
- Always return `200` promptly
- Log all incoming webhooks for replay if needed
- Use the SingleKey admin portal to check webhook delivery status

---

## Testing

### Local Development

Use a tunnel service for local testing:

```bash
# Install ngrok
brew install ngrok

# Start tunnel
ngrok http 3000

# Use the generated URL as your webhook URL
# https://abc123.ngrok.io/webhooks/singlekey
```

### Manual Testing

Simulate webhook payloads locally:

```python
import requests

def simulate_webhook(detail, purchase_token):
    """Simulate a SingleKey webhook for testing."""
    payload = {
        "detail": detail,
        "purchase_token": purchase_token,
        "external_customer_id": "test-landlord",
        "external_tenant_id": "test-tenant"
    }

    response = requests.post(
        "http://localhost:5000/webhooks/singlekey",
        json=payload,
        headers={"Handshake-Token": "your_handshake_token"},
        params={"pt": purchase_token}
    )

    print(f"Status: {response.status_code}")
    return response

# Test each webhook type
simulate_webhook("Request sent to tenant", "test_token_123")
simulate_webhook("Tenant email opened", "test_token_123")
simulate_webhook("Report in Progress", "test_token_123")
simulate_webhook("Partial Report Complete", "test_token_123")
simulate_webhook("Report Complete", "test_token_123")
```

### Webhook Logs

View webhook delivery logs in your SingleKey admin portal:

1. Log in to `platform.singlekey.com/admin`
2. Navigate to **Webhooks** > **Delivery Logs**
3. View status, payload, and response for each delivery attempt

---

## Complete Example

### Python (Flask)

```python
from flask import Flask, request, jsonify
import logging
import requests

app = Flask(__name__)
logger = logging.getLogger('webhooks')

HANDSHAKE_TOKEN = "your_handshake_token"
SINGLEKEY_TOKEN = "your_api_token"
SINGLEKEY_BASE_URL = "https://platform.singlekey.com"

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    # Verify handshake token
    token = request.headers.get('Handshake-Token', '')
    if HANDSHAKE_TOKEN and token != HANDSHAKE_TOKEN:
        logger.warning("Invalid handshake token")
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    detail = data.get('detail')
    purchase_token = data.get('purchase_token')

    logger.info(f"Webhook received: {detail}, token: {purchase_token}")

    try:
        if detail == 'Report Complete':
            handle_report_complete(data)
        elif detail == 'Report in Progress':
            handle_report_in_progress(data)
        elif detail == 'Partial Report Complete':
            handle_partial_report(data)
        elif detail == 'Request sent to tenant':
            handle_request_sent(data)
        elif detail == 'Tenant email opened':
            handle_email_opened(data)
        else:
            logger.info(f"Unknown webhook detail: {detail}")
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")

    return jsonify({"received": True}), 200


def handle_report_complete(data):
    purchase_token = data['purchase_token']

    # Fetch the full report
    response = requests.get(
        f"{SINGLEKEY_BASE_URL}/api/report/{purchase_token}",
        headers={"Authorization": f"Token {SINGLEKEY_TOKEN}"}
    )
    report = response.json()

    logger.info(f"Report complete for {purchase_token}")
    # Update your database, notify landlord, etc.


def handle_report_in_progress(data):
    logger.info(f"Tenant submitted application: {data['purchase_token']}")


def handle_partial_report(data):
    logger.info(f"Partial report ready: {data['purchase_token']}")


def handle_request_sent(data):
    logger.info(f"Invitation sent to tenant: {data['purchase_token']}")


def handle_email_opened(data):
    logger.info(f"Tenant started application: {data['purchase_token']}")


if __name__ == '__main__':
    app.run(port=5000)
```

### Node.js (Express)

```javascript
const express = require('express');
const app = express();
app.use(express.json());

const HANDSHAKE_TOKEN = 'your_handshake_token';

app.post('/webhooks/singlekey', (req, res) => {
  // Verify handshake token
  if (HANDSHAKE_TOKEN && req.headers['handshake-token'] !== HANDSHAKE_TOKEN) {
    console.warn('Invalid handshake token');
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const { detail, purchase_token, external_customer_id, external_tenant_id } = req.body;
  console.log(`Webhook received: ${detail}, token: ${purchase_token}`);

  switch (detail) {
    case 'Report Complete':
      console.log(`Report ready — fetch via GET /api/report/${purchase_token}`);
      break;

    case 'Report in Progress':
      console.log(`Tenant submitted application for ${purchase_token}`);
      break;

    case 'Partial Report Complete':
      console.log(`Partial report available for ${purchase_token}`);
      break;

    case 'Request sent to tenant':
      console.log(`Invitation sent for ${purchase_token}`);
      break;

    case 'Tenant email opened':
      console.log(`Tenant started application for ${purchase_token}`);
      break;

    default:
      console.log(`Unknown webhook: ${detail}`);
  }

  res.json({ received: true });
});

app.listen(3000, () => console.log('Webhook server running on port 3000'));
```

---

## See Also

- [Webhook Events Reference](../webhooks/events.md)
- [Webhook Payload Reference](../webhooks/payload-reference.md)
- [Form-Based Integration](./form-based-integration.md)
- [Direct API Integration](./direct-api-integration.md)
