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

### Step 1: Create Endpoint

Create a publicly accessible HTTPS endpoint to receive webhook notifications.

**Requirements:**
- HTTPS protocol (HTTP not supported)
- Responds within 30 seconds
- Returns 2xx status code on success
- Handles POST requests with JSON body

### Step 2: Include Callback URL

Add `callback_url` to your screening requests:

```json
{
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456",
  "callback_url": "https://yoursite.com/webhooks/singlekey",
  // ... other fields
}
```

### Step 3: Implement Handler

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    # Parse event
    event = request.json
    event_type = event.get('event')
    data = event.get('data', {})

    # Route to handler
    handlers = {
        'screening.completed': handle_completed,
        'screening.submitted': handle_submitted,
        'screening.failed': handle_failed,
        'form.opened': handle_form_opened,
        'invite.sent': handle_invite_sent,
    }

    handler = handlers.get(event_type)
    if handler:
        handler(data)

    # Always return 200 to acknowledge receipt
    return jsonify({"received": True}), 200
```

---

## Webhook Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           WEBHOOK FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────┐      ┌────────────┐      ┌────────────┐      ┌────────────┐
│ SingleKey  │      │  Webhook   │      │   Your     │      │   Your     │
│ Event      │─────►│  Dispatch  │─────►│  Endpoint  │─────►│  Handler   │
└────────────┘      └────────────┘      └────────────┘      └────────────┘
                          │                   │
                          │                   │
                    ┌─────▼─────┐       ┌─────▼─────┐
                    │  Retry    │       │  Return   │
                    │  Queue    │◄──────│  200 OK   │
                    └───────────┘       └───────────┘
                          │
                          │ On failure
                          ▼
                    ┌───────────┐
                    │  Retry    │
                    │  (6x max) │
                    └───────────┘
```

---

## Event Handlers

### Screening Completed

The most important event - fired when a report is ready.

```python
def handle_completed(data):
    """Handle completed screening."""
    purchase_token = data['purchase_token']
    tenant_id = data['external_tenant_id']
    customer_id = data['external_customer_id']
    score = data.get('singlekey_score')

    # Update your database
    screening = Screening.objects.get(purchase_token=purchase_token)
    screening.status = 'completed'
    screening.score = score
    screening.completed_at = timezone.now()
    screening.save()

    # Fetch full report
    report = fetch_report(purchase_token)

    # Notify landlord
    send_landlord_notification(
        customer_id,
        tenant_id,
        score,
        report['report_url']
    )

    # Update application status
    update_application_status(tenant_id, 'screened', score)

    logger.info(f"Screening completed: {purchase_token}, score: {score}")
```

### Screening Submitted

Fired when tenant submits their application (before processing).

```python
def handle_submitted(data):
    """Handle application submission."""
    purchase_token = data['purchase_token']
    tenant_id = data['external_tenant_id']

    # Update status
    screening = Screening.objects.get(purchase_token=purchase_token)
    screening.status = 'processing'
    screening.submitted_at = timezone.now()
    screening.save()

    # Notify landlord that application is being processed
    send_notification(
        screening.landlord_id,
        f"Tenant application submitted - processing in progress"
    )

    logger.info(f"Screening submitted: {purchase_token}")
```

### Screening Failed

Fired when screening cannot be completed.

```python
def handle_failed(data):
    """Handle screening failure."""
    purchase_token = data['purchase_token']
    reason = data.get('reason', 'unknown')
    errors = data.get('errors', [])

    # Update status
    screening = Screening.objects.get(purchase_token=purchase_token)
    screening.status = 'failed'
    screening.failure_reason = reason
    screening.save()

    # Alert team for investigation
    send_alert(
        f"Screening failed: {purchase_token}\n"
        f"Reason: {reason}\n"
        f"Errors: {', '.join(errors)}"
    )

    # Notify landlord
    send_landlord_notification(
        screening.landlord_id,
        f"Screening could not be completed. Our team is investigating."
    )

    logger.error(f"Screening failed: {purchase_token}, reason: {reason}")
```

### Form Opened

Fired when tenant opens the application form.

```python
def handle_form_opened(data):
    """Track when tenant opens form."""
    purchase_token = data['purchase_token']
    tenant_email = data.get('tenant', {}).get('email')

    # Update tracking
    screening = Screening.objects.get(purchase_token=purchase_token)
    screening.form_opened_at = timezone.now()
    screening.save()

    # Could trigger reminder cancellation
    cancel_reminder(purchase_token)

    logger.info(f"Form opened: {purchase_token}, tenant: {tenant_email}")
```

### Invite Sent

Fired when invitation email is sent to tenant.

```python
def handle_invite_sent(data):
    """Track invitation sent."""
    purchase_token = data['purchase_token']
    tenant_email = data.get('tenant', {}).get('email')
    invite_type = data.get('invite', {}).get('type')

    # Update tracking
    screening = Screening.objects.get(purchase_token=purchase_token)
    screening.invite_sent_at = timezone.now()
    screening.invite_type = invite_type
    screening.save()

    # Schedule reminder if not completed within 24 hours
    schedule_reminder(purchase_token, delay_hours=24)

    logger.info(f"Invite sent: {purchase_token}, type: {invite_type}")
```

