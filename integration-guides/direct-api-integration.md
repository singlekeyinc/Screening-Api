# Direct API Integration Guide

This guide covers integrating SingleKey using direct API calls where you collect all tenant data and submit it for immediate processing.

## Overview

Direct API integration is ideal when you:
- Already collect tenant information in your application
- Want immediate screening results (no forms)
- Need full control over the user experience
- Have proper data handling and compliance in place

## Integration Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DIRECT API INTEGRATION FLOW                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Your    │     │  SingleKey   │     │  Credit      │     │  Background  │
│  System  │     │  API         │     │  Bureau      │     │  Check       │
└────┬─────┘     └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
     │                  │                    │                    │
     │  1. Collect all tenant data           │                    │
     │  (name, DOB, SIN, address)            │                    │
     │                  │                    │                    │
     │  2. POST /api/request                 │                    │
     │  with run_now: true                   │                    │
     │ ─────────────────►                    │                    │
     │                  │                    │                    │
     │                  │  3. Fetch credit   │                    │
     │                  │ ──────────────────►│                    │
     │                  │                    │                    │
     │                  │  4. Credit data    │                    │
     │                  │ ◄──────────────────                     │
     │                  │                    │                    │
     │                  │  5. Run background │                    │
     │                  │ ───────────────────────────────────────►│
     │                  │                    │                    │
     │                  │  6. Background data│                    │
     │                  │ ◄───────────────────────────────────────│
     │                  │                    │                    │
     │  7. Return purchase_token             │                    │
     │ ◄─────────────────                    │                    │
     │                  │                    │                    │
     │  8. Poll or wait for webhook          │                    │
     │                  │                    │                    │
     │  9. GET /api/report/{token}           │                    │
     │ ─────────────────►                    │                    │
     │                  │                    │                    │
     │  10. Return complete report           │                    │
     │ ◄─────────────────                    │                    │
```

## Quick Start

### Basic Request

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
    "callback_url": "https://yoursite.com/webhooks/singlekey"
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

## Required Fields for Direct API

When using `run_now: true`, all data must be provided upfront:

### Landlord Information

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ll_first_name` | string | Yes | Landlord first name |
| `ll_last_name` | string | Yes | Landlord last name |
| `ll_email` | string | Yes | Landlord email |

### Tenant Personal Information

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ten_first_name` | string | Yes | Tenant legal first name |
| `ten_last_name` | string | Yes | Tenant legal last name |
| `ten_email` | string | Yes | Tenant email |
| `ten_tel` | string | Yes | Tenant phone (10 digits) |

### Tenant Date of Birth

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ten_dob_year` | integer | Yes | Birth year (YYYY) |
| `ten_dob_month` | integer | Yes | Birth month (1-12) |
| `ten_dob_day` | integer | Yes | Birth day (1-31) |

### Tenant Address & Identity

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ten_address` | string | Yes | Current address |
| `ten_sin` | string | Yes (Canada) | 9-digit SIN |

---

## Complete Integration Example

### Python Implementation

```python
import requests
import time

