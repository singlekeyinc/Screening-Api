# Direct API Request

Immediate screening without forms. Requires all tenant data and `run_now: true`.

## Endpoint

```
POST /api/request
```

## Headers

```
Authorization: Token your_api_token
Content-Type: application/json
```

## Request Payload

```json
{
  "external_customer_id": "landlord-12345",
  "external_tenant_id": "tenant-67890",
  "external_deal_id": "deal-abc123",
  "external_listing_id": "listing-xyz789",

  "run_now": true,

  "ll_first_name": "John",
  "ll_last_name": "Smith",
  "ll_tel": "5551234567",
  "ll_email": "landlord@example.com",

  "ten_first_name": "Jane",
  "ten_last_name": "Doe",
  "ten_email": "tenant@example.com",
  "ten_tel": "5559876543",
  "ten_dob_year": 1990,
  "ten_dob_month": 6,
  "ten_dob_day": 15,
  "ten_sin": "123456789",
  "ten_address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",

  "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
  "purchase_rent": 2000
}
```

## Field Descriptions

### External Identifiers

| Field | Type | Description |
|-------|------|-------------|
| `external_customer_id` | string | Your unique ID for the landlord |
| `external_tenant_id` | string | Your unique ID for the tenant |
| `external_deal_id` | string | Your CRM deal ID (optional) |
| `external_listing_id` | string | Your listing ID (optional) |

### Control Flag

| Field | Type | Description |
|-------|------|-------------|
| `run_now` | boolean | Must be `true` for immediate processing |

### Landlord Information

| Field | Type | Description |
|-------|------|-------------|
| `ll_first_name` | string | Landlord's first name |
| `ll_last_name` | string | Landlord's last name |
| `ll_tel` | string | Landlord's phone (10 digits) |
| `ll_email` | string | Landlord's email |

### Tenant Information

| Field | Type | Description |
|-------|------|-------------|
| `ten_first_name` | string | Tenant's first name |
| `ten_last_name` | string | Tenant's last name |
| `ten_email` | string | Tenant's email |
| `ten_tel` | string | Tenant's phone (10 digits) |
| `ten_dob_year` | integer | Birth year (4 digits) |
| `ten_dob_month` | integer | Birth month (1-12) |
| `ten_dob_day` | integer | Birth day (1-31) |
| `ten_sin` | string | SIN (Canada) or SSN (USA) - 9 digits |
| `ten_address` | string | Tenant's current address |

### Property Information

| Field | Type | Description |
|-------|------|-------------|
| `purchase_address` | string | Address being rented |
| `purchase_rent` | integer | Monthly rent amount |

## Expected Response

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "payment_status": "paid",
  "created": "2025-01-15T10:30:00.000000+00:00",
  "initiated": true
}
```

## cURL Example

```bash
curl -X POST "https://platform.singlekey.com/api/request" \
  -H "Authorization: Token your_api_token" \
  -H "Content-Type: application/json" \
  -d '{
    "external_customer_id": "landlord-12345",
    "external_tenant_id": "tenant-67890",
    "run_now": true,
    "ll_first_name": "John",
    "ll_last_name": "Smith",
    "ll_tel": "5551234567",
    "ll_email": "landlord@example.com",
    "ten_first_name": "Jane",
    "ten_last_name": "Doe",
    "ten_email": "tenant@example.com",
    "ten_tel": "5559876543",
    "ten_dob_year": 1990,
    "ten_dob_month": 6,
    "ten_dob_day": 15,
    "ten_sin": "123456789",
    "ten_address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
    "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
    "purchase_rent": 2000
  }'
```

## Notes

- `run_now: true` requires all tenant data to be provided
- A payment method must be on file or monthly billing enabled
- The report will begin processing immediately
- Use webhooks or poll `/api/report/<token>` for completion

## See Also

- [Landlord Form Request](./landlord-form-request.md)
- [Tenant Form Request](./tenant-form-request.md)
- [Available Fields](../fields/available-fields.md)
