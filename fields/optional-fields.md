# Optional Fields Reference

This document covers all optional fields that can enhance screening requests with additional applicant information.

## Flow Control Fields

These fields control how the screening request is processed.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `run_now` | boolean | `false` | Process screening immediately (requires all tenant data) |
| `tenant_form` | boolean | `false` | Use direct tenant form instead of landlord form |
| `embedded_flow` | boolean | `false` | Enable embedded form flow |
| `update` | boolean | `false` | Force new report even if cached data exists (within 30 days) |
| `tenant_pays` | boolean | `false` | Tenant provides payment during application |

### Example: Immediate Processing

```json
{
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456",
  "run_now": true,
  // ... all required tenant fields
}
```

### Example: Tenant-Pays Model

```json
{
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456",
  "tenant_pays": true,
  "tenant_form": true,
  "purchase_address": "123 Main St, City, State, Country, Zip"
}
```

---

## Partner Integration Fields

Fields for integrating with your CRM or property management system.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `external_deal_id` | string | Your CRM deal/transaction ID | `"deal-abc123"` |
| `external_listing_id` | string | Your property listing ID | `"listing-xyz789"` |
| `callback_url` | string | Webhook URL for notifications | `"https://yoursite.com/webhooks/screening"` |

### Example: Full Integration

```json
{
  "external_customer_id": "landlord-123",
  "external_tenant_id": "tenant-456",
  "external_deal_id": "deal-abc123",
  "external_listing_id": "listing-xyz789",
  "callback_url": "https://yoursite.com/webhooks/screening",
  // ... other fields
}
```

---

## Product Selection Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `product_id` | string | Specific screening product ID | `"standard-ca"` |
| `jurisdiction` | string | Province/State for product selection | `"ON"`, `"CA"`, `"NY"` |

---

## Property Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `purchase_address` | string | Property address being rented | `"123 Main St, Toronto, ON, Canada, M5V 1A1"` |
| `purchase_rent` | integer | Monthly rent amount (cents) | `150000` (= $1,500.00) |
| `purchase_unit` | string | Unit/apartment number | `"Suite 4B"` |

---

## Tenant Personal Information

### Additional Contact Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `ten_middle_name` | string | Tenant's middle name | `"Marie"` |
| `ten_tel_alt` | string | Alternative phone number | `"5551112222"` |

### Current Address Details

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `ten_address_move_in_date` | string | Move-in date at current address | `"2020-01-15"` |
| `ten_address_move_out_date` | string | Expected move-out date | `"2024-03-01"` |
| `ten_address_rent` | integer | Current rent amount | `1200` |

---

## Employment Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `ten_employer` | string | Current employer name | `"Acme Corporation"` |
| `ten_job_title` | string | Job title/position | `"Software Engineer"` |
| `ten_employment_length` | string | Duration at current job | `"3 years"` |
| `ten_employment_status` | string | Employment status | `"full-time"`, `"part-time"`, `"self-employed"` |

---

## Income Information

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `ten_annual_income` | integer | Tenant's annual income | `75000` |
| `ten_household_income` | integer | Total household income | `120000` |
| `ten_other_income` | integer | Additional income sources | `5000` |
| `ten_income_source` | string | Primary income source | `"employment"`, `"investments"`, `"retirement"` |

---

## Previous Addresses (Residential History)

Provide previous addresses as an array for more thorough background checks.

| Field | Type | Description |
|-------|------|-------------|
| `previous_addresses` | array | List of previous address objects |

### Previous Address Object

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `address` | string | Full address | `"789 Oak St, Montreal, QC, Canada, H2Y 1C6"` |
| `move_in_date` | string | Move-in date | `"2018-06-01"` |
| `move_out_date` | string | Move-out date | `"2020-01-14"` |
| `rent` | integer | Monthly rent | `1100` |
| `landlord_name` | string | Previous landlord name | `"Bob Johnson"` |
| `landlord_phone` | string | Previous landlord phone | `"5143334444"` |

### Example

```json
{
  "previous_addresses": [
    {
      "address": "789 Oak St, Montreal, QC, Canada, H2Y 1C6",
      "move_in_date": "2018-06-01",
      "move_out_date": "2020-01-14",
      "rent": 1100,
      "landlord_name": "Bob Johnson",
      "landlord_phone": "5143334444"
    },
    {
      "address": "321 Pine Ave, Ottawa, ON, Canada, K1A 0B1",
      "move_in_date": "2015-09-01",
      "move_out_date": "2018-05-31",
      "rent": 950
    }
  ]
}
```

---

## Pets

| Field | Type | Description |
|-------|------|-------------|
| `pet` | boolean | Has pets (`true`/`false` or `"yes"`/`"no"`) |
| `pets` | array | List of pet objects |

### Pet Object

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `type` | string | Type of pet | `"dog"`, `"cat"`, `"fish"` |
| `breed` | string | Breed (if applicable) | `"Golden Retriever"` |
| `weight` | string | Weight | `"50 lbs"` |
| `name` | string | Pet's name | `"Max"` |

### Example

