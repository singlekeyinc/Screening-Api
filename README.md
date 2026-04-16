# SingleKey Screening API

Tenant screening and credit reporting API for landlords and property managers. Process comprehensive background checks in under 5 minutes with full Equifax/TransUnion credit data.

## Quick Links

| Getting Started | Integration | Reference |
|-----------------|-------------|-----------|
| [Quickstart](getting-started/quickstart.md) | [Form-Based](integration-guides/form-based-integration.md) | [API Endpoints](api-reference/) |
| [Authentication](getting-started/authentication.md) | [Direct API](integration-guides/direct-api-integration.md) | [Field Reference](fields/) |
| [Environments](getting-started/environments.md) | [Webhooks](integration-guides/webhook-integration.md) | [Error Codes](troubleshooting/error-codes.md) |

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SINGLEKEY SCREENING FLOW                             │
└─────────────────────────────────────────────────────────────────────────────┘

    Your System                 SingleKey                    Credit Bureaus
         │                          │                              │
         │  1. Create screening     │                              │
         │ ─────────────────────────►                              │
         │                          │                              │
         │  2. purchase_token       │                              │
         │ ◄─────────────────────────                              │
         │                          │  3. Credit & Background      │
         │                          │ ────────────────────────────►│
         │                          │                              │
         │                          │  4. Data returned            │
         │  5. Webhook notification │ ◄────────────────────────────│
         │ ◄─────────────────────────                              │
         │                          │                              │
         │  6. GET /api/report      │                              │
         │ ─────────────────────────►                              │
         │                          │                              │
         │  7. Full report          │                              │
         │ ◄─────────────────────────                              │
```

## Features

- **Fast Processing**: Reports ready in 2-5 minutes
- **Comprehensive Data**: Credit scores, background checks, eviction history
- **Dual Integration**: Form-based or direct API
- **Real-time Updates**: Webhook notifications
- **Multi-Jurisdiction**: USA and Canada support

## Quick Start

### 1. Get Your API Token

Contact your SingleKey account manager or email **info@singlekey.com** for sandbox and production tokens.

### 2. Make Your First Request

```bash
curl -X POST "https://sandbox.singlekey.com/screen/embedded_flow_request" \
  -H "Authorization: Token YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-456",
    "tenant_form": true,
    "ten_email": "tenant@example.com",
    "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1"
  }'
```

### 3. Get the Report

```bash
curl -X GET "https://sandbox.singlekey.com/screen/embedded_flow_get_report/PURCHASE_TOKEN" \
  -H "Authorization: Token YOUR_API_TOKEN"
```

## Environments

| Environment | Base URL | Purpose |
|-------------|----------|---------|
| Sandbox | `https://sandbox.singlekey.com` | Testing |
| Production | `https://platform.singlekey.com` | Live |

## API Endpoints

### Create Screening

| Endpoint | Method | Use For |
|----------|--------|---------|
| [`/screen/embedded_flow_request`](api-reference/request.md) | POST | Form-based flows (landlord form, tenant form) and deferred execution |
| [`/api/request`](api-reference/request.md) | POST | Direct API / immediate screening (`run_now` is auto-set to `true`) |

Both create-screening endpoints accept the same fields. The difference is that `/api/request` automatically sets `run_now: true`, so it should only be used when you have all tenant data and want immediate processing.

### Other Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| [`/api/report/<token>`](api-reference/report.md) | GET | Fetch screening report |
| [`/screen/embedded_flow_get_report/<token>`](routes/fetch-report-route.md) | GET | Fetch screening report (embedded flow) |
| [`/api/applicant/<token>`](api-reference/applicant.md) | GET | Get applicant details |
| [`/screen/applicant/<token>`](routes/applicant-data-route.md) | GET | Get applicant details (embedded flow) |
| [`/api/report_pdf/<token>`](api-reference/report-pdf.md) | GET | Download report PDF |
| [`/api/purchase_errors/<id>`](api-reference/purchase-errors.md) | POST | Validate screening data |
| [`/api/payments`](api-reference/payments.md) | GET/POST | Payment management |

## Integration Options

### Form-Based (Recommended for Most Users)

SingleKey hosts the data collection forms. You just create the request and redirect users.

```
Your App → POST /screen/embedded_flow_request → Form URL → User Completes Form → Webhook → Fetch Report
```

**Two form types available:**
- **Landlord Form**: Landlord invites tenant or screens directly (with consent)
- **Tenant Form**: Direct application link for tenants (`tenant_form: true`)

[Form-Based Integration Guide →](integration-guides/form-based-integration.md)

### Direct API

You collect all tenant data and submit directly for immediate processing.

```
Your App → Collect Data → POST /api/request → Poll/Webhook → Fetch Report
```

