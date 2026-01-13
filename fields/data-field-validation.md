# Data Field Validation

Validation rules for all fields submitted to the SingleKey API. Requests that violate these rules will fail with descriptive error messages.

## Error Response Format

When validation fails, you'll receive:

```json
{
  "success": false,
  "detail": "missing or incomplete data",
  "errors": [
    "ten_tel: the phone number --555555-- is not the expected length"
  ]
}
```

---

## Name Fields

**Applies to:** `ten_first_name`, `ten_last_name`, `ll_first_name`, `ll_last_name`

| Rule | Requirement |
|------|-------------|
| Type | String |
| Length | 1-256 characters |
| Characters | Any UTF-8 character |
| Required | Cannot be null, empty, or whitespace |

### Examples

| Value | Valid | Reason |
|-------|-------|--------|
| `"John"` | Yes | |
| `"Mary-Jane"` | Yes | Hyphens allowed |
| `"O'Connor"` | Yes | Apostrophes allowed |
| `"José"` | Yes | UTF-8 characters allowed |
| `""` | No | Empty string |
| `null` | No | Null value |
| `"   "` | No | Whitespace only |

---

## Email Fields

**Applies to:** `ten_email`, `ll_email`

| Rule | Requirement |
|------|-------------|
| Type | String |
| Format | Must contain `@` with local part and domain |
| Domain TLD | 2-5 characters |

### Examples

| Value | Valid | Reason |
|-------|-------|--------|
| `"user@example.com"` | Yes | |
| `"user.name@company.co.uk"` | Yes | |
| `"user+tag@domain.org"` | Yes | |
| `"@example.com"` | No | Missing local part |
| `"user@"` | No | Missing domain |
| `"user@domain"` | No | Missing TLD |
| `"user@domain.toolong"` | No | TLD exceeds 5 characters |

---

## Phone Number Fields

**Applies to:** `ten_tel`, `ll_tel`

| Rule | Requirement |
|------|-------------|
| Type | String (not integer) |
| Length | 10 digits, or 11 digits with leading "1" |
| Format | Brackets and hyphens allowed |
| Area Code | Required (3 digits) |

### Important Notes

- Phone numbers **must be strings**, not integers
- Leading "1" is stripped before saving
- Only numeric characters count toward length
- A 10-digit number starting with "1" is invalid (becomes 9 digits after stripping)

### Examples

| Value | Valid | Reason |
|-------|-------|--------|
| `"5551234567"` | Yes | 10 digits |
| `"1-555-123-4567"` | Yes | 11 digits with country code |
| `"(555) 123-4567"` | Yes | Formatting stripped |
| `"[555]5555555"` | Yes | Brackets allowed |
| `5551234567` | No | Must be string, not integer |
| `"555123456"` | No | Only 9 digits |
| `"155-555-5555"` | No | After stripping "1", becomes 9 digits |
| `"123-4567"` | No | Missing area code |

### Normalization Process

```
Input: "(555) 123-4567"
Step 1: Remove non-digits → "5551234567"
Step 2: Check length → 10 digits ✓
Result: Valid
```

```
Input: "155-555-5555"
Step 1: Remove non-digits → "1555555555"
Step 2: Starts with "1" and 11 digits? No (10 digits)
Step 3: Check if 10 digits → Yes, but starts with "1"
Step 4: After stripping "1" → "555555555" (9 digits)
Result: Invalid
```

---

## Date of Birth Fields

**Applies to:** `ten_dob_year`, `ten_dob_month`, `ten_dob_day`

### Year (`ten_dob_year`)

| Rule | Requirement |
|------|-------------|
| Type | Integer or string |
| Length | 4 digits |
| Range | After 1900 |
| Age | Applicant must be 18+ years old |

### Month (`ten_dob_month`)

| Rule | Requirement |
|------|-------------|
| Type | Integer or string |
| Range | 1-12 |

### Day (`ten_dob_day`)

| Rule | Requirement |
|------|-------------|
| Type | Integer or string |
| Range | 1-31 (must be valid for month) |

### Examples

| Value | Valid | Reason |
|-------|-------|--------|
| `{"year": 1990, "month": 6, "day": 15}` | Yes | |
| `{"year": "1990", "month": "06", "day": "15"}` | Yes | Strings accepted |
| `{"year": 90, "month": 6, "day": 15}` | No | Year must be 4 digits |
| `{"year": 1890, "month": 6, "day": 15}` | No | Before 1900 |
| `{"year": 2010, "month": 6, "day": 15}` | No | Under 18 years old |
| `{"year": 1990, "month": 13, "day": 15}` | No | Invalid month |
| `{"year": 1990, "month": 2, "day": 30}` | No | February 30 doesn't exist |