---

## Security

### Signature Verification

Verify webhook authenticity using HMAC-SHA256 signatures.

```python
import hmac
import hashlib

WEBHOOK_SECRET = "your_webhook_secret"  # From SingleKey dashboard

def verify_signature(payload_body, signature):
    """Verify webhook signature."""
    expected = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        payload_body.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    # Get signature from header
    signature = request.headers.get('X-SingleKey-Signature', '')

    # Get raw body
    payload_body = request.get_data(as_text=True)

    # Verify signature
    if not verify_signature(payload_body, signature):
        logger.warning("Invalid webhook signature")
        return jsonify({"error": "Invalid signature"}), 401

    # Process event
    event = request.json
    # ... handler logic

    return jsonify({"received": True}), 200
```

### Timestamp Validation

Prevent replay attacks by validating timestamp freshness.

```python
import time

MAX_AGE_SECONDS = 300  # 5 minutes

def validate_timestamp(timestamp_header):
    """Ensure webhook is recent."""
    try:
        webhook_time = int(timestamp_header)
        current_time = int(time.time())
        age = abs(current_time - webhook_time)

        return age < MAX_AGE_SECONDS
    except (TypeError, ValueError):
        return False

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    # Validate timestamp
    timestamp = request.headers.get('X-SingleKey-Timestamp', '')
    if not validate_timestamp(timestamp):
        logger.warning("Webhook timestamp too old or invalid")
        return jsonify({"error": "Invalid timestamp"}), 401

    # Verify signature
    # ... signature verification

    # Process event
    # ... handler logic
```

---

## Reliability

### Idempotent Handlers

Webhooks may be delivered multiple times. Design handlers to be idempotent.

```python
def handle_completed(data):
    """Idempotent handler for completed screening."""
    purchase_token = data['purchase_token']
    webhook_id = data.get('webhook_id')

    # Check if already processed
    if ProcessedWebhook.objects.filter(webhook_id=webhook_id).exists():
        logger.info(f"Webhook already processed: {webhook_id}")
        return

    # Process in transaction
    with transaction.atomic():
        # Mark as processed first (prevents race conditions)
        ProcessedWebhook.objects.create(
            webhook_id=webhook_id,
            event_type='screening.completed',
            purchase_token=purchase_token
        )

        # Now process the event
        screening = Screening.objects.select_for_update().get(
            purchase_token=purchase_token
        )

        if screening.status != 'completed':
            screening.status = 'completed'
            screening.score = data.get('singlekey_score')
            screening.save()

            # Trigger side effects
            notify_landlord(screening)
```

### Async Processing

For long-running tasks, acknowledge immediately and process asynchronously.

```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    # Verify signature (quick)
    if not verify_signature(request):
        return jsonify({"error": "Invalid signature"}), 401

    # Queue for async processing
    event = request.json
    process_webhook.delay(event)

    # Return immediately
    return jsonify({"received": True}), 200

@celery.task(bind=True, max_retries=3)
def process_webhook(self, event):
    """Process webhook asynchronously."""
    try:
        event_type = event.get('event')
        data = event.get('data', {})

        if event_type == 'screening.completed':
            handle_completed(data)
        elif event_type == 'screening.failed':
            handle_failed(data)
        # ... other handlers

    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
```

### Error Handling

Always return 200 to prevent unnecessary retries for handled events.

```python
@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    try:
        # Verify and process
        if not verify_signature(request):
            return jsonify({"error": "Invalid signature"}), 401

        event = request.json
        process_event(event)

    except ScreeningNotFound:
        # Screening doesn't exist in our system - don't retry
        logger.warning(f"Unknown screening: {event.get('data', {}).get('purchase_token')}")

    except TransientError as e:
        # Temporary failure - do retry
        logger.error(f"Transient error: {e}")
        return jsonify({"error": "Temporary failure"}), 500

    except Exception as e:
        # Log error but don't retry - we received it
        logger.error(f"Webhook processing error: {e}")

    # Always return 200 for non-transient cases
    return jsonify({"received": True}), 200
```

---

## Retry Policy

SingleKey retries failed webhook deliveries with exponential backoff:

| Attempt | Delay | Total Time |
|---------|-------|------------|
| 1 | Immediate | 0 |
| 2 | 1 minute | 1 min |
| 3 | 5 minutes | 6 min |
| 4 | 30 minutes | 36 min |
| 5 | 2 hours | 2.5 hours |
| 6 | 12 hours | 14.5 hours |

After 6 failed attempts, the webhook is abandoned.

### What Triggers Retries

| Response | Retried? |
|----------|----------|
| 200-299 | No |
| 400-499 | No (client error) |
| 500-599 | Yes |
| Timeout (>30s) | Yes |
| Connection refused | Yes |

---

## Testing

### Local Development

Use a tunnel service for local testing:

```bash
# Install ngrok
brew install ngrok

# Start tunnel
ngrok http 3000

# Use the URL as callback_url
# https://abc123.ngrok.io/webhooks/singlekey
```

