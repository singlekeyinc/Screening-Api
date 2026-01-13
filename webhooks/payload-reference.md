# Webhook Payload Reference

Complete reference for all webhook payload structures.

## Payload Headers

All webhook requests include these headers:

| Header | Description | Example |
|--------|-------------|---------|
| `Content-Type` | Always `application/json` | `application/json` |
| `X-SingleKey-Signature` | HMAC-SHA256 signature | `a1b2c3d4e5...` |
| `X-SingleKey-Event` | Event type | `screening.completed` |
| `X-SingleKey-Timestamp` | Unix timestamp | `1705312200` |
| `User-Agent` | SingleKey identifier | `SingleKey-Webhook/1.0` |

---

## Base Payload Structure

```json
{
  "event": "event.type",
  "timestamp": "2024-01-15T10:30:00Z",
  "webhook_id": "wh_abc123def456",
  "api_version": "2024-01",
  "data": {
    // Event-specific fields
  }
}
```

### Base Fields

| Field | Type | Description |
|-------|------|-------------|
| `event` | string | Event type identifier |
| `timestamp` | string | ISO 8601 timestamp when event occurred |
| `webhook_id` | string | Unique identifier for this webhook delivery |
| `api_version` | string | API version (for future compatibility) |
| `data` | object | Event-specific payload data |

---

## Event Payloads

### screening.completed

Sent when a screening report is fully processed and ready.

