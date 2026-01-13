# Webhook Events

SingleKey sends webhook notifications to your configured `callback_url` when important events occur during the screening process.

## Configuration

### Setting Up Webhooks

Include a `callback_url` in your screening request:

```json
{
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456",
  "callback_url": "https://yoursite.com/webhooks/singlekey",
  // ... other fields
}
```

### Requirements

| Requirement | Details |
|-------------|---------|
| Protocol | HTTPS required (HTTP not supported) |
| Response | Return `200 OK` within 30 seconds |
| Availability | Endpoint must be publicly accessible |
| Content-Type | Webhooks are sent as `application/json` |

---

## Event Types

### `screening.completed`

Sent when a screening report is ready for retrieval.

```json
{
  "event": "screening.completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-456",
    "external_deal_id": "deal-abc123",
    "tenant_email": "tenant@example.com",
    "landlord_email": "landlord@example.com",
    "status": "completed",
    "singlekey_score": 720,
    "report_url": "https://platform.singlekey.com/api/report/abc123..."
  }
}
```

### `screening.submitted`

Sent when a tenant submits their application (before processing completes).

```json
{
  "event": "screening.submitted",
  "timestamp": "2024-01-15T10:25:00Z",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-456",
    "external_deal_id": "deal-abc123",
    "tenant_email": "tenant@example.com",
    "status": "processing"
  }
}
```

### `screening.payment_captured`

Sent when payment is successfully captured.

```json
{
  "event": "screening.payment_captured",
  "timestamp": "2024-01-15T10:26:00Z",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-456",
    "amount": 2249,
    "currency": "CAD",
    "payment_method": "card_ending_4242"
  }
}
```

### `screening.failed`

Sent when a screening cannot be completed due to errors.

```json
{
  "event": "screening.failed",
  "timestamp": "2024-01-15T10:35:00Z",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-456",
    "status": "failed",
    "reason": "Credit bureau unavailable",
    "errors": [
      "Unable to retrieve credit report from Equifax"
    ]
  }
}
```

### `form.opened`

Sent when a tenant opens their application form link.

```json
{
  "event": "form.opened",
  "timestamp": "2024-01-15T09:00:00Z",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-456",
    "tenant_email": "tenant@example.com"
  }
}
```

### `invite.sent`

Sent when an invitation email is sent to a tenant.

```json
{
  "event": "invite.sent",
  "timestamp": "2024-01-15T08:30:00Z",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-456",
    "tenant_email": "tenant@example.com",
    "invite_type": "email"
  }
}
```

---

## Event Payload Structure

All webhook payloads follow this structure:

```json
{
  "event": "event.type",
  "timestamp": "ISO 8601 timestamp",
  "data": {
    // Event-specific data
  }
}
```

### Common Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `purchase_token` | string | Unique screening identifier |
| `external_customer_id` | string | Your landlord ID |
| `external_tenant_id` | string | Your tenant ID |
| `external_deal_id` | string | Your deal/transaction ID (if provided) |
| `tenant_email` | string | Tenant's email address |
| `landlord_email` | string | Landlord's email address |
| `status` | string | Current screening status |
| `timestamp` | string | ISO 8601 formatted timestamp |

---

## Handling Webhooks

### Verification

Verify webhook authenticity by checking the `X-SingleKey-Signature` header:

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)
```

### Response Requirements

| Response | Result |
|----------|--------|
| `200 OK` | Webhook acknowledged |
| `2xx` | Webhook acknowledged |
| `4xx` | Webhook failed, will retry |
| `5xx` | Webhook failed, will retry |
| Timeout (>30s) | Webhook failed, will retry |

### Example Handler (Python/Flask)

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)
WEBHOOK_SECRET = "your_webhook_secret"

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    # Verify signature
    signature = request.headers.get('X-SingleKey-Signature', '')
    payload = request.get_data(as_text=True)

    if not verify_signature(payload, signature):
        return jsonify({"error": "Invalid signature"}), 401

    # Parse event
    event = request.json
    event_type = event.get('event')
    data = event.get('data', {})

    # Handle event
    if event_type == 'screening.completed':
        handle_screening_completed(data)
    elif event_type == 'screening.submitted':
        handle_screening_submitted(data)
    elif event_type == 'screening.failed':
        handle_screening_failed(data)

    return jsonify({"received": True}), 200

def verify_signature(payload, signature):
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)

def handle_screening_completed(data):
    purchase_token = data['purchase_token']
    external_tenant_id = data['external_tenant_id']
    score = data.get('singlekey_score')

    # Update your database
    print(f"Screening completed for tenant {external_tenant_id}")
    print(f"SingleKey Score: {score}")
    print(f"Fetch full report: GET /api/report/{purchase_token}")

def handle_screening_submitted(data):
    print(f"Tenant {data['external_tenant_id']} submitted application")

def handle_screening_failed(data):
    print(f"Screening failed: {data.get('reason')}")
    for error in data.get('errors', []):
        print(f"  - {error}")
```

