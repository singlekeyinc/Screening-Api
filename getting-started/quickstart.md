# Quickstart Guide

Get started with the SingleKey Screening API in minutes.

## Prerequisites

- SingleKey API token (contact your account manager)
- HTTPS endpoint for webhooks (optional but recommended)

## Choose Your Integration

| Integration | Best For | Data Collection |
|-------------|----------|-----------------|
| **Form-Based** | Minimal data handling | SingleKey forms |
| **Direct API** | Full control | Your application |

---

## Option 1: Form-Based Integration (Easiest)

Let SingleKey handle data collection through hosted forms.

### Step 1: Create a Request

```bash
curl -X POST "https://sandbox.singlekey.com/api/request" \
  -H "Authorization: Token YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-456",
    "tenant_form": true,
    "ten_email": "tenant@example.com",
    "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
    "callback_url": "https://yoursite.com/webhooks"
  }'
```

### Step 2: Handle Response

```json
{
  "success": true,
  "purchase_token": "abc123def456...",
  "tenant_form_url": "https://platform.singlekey.com/screen/tenant?token=XYZ"
}
```

### Step 3: Redirect Tenant

Send the tenant to `tenant_form_url` to complete their application.

### Step 4: Receive Webhook

When complete, you'll receive:

```json
{
  "event": "screening.completed",
  "data": {
    "purchase_token": "abc123def456...",
    "singlekey_score": 720
  }
}
```

### Step 5: Fetch Report

```bash
curl -X GET "https://sandbox.singlekey.com/api/report/abc123def456..." \
  -H "Authorization: Token YOUR_API_TOKEN"
```

---

## Option 2: Direct API Integration

Submit all tenant data directly for immediate processing.

### Step 1: Create Request with Full Data

```bash
curl -X POST "https://sandbox.singlekey.com/api/request" \
  -H "Authorization: Token YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-456",
    "run_now": true,

    "ll_first_name": "John",
    "ll_last_name": "Smith",
    "ll_email": "landlord@example.com",

    "ten_first_name": "Jane",
    "ten_last_name": "Doe",
    "ten_email": "tenant@example.com",
    "ten_tel": "5551234567",
    "ten_dob_year": 1990,
    "ten_dob_month": 6,
    "ten_dob_day": 15,
    "ten_address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
    "ten_sin": "123456789",

    "callback_url": "https://yoursite.com/webhooks"
  }'
```

### Step 2: Handle Response

```json
{
  "success": true,
  "purchase_token": "abc123def456...",
  "detail": "Screening request submitted"
}
```

### Step 3: Wait for Completion

Poll the report endpoint or wait for webhook:

```bash
# Poll every 10 seconds until ready
curl -X GET "https://sandbox.singlekey.com/api/report/abc123def456..." \
  -H "Authorization: Token YOUR_API_TOKEN"
```

### Step 4: Get Complete Report

```json
{
  "success": true,
  "purchase_token": "abc123def456...",
  "singlekey_score": 720,
  "report_url": "https://s3.amazonaws.com/...",
  "cost": 2249,
  "currency": "CAD"
}
```

---

## Quick Code Examples

### Python

```python
import requests

API_TOKEN = "YOUR_API_TOKEN"
BASE_URL = "https://sandbox.singlekey.com"

# Create screening
response = requests.post(
    f"{BASE_URL}/api/request",
    headers={
        "Authorization": f"Token {API_TOKEN}",
        "Content-Type": "application/json"
    },
    json={
        "external_customer_id": "landlord-123",
        "external_tenant_id": "tenant-456",
        "run_now": True,
        "ll_first_name": "John",
        "ll_last_name": "Smith",
        "ll_email": "landlord@example.com",
        "ten_first_name": "Jane",
        "ten_last_name": "Doe",
        "ten_email": "tenant@example.com",
        "ten_tel": "5551234567",
        "ten_dob_year": 1990,
        "ten_dob_month": 6,
        "ten_dob_day": 15,
        "ten_address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
        "ten_sin": "123456789"
    }
)

result = response.json()
print(f"Token: {result['purchase_token']}")
```

### JavaScript

```javascript
const response = await fetch('https://sandbox.singlekey.com/api/request', {
  method: 'POST',
  headers: {
    'Authorization': 'Token YOUR_API_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    external_customer_id: 'landlord-123',
    external_tenant_id: 'tenant-456',
    run_now: true,
    ll_first_name: 'John',
    ll_last_name: 'Smith',
    ll_email: 'landlord@example.com',
    ten_first_name: 'Jane',
    ten_last_name: 'Doe',
    ten_email: 'tenant@example.com',
    ten_tel: '5551234567',
    ten_dob_year: 1990,
    ten_dob_month: 6,
    ten_dob_day: 15,
    ten_address: '456 Oak Ave, Toronto, ON, Canada, M5V 2B3',
    ten_sin: '123456789'
  })
});

const result = await response.json();
console.log(`Token: ${result.purchase_token}`);
```

---

## Common Issues

| Problem | Solution |
|---------|----------|
| 401 Unauthorized | Check token has `Token ` prefix |
| 400 Validation Error | Check `errors` array in response |
| Phone format | Use string: `"5551234567"` not integer |
| Address error | Include commas: `"Street, City, Province, Country, Postal"` |

---

## Next Steps

1. **Test in Sandbox**: Use `sandbox.singlekey.com` and test tokens
2. **Set Up Webhooks**: Implement webhook handler for real-time updates
3. **Go Live**: Switch to production URL and tokens

---

## Helpful Resources

| Resource | Link |
|----------|------|
| Full API Reference | [api-reference/](../api-reference/) |
| Field Validation | [fields/validation-rules.md](../fields/validation-rules.md) |
| Integration Guides | [integration-guides/](../integration-guides/) |
| Code Examples | [examples/](../examples/) |
| Troubleshooting | [troubleshooting/](../troubleshooting/) |

---

## Get Help

- API Support: `api-support@singlekey.com`
- Documentation Issues: Open a GitHub issue
- Account Questions: Contact your account manager
