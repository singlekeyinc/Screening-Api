# Get Applicant Information

`GET /api/applicant/<purchase_token>`

Retrieve detailed applicant (tenant) information for a screening.

## Authentication

| Header | Value |
|--------|-------|
| `Authorization` | `Token <your_api_token>` |

## Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `purchase_token` | string | Yes | 32-character token from screening request |

## Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `detailed` | boolean | `false` | Include detailed info (co-occupants, guarantors) |
| `show_credit_score` | boolean | `false` | Include credit score in response |

## Request

### Basic Request

```bash
curl -X GET "https://platform.singlekey.com/api/applicant/abc123def456ghi789jkl012mno345pq" \
  -H "Authorization: Token your_api_token"
```

### With Options

```bash
curl -X GET "https://platform.singlekey.com/api/applicant/abc123def456ghi789jkl012mno345pq?detailed=true&show_credit_score=true" \
  -H "Authorization: Token your_api_token"
```

---

## Response

### Basic Response

```json
{
  "success": true,
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane@example.com",
  "phone": "5551234567",
  "date_of_birth": "1990-06-15",
  "current_address": {
    "address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
    "move_in_date": "2020-01-15",
    "move_out_date": null,
    "rent": 1500
  },
  "previous_addresses": [
    {
      "address": "789 Pine St, Vancouver, BC, Canada, V6B 1A1",
      "move_in_date": "2018-06-01",
      "move_out_date": "2020-01-14",
      "rent": 1200
    }
  ],
  "employment": [
    {
      "employer": "Tech Corp",
      "job_title": "Software Engineer",
      "employment_length": "3 years",
      "income": 85000
    }
  ],
  "annual_income": 85000,
  "household_income": 85000,
  "pets": [
    {
      "type": "dog",
      "breed": "Labrador",
      "name": "Max"
    }
  ],
  "automobiles": [
    {
      "make": "Toyota",
      "model": "Camry",
      "year": 2020
    }
  ],
  "declarations": {
    "smoking": false,
    "bankruptcy": false,
    "eviction": false,
    "non_payment": false
  }
}
```

### Detailed Response (with `detailed=true`)

Includes additional fields:

```json
{
  "success": true,
  "first_name": "Jane",
  "last_name": "Doe",
  // ... basic fields ...

  "co_occupants": [
    {
      "first_name": "John",
      "last_name": "Doe",
      "relationship": "spouse",
      "date_of_birth": "1988-03-20",
      "income": 65000
    }
  ],
  "guarantor": {
    "first_name": "Robert",
    "last_name": "Smith",
    "email": "robert@example.com",
    "phone": "5559876543",
    "relationship": "parent",
    "address": "100 Guarantor St, Toronto, ON, Canada, M5V 1A1"
  },
  "income_sources": [
    {
      "source": "employment",
      "amount": 85000,
      "frequency": "annual"
    }
  ]
}
```

### With Credit Score (with `show_credit_score=true`)

```json
{
  "success": true,
  "first_name": "Jane",
  "last_name": "Doe",
  // ... other fields ...

  "credit_score": 720
}
```

---

## Response Fields

### Personal Information

| Field | Type | Description |
|-------|------|-------------|
| `first_name` | string | Tenant's first name |
| `last_name` | string | Tenant's last name |
| `email` | string | Tenant's email |
| `phone` | string | Tenant's phone number |
| `date_of_birth` | string | DOB in YYYY-MM-DD format |

### Address Information

| Field | Type | Description |
|-------|------|-------------|
| `current_address` | object | Current residence details |
| `current_address.address` | string | Full address |
| `current_address.move_in_date` | string | Move-in date |
| `current_address.move_out_date` | string | Expected move-out (if known) |
| `current_address.rent` | integer | Current monthly rent |
| `previous_addresses` | array | Previous residence history |

### Employment & Income

| Field | Type | Description |
|-------|------|-------------|
| `employment` | array | Employment records |
| `employment[].employer` | string | Employer name |
| `employment[].job_title` | string | Position/title |
| `employment[].employment_length` | string | Time at job |
| `employment[].income` | integer | Annual income |
| `annual_income` | integer | Total annual income |
| `household_income` | integer | Total household income |

### Pets & Vehicles

| Field | Type | Description |
|-------|------|-------------|
| `pets` | array | Pet information |
| `pets[].type` | string | Pet type (dog, cat, etc.) |
| `pets[].breed` | string | Breed |
| `pets[].name` | string | Pet's name |
| `automobiles` | array | Vehicle information |
| `automobiles[].make` | string | Vehicle make |
| `automobiles[].model` | string | Vehicle model |
| `automobiles[].year` | integer | Vehicle year |

### Declarations

| Field | Type | Description |
|-------|------|-------------|
| `declarations.smoking` | boolean | Tenant smokes |
| `declarations.bankruptcy` | boolean | History of bankruptcy |
| `declarations.eviction` | boolean | History of eviction |
| `declarations.non_payment` | boolean | History of non-payment |

### Detailed Fields (requires `detailed=true`)

| Field | Type | Description |
|-------|------|-------------|
| `co_occupants` | array | Additional occupants |
| `guarantor` | object | Guarantor information |
| `income_sources` | array | Detailed income breakdown |

### Credit (requires `show_credit_score=true`)

| Field | Type | Description |
|-------|------|-------------|
| `credit_score` | integer | Credit score (300-900) |

---

## HTTP Status Codes

| Status | Description |
|--------|-------------|
| `200` | Success |
| `401` | Invalid or missing token |
| `404` | Screening not found |
| `500` | Server error |

---

## Use Cases

### Pre-Populate Application Review

```python
def get_applicant_summary(token, api_token):
    response = requests.get(
        f"https://platform.singlekey.com/api/applicant/{token}",
        headers={"Authorization": f"Token {api_token}"},
        params={"detailed": "true", "show_credit_score": "true"}
    )

    data = response.json()

    return {
        "name": f"{data['first_name']} {data['last_name']}",
        "income": data['annual_income'],
        "credit_score": data.get('credit_score'),
        "pets": len(data.get('pets', [])),
        "smoking": data['declarations']['smoking']
    }
```

### Display to Landlord

```javascript
async function displayApplicant(purchaseToken) {
  const response = await fetch(
    `https://platform.singlekey.com/api/applicant/${purchaseToken}?detailed=true`,
    { headers: { 'Authorization': `Token ${API_TOKEN}` } }
  );

  const applicant = await response.json();

  return `
    <h2>${applicant.first_name} ${applicant.last_name}</h2>
    <p>Income: $${applicant.annual_income.toLocaleString()}/year</p>
    <p>Current Rent: $${applicant.current_address.rent}/month</p>
    <p>Employment: ${applicant.employment[0]?.employer || 'N/A'}</p>
  `;
}
```

---

## See Also

- [Get Report](./report.md)
- [Download PDF](./report-pdf.md)
- [Create Request](./request.md)
