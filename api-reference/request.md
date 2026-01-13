# Create Screening Request

`POST /api/request`

Create a new tenant screening request. This is the primary endpoint for initiating screenings.

## Authentication

| Header | Value |
|--------|-------|
| `Authorization` | `Token <your_api_token>` |
| `Content-Type` | `application/json` |

## Request Modes

| Mode | Description | Key Parameter |
|------|-------------|---------------|
| **Form-Based (Landlord)** | Landlord receives form to complete | Default (no special flag) |
| **Form-Based (Tenant)** | Tenant receives direct application form | `tenant_form: true` |
| **Direct API** | Immediate processing with all data | `run_now: true` |

---

## Form-Based Request (Landlord Form)

Minimal data required. Landlord completes the rest via hosted form.

### Request

```bash
curl -X POST "https://platform.singlekey.com/api/request" \
  -H "Authorization: Token your_api_token" \
  -H "Content-Type: application/json" \
  -d '{
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-456",
    "ll_first_name": "John",
    "ll_last_name": "Smith",
    "ll_email": "landlord@example.com",
    "ll_tel": "5551234567",
    "ten_first_name": "Jane",
    "ten_last_name": "Doe",
    "ten_email": "tenant@example.com",
    "callback_url": "https://yoursite.com/webhooks"
  }'
```

### Response

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "form_url": "https://platform.singlekey.com/screen/landlord?token=XYZ789",
  "tenant_form_url": "https://platform.singlekey.com/screen/tenant?token=ABC123",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

---

## Form-Based Request (Tenant Form)

Direct tenant application form. Requires property address for jurisdiction.

### Request

```bash
curl -X POST "https://platform.singlekey.com/api/request" \
  -H "Authorization: Token your_api_token" \
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

### Response

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "tenant_form_url": "https://platform.singlekey.com/screen/tenant?token=ABC123",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

---

## Direct API Request

Submit all data for immediate processing. No forms required.

### Request

```bash
curl -X POST "https://platform.singlekey.com/api/request" \
  -H "Authorization: Token your_api_token" \
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

    "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
    "purchase_rent": 2000,

    "callback_url": "https://yoursite.com/webhooks"
  }'
```

### Response

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456",
  "detail": "Screening request submitted"
}
```

---

## Request Fields

### Always Required

| Field | Type | Description |
|-------|------|-------------|
| `external_customer_id` | string | Your unique landlord/PM identifier |
| `external_tenant_id` | string | Your unique tenant identifier |

### Landlord Information

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ll_first_name` | string | Form/Direct | Landlord first name |
| `ll_last_name` | string | Form/Direct | Landlord last name |
| `ll_email` | string | Form/Direct | Landlord email |
| `ll_tel` | string | Form only | Landlord phone (10 digits) |

### Tenant Information

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ten_first_name` | string | Landlord form, Direct | Tenant first name |
| `ten_last_name` | string | Landlord form, Direct | Tenant last name |
| `ten_email` | string | All modes | Tenant email |
| `ten_tel` | string | Direct only | Tenant phone (10 digits) |
| `ten_dob_year` | integer | Direct only | Birth year (YYYY) |
| `ten_dob_month` | integer | Direct only | Birth month (1-12) |
| `ten_dob_day` | integer | Direct only | Birth day (1-31) |
| `ten_address` | string | Direct only | Current address |
| `ten_sin` | string | Direct (Canada) | 9-digit SIN |

### Property Information

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `purchase_address` | string | Tenant form | Property address |
| `purchase_rent` | integer | Optional | Monthly rent amount |
| `purchase_unit` | string | Optional | Unit/apartment number |

### Control Flags

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `run_now` | boolean | `false` | Process immediately (direct API) |
| `tenant_form` | boolean | `false` | Use tenant form flow |
| `tenant_pays` | boolean | `false` | Tenant provides payment |
| `update` | boolean | `false` | Force new report (bypass cache) |

### Integration

| Field | Type | Description |
|-------|------|-------------|
| `callback_url` | string | Webhook URL for notifications |
| `external_deal_id` | string | Your CRM deal ID |
| `external_listing_id` | string | Your listing ID |
| `promo_code` | string | Promotional code |

---

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Request successful |
| `purchase_token` | string | 32-character unique identifier |
| `form_url` | string | Landlord form URL (if applicable) |
| `tenant_form_url` | string | Tenant form URL |
| `external_customer_id` | string | Echo of your landlord ID |
| `external_tenant_id` | string | Echo of your tenant ID |
| `detail` | string | Status message |

---

## Error Response

```json
{
  "success": false,
  "detail": "Validation failed",
  "errors": [
    "Tenant email is required",
    "Phone must be 10 digits"
  ]
}
```

---

## HTTP Status Codes

| Status | Description |
|--------|-------------|
| `200` | Success |
| `400` | Validation error (check `errors` array) |
| `401` | Invalid or missing token |
| `500` | Server error |

---

## Duplicate Detection

Requests with identical `external_customer_id` + `external_tenant_id` + `external_deal_id` within 60 seconds are flagged as duplicates. The existing `purchase_token` is returned.

---

## See Also

- [Required Fields](../fields/required-fields.md)
- [Optional Fields](../fields/optional-fields.md)
- [Validation Rules](../fields/validation-rules.md)
- [Form-Based Integration Guide](../integration-guides/form-based-integration.md)
- [Direct API Integration Guide](../integration-guides/direct-api-integration.md)
