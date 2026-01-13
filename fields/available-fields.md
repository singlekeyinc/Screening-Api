# Available Fields Reference

Complete list of all data fields accepted when submitting a screening request to the SingleKey API.

## Terminology

- **Landlord (ll_)**: The person requesting the screening (property manager, landlord, agent)
- **Tenant (ten_)**: The person being screened (applicant)
- **Purchase**: The property/unit the tenant is applying to rent

---

## External Identifiers

Fields for tracking and correlating records with your system.

| Field | Type | Description |
|-------|------|-------------|
| `external_customer_id` | string | Your unique ID for the landlord/PM |
| `external_tenant_id` | string | Your unique ID for the tenant |
| `external_deal_id` | string | Your CRM deal/transaction ID |
| `external_property_id` | string | Your ID for the property/listing |

---

## Landlord Information

| Field | Type | Description |
|-------|------|-------------|
| `ll_first_name` | string | Landlord's first name |
| `ll_last_name` | string | Landlord's last name |
| `ll_email` | string | Landlord's email address |
| `ll_tel` | string | Landlord's phone number (10 digits) |
| `ll_address` | string | Landlord's address |
| `ll_description` | string | Role description (default: "Property Manager") |
| `ll_n_properties` | integer | Number of properties managed |

---

## Tenant Personal Information

| Field | Type | Description |
|-------|------|-------------|
| `ten_first_name` | string | Tenant's first name |
| `ten_middle_names` | string | Tenant's middle name(s) |
| `ten_last_name` | string | Tenant's last name |
| `ten_email` | string | Tenant's email address |
| `ten_tel` | string | Tenant's phone number (10 digits) |

---

## Tenant Date of Birth

| Field | Type | Description |
|-------|------|-------------|
| `ten_dob_day` | integer | Birth day (1-31) |
| `ten_dob_month` | integer | Birth month (1-12) |
| `ten_dob_year` | integer | Birth year (4 digits, e.g., 1990) |

---

## Tenant Identification

| Field | Type | Description |
|-------|------|-------------|
| `ten_sin` | string | Social Insurance Number (Canada) or SSN (USA) - 9 digits |
| `ten_drivers_license_number` | string | Driver's license number |

---

## Tenant Current Address

| Field | Type | Description |
|-------|------|-------------|
| `ten_address` | string | Current address (see format below) |
| `ten_address_unit` | string | Unit/apartment number |
| `ten_address_year` | integer | Year moved in (2 or 4 digits) |
| `ten_address_month` | integer | Month moved in (1-12) |
| `ten_address_day` | integer | Day moved in (1-31) |
| `address_residential_status` | string | Status: "Rent", "Own", "Live with parents/relatives", "Other" |

### Current Landlord Reference

| Field | Type | Description |
|-------|------|-------------|
| `current_ll_name` | string | Current landlord's name |
| `current_ll_email` | string | Current landlord's email |
| `current_ll_tel` | string | Current landlord's phone |
| `agree_to_contact_current_ll` | boolean | Permission to contact current landlord |

---

## Tenant Previous Address

| Field | Type | Description |
|-------|------|-------------|
| `ten_prev_address` | string | Previous address |
| `ten_prev_address_year` | integer | Year moved in |
| `ten_prev_address_month` | integer | Month moved in |
| `ten_prev_address_day` | integer | Day moved in |
| `prev_address_residential_status` | string | Status at previous address |

### Previous Landlord Reference

| Field | Type | Description |
|-------|------|-------------|
| `prev_ll_name` | string | Previous landlord's name |
| `prev_ll_email` | string | Previous landlord's email |
| `prev_ll_tel` | string | Previous landlord's phone |
| `agree_to_contact_prev_ll` | boolean | Permission to contact previous landlord |

---

## Employment & Income

| Field | Type | Description |
|-------|------|-------------|
| `job_title` | string | Current job title |
| `employer` | string | Current employer name |
| `employer_website` | string | Employer's website |
| `employment_length` | string | Time with current employer |
| `income` | integer | Tenant's annual income |
| `partner_income` | integer | Partner's or co-applicants' combined annual income |
| `additional_job_info` | string | Additional employment notes (max 250 chars) |

---

## Vehicles & Pets

| Field | Type | Description |
|-------|------|-------------|
| `car` | boolean | Tenant owns a vehicle |
| `car_info` | string | Vehicle details (max 63 chars) |
| `pet` | boolean | Tenant has pets |
| `pet_info` | string | Pet details (max 63 chars) |

---

## Declarations

| Field | Type | Description |
|-------|------|-------------|
| `smoke` | boolean | Tenant is a smoker |
| `bankruptcy` | boolean | Has declared bankruptcy |
| `bankruptcy_info` | string | Bankruptcy details (max 63 chars) |
| `evicted` | boolean | Has been evicted |
| `refused_to_pay_rent` | boolean | Has refused to pay rent |
| `felony` | boolean | Has felony conviction |
| `additional_info` | string | Additional application notes (max 330 chars) |

---

## Property/Purchase Information

| Field | Type | Description |
|-------|------|-------------|
| `purchase_address` | string | Property address being applied to |
| `purchase_unit` | string | Unit number at property |
| `purchase_rent` | integer | Expected monthly rent |
| `purchase_term` | integer | Lease term in months (minimum 6) |
| `purchase_start_year` | integer | Lease start year |
| `purchase_start_month` | integer | Lease start month |
| `purchase_start_day` | integer | Lease start day |

---

## Control Flags

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `run_now` | boolean | `false` | Process screening immediately |
| `update` | boolean | `false` | Force new report (bypass 30-day cache) |
| `tenant_form` | boolean | `false` | Use direct tenant form |
| `tenant_pays` | boolean | `false` | Tenant provides payment |

---

## Other

| Field | Type | Description |
|-------|------|-------------|
| `promo_code` | string | Promotional code for discounts |
| `callback_url` | string | Webhook URL for notifications |

---

## Address Format

All address fields should follow this format:

```
"Street Address, City, Province/State, Country, Postal/Zip"
```

**Examples:**
```
"123 Main St, Toronto, ON, Canada, M5V 1A1"
"456 Oak Ave, Los Angeles, CA, USA, 90210"
```

**Notes:**
- Use two-letter province/state abbreviations (ON, CA, NY)
- Country should be "Canada" or "USA"
- Canadian postal codes: 6 characters (A1A 1A1)
- US zip codes: 5 digits

---

## Example Request

```json
{
  "external_customer_id": "landlord-12345",
  "external_tenant_id": "tenant-67890",
  "run_now": true,

  "ll_first_name": "John",
  "ll_last_name": "Smith",
  "ll_email": "john@example.com",
  "ll_tel": "5551234567",

  "ten_first_name": "Jane",
  "ten_last_name": "Doe",
  "ten_email": "jane@example.com",
  "ten_tel": "5559876543",
  "ten_dob_year": 1990,
  "ten_dob_month": 6,
  "ten_dob_day": 15,
  "ten_address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
  "ten_sin": "123456789",

  "job_title": "Software Engineer",
  "employer": "Tech Corp",
  "income": 85000,

  "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
  "purchase_rent": 2000,
  "purchase_term": 12,

  "pet": true,
  "pet_info": "One small dog",
  "smoke": false,
  "car": true,
  "car_info": "2020 Toyota Camry"
}
```

---

## See Also

- [Required Fields](./required-fields.md) - Fields required by integration type
- [Optional Fields](./optional-fields.md) - Detailed optional field documentation
- [Validation Rules](./validation-rules.md) - Field validation requirements
