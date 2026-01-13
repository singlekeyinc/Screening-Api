# Validate Screening Data

`POST /api/purchase_errors/<screening_id>`

Validates screening data for completeness and correctness before processing. Use this endpoint to check for issues that would prevent a screening from being processed.

## Authentication

| Header | Value |
|--------|-------|
| `Authorization` | `Token <your_api_token>` |
| `Content-Type` | `application/json` |

## Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `screening_id` | string | Yes | The screening ID to validate |

## Request

No request body required.

```bash
curl -X POST "https://platform.singlekey.com/api/purchase_errors/12345" \
  -H "Authorization: Token your_api_token"
```

## Response

### Success - No Errors Found

```json
{
  "success": true,
  "detail": "No errors found",
  "errors": [],
  "purchase_id": 12345,
  "token": "abc123def456..."
}
```

### Success - Errors Found

```json
{
  "success": false,
  "detail": "Validation errors found",
  "errors": [
    "Tenant email is required",
    "Date of birth is invalid",
    "Address could not be validated"
  ],
  "purchase_id": 12345,
  "token": "abc123def456..."
}
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | `true` if no validation errors, `false` otherwise |
| `detail` | string | Human-readable status message |
| `errors` | array | List of validation error messages |
| `purchase_id` | integer | The screening purchase ID |
| `token` | string | The purchase token for this screening |

## Common Validation Errors

| Error Message | Cause | Resolution |
|---------------|-------|------------|
| `Tenant email is required` | Missing `ten_email` field | Provide valid tenant email |
| `Date of birth is invalid` | Invalid DOB format or underage | Use YYYY-MM-DD format, tenant must be 18+ |
| `Address could not be validated` | Address not recognized by Google Maps | Use format: "123 Main St, City, State, Country, Zip" |
| `SIN/SSN is required` | Missing identification number | Provide 9-digit SIN (Canada) or SSN (US) |
| `Phone number is invalid` | Wrong phone format | Use 10-digit format with area code |

## Use Cases

### Pre-Submission Validation

Call this endpoint before finalizing a screening to catch errors early:

```python
import requests

def validate_screening(screening_id, api_token):
    response = requests.post(
        f"https://platform.singlekey.com/api/purchase_errors/{screening_id}",
        headers={"Authorization": f"Token {api_token}"}
    )

    data = response.json()

    if data["success"]:
        print("Screening is valid and ready to process")
    else:
        print("Errors found:")
        for error in data["errors"]:
            print(f"  - {error}")

    return data
```

### Error Handling in Embedded Flow

After a user submits the embedded form, use this endpoint to check if their submission was complete:

```javascript
async function checkSubmission(screeningId) {
  const response = await fetch(
    `https://platform.singlekey.com/api/purchase_errors/${screeningId}`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Token ${API_TOKEN}`
      }
    }
  );

  const data = await response.json();

  if (!data.success) {
    // Redirect user back to form with errors
    return { valid: false, errors: data.errors };
  }

  return { valid: true, token: data.token };
}
```

## HTTP Status Codes

| Status | Description |
|--------|-------------|
| `200` | Request processed (check `success` field for validation result) |
| `401` | Invalid or missing authentication token |
| `404` | Screening not found |
| `500` | Internal server error |
