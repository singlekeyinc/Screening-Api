# Create Screening Request

`POST /api/request` or `POST /screen/embedded_flow_request`

Create a new tenant screening request. This endpoint supports three request modes.

## Authentication

| Header | Value |
|--------|-------|
| `Authorization` | `Token <your_api_token>` |
| `Content-Type` | `application/json` |

---

## Request Modes

| Mode | Description | Key Parameter |
|------|-------------|---------------|
| **Landlord Form** | Returns form URL for landlord to complete | Default |
| **Tenant Form** | Returns direct tenant application form | `tenant_form: true` |
| **Immediate Screening** | Processes screening instantly | `run_now: true` |

All request modes return a `purchase_token` that identifies the screening.

---

## 1. Landlord Form Request

Retrieve a form to redirect landlords to. The landlord can then:
- Send an invite to the tenant to complete the application
- Initiate screening directly (with tenant's consent and required information)

### Minimum Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `ll_first_name` | string | Landlord's first name |
| `ll_last_name` | string | Landlord's last name |
| `ll_email` | string | Landlord's email |
| `ten_first_name` | string | Tenant's first name |
| `ten_last_name` | string | Tenant's last name |
| `ten_email` | string | Tenant's email |

### Example Request

```bash
curl -X POST "https://platform.singlekey.com/api/request" \
  -H "Authorization: Token your_api_token" \
  -H "Content-Type: application/json" \
  -d '{
    "ll_first_name": "John",
    "ll_last_name": "Smith",
    "ll_email": "landlord@example.com",
    "ten_first_name": "Jane",
    "ten_last_name": "Doe",
    "ten_email": "tenant@example.com"
  }'
```

### Example Response

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "payment_status": "landlord has not submitted",
  "created": "2025-01-09T19:40:26.632576+00:00",
  "form_url": "https://platform.singlekey.com/screen/request?purchase_token=abc123..."
}
```

> **Note:** The landlord will be required to enter additional information about the tenant and property before submitting the form.

---

## 2. Tenant Form Request

Retrieve a form URL to send directly to the tenant. Include `tenant_form: true` in your request.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `ll_first_name` | string | Landlord's first name |
| `ll_last_name` | string | Landlord's last name |
| `ll_email` | string | Landlord's email |
| `ten_first_name` | string | Tenant's first name |
| `ten_last_name` | string | Tenant's last name |
| `ten_email` | string | Tenant's email |
| `purchase_address` | string | Property address (for jurisdiction) |
| `tenant_form` | boolean | Must be `true` |

### Example Request

```bash
curl -X POST "https://platform.singlekey.com/api/request" \
  -H "Authorization: Token your_api_token" \
  -H "Content-Type: application/json" \
  -d '{
    "ll_first_name": "John",
    "ll_last_name": "Smith",
    "ll_email": "landlord@example.com",
    "ten_first_name": "Jane",
    "ten_last_name": "Doe",
    "ten_email": "tenant@example.com",
    "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
    "tenant_form": true
  }'
```

### Example Response

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "payment_status": "on hold, payment will be captured on submission",
  "created": "2025-01-09T19:56:09.920818+00:00",
  "tenant_form": true,
  "form_url": "https://app.singlekey.com/t/listings/.../applications/new?tenant_token=..."
}
```

> **Note:** The `purchase_address` is required to determine the jurisdiction of the transaction.

---

## 3. Immediate Screening Request

Screen an applicant immediately without forms. Requires all tenant data and consent. Include `run_now: true` in your request.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `ll_first_name` | string | Landlord's first name |
| `ll_last_name` | string | Landlord's last name |
| `ll_email` | string | Landlord's email |
| `ten_first_name` | string | Tenant's first name |
| `ten_last_name` | string | Tenant's last name |
| `ten_email` | string | Tenant's email |
| `ten_address` | string | Tenant's current address |
| `ten_dob_year` | integer | Birth year (4 digits) |
| `ten_dob_month` | integer | Birth month (1-12) |
| `ten_dob_day` | integer | Birth day (1-31) |
| `purchase_address` | string | Property address |
| `run_now` | boolean | Must be `true` |

### Example Request

```bash
curl -X POST "https://platform.singlekey.com/api/request" \
  -H "Authorization: Token your_api_token" \
  -H "Content-Type: application/json" \
  -d '{
    "ll_first_name": "John",
    "ll_last_name": "Smith",
    "ll_email": "landlord@example.com",
    "ten_first_name": "Jane",
    "ten_last_name": "Doe",
    "ten_email": "tenant@example.com",
    "ten_address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
    "ten_dob_year": 1990,
    "ten_dob_month": 6,
    "ten_dob_day": 15,
    "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
    "run_now": true
  }'
```

### Example Response

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "payment_status": "paid",
  "created": "2025-01-09T20:01:58.642255+00:00",
  "initiated": true
}
```

---

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Request was successful |
| `purchase_token` | string | Unique 32-character identifier for this screening |
| `payment_status` | string | Current payment status (see below) |
| `created` | string | ISO 8601 timestamp |
| `form_url` | string | Landlord form URL (if applicable) |
| `tenant_form_url` | string | Tenant form URL (if applicable) |
| `initiated` | boolean | Screening has started processing (run_now mode) |

---

## Payment Status Values

| Status | Description |
|--------|-------------|
| `"paid"` | Screening is funded (immediate billing, monthly billing, or credits) |
| `"landlord has not submitted"` | Landlord form obtained but not yet submitted |
| `"on hold, payment will be captured on submission"` | Payment authorized, captured when tenant submits (5-day hold) |
| `"unpaid"` | No payment received (tenant invite sent, awaiting payment) |

---

## Additional Fields

You can include any field from the [Available Fields Reference](../fields/available-fields.md) to pre-populate forms or provide additional data.

### Common Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `external_customer_id` | string | Your landlord ID |
| `external_tenant_id` | string | Your tenant ID |
| `external_deal_id` | string | Your CRM deal ID |
| `ll_tel` | string | Landlord phone number |
| `ten_tel` | string | Tenant phone number |
| `purchase_rent` | integer | Monthly rent amount |
| `callback_url` | string | Webhook URL for notifications |

---

## See Also

- [Get Report](./fetch-report-route.md)
- [Get Applicant Data](./applicant-data-route.md)
- [Available Fields](../fields/available-fields.md)
- [Response Examples](../responses/responses.md)
