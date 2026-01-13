# Status Codes and Errors

HTTP status codes and error handling for the SingleKey API.

---

## Success Responses

### HTTP 200 OK

All successful requests return a `200` status code with:
- `Content-Type: application/json` header
- JSON body containing `"success": true`

```json
{
  "success": true,
  "purchase_token": "abc123def456ghi789jkl012mno345pq",
  // ... additional fields
}
```

---

## Error Responses

### Error Response Format

All error responses (except 500 without JSON) include:

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Always `false` for errors |
| `detail` | string | Human-readable error description |
| `errors` | array | List of specific error messages |

```json
{
  "success": false,
  "detail": "missing or incomplete data",
  "errors": [
    "ten_email: the email --invalid-- is not formatted like an email",
    "ten_tel: the phone number --555-- is not the expected length"
  ]
}
```

> **Tip:** The `errors` array contains user-friendly messages that can be displayed to your users.

---

## HTTP Status Codes

### 200 OK

Request was successful. Check the `success` field in the response body.

### 400 Bad Request

Request was properly formatted but contains invalid or missing data.

**Example:**

```json
{
  "success": false,
  "detail": "missing or incomplete data",
  "errors": [
    "12345: SIN numbers must be 9 digits long",
    "ten_email: the email --invalid-- is not formatted like an email"
  ]
}
```

**Resolution:** Check the `errors` array and fix the indicated fields.

---

### 401 Unauthorized

Authentication failed.

**Invalid Token:**

```json
{
  "detail": "Invalid token."
}
```

**Missing Credentials:**

```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Resolution:** Ensure your request includes the correct header:

```
Authorization: Token your_api_token_here
```

---

### 404 Not Found

The requested resource does not exist.

```json
{
  "success": false,
  "detail": "Report does not exist",
  "errors": [
    "Report does not exist"
  ]
}
```

**Resolution:** Verify you're using the correct `purchase_token`.

---

### 500 Internal Server Error

Server-side error. Two types exist:

#### HTML Response (No JSON)

| Header | Value |
|--------|-------|
| `Content-Type` | `text/html;charset=UTF-8` |

**Cause:** Your IP address may be blocked by Cloudflare or AWS WAF.

**Resolution:** Contact support to have your server's IP address added to the allow list.

#### JSON Response

| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |

**Cause:** Internal server error that was handled but prevents normal operation.

**Resolution:** Contact support with the full JSON response for investigation.

---

## Error Examples by Field

### Email Errors

```json
{
  "success": false,
  "detail": "missing or incomplete data",
  "errors": [
    "ten_email: the email --no_at_sign.com-- is not formatted like an email",
    "ll_email: the email --no_domain@email-- is not formatted like an email"
  ]
}
```

### Phone Errors

```json
{
  "success": false,
  "detail": "missing or incomplete data",
  "errors": [
    "ten_tel: the phone number --555555-- is not the expected length"
  ]
}
```

### SIN/SSN Errors

```json
{
  "success": false,
  "detail": "missing or incomplete data",
  "errors": [
    "12345: SIN numbers must be 9 digits long"
  ]
}
```

### Address Errors

```json
{
  "success": false,
  "detail": "missing or incomplete data",
  "errors": [
    "ten_address: address could not be validated"
  ]
}
```

### Date of Birth Errors

```json
{
  "success": false,
  "detail": "missing or incomplete data",
  "errors": [
    "Applicant must be at least 18 years old"
  ]
}
```

---

## Quick Reference

| Status | Meaning | Has JSON? | Has `success` field? |
|--------|---------|-----------|---------------------|
| 200 | Success | Yes | Yes (`true`) |
| 400 | Validation Error | Yes | Yes (`false`) |
| 401 | Auth Failed | Yes | No |
| 404 | Not Found | Yes | Yes (`false`) |
| 500 | Server Error | Maybe | Maybe |

---

## Handling Errors

### Python Example

```python
import requests

def make_api_request(url, data):
    response = requests.post(
        url,
        headers={
            "Authorization": f"Token {API_TOKEN}",
            "Content-Type": "application/json"
        },
        json=data
    )

    # Check status code
    if response.status_code == 401:
        raise AuthenticationError("Invalid or missing API token")

    if response.status_code == 404:
        raise NotFoundError("Resource not found")

    if response.status_code == 500:
        if 'application/json' in response.headers.get('Content-Type', ''):
            raise ServerError(response.json())
        else:
            raise IPBlockedError("IP may be blocked - contact support")

    # Parse JSON response
    result = response.json()

    if not result.get('success', True):
        errors = result.get('errors', [])
        raise ValidationError(result.get('detail'), errors)

    return result
```

### JavaScript Example

```javascript
async function makeApiRequest(url, data) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Token ${API_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });

  // Handle status codes
  if (response.status === 401) {
    throw new Error('Invalid or missing API token');
  }

  if (response.status === 404) {
    throw new Error('Resource not found');
  }

  if (response.status === 500) {
    const contentType = response.headers.get('Content-Type');
    if (contentType?.includes('text/html')) {
      throw new Error('IP may be blocked - contact support');
    }
    const error = await response.json();
    throw new Error(`Server error: ${JSON.stringify(error)}`);
  }

  // Parse response
  const result = await response.json();

  if (result.success === false) {
    const errorMessages = result.errors?.join(', ') || result.detail;
    throw new Error(`Validation error: ${errorMessages}`);
  }

  return result;
}
```

---

## See Also

- [Response Examples](./response-examples.md)
- [Field Validation Rules](../fields/data-field-validation.md)
- [Troubleshooting FAQ](../troubleshooting/faq.md)