```json
{
  "pet": true,
  "pets": [
    {
      "type": "dog",
      "breed": "Golden Retriever",
      "weight": "50 lbs",
      "name": "Max"
    },
    {
      "type": "cat",
      "breed": "Domestic Shorthair",
      "name": "Whiskers"
    }
  ]
}
```

---

## Vehicles

| Field | Type | Description |
|-------|------|-------------|
| `car` | boolean | Has vehicles |
| `automobiles` | array | List of vehicle objects |

### Vehicle Object

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `make` | string | Vehicle manufacturer | `"Toyota"` |
| `model` | string | Vehicle model | `"Camry"` |
| `year` | integer | Vehicle year | `2020` |
| `license_plate` | string | License plate number | `"ABC 123"` |

### Example

```json
{
  "car": true,
  "automobiles": [
    {
      "make": "Toyota",
      "model": "Camry",
      "year": 2020,
      "license_plate": "ABC 123"
    }
  ]
}
```

---

## Declarations (Yes/No Fields)

These fields capture tenant declarations. Accept `true`/`false` boolean or `"yes"`/`"no"` string.

| Field | Type | Description |
|-------|------|-------------|
| `smoke` | boolean | Does the tenant smoke? |
| `bankruptcy` | boolean | Has the tenant declared bankruptcy? |
| `evicted` | boolean | Has the tenant been evicted? |
| `refused_to_pay_rent` | boolean | Has the tenant ever refused to pay rent? |
| `felony` | boolean | Has the tenant been convicted of a felony? |

### Example

```json
{
  "smoke": false,
  "bankruptcy": false,
  "evicted": false,
  "refused_to_pay_rent": false,
  "felony": false
}
```

---

## Co-Occupants

| Field | Type | Description |
|-------|------|-------------|
| `co_occupants` | array | List of additional occupants |

### Co-Occupant Object

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `first_name` | string | First name | `"John"` |
| `last_name` | string | Last name | `"Doe"` |
| `relationship` | string | Relationship to applicant | `"spouse"`, `"roommate"`, `"child"` |
| `dob` | string | Date of birth | `"1992-03-15"` |
| `income` | integer | Annual income | `50000` |

### Example

```json
{
  "co_occupants": [
    {
      "first_name": "John",
      "last_name": "Doe",
      "relationship": "spouse",
      "dob": "1992-03-15",
      "income": 50000
    }
  ]
}
```

---

## Guarantor Information

| Field | Type | Description |
|-------|------|-------------|
| `guarantor` | object | Guarantor details (if applicable) |

### Guarantor Object

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `first_name` | string | First name | `"Robert"` |
| `last_name` | string | Last name | `"Smith"` |
| `email` | string | Email address | `"robert@example.com"` |
| `phone` | string | Phone number | `"5557778888"` |
| `relationship` | string | Relationship to applicant | `"parent"`, `"employer"` |
| `address` | string | Full address | `"100 Guarantor St, City, State, Country, Zip"` |

### Example

```json
{
  "guarantor": {
    "first_name": "Robert",
    "last_name": "Smith",
    "email": "robert@example.com",
    "phone": "5557778888",
    "relationship": "parent",
    "address": "100 Guarantor St, Toronto, ON, Canada, M5V 2B3"
  }
}
```

---

## Promo Codes

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `promo_code` | string | Promotional code for discount | `"PARTNER2024"` |

---

## Complete Example with Optional Fields

```json
{
  "external_customer_id": "landlord-12345",
  "external_tenant_id": "tenant-67890",
  "external_deal_id": "deal-abc123",
  "external_listing_id": "listing-xyz789",
  "callback_url": "https://yoursite.com/webhooks/screening",

  "run_now": true,

  "ll_first_name": "John",
  "ll_last_name": "Smith",
  "ll_email": "john@example.com",
  "ll_tel": "5551234567",

  "ten_first_name": "Jane",
  "ten_middle_name": "Marie",
  "ten_last_name": "Doe",
  "ten_email": "jane@example.com",
  "ten_tel": "5559876543",
  "ten_dob_year": 1990,
  "ten_dob_month": 6,
  "ten_dob_day": 15,
  "ten_address": "456 Oak Ave, Vancouver, BC, Canada, V6B 2W2",
  "ten_sin": "123456789",

  "ten_employer": "Tech Corp",
  "ten_job_title": "Software Developer",
  "ten_employment_length": "3 years",
  "ten_annual_income": 85000,
  "ten_household_income": 85000,

  "purchase_address": "123 Main St, Vancouver, BC, Canada, V6B 1A1",
  "purchase_rent": 2000,
  "purchase_unit": "Unit 5",

  "previous_addresses": [
    {
      "address": "789 Previous St, Toronto, ON, Canada, M5V 1A1",
      "move_in_date": "2018-01-01",
      "move_out_date": "2022-12-31",
      "rent": 1500
    }
  ],

  "pet": true,
  "pets": [
    {"type": "cat", "breed": "Siamese", "name": "Luna"}
  ],

  "car": false,
  "automobiles": [],

  "smoke": false,
  "bankruptcy": false,
  "evicted": false,
  "refused_to_pay_rent": false
}
```

---

## See Also

- [Required Fields Reference](./required-fields.md)
- [Field Validation Rules](./validation-rules.md)
- [API Request Endpoint](../api-reference/request.md)
