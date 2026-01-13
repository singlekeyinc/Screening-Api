# Payment Methods

`GET /api/payments`

Check payment authorization status and retrieve saved payment method information.

## Authentication

| Header | Value |
|--------|-------|
| `Authorization` | `Token <your_api_token>` |

## Request

```bash
curl -X GET "https://platform.singlekey.com/api/payments" \
  -H "Authorization: Token your_api_token"
```

## Response

### Success - Payment Method on File

```json
{
  "success": true,
  "has_payment_method": true,
  "payment_method": {
    "brand": "visa",
    "last_4": "4242",
    "exp_month": 12,
    "exp_year": 2025
  }
}
```

### Success - No Payment Method

```json
{
  "success": true,
  "has_payment_method": false,
  "payment_method": null
}
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Always `true` for successful requests |
| `has_payment_method` | boolean | Whether a payment method is saved |
| `payment_method` | object/null | Payment method details if available |
| `payment_method.brand` | string | Card brand (visa, mastercard, amex, etc.) |
| `payment_method.last_4` | string | Last 4 digits of card number |
| `payment_method.exp_month` | integer | Card expiration month (1-12) |
| `payment_method.exp_year` | integer | Card expiration year (YYYY) |

## HTTP Status Codes

| Status | Description |
|--------|-------------|
| `200` | Success |
| `401` | Invalid or missing authentication token |
| `500` | Internal server error |

---

# Add Payment Method

`POST /api/payments`

Add a new payment method (credit card) for your account. This payment method will be used for screening charges.

## Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `card_number` | string | Yes | Full credit card number |
| `exp_month` | integer | Yes | Expiration month (1-12) |
| `exp_year` | integer | Yes | Expiration year (YYYY) |
| `cvc` | string | Yes | Card security code (3-4 digits) |
| `name` | string | No | Cardholder name |

## Request Example

```bash
curl -X POST "https://platform.singlekey.com/api/payments" \
  -H "Authorization: Token your_api_token" \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4242424242424242",
    "exp_month": 12,
    "exp_year": 2025,
    "cvc": "123",
    "name": "John Smith"
  }'
```

## Response

### Success

```json
{
  "success": true,
  "detail": "Payment method added successfully",
  "payment_method": {
    "brand": "visa",
    "last_4": "4242",
    "exp_month": 12,
    "exp_year": 2025
  }
}
```

### Error - Invalid Card

```json
{
  "success": false,
  "detail": "Your card was declined",
  "errors": ["Card number is invalid"]
}
```

## HTTP Status Codes

| Status | Description |
|--------|-------------|
| `200` | Payment method added successfully |
| `400` | Invalid card details |
| `401` | Invalid or missing authentication token |
| `500` | Internal server error |

---

# Payment Processing

## How Payments Work

SingleKey supports multiple payment models depending on your account configuration:

### 1. Saved Payment Method (Default)

Charges are automatically applied to your saved payment method when a screening is completed.

```
Partner creates request → Tenant submits → Screening completes → Card charged
```

### 2. Monthly Billing

For high-volume partners, charges accumulate and are billed monthly.

```
Partner creates requests → Screenings complete → Monthly invoice generated
```

Contact your account manager to enable monthly billing.

### 3. Tenant-Pays Model

The tenant provides payment during their application. Set `tenant_pays: true` in your request.

```
Partner creates request (tenant_pays: true) → Tenant submits + pays → Screening completes
```

### 4. Promo Codes

Apply promotional codes for discounted or free screenings:

```json
{
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456",
  "promo_code": "PARTNER2024",
  ...
}
```

## Payment Status Values

When you retrieve a screening, the `payment_status` field indicates the current state:

| Status | Description |
|--------|-------------|
| `paid` | Payment has been captured, screening is funded |
| `landlord has not submitted` | Waiting for landlord to complete form |
| `on hold, payment will be captured on submission` | Payment authorized, will capture when tenant submits |
| `unpaid` | No payment received or payment failed |

## Payment Status Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Request Created                                                │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────┐                                    │
│  │ landlord has not        │                                    │
│  │ submitted               │                                    │
│  └───────────┬─────────────┘                                    │
│              │                                                  │
│              │ Landlord submits form                            │
│              ▼                                                  │
│  ┌─────────────────────────┐                                    │
│  │ on hold, payment will   │ ◄── Payment pre-authorized        │
│  │ be captured on          │     (5-day hold)                   │
│  │ submission              │                                    │
│  └───────────┬─────────────┘                                    │
│              │                                                  │
│              │ Tenant submits application                       │
│              ▼                                                  │
│  ┌─────────────────────────┐                                    │
│  │ paid                    │ ◄── Payment captured               │
│  └─────────────────────────┘                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Pricing

| Product | Canada (CAD) | USA (USD) |
|---------|--------------|-----------|
| Standard Screening | $22.49 | $19.99 |
| Premium Screening | $34.99 | $29.99 |

*Prices exclude applicable taxes. Tax is calculated based on the property jurisdiction.*

## Test Mode

In the sandbox environment, use these test card numbers:

| Card Number | Result |
|-------------|--------|
| `4242424242424242` | Successful charge |
| `4000000000000002` | Card declined |
| `4000000000009995` | Insufficient funds |

All test cards use any future expiration date and any 3-digit CVC.

## Related Endpoints

| Endpoint | Description |
|----------|-------------|
| [`POST /api/request`](./request.md) | Create screening (triggers payment) |
| [`GET /api/report/<token>`](./report.md) | Check payment status in report |
