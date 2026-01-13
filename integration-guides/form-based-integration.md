# Form-Based Integration Guide

This guide covers integrating SingleKey using embedded forms where landlords or tenants complete the application through SingleKey-hosted pages.

## Overview

Form-based integration is ideal when you want to:
- Minimize data collection on your end
- Let SingleKey handle PII (personally identifiable information)
- Provide a seamless user experience with hosted forms
- Reduce compliance burden for sensitive data

## Integration Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FORM-BASED INTEGRATION FLOW                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Your    │     │  SingleKey   │     │  Landlord/   │     │  SingleKey   │
│  System  │     │  API         │     │  Tenant      │     │  Processing  │
└────┬─────┘     └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
     │                  │                    │                    │
     │  1. POST /api/request                 │                    │
     │  (minimal tenant data)                │                    │
     │ ─────────────────►                    │                    │
     │                  │                    │                    │
     │  2. Return form_url                   │                    │
     │ ◄─────────────────                    │                    │
     │                  │                    │                    │
     │  3. Redirect/email form_url           │                    │
     │ ──────────────────────────────────────►                    │
     │                  │                    │                    │
     │                  │  4. User completes │                    │
     │                  │     form           │                    │
     │                  │ ◄──────────────────                     │
     │                  │                    │                    │
     │                  │  5. Process screening                   │
     │                  │ ───────────────────────────────────────►│
     │                  │                    │                    │
     │  6. Webhook: screening.completed      │                    │
     │ ◄─────────────────────────────────────────────────────────│
     │                  │                    │                    │
     │  7. GET /api/report/{token}           │                    │
     │ ─────────────────►                    │                    │
     │                  │                    │                    │
     │  8. Return report data                │                    │
     │ ◄─────────────────                    │                    │
     │                  │                    │                    │
```

## Two Form Types

### 1. Landlord Form (Default)

The landlord receives a form to enter property and tenant details, then invites the tenant.

**Best for:**
- Landlords who want to initiate the screening
- Cases where landlord has tenant contact info
- Multi-step landlord → tenant flow

```
Your System → API → Landlord Form → Tenant Invitation → Tenant Form → Report
```

### 2. Tenant Form (Direct)

The tenant receives a direct link to complete their application.

**Best for:**
- Direct tenant applications
- Property listing integrations
- Self-serve tenant screening

```
Your System → API → Tenant Form → Report
```

---

## Landlord Form Integration

### Step 1: Create Screening Request

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
    "callback_url": "https://yoursite.com/webhooks/singlekey"
  }'
```

### Step 2: Handle Response

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

### Step 3: Direct Landlord to Form

Option A: Redirect immediately
```javascript
window.location.href = response.form_url;
```

Option B: Send via email
```javascript
await sendEmail({
  to: "landlord@example.com",
  subject: "Complete Tenant Screening",
  body: `Click here to complete the screening: ${response.form_url}`
});
```

### Step 4: Landlord Completes Form

The landlord fills in:
- Property details (address, rent, lease terms)
- Tenant information (or confirms pre-filled data)
- Payment information (if landlord pays)

### Step 5: Tenant Receives Invitation

After landlord submits, tenant receives an email with their application link.

### Step 6: Receive Webhook & Fetch Report

```python
# Webhook handler
@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    event = request.json

    if event['event'] == 'screening.completed':
        token = event['data']['purchase_token']
        fetch_and_store_report(token)

    return jsonify({"received": True}), 200

def fetch_and_store_report(token):
    response = requests.get(
        f"https://platform.singlekey.com/api/report/{token}",
        headers={"Authorization": f"Token {API_TOKEN}"}
    )
    report = response.json()

    # Store in your database
    save_screening_result(
        tenant_id=report['external_tenant_id'],
        score=report['singlekey_score'],
        report_url=report['report_url']
    )
```

---

## Tenant Form Integration

### Step 1: Create Screening Request

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
    "callback_url": "https://yoursite.com/webhooks/singlekey"
  }'
```

### Step 2: Handle Response

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  "tenant_form_url": "https://platform.singlekey.com/screen/tenant?token=ABC123",
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
}
```

### Step 3: Direct Tenant to Form

```javascript
// Redirect tenant to their application form
window.location.href = response.tenant_form_url;
```

### Tenant Form Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     TENANT FORM EXPERIENCE                       │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │  Personal   │     │  Address &  │     │  Identity   │
    │  Info       │────►│  Employment │────►│  & Payment  │
    └─────────────┘     └─────────────┘     └─────────────┘
          │                   │                   │
          ▼                   ▼                   ▼
    - Full name         - Current address   - SIN/SSN entry
    - Date of birth     - Move-in date      - ID verification
    - Phone number      - Previous addrs    - Credit card
    - Email             - Employment info     (if tenant pays)
                        - Income
