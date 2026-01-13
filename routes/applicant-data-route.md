# Get Applicant Data

`GET /api/applicant/<purchase_token>` or `GET /screen/applicant/<purchase_token>`

Retrieve detailed information about a tenant applicant. Available at any time after obtaining a purchase token.

## Authentication

| Header | Value |
|--------|-------|
| `Authorization` | `Token <your_api_token>` |

## Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `purchase_token` | string | 32-character token from screening request |

---

## Response

Returns whatever applicant data is currently available. If the tenant is still completing their application, partial data may be returned.

### Example Response

```json
{
  "ten_first_name": "Jane",
  "ten_middle_names": null,
  "ten_last_name": "Doe",
  "ten_email": "tenant@example.com",
  "ten_tel": "5551234567",
  "ten_dob_day": "15",
  "ten_dob_month": "6",
  "ten_dob_year": "1990",
  "ten_address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
  "ten_previous_addresses": [
    "789 Pine St, Vancouver, BC, Canada, V6B 1A1"
  ],
  "ten_employments": [
    {
      "job_title": "Software Engineer",
      "employer": "Tech Corp",
      "employment_length": "3 Years",
      "income": 85000
    }
  ],
  "ten_annual_income": 85000,
  "ten_household_income": 85000,
  "ten_pets": [
    {
      "type": "dog",
      "breed": "Golden Retriever"
    }
  ],
  "ten_automobiles": [
    {
      "make": "Toyota",
      "model": "Camry"
    }
  ],
  "ten_smoke": false,
  "ten_refused_to_pay_rent": false,
  "ten_bankruptcy": false,
  "ten_evicted": false,
  "ten_given_notice": true,
  "ten_additional_info": "I am a quiet and respectful tenant."
}
```

---

## Response Fields

### Personal Information

| Field | Type | Description |
|-------|------|-------------|
| `ten_first_name` | string | Tenant's first name |
| `ten_middle_names` | string | Middle name(s), or `null` |
| `ten_last_name` | string | Tenant's last name |
| `ten_email` | string | Tenant's email address |
| `ten_tel` | string | Tenant's phone number |

### Date of Birth

| Field | Type | Description |
|-------|------|-------------|
| `ten_dob_day` | string | Birth day |
| `ten_dob_month` | string | Birth month |
| `ten_dob_year` | string | Birth year |

### Address Information

| Field | Type | Description |
|-------|------|-------------|
| `ten_address` | string | Current address |
| `ten_previous_addresses` | array | List of previous addresses (strings) |

### Employment Information

| Field | Type | Description |
|-------|------|-------------|
| `ten_employments` | array | List of employment records |
| `ten_employments[].job_title` | string | Position/title |
| `ten_employments[].employer` | string | Employer name |
| `ten_employments[].employment_length` | string | Duration at job |
| `ten_employments[].income` | integer | Annual income |
| `ten_annual_income` | integer | Total declared annual income |
| `ten_household_income` | integer | Total household income |

### Pets & Vehicles

| Field | Type | Description |
|-------|------|-------------|
| `ten_pets` | array | List of pets |
| `ten_pets[].type` | string | Pet type (dog, cat, etc.) |
| `ten_pets[].breed` | string | Breed |
| `ten_automobiles` | array | List of vehicles |
| `ten_automobiles[].make` | string | Vehicle make |
| `ten_automobiles[].model` | string | Vehicle model |

### Declarations

| Field | Type | Description |
|-------|------|-------------|
| `ten_smoke` | boolean | Tenant smokes |
| `ten_refused_to_pay_rent` | boolean | Has refused to pay rent |
| `ten_bankruptcy` | boolean | Has declared bankruptcy |
| `ten_evicted` | boolean | Has been evicted |
| `ten_given_notice` | boolean | Has given notice to current landlord |
| `ten_additional_info` | string | Additional notes from tenant |

---

## Notes

- **Partial Data**: If the tenant is still completing their application, fields may be `null` or arrays may be empty.
- **Direct Screening**: When using `run_now: true` without forms, much of this data (pets, vehicles, previous addresses) will be `null` unless you provided it in the request.
- **Empty Lists**: If no data exists for array fields (previous addresses, employments, pets, automobiles), an empty list `[]` is returned.

---

## Example Request

```bash
curl -X GET "https://platform.singlekey.com/api/applicant/abc123def456ghi789jkl012mno345pq" \
  -H "Authorization: Token your_api_token"
```

---

## HTTP Status Codes

| Status | Description |
|--------|-------------|
| `200` | Success |
| `401` | Invalid or missing authentication token |
| `404` | Screening not found |

---

## Use Cases

### Display Application Summary

```python
def get_applicant_summary(token, api_token):
    response = requests.get(
        f"https://platform.singlekey.com/api/applicant/{token}",
        headers={"Authorization": f"Token {api_token}"}
    )

    data = response.json()

    return {
        "name": f"{data['ten_first_name']} {data['ten_last_name']}",
        "email": data['ten_email'],
        "income": data.get('ten_annual_income'),
        "has_pets": len(data.get('ten_pets', [])) > 0,
        "smoking": data.get('ten_smoke', False)
    }
```

### Pre-populate Landlord Dashboard

```javascript
async function displayApplicantCard(purchaseToken) {
  const response = await fetch(
    `https://platform.singlekey.com/api/applicant/${purchaseToken}`,
    { headers: { 'Authorization': `Token ${API_TOKEN}` } }
  );

  const applicant = await response.json();

  return `
    <div class="applicant-card">
      <h3>${applicant.ten_first_name} ${applicant.ten_last_name}</h3>
      <p>Income: $${applicant.ten_annual_income?.toLocaleString() || 'N/A'}</p>
      <p>Employment: ${applicant.ten_employments?.[0]?.employer || 'Not provided'}</p>
      <p>Pets: ${applicant.ten_pets?.length > 0 ? 'Yes' : 'No'}</p>
    </div>
  `;
}
```

---

## See Also

- [Create Request](./request-route.md)
- [Fetch Report](./fetch-report-route.md)
- [Available Fields](../fields/available-fields.md)
