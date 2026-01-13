# Error Codes Reference

Complete reference for all API error codes, their meanings, and how to resolve them.

## HTTP Status Codes

| Status | Meaning | Action |
|--------|---------|--------|
| `200` | Success | Request completed successfully |
| `400` | Bad Request | Fix validation errors and retry |
| `401` | Unauthorized | Check API token |
| `404` | Not Found | Verify resource exists |
| `429` | Rate Limited | Wait and retry |
| `500` | Server Error | Contact support |

---

## Response Format

### Success Response

```json
{
  "success": true,
  "purchase_token": "abc123...",
  // ... additional data
}
```

### Error Response

```json
{
  "success": false,
  "detail": "Human-readable error message",
  "errors": [
    "Specific error 1",
    "Specific error 2"
  ]
}
```

---

## Validation Errors

### Name Fields

| Error | Cause | Resolution |
|-------|-------|------------|
| `"First name is required"` | Missing `ten_first_name` or `ll_first_name` | Provide non-empty name |
| `"Last name is required"` | Missing `ten_last_name` or `ll_last_name` | Provide non-empty name |
| `"Name too long"` | Name exceeds 256 characters | Truncate to 256 chars |

### Email Fields

| Error | Cause | Resolution |
|-------|-------|------------|
| `"Tenant email is required"` | Missing `ten_email` | Provide valid email |
| `"Landlord email is required"` | Missing `ll_email` | Provide valid email |
| `"Invalid email format"` | Email doesn't match pattern | Use format: `user@domain.com` |
| `"Email domain invalid"` | TLD too long or missing | Use valid domain (2-5 char TLD) |

**Valid email examples:**
```
user@example.com       ✓
user.name@company.co   ✓
user@domain.io         ✓
```

**Invalid email examples:**
```
@example.com           ✗  (missing local part)
user@                  ✗  (missing domain)
user@domain            ✗  (missing TLD)
user@domain.toolong    ✗  (TLD > 5 chars)
```

### Phone Fields

| Error | Cause | Resolution |
|-------|-------|------------|
| `"Tenant phone is required"` | Missing `ten_tel` | Provide phone number |
| `"Phone must be 10 digits"` | Wrong number of digits | Use 10-digit format |
| `"Phone must be a string"` | Passed as integer | Pass as string: `"5551234567"` |
| `"Invalid phone format"` | Contains invalid characters | Use digits only |

**Valid phone examples:**
```
"5551234567"           ✓  (10 digits)
"15551234567"          ✓  (11 digits with country code)
"(555) 123-4567"       ✓  (formatted, will be normalized)
```

**Invalid phone examples:**
```
5551234567             ✗  (integer, not string)
"555123456"            ✗  (9 digits)
"55512345678"          ✗  (11 digits without leading 1)
"555-CALL-NOW"         ✗  (contains letters)
```

### Date of Birth

| Error | Cause | Resolution |
|-------|-------|------------|
| `"Date of birth is required"` | Missing DOB fields | Provide all three: year, month, day |
| `"Invalid birth year"` | Year not 4 digits or < 1900 | Use 4-digit year after 1900 |
| `"Invalid birth month"` | Month not 1-12 | Use 1-12 |
| `"Invalid birth day"` | Day not valid for month | Use valid day for the month |
| `"Applicant must be at least 18 years old"` | Calculated age < 18 | Tenant must be 18+ |

**Valid DOB examples:**
```json
{"ten_dob_year": 1990, "ten_dob_month": 6, "ten_dob_day": 15}     ✓
{"ten_dob_year": "1985", "ten_dob_month": "12", "ten_dob_day": "31"} ✓
```

**Invalid DOB examples:**
```json
{"ten_dob_year": 90, "ten_dob_month": 6, "ten_dob_day": 15}       ✗  (2-digit year)
{"ten_dob_year": 2010, "ten_dob_month": 6, "ten_dob_day": 15}     ✗  (under 18)
{"ten_dob_year": 1990, "ten_dob_month": 2, "ten_dob_day": 30}     ✗  (Feb 30)
```

### Address Fields

| Error | Cause | Resolution |
|-------|-------|------------|
| `"Tenant address is required"` | Missing `ten_address` | Provide current address |
| `"Address must contain comma"` | No commas in address | Use comma-separated format |
| `"Address could not be validated"` | Address not recognized | Verify address exists |
| `"Address must be in US or Canada"` | Non-US/Canada address | Only US/Canada supported |
| `"Invalid postal code"` | Wrong postal/zip format | Canada: A1A 1A1, US: 12345 |

**Valid address format:**
```
"Street, City, Province/State, Country, Postal/Zip"

"123 Main Street, Toronto, ON, Canada, M5V 1A1"     ✓
"456 Oak Ave, Los Angeles, CA, USA, 90210"          ✓
```

**Invalid address examples:**
```
"123 Main Street Toronto ON Canada"                  ✗  (no commas)
"123 Main Street, London, UK"                        ✗  (not US/Canada)
```

### SIN/SSN Fields