```

---

## Embedding Forms (iFrame)

You can embed SingleKey forms directly in your application:

```html
<iframe
  src="https://platform.singlekey.com/screen/tenant?token=ABC123"
  width="100%"
  height="800"
  frameborder="0"
  allow="camera; microphone"
>
</iframe>
```

### Responsive Embedding

```html
<div style="position: relative; padding-bottom: 100%; height: 0; overflow: hidden;">
  <iframe
    src="https://platform.singlekey.com/screen/tenant?token=ABC123"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
    frameborder="0"
    allow="camera; microphone"
  ></iframe>
</div>
```

### PostMessage Communication

Listen for form events:

```javascript
window.addEventListener('message', function(event) {
  // Verify origin
  if (event.origin !== 'https://platform.singlekey.com') return;

  const { type, data } = event.data;

  switch (type) {
    case 'form.submitted':
      console.log('Form submitted, processing...');
      break;
    case 'form.completed':
      console.log('Screening complete:', data.purchase_token);
      break;
    case 'form.error':
      console.error('Form error:', data.message);
      break;
  }
});
```

---

## Pre-Populating Form Data

Reduce friction by pre-filling known data:

```json
{
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456",
  "tenant_form": true,

  "ten_first_name": "Jane",
  "ten_last_name": "Doe",
  "ten_email": "jane@example.com",
  "ten_tel": "5551234567",

  "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
  "purchase_rent": 2000,
  "purchase_unit": "Unit 5B"
}
```

Pre-filled fields appear in the form but remain editable by the user.

---

## Payment Options

### Landlord Pays (Default)

Landlord provides payment during form completion.

```json
{
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456"
  // No tenant_pays flag
}
```

### Tenant Pays

Tenant provides payment during their application.

```json
{
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456",
  "tenant_form": true,
  "tenant_pays": true,
  "purchase_address": "123 Main St, City, Province, Country, Postal"
}
```

### Partner Billing

If you have monthly billing enabled, no payment form appears.

---

## Tracking Application Status

### Check Status via API

```python
def check_screening_status(purchase_token):
    response = requests.get(
        f"https://platform.singlekey.com/api/report/{purchase_token}",
        headers={"Authorization": f"Token {API_TOKEN}"}
    )

    data = response.json()

    if data.get('success'):
        return {
            'status': 'completed',
            'score': data.get('singlekey_score'),
            'report_url': data.get('report_url')
        }
    else:
        return {
            'status': data.get('detail', 'pending'),
            'form_url': data.get('form_url'),
            'tenant_form_url': data.get('tenant_form_url')
        }
```

### Status Messages

| Status | Meaning |
|--------|---------|
| `"Tenant has not submitted invite"` | Waiting for tenant to complete form |
| `"They have not opened their invite email"` | Tenant hasn't clicked email link |
| `"They have opened their invite email"` | Tenant opened but hasn't submitted |
| `"Report creation in progress"` | Processing (wait 2-5 minutes) |
| `success: true` | Report ready |

---

## Complete Integration Example

```python
import requests
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)
API_TOKEN = "your_api_token"
BASE_URL = "https://platform.singlekey.com"

# Step 1: Create screening request
@app.route('/apply/<listing_id>', methods=['POST'])
def create_application(listing_id):
    tenant_email = request.form['email']
    listing = get_listing(listing_id)

    response = requests.post(
        f"{BASE_URL}/api/request",
        headers={
            "Authorization": f"Token {API_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "external_customer_id": listing['landlord_id'],
            "external_tenant_id": f"tenant-{tenant_email}",
            "external_listing_id": listing_id,
            "tenant_form": True,
            "ten_email": tenant_email,
            "purchase_address": listing['address'],
            "purchase_rent": listing['rent'],
            "callback_url": "https://yoursite.com/webhooks/singlekey"
        }
    )

    data = response.json()

    # Save application record
    save_application(
        listing_id=listing_id,
        tenant_email=tenant_email,
        purchase_token=data['purchase_token'],
        status='pending'
    )

    # Redirect tenant to application form
    return redirect(data['tenant_form_url'])

# Step 2: Handle webhook
@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    event = request.json

    if event['event'] == 'screening.completed':
        token = event['data']['purchase_token']
        tenant_id = event['data']['external_tenant_id']
        score = event['data'].get('singlekey_score')

        # Update application status
        update_application(
            purchase_token=token,
            status='completed',
            score=score
        )

        # Notify landlord
        notify_landlord(token, score)

    return jsonify({"received": True}), 200

# Step 3: View report
@app.route('/applications/<token>/report')
def view_report(token):
    response = requests.get(
        f"{BASE_URL}/api/report/{token}",
        headers={"Authorization": f"Token {API_TOKEN}"}
    )

    return jsonify(response.json())

if __name__ == '__main__':
    app.run()
```

---

## See Also

- [Direct API Integration](./direct-api-integration.md)
- [Webhook Integration](./webhook-integration.md)
- [Field Reference](../fields/required-fields.md)
- [API Reference](../api-reference/request.md)