class SingleKeyAPI:
    def __init__(self, api_token, base_url="https://platform.singlekey.com"):
        self.api_token = api_token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json"
        }

    def create_screening(self, landlord, tenant, property_info):
        """
        Create an immediate screening request.

        Args:
            landlord: dict with first_name, last_name, email
            tenant: dict with first_name, last_name, email, phone, dob, address, sin
            property_info: dict with address, rent (optional)

        Returns:
            dict with purchase_token and status
        """
        payload = {
            "external_customer_id": landlord.get('id', f"ll-{landlord['email']}"),
            "external_tenant_id": tenant.get('id', f"tn-{tenant['email']}"),
            "run_now": True,

            # Landlord info
            "ll_first_name": landlord['first_name'],
            "ll_last_name": landlord['last_name'],
            "ll_email": landlord['email'],

            # Tenant info
            "ten_first_name": tenant['first_name'],
            "ten_last_name": tenant['last_name'],
            "ten_email": tenant['email'],
            "ten_tel": tenant['phone'],
            "ten_dob_year": tenant['dob']['year'],
            "ten_dob_month": tenant['dob']['month'],
            "ten_dob_day": tenant['dob']['day'],
            "ten_address": tenant['address'],
            "ten_sin": tenant['sin'],

            # Property info (optional)
            "purchase_address": property_info.get('address'),
            "purchase_rent": property_info.get('rent'),

            # Webhook for notifications
            "callback_url": "https://yoursite.com/webhooks/singlekey"
        }

        response = requests.post(
            f"{self.base_url}/api/request",
            headers=self.headers,
            json=payload
        )

        return response.json()

    def get_report(self, purchase_token):
        """
        Fetch screening report.

        Args:
            purchase_token: 32-character token from create_screening

        Returns:
            dict with report data or status
        """
        response = requests.get(
            f"{self.base_url}/api/report/{purchase_token}",
            headers=self.headers
        )

        return response.json()

    def wait_for_report(self, purchase_token, timeout=300, poll_interval=10):
        """
        Poll for report completion.

        Args:
            purchase_token: token from create_screening
            timeout: max seconds to wait (default 5 minutes)
            poll_interval: seconds between checks (default 10)

        Returns:
            dict with completed report or timeout error
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            report = self.get_report(purchase_token)

            if report.get('success') and report.get('singlekey_score'):
                return report

            print(f"Status: {report.get('detail', 'Processing...')}")
            time.sleep(poll_interval)

        return {"error": "Timeout waiting for report"}

    def download_pdf(self, purchase_token, output_path):
        """
        Download report as PDF.

        Args:
            purchase_token: token from create_screening
            output_path: file path to save PDF

        Returns:
            bool indicating success
        """
        response = requests.get(
            f"{self.base_url}/api/report_pdf/{purchase_token}",
            headers=self.headers,
            stream=True
        )

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True

        return False


# Usage Example
if __name__ == "__main__":
    api = SingleKeyAPI("your_api_token")

    # Create screening
    result = api.create_screening(
        landlord={
            "id": "landlord-123",
            "first_name": "John",
            "last_name": "Smith",
            "email": "john@landlord.com"
        },
        tenant={
            "id": "tenant-456",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@tenant.com",
            "phone": "5551234567",
            "dob": {"year": 1990, "month": 6, "day": 15},
            "address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
            "sin": "123456789"
        },
        property_info={
            "address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
            "rent": 2000
        }
    )

    print(f"Screening created: {result['purchase_token']}")

    # Wait for completion
    report = api.wait_for_report(result['purchase_token'])

    if report.get('success'):
        print(f"SingleKey Score: {report['singlekey_score']}")
        print(f"Report URL: {report['report_url']}")

        # Download PDF
        api.download_pdf(result['purchase_token'], "screening_report.pdf")
        print("PDF saved to screening_report.pdf")
    else:
        print(f"Error: {report.get('error', report.get('detail'))}")
```

### JavaScript/Node.js Implementation

```javascript
const axios = require('axios');

class SingleKeyAPI {
  constructor(apiToken, baseUrl = 'https://platform.singlekey.com') {
    this.baseUrl = baseUrl;
    this.headers = {
      'Authorization': `Token ${apiToken}`,
      'Content-Type': 'application/json'
    };
  }

  async createScreening(landlord, tenant, propertyInfo) {
    const payload = {
      external_customer_id: landlord.id || `ll-${landlord.email}`,
      external_tenant_id: tenant.id || `tn-${tenant.email}`,
      run_now: true,

      // Landlord info
      ll_first_name: landlord.firstName,
      ll_last_name: landlord.lastName,
      ll_email: landlord.email,

      // Tenant info
      ten_first_name: tenant.firstName,
      ten_last_name: tenant.lastName,
      ten_email: tenant.email,
      ten_tel: tenant.phone,
      ten_dob_year: tenant.dob.year,
      ten_dob_month: tenant.dob.month,
      ten_dob_day: tenant.dob.day,
      ten_address: tenant.address,
      ten_sin: tenant.sin,

      // Property info
      purchase_address: propertyInfo?.address,
      purchase_rent: propertyInfo?.rent,

      // Webhook
      callback_url: 'https://yoursite.com/webhooks/singlekey'
    };

    const response = await axios.post(
      `${this.baseUrl}/api/request`,
      payload,
      { headers: this.headers }
    );

    return response.data;
  }

  async getReport(purchaseToken) {
    const response = await axios.get(
      `${this.baseUrl}/api/report/${purchaseToken}`,
      { headers: this.headers }
    );

    return response.data;
  }

  async waitForReport(purchaseToken, timeout = 300000, pollInterval = 10000) {
    const startTime = Date.now();

    while (Date.now() - startTime < timeout) {
      const report = await this.getReport(purchaseToken);

      if (report.success && report.singlekey_score) {
        return report;
      }

      console.log(`Status: ${report.detail || 'Processing...'}`);
      await new Promise(resolve => setTimeout(resolve, pollInterval));
    }

    throw new Error('Timeout waiting for report');
  }
}

// Usage
async function main() {
  const api = new SingleKeyAPI('your_api_token');

  try {
    // Create screening
    const result = await api.createScreening(
      {
        id: 'landlord-123',
        firstName: 'John',
        lastName: 'Smith',
        email: 'john@landlord.com'
      },
      {
        id: 'tenant-456',
        firstName: 'Jane',
        lastName: 'Doe',
        email: 'jane@tenant.com',
        phone: '5551234567',
        dob: { year: 1990, month: 6, day: 15 },
        address: '456 Oak Ave, Toronto, ON, Canada, M5V 2B3',
        sin: '123456789'
      },
      {
        address: '123 Main St, Toronto, ON, Canada, M5V 1A1',
        rent: 2000
      }
    );

    console.log(`Screening created: ${result.purchase_token}`);

    // Wait for completion
    const report = await api.waitForReport(result.purchase_token);

    console.log(`SingleKey Score: ${report.singlekey_score}`);
    console.log(`Report URL: ${report.report_url}`);

  } catch (error) {
    console.error('Error:', error.message);
  }
}

main();
```

---

## Processing Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    TYPICAL PROCESSING TIMELINE                   │
└─────────────────────────────────────────────────────────────────┘

  0s              30s             60s            120s           300s
  │               │               │               │               │
  ▼               ▼               ▼               ▼               ▼
  ┌───────────────┬───────────────┬───────────────┬───────────────┐
  │  Request      │  Credit       │  Background   │  Report       │
  │  Received     │  Check        │  Check        │  Generated    │
  └───────────────┴───────────────┴───────────────┴───────────────┘

  Average completion: 2-3 minutes
  Maximum time: 5 minutes (complex cases)
```

## Polling vs Webhooks

### Option 1: Polling (Simple)

```python
def poll_for_report(api, token, max_attempts=30, delay=10):
    for attempt in range(max_attempts):
        report = api.get_report(token)

        if report.get('success') and report.get('singlekey_score'):
            return report

        time.sleep(delay)

    raise TimeoutError("Report not ready after maximum attempts")
```

### Option 2: Webhooks (Recommended)

```python
# Your webhook endpoint
@app.route('/webhooks/singlekey', methods=['POST'])
def handle_webhook():
    event = request.json

    if event['event'] == 'screening.completed':
        token = event['data']['purchase_token']
        score = event['data']['singlekey_score']

        # Update your database
        update_screening_status(token, 'completed', score)

        # Notify relevant parties
        send_notification(token)

    return jsonify({"received": True}), 200
```

---

## Error Handling

### Validation Errors

```python
result = api.create_screening(landlord, tenant, property_info)

if not result.get('success'):
    errors = result.get('errors', [])
    for error in errors:
        print(f"Validation error: {error}")
    # Handle: show errors to user, fix data, retry
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `"Tenant email is required"` | Missing `ten_email` | Provide valid email |
| `"Phone must be 10 digits"` | Invalid phone format | Format as 10 digits |
| `"SIN must be 9 digits"` | Invalid SIN | Verify SIN format |
| `"Address not recognized"` | Invalid address | Use proper format |
| `"Applicant must be 18+"` | Underage tenant | Verify DOB |
| `"Payment required"` | No payment method | Add payment or use monthly billing |

### Retry Logic

```python
import time
from requests.exceptions import RequestException

def create_screening_with_retry(api, landlord, tenant, property_info, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = api.create_screening(landlord, tenant, property_info)

            if result.get('success'):
                return result

            # Validation error - don't retry
            if result.get('errors'):
                return result

        except RequestException as e:
            if attempt == max_retries - 1:
                raise

            # Exponential backoff
            time.sleep(2 ** attempt)

    raise Exception("Max retries exceeded")
```

---

## Data Security Best Practices

### Handling Sensitive Data

```python
# Good: Validate before sending
def validate_sin(sin):
    """Validate SIN format before API call."""
    clean_sin = ''.join(filter(str.isdigit, sin))
    if len(clean_sin) != 9:
        raise ValueError("SIN must be exactly 9 digits")
    return clean_sin

# Good: Don't log sensitive data
def create_screening(tenant_data):
    logger.info(f"Creating screening for tenant: {tenant_data['email']}")
    # Don't log: SIN, full DOB, full address
```

### Secure Storage

```python
# Don't store SIN/SSN after submission
tenant = {
    "sin": "123456789"  # Clear after API call
}

result = api.create_screening(landlord, tenant, property)

# Clear sensitive data
tenant['sin'] = None
```

---

## Tenant Consent

Ensure you have tenant consent before running screenings:

```python
def request_screening(tenant_id, consent_given):
    if not consent_given:
        raise PermissionError("Tenant consent required for screening")

    # Proceed with screening
    tenant = get_tenant(tenant_id)
    return api.create_screening(landlord, tenant, property)
```

Required consent elements:
- Credit check authorization
- Background check authorization
- Data sharing acknowledgment

---

## See Also

- [Form-Based Integration](./form-based-integration.md)
- [Webhook Integration](./webhook-integration.md)
- [Field Reference](../fields/required-fields.md)
- [Error Codes](../troubleshooting/error-codes.md)
