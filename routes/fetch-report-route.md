# Fetch Screening Report

`GET /api/report/<purchase_token>` or `GET /screen/embedded_flow_get_report/<purchase_token>`

Retrieve a screening report. Returns status updates if the report is not yet ready.

## Authentication

| Header | Value |
|--------|-------|
| `Authorization` | `Token <your_api_token>` |

## Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `purchase_token` | string | 32-character token from screening request |

---

## Response States

The response depends on the current state of the screening.

### 1. Report Not Ready

If the report is still processing, the response provides status updates.

#### Tenant Invited - Email Not Opened

```json
{
  "success": true,
  "detail": "Tenant has not submitted invite. They have not opened their invite email.",
  "created": "2024-12-29T16:07:31.728743+00:00",
  "form_url": "https://platform.singlekey.com/screen/request?purchase_token=abc123...",
  "tenant_form_url": "https://platform.singlekey.com/screen/tenant?token=XYZ789"
}
```

#### Tenant Invited - Email Opened

```json
{
  "success": true,
  "detail": "Tenant has not submitted invite. They have opened their invite email.",
  "created": "2024-12-29T16:07:31.728743+00:00",
  "form_url": "https://platform.singlekey.com/screen/request?purchase_token=abc123...",
  "tenant_form_url": "https://platform.singlekey.com/screen/tenant?token=XYZ789"
}
```

#### Report Processing

```json
{
  "success": true,
  "detail": "Report creation in progress",
  "created": "2024-12-29T16:07:31.728743+00:00"
}
```

#### Submission Errors

When there are validation errors, the tenant form is marked as unsubmitted so they can fix the errors.

```json
{
  "success": false,
  "detail": "missing or incomplete data",
  "errors": [
    "1232133: SIN numbers must be 9 digits long"
  ],
  "created": "2024-12-29T16:07:31.728743+00:00",
  "form_url": "https://platform.singlekey.com/screen/tenant?token=XYZ789",
  "tenant_form_url": "https://platform.singlekey.com/screen/tenant?token=XYZ789"
}
```

### Status Detail Values

| Detail | Meaning |
|--------|---------|
| `"missing or incomplete data"` | Submission has errors that need to be fixed |
| `"Tenant has not submitted invite. They have not opened their invite email."` | Waiting for tenant, email not opened |
| `"Tenant has not submitted invite. They have opened their invite email."` | Tenant opened email but hasn't submitted |
| `"Report creation in progress"` | All data submitted, report being generated |

---

### 2. Report Complete

When the report is ready, you receive full details.

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "cost": 2999,
  "tax_collected": 0,
  "currency": "USD",
  "date_created": "Jan 08/2025, 01:07PM",
  "external_customer_id": "landlord-123",
  "external_deal_id": "deal-abc",
  "landlord_email": "landlord@example.com",
  "external_tenant_id": "tenant-456",
  "tenant_email": "tenant@example.com",
  "credit_card_last_4": null,
  "landlord_has_tenant_info": false,
  "tenant_pays": true,
  "embedded_flow_request": true,
  "api_only_purchase": false,
  "partial": false,
  "report_url": "https://s3.amazonaws.com/.../report.pdf?...",
  "singlekey_score": 720
}
```

---

## Response Fields (Complete Report)

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Always `true` for complete reports |
| `purchase_token` | string | Unique 32-character identifier |
| `cost` | integer | Screening cost before tax (in cents) |
| `tax_collected` | integer | Tax amount (in cents) |
| `currency` | string | `"CAD"` or `"USD"` |
| `date_created` | string | When screening was created |
| `external_customer_id` | string | Your landlord ID |
| `external_deal_id` | string | Your deal ID (if provided) |
| `landlord_email` | string | Landlord's email |
| `external_tenant_id` | string | Your tenant ID |
| `tenant_email` | string | Tenant's email |
| `credit_card_last_4` | string | Last 4 digits of card used (if applicable) |
| `landlord_has_tenant_info` | boolean | Landlord used self-serve screening |
| `tenant_pays` | boolean | Tenant paid for screening |
| `embedded_flow_request` | boolean | Used embedded form flow |
| `api_only_purchase` | boolean | Used direct API (no forms) |
| `partial` | boolean | Credit data received, background check pending |
| `report_url` | string | S3 URL to PDF report (expires in 5 days) |
| `singlekey_score` | integer | SingleKey credit score (300-900) or `null` |

---

## Response Fields (In Progress)

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Request status |
| `detail` | string | Current status message |
| `created` | string | When screening was created |
| `form_url` | string | Landlord form URL |
| `tenant_form_url` | string | Tenant form URL |
| `errors` | array | Validation errors (if any) |

---

## Report URL Expiration

The `report_url` is a pre-signed S3 URL that expires after **5 days**. Each time you call this endpoint, you receive a fresh URL.

```python
# Get a fresh URL whenever needed
response = requests.get(
    f"https://platform.singlekey.com/api/report/{token}",
    headers={"Authorization": f"Token {API_TOKEN}"}
)
fresh_url = response.json()["report_url"]
```

---

## Partial Reports

When `partial: true`, the credit report is available but background check is still processing:
- A PDF report is available immediately
- When the background check completes, the PDF is replaced
- You will receive a webhook notification when the full report is ready

---

## Example Request

```bash
curl -X GET "https://platform.singlekey.com/api/report/abc123def456ghi789jkl012mno345pq" \
  -H "Authorization: Token your_api_token"
```

---

## HTTP Status Codes

| Status | Description |
|--------|-------------|
| `200` | Success (check response for report status) |
| `401` | Invalid or missing authentication token |
| `404` | Report does not exist |

---

## See Also

- [Create Request](./request-route.md)
- [Get Applicant Data](./applicant-data-route.md)
- [Response Examples](../responses/responses.md)
