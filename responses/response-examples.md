# Response Examples

Example responses for common API scenarios.

---

## Create Screening Request

`POST /api/request`

### Initial Request - Landlord Form

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "payment_status": "landlord has not submitted",
  "created": "2025-01-15T10:30:00.000000+00:00",
  "form_url": "https://platform.singlekey.com/screen/request?purchase_token=abc123..."
}
```

### Initial Request - Tenant Form

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "payment_status": "on hold, payment will be captured on submission",
  "created": "2025-01-15T10:30:00.000000+00:00",
  "tenant_form": true,
  "form_url": "https://app.singlekey.com/t/listings/.../applications/new?tenant_token=..."
}
```

### Initial Request - Immediate Screening

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "payment_status": "paid",
  "created": "2025-01-15T10:30:00.000000+00:00",
  "initiated": true
}
```

---

## Fetch Report

`GET /api/report/<purchase_token>`

### Tenant Invited - Email Not Opened

```json
{
  "success": true,
  "detail": "Tenant has not submitted invite. They have not opened their invite email.",
  "created": "2025-01-15T10:30:00.000000+00:00",
  "form_url": "https://platform.singlekey.com/screen/request?purchase_token=abc123...",
  "tenant_form_url": "https://platform.singlekey.com/screen/tenant?token=XYZ789"
}
```

### Tenant Invited - Email Opened

```json
{
  "success": true,
  "detail": "Tenant has not submitted invite. They have opened their invite email.",
  "created": "2025-01-15T10:30:00.000000+00:00",
  "form_url": "https://platform.singlekey.com/screen/request?purchase_token=abc123...",
  "tenant_form_url": "https://platform.singlekey.com/screen/tenant?token=XYZ789"
}
```

### Report Processing

```json
{
  "success": true,
  "detail": "Report creation in progress",
  "created": "2025-01-15T10:30:00.000000+00:00"
}
```

### Report Complete

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "cost": 2249,
  "tax_collected": 292,
  "currency": "CAD",
  "date_created": "Jan 15/2025, 10:30AM",
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
  "report_url": "https://s3.amazonaws.com/.../report.pdf?...",
  "singlekey_score": 720
}
```

### Submission Has Errors

```json
{
  "success": false,
  "detail": "missing or incomplete data",
  "errors": [
    "1232133: SIN numbers must be 9 digits long"
  ],
  "created": "2025-01-15T10:30:00.000000+00:00",
  "form_url": "https://platform.singlekey.com/screen/tenant?token=XYZ789",
  "tenant_form_url": "https://platform.singlekey.com/screen/tenant?token=XYZ789"
}
```

> **Note:** When errors exist, the tenant form is marked as unsubmitted so the tenant can return and fix the errors.

---

## Get Applicant Data

`GET /api/applicant/<purchase_token>`

```json
{
  "ten_first_name": "Jane",
  "ten_middle_names": null,
  "ten_last_name": "Doe",
  "ten_email": "tenant@example.com",
  "ten_tel": "5551234567",
  "ten_dob_day": "15",
  "ten_dob_month": "6",
  "ten_dob_year": "1990",
  "ten_address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
  "ten_previous_addresses": [
    "789 Pine St, Vancouver, BC, Canada, V6B 1A1"
  ],
  "ten_employments": [
    {
      "job_title": "Software Engineer",
      "employer": "Tech Corp",
      "employment_length": "3 Years",
      "income": 85000
    }
  ],
  "ten_annual_income": 85000,
  "ten_household_income": 85000,
  "ten_pets": [
    {
      "type": "dog",
      "breed": "Golden Retriever"
    }
  ],
  "ten_automobiles": [
    {
      "make": "Toyota",
      "model": "Camry"
    }
  ],
  "ten_smoke": false,
  "ten_refused_to_pay_rent": false,
  "ten_bankruptcy": false,
  "ten_evicted": false,
  "ten_given_notice": true,
  "ten_additional_info": "I am a quiet and respectful tenant."
}
```

---

## Error Responses

### Validation Error (400)

```json
{
  "success": false,
  "detail": "missing or incomplete data",
  "errors": [
    "ten_email: the email --invalid_email-- is not formatted like an email",
    "ten_tel: the phone number --555-- is not the expected length"
  ]
}
```

### Authentication Error (401)

```json
{
  "detail": "Invalid token."
}
```

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Not Found Error (404)

```json
{
  "success": false,
  "detail": "Report does not exist",
  "errors": [
    "Report does not exist"
  ]
}
```

---

## Payment Status Values

| Status | Description |
|--------|-------------|
| `"paid"` | Screening is funded |
| `"landlord has not submitted"` | Landlord form not yet submitted |
| `"on hold, payment will be captured on submission"` | Payment authorized, pending tenant submission |
| `"unpaid"` | No payment received |

---

## See Also

- [Status Codes and Errors](./status-codes-and-errors.md)
- [Create Request Route](../routes/request-route.md)
- [Fetch Report Route](../routes/fetch-report-route.md)