### Deferred Execution (Direct API with Documents)

For integrations requiring document uploads or multi-step data collection:

```
Your App → Create Screening → Update Data / Attach Documents → Execute (run_now: true) → Fetch Report
```

The deferred flow uses `POST /screen/embedded_flow_request` with a `purchase_token` to identify the screening across steps. Use `/api/request` only for the final execution step, or pass `run_now: true` explicitly on the last call.

[Direct API Integration Guide →](integration-guides/direct-api-integration.md)

## Authentication

All requests require token authentication:

```
Authorization: Token your_api_token_here
```

[Authentication Guide →](getting-started/authentication.md)

## Code Examples

### Python

```python
import requests

response = requests.post(
    "https://sandbox.singlekey.com/api/request",
    headers={
        "Authorization": "Token YOUR_TOKEN",
        "Content-Type": "application/json"
    },
    json={
        "external_customer_id": "landlord-123",
        "external_tenant_id": "tenant-456",
        "run_now": True,
        "ll_first_name": "John",
        "ll_last_name": "Smith",
        "ll_email": "john@example.com",
        "ten_first_name": "Jane",
        "ten_last_name": "Doe",
        "ten_email": "jane@example.com",
        "ten_tel": "5551234567",
        "ten_dob_year": 1990,
        "ten_dob_month": 6,
        "ten_dob_day": 15,
        "ten_address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
        "ten_sin": "123456789"
    }
)

print(response.json()["purchase_token"])
```

[Full Python Client →](examples/python/)

### JavaScript

```javascript
const response = await fetch('https://sandbox.singlekey.com/screen/embedded_flow_request', {
  method: 'POST',
  headers: {
    'Authorization': 'Token YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    external_customer_id: 'landlord-123',
    external_tenant_id: 'tenant-456',
    tenant_form: true,
    ten_email: 'jane@example.com',
    purchase_address: '123 Main St, Toronto, ON, Canada, M5V 1A1'
  })
});

const data = await response.json();
console.log(data.tenant_form_url);
```

[Full JavaScript Client →](examples/javascript/)

### cURL

```bash
curl -X POST "https://sandbox.singlekey.com/screen/embedded_flow_request" \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"external_customer_id":"landlord-123","external_tenant_id":"tenant-456","tenant_form":true,"ten_email":"jane@example.com","purchase_address":"123 Main St, Toronto, ON, Canada, M5V 1A1"}'
```

[More cURL Examples →](examples/curl/)

## Webhooks

Receive real-time notifications when screening events occur:

```json
{
  "detail": "Report Complete",
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

Configure your webhook URL in the **Partner Portal**. Optionally set a **Handshake Token** to verify webhook authenticity via the `Handshake-Token` header.

[Webhook Integration Guide →](integration-guides/webhook-integration.md) | [Event Reference →](webhooks/events.md)

## Tenant Re-screening

Use `external_tenant_id` to track tenants across multiple landlords:
- Recent credit data cached for 30 days (prevents duplicate charges)
- Use `"update": true` to force a new report within the 30-day window

## Documentation Structure

```
├── getting-started/
│   ├── quickstart.md          # Get started in 5 minutes
│   ├── authentication.md      # API token usage
│   └── environments.md        # Sandbox vs Production
│
├── integration-guides/
│   ├── form-based-integration.md
│   ├── direct-api-integration.md
│   └── webhook-integration.md
│
├── api-reference/
│   ├── request.md             # POST /api/request
│   ├── report.md              # GET /api/report
│   ├── applicant.md           # GET /api/applicant
│   ├── report-pdf.md          # GET /api/report_pdf
│   ├── purchase-errors.md     # POST /api/purchase_errors
│   └── payments.md            # Payment management
│
├── fields/
│   ├── required-fields.md     # Required fields by integration type
│   ├── optional-fields.md     # Optional enhancement fields
│   └── validation-rules.md    # Field validation rules
│
├── webhooks/
│   ├── events.md              # Event types and handling
│   └── payload-reference.md   # Full payload documentation
│
├── examples/
│   ├── python/                # Python client and examples
│   ├── javascript/            # JavaScript/Node.js client
│   └── curl/                  # cURL command examples
│
└── troubleshooting/
    ├── error-codes.md         # Error code reference
    └── faq.md                 # Common issues and solutions
```

## Admin Portal

Access your admin portal to:
- Check application status
- Resend tenant invites
- Identify submission errors
- View webhook delivery logs

## Support

| Type | Contact |
|------|---------|
| Sales & Onboarding | info@singlekey.com |
| API Questions | api-support@singlekey.com |
| Phone | 1 (877) 978-1404 |
| Website | [singlekey.com](https://singlekey.com) |

## License

Copyright SingleKey Inc. All rights reserved.
