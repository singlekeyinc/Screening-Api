# Get Screening Report

`GET /api/report/<purchase_token>`

Retrieve screening report data, status, and results.

## Authentication

| Header | Value |
|--------|-------|
| `Authorization` | `Token <your_api_token>` |

## Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `purchase_token` | string | Yes | 32-character token from screening request |

## Request

```bash
curl -X GET "https://platform.singlekey.com/api/report/abc123def456ghi789jkl012mno345pq" \
  -H "Authorization: Token your_api_token"
```

---

## Response States

### Report Complete

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "cost": 2249,
  "tax_collected": 292,
  "currency": "CAD",
  "date_created": "Jan 15/2024, 10:30AM",
  "external_customer_id": "landlord-123",
  "external_deal_id": "deal-abc",
  "landlord_email": "landlord@example.com",
  "external_tenant_id": "tenant-456",
  "tenant_email": "tenant@example.com",
  "credit_card_last_4": "4242",
  "landlord_has_tenant_info": true,
  "tenant_pays": false,
  "embedded_flow_request": true,
  "api_only_purchase": false,
  "partial": false,
  "pdf_report_ready": true,
  "report_url": "https://s3.amazonaws.com/singlekey-reports/...",
  "html_report_url": "https://platform.singlekey.com/report/view/...",
  "singlekey_score": 720
}
```

### Report In Progress

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "detail": "Report creation in progress",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

### Waiting for Tenant Submission

```json
{
  "success": false,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "detail": "Tenant has not submitted invite. They have not opened their invite email.",
  "payment_status": "on hold, payment will be captured on submission",
  "form_url": "https://platform.singlekey.com/screen/landlord?token=XYZ",
  "tenant_form_url": "https://platform.singlekey.com/screen/tenant?token=ABC"
}
```

### Waiting for Landlord Submission

```json
{
  "success": false,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "detail": "Landlord has not submitted form",
  "payment_status": "landlord has not submitted",
  "form_url": "https://platform.singlekey.com/screen/landlord?token=XYZ"
}
```

### Submission Errors

```json
{
  "success": false,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "detail": "Submission contains errors",
  "errors": [
    "Invalid date of birth",
    "Address could not be verified"
  ],
  "form_url": "https://platform.singlekey.com/screen/landlord?token=XYZ"
}
```

---

## Response Fields

### Report Data (Complete)

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | `true` when report is complete |
| `purchase_token` | string | Unique screening identifier |
| `singlekey_score` | integer | Credit score (300-900), or `null` |
| `report_url` | string | S3 URL for PDF report (expires in 5 days) |
| `html_report_url` | string | Web-viewable report URL |
| `pdf_report_ready` | boolean | Whether PDF is available |

### Cost Information

| Field | Type | Description |
|-------|------|-------------|
| `cost` | integer | Charge amount in cents |
| `tax_collected` | integer | Tax amount in cents |
| `currency` | string | `"CAD"` or `"USD"` |

### Identifiers

| Field | Type | Description |
|-------|------|-------------|
| `external_customer_id` | string | Your landlord ID |
| `external_tenant_id` | string | Your tenant ID |
| `external_deal_id` | string | Your deal ID |
| `landlord_email` | string | Landlord's email |
| `tenant_email` | string | Tenant's email |

### Payment Information

| Field | Type | Description |
|-------|------|-------------|
| `credit_card_last_4` | string | Last 4 digits of card used |
| `payment_status` | string | Current payment status |
| `tenant_pays` | boolean | Whether tenant paid |

### Flow Information

| Field | Type | Description |
|-------|------|-------------|
| `landlord_has_tenant_info` | boolean | Landlord provided tenant data |
| `embedded_flow_request` | boolean | Used embedded form flow |
| `api_only_purchase` | boolean | Direct API (no forms) |
| `partial` | boolean | Some data unavailable |
| `date_created` | string | When screening was created |

### Status Fields (In Progress)

| Field | Type | Description |
|-------|------|-------------|
| `detail` | string | Current status message |
| `form_url` | string | Landlord form URL |
| `tenant_form_url` | string | Tenant form URL |
| `errors` | array | Validation errors (if any) |

---

## Payment Status Values

| Status | Meaning |
|--------|---------|
| `"paid"` | Payment captured, screening funded |
| `"landlord has not submitted"` | Waiting for landlord form |
| `"on hold, payment will be captured on submission"` | Authorized, pending tenant |
| `"unpaid"` | Payment not received |

---

## Status Messages

| Message | Meaning | Next Step |
|---------|---------|-----------|
| `"Report creation in progress"` | Processing | Wait 2-3 minutes |
| `"Tenant has not submitted invite"` | Waiting for tenant | Send reminder |
| `"They have not opened their invite email"` | Email not opened | Verify email |
| `"They have opened their invite email"` | Email opened | Wait for submission |
| `"Landlord has not submitted form"` | Waiting for landlord | Direct to form |
| `"Submission contains errors"` | Validation failed | Fix and resubmit |

---

## Report URL Expiration

The `report_url` (S3 pre-signed URL) expires after **5 days**. Call this endpoint again to get a fresh URL.

```python
# Get fresh URL
response = requests.get(
    f"https://platform.singlekey.com/api/report/{token}",
    headers={"Authorization": f"Token {API_TOKEN}"}
)
fresh_url = response.json()["report_url"]
```

---

## HTTP Status Codes

| Status | Description |
|--------|-------------|
| `200` | Success (check `success` field for completion) |
| `401` | Invalid or missing token |
| `404` | Screening not found |
| `500` | Server error |

---

## Polling Example

```python
import time
import requests

def wait_for_report(token, api_token, timeout=300, interval=10):
    """Poll until report is ready."""
    start = time.time()

    while time.time() - start < timeout:
        response = requests.get(
            f"https://platform.singlekey.com/api/report/{token}",
            headers={"Authorization": f"Token {api_token}"}
        )

        data = response.json()

        if data.get("success") and data.get("singlekey_score"):
            return data

        print(f"Status: {data.get('detail', 'Processing...')}")
        time.sleep(interval)

    raise TimeoutError("Report not ready")

# Usage
report = wait_for_report("abc123...", "your_token")
print(f"Score: {report['singlekey_score']}")
```

---

## See Also

- [Download Report PDF](./report-pdf.md)
- [Get Applicant Data](./applicant.md)
- [Webhook Events](../webhooks/events.md)
