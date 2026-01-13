# Tenant Form Request

Request a form URL to send directly to tenants. Bypasses the landlord form entirely.

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

  "tenant_form": true,

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
| `tenant_form` | boolean | Must be `true` |
| `ll_first_name` | string | Landlord's first name |
| `ll_last_name` | string | Landlord's last name |
| `ll_email` | string | Landlord's email |
| `ten_email` | string | Tenant's email |
| `purchase_address` | string | Property address (for jurisdiction) |

## Key Parameter

| Field | Type | Description |
|-------|------|-------------|
| `tenant_form` | boolean | When `true`, returns a direct tenant application URL |

> **Important:** The `purchase_address` is required to determine the jurisdiction of the transaction.

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `external_customer_id` | string | Your landlord ID |
| `external_tenant_id` | string | Your tenant ID |
| `ll_tel` | string | Landlord's phone |
| `ten_first_name` | string | Tenant's first name |
| `ten_last_name` | string | Tenant's last name |
| `ten_tel` | string | Tenant's phone |
| `purchase_rent` | integer | Monthly rent |
| `callback_url` | string | Webhook URL |

## Expected Response

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

## cURL Example

```bash
curl -X POST "https://platform.singlekey.com/api/request" \
  -H "Authorization: Token your_api_token" \
  -H "Content-Type: application/json" \
  -d '{
    "external_customer_id": "landlord-12345",
    "external_tenant_id": "tenant-67890",
    "tenant_form": true,
    "ll_first_name": "John",
    "ll_last_name": "Smith",
    "ll_email": "landlord@example.com",
    "ten_email": "tenant@example.com",
    "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1"
  }'
```

## Flow

```
1. You create request with tenant_form: true → Receive tenant_form_url
2. Send URL to tenant (redirect, email, or embed)
3. Tenant completes application
4. Tenant provides payment (if required by your agreement)
5. You receive webhook when complete
6. Fetch report via /api/report/<token>
```

## Use Cases

- **Property Listings**: Embed application link on listing pages
- **Direct Applications**: Send link to interested tenants
- **Self-Serve Screening**: Allow tenants to initiate their own screening

## Payment Handling

Depending on your account configuration:
- **Tenant Pays**: Tenant provides payment during application
- **Landlord Pays**: Payment captured from landlord's saved method
- **Monthly Billing**: No payment form shown

## Notes

- The `purchase_address` determines which screening product is used (jurisdiction-based)
- Pre-populate tenant data to reduce friction
- Use `callback_url` to receive real-time notifications

## See Also

- [Landlord Form Request](./landlord-form-request.md)
- [Direct API Request](./direct-api-request.md)
- [Available Fields](../fields/available-fields.md)
