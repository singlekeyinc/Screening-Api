# Landlord Form Request

Request a form URL to redirect landlords to. The landlord completes the application and can invite tenants.

## Endpoint

```
POST /api/request
```

## Headers

```
Authorization: Token your_api_token
Content-Type: application/json
```

## Minimum Request Payload

```json
{
  "external_customer_id": "landlord-12345",
  "external_tenant_id": "tenant-67890",

  "ll_first_name": "John",
  "ll_last_name": "Smith",
  "ll_email": "landlord@example.com",
  "ll_tel": "5551234567",

  "ten_first_name": "Jane",
  "ten_last_name": "Doe",
  "ten_email": "tenant@example.com"
}
```

## Full Request Payload (Optional Fields)

```json
{
  "external_customer_id": "landlord-12345",
  "external_tenant_id": "tenant-67890",
  "external_deal_id": "deal-abc123",
  "external_listing_id": "listing-xyz789",

  "ll_first_name": "John",
  "ll_last_name": "Smith",
  "ll_email": "landlord@example.com",
  "ll_tel": "5551234567",

  "ten_first_name": "Jane",
  "ten_last_name": "Doe",
  "ten_email": "tenant@example.com",
  "ten_tel": "5559876543",

  "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
  "purchase_rent": 2000,

  "callback_url": "https://yoursite.com/webhooks/singlekey"
}
```

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `ll_first_name` | string | Landlord's first name |
| `ll_last_name` | string | Landlord's last name |
| `ll_email` | string | Landlord's email |
| `ll_tel` | string | Landlord's phone (10 digits) |
| `ten_first_name` | string | Tenant's first name |
| `ten_last_name` | string | Tenant's last name |
| `ten_email` | string | Tenant's email |

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `external_customer_id` | string | Your landlord ID |
| `external_tenant_id` | string | Your tenant ID |
| `external_deal_id` | string | Your CRM deal ID |
| `external_listing_id` | string | Your listing ID |
| `ten_tel` | string | Tenant's phone |
| `purchase_address` | string | Property address |
| `purchase_rent` | integer | Monthly rent |
| `callback_url` | string | Webhook URL |

## Expected Response

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "payment_status": "landlord has not submitted",
  "created": "2025-01-15T10:30:00.000000+00:00",
  "form_url": "https://platform.singlekey.com/screen/request?purchase_token=abc123..."
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
    "ll_first_name": "John",
    "ll_last_name": "Smith",
    "ll_email": "landlord@example.com",
    "ll_tel": "5551234567",
    "ten_first_name": "Jane",
    "ten_last_name": "Doe",
    "ten_email": "tenant@example.com"
  }'
```

## Flow

```
1. You create request → Receive form_url
2. Redirect landlord to form_url
3. Landlord completes form (property details, payment)
4. Landlord chooses to:
   a. Invite tenant via email/SMS
   b. Screen tenant directly (with consent)
5. You receive webhook when complete
6. Fetch report via /api/report/<token>
```

## Notes

- The landlord must provide additional information (property details) on the form
- Pre-populate fields to reduce friction for landlords
- Use `callback_url` to receive webhook notifications

## See Also

- [Tenant Form Request](./tenant-form-request.md)
- [Direct API Request](./direct-api-request.md)
- [Available Fields](../fields/available-fields.md)