### Sandbox Testing

In sandbox mode, create test screenings that trigger webhooks:

```bash
curl -X POST "https://sandbox.singlekey.com/api/request" \
  -H "Authorization: Token your_sandbox_token" \
  -H "Content-Type: application/json" \
  -d '{
    "external_customer_id": "test-landlord",
    "external_tenant_id": "test-tenant",
    "run_now": true,
    "callback_url": "https://your-ngrok-url/webhooks/singlekey",
    // ... test data
  }'
```

### Manual Testing

Simulate webhook payloads locally:

```python
import requests

def simulate_webhook(event_type, data):
    """Simulate webhook for testing."""
    payload = {
        "event": event_type,
        "timestamp": "2024-01-15T10:30:00Z",
        "webhook_id": f"test_{event_type}_{time.time()}",
        "data": data
    }

    response = requests.post(
        "http://localhost:5000/webhooks/singlekey",
        json=payload,
        headers={"X-SingleKey-Signature": "test_signature"}
    )

    return response

# Test completed event
simulate_webhook('screening.completed', {
    "purchase_token": "test_token_123",
    "external_customer_id": "test-landlord",
    "external_tenant_id": "test-tenant",
    "singlekey_score": 720
})
```

---

## Monitoring

### Logging

Log all webhook activity for debugging:

```python
import logging

logger = logging.getLogger('webhooks')

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    event = request.json
    event_type = event.get('event')
    webhook_id = event.get('webhook_id')

    logger.info(f"Webhook received: {event_type}, id: {webhook_id}")

    try:
        process_event(event)
        logger.info(f"Webhook processed: {webhook_id}")

    except Exception as e:
        logger.error(f"Webhook error: {webhook_id}, error: {e}")
        raise

    return jsonify({"received": True}), 200
```

### Metrics

Track webhook metrics for observability:

```python
from prometheus_client import Counter, Histogram

webhook_received = Counter(
    'singlekey_webhooks_received_total',
    'Total webhooks received',
    ['event_type']
)

webhook_processing_time = Histogram(
    'singlekey_webhook_processing_seconds',
    'Webhook processing time',
    ['event_type']
)

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    event = request.json
    event_type = event.get('event')

    webhook_received.labels(event_type=event_type).inc()

    with webhook_processing_time.labels(event_type=event_type).time():
        process_event(event)

    return jsonify({"received": True}), 200
```

---

## Complete Example

```python
from flask import Flask, request, jsonify
import hmac
import hashlib
import logging
from celery import Celery

app = Flask(__name__)
celery = Celery('tasks', broker='redis://localhost:6379/0')
logger = logging.getLogger('webhooks')

WEBHOOK_SECRET = "your_webhook_secret"

def verify_signature(req):
    """Verify webhook signature."""
    signature = req.headers.get('X-SingleKey-Signature', '')
    payload = req.get_data(as_text=True)

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)

@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    # Verify signature
    if not verify_signature(request):
        logger.warning("Invalid webhook signature")
        return jsonify({"error": "Invalid signature"}), 401

    # Queue for async processing
    event = request.json
    process_webhook.delay(event)

    return jsonify({"received": True}), 200

@celery.task(bind=True, max_retries=3)
def process_webhook(self, event):
    """Process webhook asynchronously."""
    event_type = event.get('event')
    data = event.get('data', {})
    webhook_id = event.get('webhook_id')

    logger.info(f"Processing webhook: {event_type}, id: {webhook_id}")

    try:
        if event_type == 'screening.completed':
            handle_screening_completed(data)
        elif event_type == 'screening.submitted':
            handle_screening_submitted(data)
        elif event_type == 'screening.failed':
            handle_screening_failed(data)
        elif event_type == 'form.opened':
            handle_form_opened(data)
        elif event_type == 'invite.sent':
            handle_invite_sent(data)
        else:
            logger.info(f"Unknown event type: {event_type}")

    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise self.retry(exc=e, countdown=2 ** self.request.retries)

def handle_screening_completed(data):
    """Process completed screening."""
    purchase_token = data['purchase_token']
    score = data.get('singlekey_score')

    # Update database
    from models import Screening
    screening = Screening.objects.get(purchase_token=purchase_token)
    screening.status = 'completed'
    screening.score = score
    screening.save()

    # Notify landlord
    from notifications import send_email
    send_email(
        to=screening.landlord_email,
        subject="Tenant Screening Complete",
        body=f"Screening for {screening.tenant_name} is complete. Score: {score}"
    )

def handle_screening_submitted(data):
    pass  # Implementation

def handle_screening_failed(data):
    pass  # Implementation

def handle_form_opened(data):
    pass  # Implementation

def handle_invite_sent(data):
    pass  # Implementation

if __name__ == '__main__':
    app.run(port=5000)
```

---

## See Also

- [Webhook Events Reference](../webhooks/events.md)
- [Webhook Payload Reference](../webhooks/payload-reference.md)
- [Form-Based Integration](./form-based-integration.md)
- [Direct API Integration](./direct-api-integration.md)