```json
{
  "event": "screening.completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "webhook_id": "wh_scr_completed_abc123",
  "api_version": "2024-01",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "your-landlord-id",
    "external_tenant_id": "your-tenant-id",
    "external_deal_id": "your-deal-id",
    "external_listing_id": "your-listing-id",
    "tenant": {
      "email": "tenant@example.com",
      "first_name": "Jane",
      "last_name": "Doe"
    },
    "landlord": {
      "email": "landlord@example.com",
      "first_name": "John",
      "last_name": "Smith"
    },
    "property": {
      "address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
      "rent": 2000,
      "unit": "Suite 5"
    },
    "result": {
      "status": "completed",
      "singlekey_score": 720,
      "recommendation": "approved",
      "pdf_ready": true
    },
    "cost": {
      "amount": 2249,
      "tax": 292,
      "currency": "CAD"
    },
    "links": {
      "report": "https://platform.singlekey.com/api/report/abc123...",
      "pdf": "https://platform.singlekey.com/api/report_pdf/abc123..."
    },
    "created_at": "2024-01-15T09:00:00Z",
    "completed_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `purchase_token` | string | Unique 32-character token |
| `external_customer_id` | string | Your landlord identifier |
| `external_tenant_id` | string | Your tenant identifier |
| `external_deal_id` | string | Your deal ID (if provided) |
| `external_listing_id` | string | Your listing ID (if provided) |
| `tenant.email` | string | Tenant's email |
| `tenant.first_name` | string | Tenant's first name |
| `tenant.last_name` | string | Tenant's last name |
| `landlord.email` | string | Landlord's email |
| `landlord.first_name` | string | Landlord's first name |
| `landlord.last_name` | string | Landlord's last name |
| `property.address` | string | Property address |
| `property.rent` | integer | Monthly rent |
| `property.unit` | string | Unit number |
| `result.status` | string | `"completed"` |
| `result.singlekey_score` | integer | Credit score (300-900) |
| `result.recommendation` | string | `"approved"`, `"conditional"`, `"declined"` |
| `result.pdf_ready` | boolean | Whether PDF is available |
| `cost.amount` | integer | Charge amount in cents |
| `cost.tax` | integer | Tax amount in cents |
| `cost.currency` | string | `"CAD"` or `"USD"` |
| `links.report` | string | API endpoint for full report |
| `links.pdf` | string | API endpoint for PDF download |
| `created_at` | string | When screening was created |
| `completed_at` | string | When screening completed |

---

### screening.submitted

Sent when tenant submits their application form.

```json
{
  "event": "screening.submitted",
  "timestamp": "2024-01-15T10:25:00Z",
  "webhook_id": "wh_scr_submitted_abc123",
  "api_version": "2024-01",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "your-landlord-id",
    "external_tenant_id": "your-tenant-id",
    "external_deal_id": "your-deal-id",
    "tenant": {
      "email": "tenant@example.com",
      "first_name": "Jane",
      "last_name": "Doe"
    },
    "status": "processing",
    "submitted_at": "2024-01-15T10:25:00Z",
    "estimated_completion": "2024-01-15T10:30:00Z"
  }
}
```

---

### screening.payment_captured

Sent when payment is successfully charged.

```json
{
  "event": "screening.payment_captured",
  "timestamp": "2024-01-15T10:26:00Z",
  "webhook_id": "wh_pay_captured_abc123",
  "api_version": "2024-01",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "your-landlord-id",
    "external_tenant_id": "your-tenant-id",
    "payment": {
      "amount": 2249,
      "tax": 292,
      "total": 2541,
      "currency": "CAD",
      "method": {
        "type": "card",
        "brand": "visa",
        "last_4": "4242"
      },
      "paid_by": "landlord"
    },
    "charged_at": "2024-01-15T10:26:00Z"
  }
}
```

#### Payment Fields

| Field | Type | Description |
|-------|------|-------------|
| `payment.amount` | integer | Base amount in cents |
| `payment.tax` | integer | Tax in cents |
| `payment.total` | integer | Total charged in cents |
| `payment.currency` | string | Currency code |
| `payment.method.type` | string | `"card"`, `"invoice"` |
| `payment.method.brand` | string | Card brand |
| `payment.method.last_4` | string | Last 4 digits |
| `payment.paid_by` | string | `"landlord"` or `"tenant"` |

---

### screening.failed

Sent when screening cannot be completed.

```json
{
  "event": "screening.failed",
  "timestamp": "2024-01-15T10:35:00Z",
  "webhook_id": "wh_scr_failed_abc123",
  "api_version": "2024-01",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "your-landlord-id",
    "external_tenant_id": "your-tenant-id",
    "tenant": {
      "email": "tenant@example.com",
      "first_name": "Jane",
      "last_name": "Doe"
    },
    "failure": {
      "status": "failed",
      "reason": "credit_bureau_unavailable",
      "message": "Unable to retrieve credit report from Equifax",
      "errors": [
        "Credit bureau returned error: Service temporarily unavailable",
        "Retry recommended in 30 minutes"
      ],
      "recoverable": true
    },
    "failed_at": "2024-01-15T10:35:00Z"
  }
}
```

#### Failure Reason Codes

| Code | Description |
|------|-------------|
| `credit_bureau_unavailable` | Credit bureau service is down |
| `identity_verification_failed` | Could not verify tenant identity |
| `invalid_sin_ssn` | SIN/SSN validation failed |
| `address_verification_failed` | Could not verify address |
| `payment_failed` | Payment was declined |
| `data_validation_error` | Submitted data has errors |
| `timeout` | Processing timed out |

---

### form.opened

Sent when tenant opens the application form.

```json
{
  "event": "form.opened",
  "timestamp": "2024-01-15T09:00:00Z",
  "webhook_id": "wh_form_opened_abc123",
  "api_version": "2024-01",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "your-landlord-id",
    "external_tenant_id": "your-tenant-id",
    "tenant": {
      "email": "tenant@example.com"
    },
    "form": {
      "type": "tenant_application",
      "url": "https://platform.singlekey.com/screen/tenant?token=ABC123"
    },
    "opened_at": "2024-01-15T09:00:00Z",
    "source": {
      "ip": "192.168.1.1",
      "user_agent": "Mozilla/5.0...",
      "referrer": "https://email.provider.com"
    }
  }
}
```

---

### invite.sent

Sent when invitation email/SMS is delivered.

```json
{
  "event": "invite.sent",
  "timestamp": "2024-01-15T08:30:00Z",
  "webhook_id": "wh_invite_sent_abc123",
  "api_version": "2024-01",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "your-landlord-id",
    "external_tenant_id": "your-tenant-id",
    "tenant": {
      "email": "tenant@example.com",
      "phone": "5551234567"
    },
    "invite": {
      "type": "email",
      "recipient": "tenant@example.com",
      "subject": "Complete Your Rental Application",
      "form_url": "https://platform.singlekey.com/screen/tenant?token=ABC123"
    },
    "sent_at": "2024-01-15T08:30:00Z"
  }
}
```

#### Invite Types

| Type | Description |
|------|-------------|
| `email` | Email invitation sent |
| `sms` | SMS invitation sent |
| `reminder` | Reminder notification sent |

---

### invite.opened

Sent when tenant opens the invitation email.

```json
{
  "event": "invite.opened",
  "timestamp": "2024-01-15T08:45:00Z",
  "webhook_id": "wh_invite_opened_abc123",
  "api_version": "2024-01",
  "data": {
    "purchase_token": "abc123def456ghi789jkl012mno345pq",
    "external_customer_id": "your-landlord-id",
    "external_tenant_id": "your-tenant-id",
    "tenant": {
      "email": "tenant@example.com"
    },
    "invite": {
      "type": "email",
      "opened_count": 1
    },
    "opened_at": "2024-01-15T08:45:00Z"
  }
}
```

---

## Signature Verification

### Algorithm

Signatures are computed using HMAC-SHA256:

```
signature = HMAC-SHA256(webhook_secret, raw_request_body)
```

### Verification Examples

**Python:**
```python
import hmac
import hashlib

def verify_signature(payload_body, signature, secret):
    expected = hmac.new(
        secret.encode('utf-8'),
        payload_body.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)
```

**Node.js:**
```javascript
const crypto = require('crypto');

function verifySignature(payloadBody, signature, secret) {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(payloadBody, 'utf8')
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(signature)
  );
}
```

**PHP:**
```php
function verifySignature($payloadBody, $signature, $secret) {
    $expected = hash_hmac('sha256', $payloadBody, $secret);
    return hash_equals($expected, $signature);
}
```

**Ruby:**
```ruby
require 'openssl'

def verify_signature(payload_body, signature, secret)
  expected = OpenSSL::HMAC.hexdigest('SHA256', secret, payload_body)
  Rack::Utils.secure_compare(expected, signature)
end
```

---

## Timestamp Validation

To prevent replay attacks, validate the timestamp is recent:

```python
import time

def validate_timestamp(timestamp_header, tolerance_seconds=300):
    webhook_time = int(timestamp_header)
    current_time = int(time.time())
    return abs(current_time - webhook_time) < tolerance_seconds
```

---

## See Also

- [Webhook Events Overview](./events.md)
- [Integration Guides](../integration-guides/)
- [Troubleshooting](../troubleshooting/error-codes.md)