| Error | Cause | Resolution |
|-------|-------|------------|
| `"SIN is required for Canadian addresses"` | Missing SIN for Canada | Provide 9-digit SIN |
| `"SSN is required for US addresses"` | Missing SSN for US | Provide 9-digit SSN |
| `"SIN/SSN must be exactly 9 digits"` | Wrong length | Use exactly 9 digits |
| `"SIN/SSN must contain only digits"` | Contains non-digits | Remove spaces/dashes |

**Valid format:**
```
"123456789"            ✓
```

**Invalid format:**
```
"12345678"             ✗  (8 digits)
"123-456-789"          ✗  (contains dashes)
"123 456 789"          ✗  (contains spaces)
123456789              ✗  (integer, not string)
```

---

## Authentication Errors

| Error | Status | Resolution |
|-------|--------|------------|
| `"Invalid token."` | 401 | Check token is correct |
| `"Authentication credentials were not provided."` | 401 | Include `Authorization` header |
| `"Token has expired"` | 401 | Request new API token |

**Correct header format:**
```
Authorization: Token your_api_token_here
```

**Common mistakes:**
```
Authorization: your_api_token         ✗  (missing "Token" prefix)
Authorization: Bearer your_api_token  ✗  (wrong prefix)
authorization: Token your_api_token   ✗  (lowercase header)
```

---

## Resource Errors

| Error | Status | Resolution |
|-------|--------|------------|
| `"Report does not exist"` | 404 | Verify purchase_token |
| `"Screening not found"` | 404 | Check screening ID |
| `"Resource not found"` | 404 | Verify endpoint URL |

---

## Payment Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `"Payment required"` | No payment method on file | Add payment method |
| `"Payment method declined"` | Card was declined | Use different card |
| `"Card expired"` | Card expiration passed | Update card details |
| `"Insufficient funds"` | Card has no funds | Use different card |
| `"Payment already processed"` | Duplicate charge attempt | Check if already paid |

---

## Processing Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `"Credit bureau unavailable"` | External service down | Retry in 30 minutes |
| `"Identity verification failed"` | Could not verify identity | Check tenant data accuracy |
| `"Address verification failed"` | Address not verifiable | Use complete, valid address |
| `"Report creation in progress"` | Still processing | Wait and poll again |
| `"Processing timeout"` | Took too long | Retry the request |

---

## Duplicate Request Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `"Duplicate request detected"` | Same request within 60 seconds | Use existing purchase_token |
| `"Screening already exists for this tenant"` | Recent screening exists | Use `update: true` or wait 30 days |

---

## Rate Limiting

| Error | Status | Resolution |
|-------|--------|------------|
| `"Rate limit exceeded"` | 429 | Wait before retrying |
| `"Too many requests"` | 429 | Implement backoff |

**Recommended backoff:**
```python
import time

def request_with_backoff(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = 2 ** attempt  # 1, 2, 4, 8, 16 seconds
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

---

## Server Errors

| Error | Status | Resolution |
|-------|--------|------------|
| `"Internal server error"` | 500 | Contact support with request ID |
| `"Service temporarily unavailable"` | 503 | Retry after delay |
| HTML response (no JSON) | 500 | May be blocked by WAF - contact support |

---

## Error Code Quick Reference

| Code | Category | Description |
|------|----------|-------------|
| `INVALID_EMAIL` | Validation | Email format is invalid |
| `INVALID_PHONE` | Validation | Phone format is invalid |
| `INVALID_ADDRESS` | Validation | Address could not be validated |
| `INVALID_DOB` | Validation | Date of birth is invalid |
| `INVALID_SIN` | Validation | SIN/SSN format is invalid |
| `UNDERAGE` | Validation | Applicant is under 18 |
| `MISSING_FIELD` | Validation | Required field is missing |
| `AUTH_FAILED` | Authentication | Token is invalid or missing |
| `NOT_FOUND` | Resource | Resource does not exist |
| `PAYMENT_REQUIRED` | Payment | No payment method available |
| `PAYMENT_FAILED` | Payment | Payment was declined |
| `DUPLICATE` | Logic | Duplicate request detected |
| `RATE_LIMITED` | Rate Limit | Too many requests |
| `BUREAU_UNAVAILABLE` | External | Credit bureau is down |
| `PROCESSING` | Status | Request is still processing |

---

## Debugging Tips

### 1. Log Full Responses

```python
response = requests.post(url, headers=headers, json=data)
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Body: {response.text}")
```

### 2. Validate Before Sending

```python
def validate_tenant_data(tenant):
    errors = []

    if not tenant.get('ten_email'):
        errors.append("Tenant email is required")

    phone = tenant.get('ten_tel', '')
    digits = ''.join(filter(str.isdigit, str(phone)))
    if len(digits) not in (10, 11):
        errors.append("Phone must be 10 or 11 digits")

    sin = tenant.get('ten_sin', '')
    if len(str(sin)) != 9:
        errors.append("SIN must be 9 digits")

    return errors
```

### 3. Use Sandbox for Testing

Test with sandbox environment before production:

```python
# Sandbox
BASE_URL = "https://sandbox.singlekey.com"

# Production
BASE_URL = "https://platform.singlekey.com"
```

---

## See Also

- [Troubleshooting Guide](./faq.md)
- [Field Validation Rules](../fields/validation-rules.md)
- [API Reference](../api-reference/)