---

## Address Fields

**Applies to:** `ten_address`, `purchase_address`

| Rule | Requirement |
|------|-------------|
| Type | String |
| Format | Must contain at least one comma |
| Countries | USA or Canada only |
| Validation | Google Address API validates |

### Recommended Format

```
"Street Address, City, Province/State, Country, Postal/Zip"
```

### Postal Code Rules

| Country | Format | Example |
|---------|--------|---------|
| Canada | 6 characters (letter-number alternating) | `M5V 1A1` |
| USA | 5 digits | `90210` |

### Province/State

- Use two-letter abbreviations: `ON`, `BC`, `CA`, `NY`, `TX`
- Full names work but abbreviations preferred

### Examples

| Value | Valid | Reason |
|-------|-------|--------|
| `"123 Main St, Toronto, ON, Canada, M5V 1A1"` | Yes | |
| `"456 Oak Ave, Los Angeles, CA, USA, 90210"` | Yes | |
| `"100 Young Street, Toronto"` | Yes | Google corrects |
| `"123 Main St Toronto ON Canada"` | No | No commas |
| `"123 Main St, London, UK"` | No | Not USA/Canada |

### Google Address API Notes

- Addresses are validated via Google Maps API
- Minor formatting issues may be auto-corrected
- Misspellings like "Young" → "Yonge" may be fixed
- Provide complete addresses for best results

---

## SIN/SSN Field

**Applies to:** `ten_sin`

| Rule | Requirement |
|------|-------------|
| Type | String |
| Length | Exactly 9 digits |
| Characters | Numeric only |
| Required | Yes for Canadian addresses; Yes for US addresses |

### Examples

| Value | Valid | Reason |
|-------|-------|--------|
| `"123456789"` | Yes | |
| `"12345678"` | No | Only 8 digits |
| `"1234567890"` | No | 10 digits |
| `"123-456-789"` | No | Contains dashes |
| `"123 456 789"` | No | Contains spaces |
| `123456789` | No | Must be string |

---

## Integer Fields

**Applies to:** `income`, `purchase_rent`, `ll_n_properties`, etc.

| Rule | Requirement |
|------|-------------|
| Type | Integer |
| Range | -2,147,483,648 to +2,147,483,647 |
| Format | No commas or decimals |

### Examples

| Value | Valid | Reason |
|-------|-------|--------|
| `75000` | Yes | |
| `"75000"` | No | Must be integer |
| `75,000` | No | Contains comma |
| `75000.00` | No | Contains decimal |

---

## String Fields

**Applies to:** Most text fields

| Rule | Requirement |
|------|-------------|
| Type | String |
| Length | 1-256 characters (unless specified otherwise) |
| Characters | UTF-8 |

### Special Length Limits

| Field | Max Length |
|-------|------------|
| `car_info` | 63 characters |
| `pet_info` | 63 characters |
| `bankruptcy_info` | 63 characters |
| `additional_job_info` | 250 characters |
| `additional_info` | 330 characters |

---

## Boolean Fields

**Applies to:** `car`, `pet`, `smoke`, `bankruptcy`, `evicted`, `refused_to_pay_rent`, `felony`, `run_now`, `update`

| Rule | Requirement |
|------|-------------|
| Type | Boolean |
| Values | `true` or `false` |

Some boolean fields also accept string values `"yes"` or `"no"`.

---

## Quick Reference

| Field Type | Key Rules |
|------------|-----------|
| **Names** | 1-256 chars, UTF-8, not empty |
| **Emails** | Contains `@`, valid domain, 2-5 char TLD |
| **Phones** | String, 10 digits (or 11 with leading 1), includes area code |
| **DOB Year** | 4 digits, after 1900, applicant 18+ |
| **DOB Month** | 1-12 |
| **DOB Day** | 1-31, valid for month |
| **Addresses** | Contains comma, USA/Canada only |
| **SIN/SSN** | Exactly 9 digits, string |
| **Integers** | No commas/decimals, within int32 range |
| **Strings** | 1-256 chars (varies by field) |

---

## See Also

- [Required Fields](./required-fields.md)
- [Available Fields](./available_fields.md)
- [Error Codes](../troubleshooting/error-codes.md)
