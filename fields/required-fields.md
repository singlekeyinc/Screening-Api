# Required Fields Reference

This document outlines all required fields for SingleKey API requests, organized by integration type and use case.

## Quick Reference

| Integration Type | Required Fields |
|------------------|-----------------|
| Form-Based (Landlord) | `external_customer_id`, `ll_*` fields, `ten_first_name`, `ten_last_name`, `ten_email` |
| Form-Based (Tenant) | `external_customer_id`, `ten_email`, `purchase_address` |
| Direct API (`run_now`) | All landlord fields + full tenant data including DOB, address, phone, SIN/SSN |

---

## Always Required Fields

These fields are required for **all** API requests regardless of integration type.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `external_customer_id` | string | Your unique identifier for the landlord/property manager | `"landlord-12345"` |
| `external_tenant_id` | string | Your unique identifier for the tenant | `"tenant-67890"` |

---

## Form-Based Integration (Landlord Form)

When using the embedded landlord form, the landlord completes most tenant information.

### Landlord Information (Required)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `ll_first_name` | string | Landlord's first name | `"John"` |
| `ll_last_name` | string | Landlord's last name | `"Smith"` |
| `ll_email` | string | Landlord's email address | `"john@example.com"` |
| `ll_tel` | string | Landlord's phone number (10 digits) | `"5551234567"` |

### Tenant Information (Minimal - Required)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `ten_first_name` | string | Tenant's first name | `"Jane"` |
| `ten_last_name` | string | Tenant's last name | `"Doe"` |
| `ten_email` | string | Tenant's email address | `"jane@example.com"` |

### Example Request

```json
{
  "external_customer_id": "landlord-12345",
  "external_tenant_id": "tenant-67890",
  "ll_first_name": "John",
  "ll_last_name": "Smith",
  "ll_email": "john@example.com",
  "ll_tel": "5551234567",
  "ten_first_name": "Jane",
  "ten_last_name": "Doe",
  "ten_email": "jane@example.com"
}
```

---

## Form-Based Integration (Tenant Form)

When using the direct tenant form, minimal information is needed upfront.

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `external_customer_id` | string | Your landlord identifier | `"landlord-12345"` |
| `external_tenant_id` | string | Your tenant identifier | `"tenant-67890"` |
| `ten_email` | string | Tenant's email (for form link) | `"jane@example.com"` |
| `purchase_address` | string | Property address (for jurisdiction) | `"123 Main St, Toronto, ON, Canada, M5V 1A1"` |
| `tenant_form` | boolean | Must be `true` | `true` |

### Example Request

```json
{
  "external_customer_id": "landlord-12345",
  "external_tenant_id": "tenant-67890",
  "ten_email": "jane@example.com",
  "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
  "tenant_form": true
}
```

---

## Direct API Integration (`run_now: true`)

For immediate screening without forms, all tenant data must be provided upfront.

### Landlord Information (Required)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `ll_first_name` | string | Landlord's first name | `"John"` |
| `ll_last_name` | string | Landlord's last name | `"Smith"` |
| `ll_email` | string | Landlord's email address | `"john@example.com"` |

### Tenant Personal Information (Required)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `ten_first_name` | string | Tenant's legal first name | `"Jane"` |
| `ten_last_name` | string | Tenant's legal last name | `"Doe"` |
| `ten_email` | string | Tenant's email address | `"jane@example.com"` |
| `ten_tel` | string | Tenant's phone (10 digits) | `"5559876543"` |

### Tenant Date of Birth (Required)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `ten_dob_year` | integer | Birth year (YYYY) | `1990` |
| `ten_dob_month` | integer | Birth month (1-12) | `6` |
| `ten_dob_day` | integer | Birth day (1-31) | `15` |

### Tenant Address (Required)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `ten_address` | string | Current address (see format below) | `"456 Oak Ave, Vancouver, BC, Canada, V6B 2W2"` |

**Address Format:** `"Street, City, Province/State, Country, Postal/Zip"`

### Identification (Country-Specific)

| Field | Type | Required For | Description | Example |
|-------|------|--------------|-------------|---------|
| `ten_sin` | string | Canada | Social Insurance Number (9 digits) | `"123456789"` |
| `ten_ssn` | string | USA | Social Security Number (9 digits) | `"123456789"` |

> **Note:** Use `ten_sin` for Canadian applicants and `ten_ssn` for US applicants. The field name in the API is `ten_sin` for both, but we recommend using the country-appropriate terminology in your application.

### Example Request

```json
{
  "external_customer_id": "landlord-12345",
  "external_tenant_id": "tenant-67890",
  "run_now": true,
  "ll_first_name": "John",
  "ll_last_name": "Smith",
  "ll_email": "john@example.com",
  "ten_first_name": "Jane",
  "ten_last_name": "Doe",
  "ten_email": "jane@example.com",
  "ten_tel": "5559876543",
  "ten_dob_year": 1990,
  "ten_dob_month": 6,
  "ten_dob_day": 15,
  "ten_address": "456 Oak Ave, Vancouver, BC, Canada, V6B 2W2",
  "ten_sin": "123456789"
}
```

---

## Property Information (Conditionally Required)

| Field | Type | Required When | Description | Example |
|-------|------|---------------|-------------|---------|
| `purchase_address` | string | Tenant form, jurisdiction-specific products | Property address | `"123 Main St, Toronto, ON, Canada"` |
| `jurisdiction` | string | Using specific product | Province/State code | `"ON"` or `"CA"` |

---

## Field Requirements by Endpoint

| Endpoint | Method | Key Required Fields |
|----------|--------|---------------------|
| `/api/request` | POST | `external_customer_id`, `external_tenant_id`, landlord info |
| `/api/report/<token>` | GET | Valid `purchase_token` |
| `/api/applicant/<token>` | GET | Valid `purchase_token` |
| `/api/report_pdf/<token>` | GET | Valid `purchase_token` |
| `/api/purchase_errors/<id>` | POST | Valid `screening_id` |

---

## Validation Rules Summary

| Field Type | Rule |
|------------|------|
| **Names** | 1-256 characters, UTF-8, cannot be empty |
| **Emails** | Must contain `@` with valid domain (2-5 char TLD) |
| **Phones** | 10 digits (or 11 with leading "1"), digits only |
| **DOB Year** | 4 digits, after 1900, applicant must be 18+ |
| **DOB Month** | 1-12 |
| **DOB Day** | 1-31 (must be valid for the month) |
| **SIN/SSN** | Exactly 9 digits, no spaces or dashes |
| **Addresses** | Must contain at least one comma, US/Canada only |

---

## See Also

- [Optional Fields Reference](./optional-fields.md)
- [Field Validation Rules](./validation-rules.md)
- [API Request Endpoint](../api-reference/request.md)
