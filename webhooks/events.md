# Webhook Events

SingleKey sends webhook notifications to your configured webhook URL when important events occur during the screening process.

## Configuration

### Webhook URL

Your webhook URL is configured in your **Partner Portal** under API settings. All webhook notifications for your account are sent to this URL.

### Authentication

You can set an optional **Handshake Token** in your Partner Portal. When configured, SingleKey includes it in the headers of every webhook request:

```
Handshake-Token: your_handshake_token
```

Use this to verify that incoming webhooks are from SingleKey.

### Requirements

| Requirement | Details |
|-------------|---------|
| Protocol | HTTPS required |
| Response | Return `200 OK` within 30 seconds |
| Availability | Endpoint must be publicly accessible |
| Method | POST with JSON body |

---

## Webhook Types

All webhooks are POST requests with the `purchase_token` appended as a query parameter:

```
POST https://yoursite.com/webhooks/singlekey?pt=<purchase_token>
```

Every webhook payload has the same structure:

```json
{
  "detail": "<event description>",
  "purchase_token": "<purchase_token>",
  "external_customer_id": "<your_customer_id>",
  "external_tenant_id": "<your_tenant_id>"
}
```

---

### Request Sent to Tenant

Sent when SingleKey has emailed the application to the tenant.

```json
{
  "detail": "Request sent to tenant",
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

---

### Report in Progress

Sent when the tenant submits their application and screening begins processing.

```json
{
  "detail": "Report in Progress",
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

---

### Tenant Email Opened

Sent when the tenant has opened their invitation email and started the application.

```json
{
  "detail": "Tenant email opened",
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

---

### Partial Report Complete

Sent when SingleKey has completed the credit bureau portion of the report but is still waiting on additional information from the tenant to complete the rest.

```json
{
  "detail": "Partial Report Complete",
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

> **Note:** When you receive this webhook, you can fetch the partial report via `GET /api/report/<purchase_token>` to access the credit data that is already available.

---

### Report Complete

Sent when SingleKey has completed the full screening report.

```json
{
  "detail": "Report Complete",
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

> **Note:** On failure, the Report Complete webhook is retried once automatically.

---

## Typical Webhook Sequence

For a standard form-based screening, you'll receive webhooks in this order:

```
1. "Request sent to tenant"      → Tenant has been emailed
2. "Tenant email opened"         → Tenant opened the email / started the application
3. "Report in Progress"          → Tenant submitted the application
4. "Partial Report Complete"     → Credit data ready (optional — not always sent)
5. "Report Complete"             → Full report ready to fetch
```

---

## Handling Webhooks

### Verifying the Handshake Token

If you've configured a Handshake Token in your Partner Portal, verify it on every incoming request:

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

    # Route to handler
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

### Example Handler (Node.js/Express)

```javascript
const express = require('express');
const app = express();
app.use(express.json());

const HANDSHAKE_TOKEN = 'your_handshake_token';

app.post('/webhooks/singlekey', (req, res) => {
  // Verify handshake token
  if (req.headers['handshake-token'] !== HANDSHAKE_TOKEN) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const { detail, purchase_token, external_customer_id, external_tenant_id } = req.body;

  switch (detail) {
    case 'Report Complete':
      console.log(`Report ready for ${purchase_token}`);
      // Fetch report via GET /api/report/<purchase_token>
      break;

    case 'Report in Progress':
      console.log(`Tenant submitted application: ${purchase_token}`);
      break;

    case 'Partial Report Complete':
      console.log(`Partial report available: ${purchase_token}`);
      break;

    case 'Request sent to tenant':
      console.log(`Invitation sent for ${purchase_token}`);
      break;

    case 'Tenant email opened':
      console.log(`Tenant started application: ${purchase_token}`);
      break;
  }

  res.json({ received: true });
});

app.listen(3000);
```

---

## Best Practices

- **Always return 200** — Even if your processing fails, return 200 to acknowledge receipt. Log errors and handle them separately.
- **Be idempotent** — Webhooks may be delivered more than once. Check if you've already processed a given `purchase_token` event before taking action.
- **Process asynchronously** — For long-running tasks, acknowledge the webhook immediately and queue the work for background processing.
- **Use the Handshake Token** — Configure a Handshake Token in your Partner Portal to verify that webhooks are genuinely from SingleKey.

---

## See Also

- [Webhook Payload Reference](./payload-reference.md)
- [Webhook Integration Guide](../integration-guides/webhook-integration.md)
- [Troubleshooting](../troubleshooting/error-codes.md)
