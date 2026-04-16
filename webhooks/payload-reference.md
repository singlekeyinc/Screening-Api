# Webhook Payload Reference

Complete reference for all webhook payload structures.

## Request Format

All webhooks are sent as `POST` requests with the `purchase_token` appended as a query parameter:

```
POST <your_webhook_url>?pt=<purchase_token>
```

---

## Headers

| Header | Description | Example |
|--------|-------------|---------|
| `Content-Type` | Always `application/json` | `application/json` |
| `Handshake-Token` | Your handshake token (if configured in Partner Portal) | `your_handshake_token` |

---

## Payload Structure

All webhooks share the same payload format:

```json
{
  "detail": "<event description>",
  "purchase_token": "<purchase_token>",
  "external_customer_id": "<your_customer_id>",
  "external_tenant_id": "<your_tenant_id>"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `detail` | string | Describes the event (see values below) |
| `purchase_token` | string | Unique 32-character screening identifier |
| `external_customer_id` | string | Your landlord/property manager identifier |
| `external_tenant_id` | string | Your tenant identifier |

---

## Webhook Types

### Request Sent to Tenant

SingleKey has emailed the application to the tenant.

**Detail value:** `"Request sent to tenant"`

```json
{
  "detail": "Request sent to tenant",
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

---

### Tenant Email Opened

The tenant has opened their invitation email and started the application.

**Detail value:** `"Tenant email opened"`

```json
{
  "detail": "Tenant email opened",
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

---

### Report in Progress

The tenant has submitted their application and the screening is now processing.

**Detail value:** `"Report in Progress"`

```json
{
  "detail": "Report in Progress",
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

---

### Partial Report Complete

The credit bureau portion of the report is complete, but SingleKey is still waiting on additional information from the tenant.

**Detail value:** `"Partial Report Complete"`

```json
{
  "detail": "Partial Report Complete",
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

You can fetch the partial report at this point via `GET /api/report/<purchase_token>`.

---

### Report Complete

The full screening report is ready for retrieval.

**Detail value:** `"Report Complete"`

```json
{
  "detail": "Report Complete",
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

Fetch the completed report via `GET /api/report/<purchase_token>`.

---

## Detail Values Quick Reference

| `detail` Value | Meaning |
|----------------|---------|
| `"Request sent to tenant"` | Invitation emailed to tenant |
| `"Tenant email opened"` | Tenant opened email / started application |
| `"Report in Progress"` | Tenant submitted, screening processing |
| `"Partial Report Complete"` | Credit data ready, waiting on tenant for rest |
| `"Report Complete"` | Full report ready |

---

## Authentication

If you have configured a **Handshake Token** in your Partner Portal, it is included in the `Handshake-Token` header of every webhook request.

Verify it on your end to confirm the request is from SingleKey:

```python
HANDSHAKE_TOKEN = "your_handshake_token"

def verify_webhook(request):
    token = request.headers.get('Handshake-Token', '')
    return token == HANDSHAKE_TOKEN
```

```javascript
const HANDSHAKE_TOKEN = 'your_handshake_token';

function verifyWebhook(req) {
  return req.headers['handshake-token'] === HANDSHAKE_TOKEN;
}
```

---

## Retry Behavior

If your endpoint returns a non-success status code, the **Report Complete** webhook is retried once automatically. Other webhook types are not retried.

If you are not receiving webhooks, check:
1. Your webhook URL is correct in the Partner Portal
2. Your endpoint is publicly accessible over HTTPS
3. Your endpoint returns a `200` status code within 30 seconds

---

## See Also

- [Webhook Events Overview](./events.md)
- [Webhook Integration Guide](../integration-guides/webhook-integration.md)
- [Troubleshooting](../troubleshooting/error-codes.md)