### Example Handler (Node.js/Express)

```javascript
const express = require('express');
const crypto = require('crypto');

const app = express();
app.use(express.json());

const WEBHOOK_SECRET = 'your_webhook_secret';

app.post('/webhooks/singlekey', (req, res) => {
  // Verify signature
  const signature = req.headers['x-singlekey-signature'];
  const payload = JSON.stringify(req.body);

  if (!verifySignature(payload, signature)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  // Handle event
  const { event, data } = req.body;

  switch (event) {
    case 'screening.completed':
      console.log(`Screening completed for ${data.external_tenant_id}`);
      console.log(`Score: ${data.singlekey_score}`);
      // Update your database
      break;

    case 'screening.submitted':
      console.log(`Application submitted by ${data.external_tenant_id}`);
      break;

    case 'screening.failed':
      console.log(`Screening failed: ${data.reason}`);
      break;

    default:
      console.log(`Unknown event: ${event}`);
  }

  res.json({ received: true });
});

function verifySignature(payload, signature) {
  const expected = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(payload)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}

app.listen(3000);
```

---

## Retry Policy

Failed webhook deliveries are retried with exponential backoff:

| Attempt | Delay |
|---------|-------|
| 1 | Immediate |
| 2 | 1 minute |
| 3 | 5 minutes |
| 4 | 30 minutes |
| 5 | 2 hours |
| 6 | 12 hours |

After 6 failed attempts, the webhook is marked as failed and no further retries occur.

---

## Testing Webhooks

### Sandbox Environment

In the sandbox environment (`sandbox.singlekey.com`), webhooks are sent to your configured URL with test data.

### Local Development

For local development, use a tunnel service:

```bash
# Using ngrok
ngrok http 3000

# Use the generated URL as your callback_url
# https://abc123.ngrok.io/webhooks/singlekey
```

### Webhook Logs

View webhook delivery logs in your SingleKey admin portal:

1. Log in to `platform.singlekey.com/admin`
2. Navigate to **Webhooks** > **Delivery Logs**
3. View status, payload, and response for each delivery attempt

---

## Best Practices

### Idempotency

Webhooks may be delivered multiple times. Design your handlers to be idempotent:

```python
def handle_screening_completed(data):
    purchase_token = data['purchase_token']

    # Check if already processed
    if Screening.objects.filter(
        token=purchase_token,
        webhook_processed=True
    ).exists():
        return  # Already handled

    # Process and mark as handled
    screening = Screening.objects.get(token=purchase_token)
    screening.status = 'completed'
    screening.webhook_processed = True
    screening.save()
```

### Async Processing

For long-running tasks, acknowledge immediately and process asynchronously:

```python
from celery import Celery

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    # Verify signature (quick)
    if not verify_signature(request):
        return jsonify({"error": "Invalid"}), 401

    # Queue for async processing
    process_webhook.delay(request.json)

    # Return immediately
    return jsonify({"received": True}), 200

@celery.task
def process_webhook(event):
    # Long-running processing here
    pass
```

### Error Handling

Log errors but always return 200 to prevent unnecessary retries:

```python
@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    try:
        process_event(request.json)
    except Exception as e:
        # Log error for debugging
        logger.error(f"Webhook processing error: {e}")
        # Still return 200 - we received it, processing failed
        # We'll fix our code and reprocess from logs

    return jsonify({"received": True}), 200
```

---

## See Also

- [Integration Guides](../integration-guides/)
- [API Reference](../api-reference/)
- [Troubleshooting](../troubleshooting/error-codes.md)
