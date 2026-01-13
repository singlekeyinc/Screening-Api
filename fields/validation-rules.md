# Field Validation Rules

This document provides comprehensive validation rules for all fields accepted by the SingleKey API.

## Name Fields

**Applies to:** `ten_first_name`, `ten_last_name`, `ten_middle_name`, `ll_first_name`, `ll_last_name`

| Rule | Requirement |
|------|-------------|
| Length | 1-256 characters |
| Character Set | UTF-8 compatible |
| Empty Values | Not allowed (cannot be null, empty string, or whitespace only) |

### Valid Examples
```
"John"
"Mary-Jane"
"O'Connor"
"José"
"李明"
```

### Invalid Examples
```
""                    # Empty string
"   "                 # Whitespace only
null                  # Null value
```

---

## Email Fields

**Applies to:** `ten_email`, `ll_email`

| Rule | Requirement |
|------|-------------|
| Format | Must contain `@` with characters before and after |
| Domain | Must have 2-5 character TLD |
| Required | Yes (for most flows) |

### Valid Examples
```
"user@example.com"
"user.name@company.co.uk"
"user+tag@domain.org"
```

### Invalid Examples
```
"@example.com"           # Missing local part
"user@"                  # Missing domain
"user@domain"            # Missing TLD
"user@domain.toolong"    # TLD too long (>5 chars)
"userdomain.com"         # Missing @
```

---

## Phone Number Fields

**Applies to:** `ten_tel`, `ll_tel`, `ten_tel_alt`

| Rule | Requirement |
|------|-------------|
| Format | String (not integer) |
| Length | 10 numeric digits, OR 11 digits with leading "1" |
| Country Code | Leading "1" is stripped automatically |
| Special Characters | Brackets, hyphens, spaces are stripped |
| Area Code | Required |

### Valid Examples
```
"5551234567"         # 10 digits
"15551234567"        # 11 digits with country code
"(555) 123-4567"     # Formatted - will be normalized
"555-123-4567"       # Dashes - will be normalized
"1-555-123-4567"     # Full format - will be normalized
```

### Invalid Examples
```
5551234567           # Integer (must be string)
"555123456"          # Only 9 digits
"55512345678"        # 11 digits without leading 1
"155-555-5555"       # Ambiguous (could be 155 area code or 1+555)
"123-4567"           # Missing area code
"555-1234-567"       # Invalid grouping (still only counts digits)
```

### Phone Normalization Process
1. Remove all non-numeric characters
2. If 11 digits and starts with "1", remove leading "1"
3. Validate exactly 10 digits remain

---

## Date of Birth Fields

**Applies to:** `ten_dob_year`, `ten_dob_month`, `ten_dob_day`

### Year (`ten_dob_year`)

| Rule | Requirement |
|------|-------------|
| Format | Integer or string |
| Length | 4 digits |
| Range | After 1900 |
| Age Requirement | Applicant must be 18+ years old |

### Month (`ten_dob_month`)

| Rule | Requirement |
|------|-------------|
| Format | Integer or string |
| Range | 1-12 |

### Day (`ten_dob_day`)

| Rule | Requirement |
|------|-------------|
| Format | Integer or string |
| Range | 1-31 (must be valid for the given month) |

### Valid Examples
```json
{"ten_dob_year": 1990, "ten_dob_month": 6, "ten_dob_day": 15}
{"ten_dob_year": "1985", "ten_dob_month": "12", "ten_dob_day": "31"}
```

### Invalid Examples
```json
{"ten_dob_year": 90, "ten_dob_month": 6, "ten_dob_day": 15}      // 2-digit year
{"ten_dob_year": 1890, "ten_dob_month": 6, "ten_dob_day": 15}    // Before 1900
{"ten_dob_year": 2010, "ten_dob_month": 6, "ten_dob_day": 15}    // Under 18
{"ten_dob_year": 1990, "ten_dob_month": 13, "ten_dob_day": 15}   // Invalid month
{"ten_dob_year": 1990, "ten_dob_month": 2, "ten_dob_day": 30}    // Feb 30 doesn't exist
```

---

## Address Fields

**Applies to:** `ten_address`, `purchase_address`, addresses in `previous_addresses`

| Rule | Requirement |
|------|-------------|
| Format | Must contain at least one comma |
| Countries | USA or Canada only |
| Validation | Google Address API validates the address |

### Recommended Format
```
"Street Address, City, Province/State, Country, Postal/Zip Code"
```

### Postal/Zip Code Rules

**Canadian Postal Codes:**
- 6 characters (letter-number alternating)
- Space optional between first 3 and last 3
- Format: `A1A 1A1` or `A1A1A1`

**US Zip Codes:**
- 5 digits
- Format: `12345`

**Province/State:**
- Two-letter abbreviations preferred
- Examples: `ON`, `BC`, `CA`, `NY`, `TX`

### Valid Examples
```
"123 Main Street, Toronto, ON, Canada, M5V 1A1"
"456 Oak Avenue, Vancouver, British Columbia, Canada, V6B2W2"
"789 Pine Road, Los Angeles, CA, USA, 90210"
"100 Maple Drive, New York, NY, United States, 10001"
```

### Invalid Examples
```
"123 Main Street Toronto ON"        // No commas
"123 Main Street, London, UK"       // Not USA/Canada
"123 Main Street, , ON, Canada"     // Missing city
```

### Address Validation Notes
- Google Address API performs validation, so formatting is somewhat flexible
- Misspellings may be auto-corrected
- Ambiguous addresses will fail validation
- PO Boxes are generally not accepted for tenant addresses

---

## SIN/SSN Fields

**Applies to:** `ten_sin` (used for both Canadian SIN and US SSN)

| Rule | Requirement |
|------|-------------|
| Format | String |
| Length | Exactly 9 digits |
| Characters | Numeric only (no spaces or dashes) |

### Valid Examples
```
"123456789"
```

### Invalid Examples
```
"12345678"           // Only 8 digits
"1234567890"         // 10 digits
"123-456-789"        // Contains dashes
"123 456 789"        // Contains spaces
123456789            // Integer (must be string)
```

### Country-Specific Notes

**Canada (SIN - Social Insurance Number):**
- Required for Canadian credit checks
- First digit indicates province of issuance
- Validates using Luhn algorithm

**USA (SSN - Social Security Number):**
- Required for US credit checks
- Use the same `ten_sin` field name
- Different validation rules apply

---

## Integer Fields

**Applies to:** `purchase_rent`, `ten_annual_income`, `ten_household_income`, etc.

| Rule | Requirement |
|------|-------------|
| Format | Integer |
| Range | -2,147,483,648 to 2,147,483,647 |
| Formatting | No commas or decimals |

### Valid Examples
```json
{"purchase_rent": 1500}
{"ten_annual_income": 75000}
```

### Invalid Examples
```json
{"purchase_rent": "1,500"}      // Contains comma
{"purchase_rent": 1500.00}      // Contains decimal
{"purchase_rent": "$1500"}      // Contains currency symbol
```

---

## Boolean/Radio Fields

**Applies to:** `smoke`, `bankruptcy`, `evicted`, `refused_to_pay_rent`, `felony`, `pet`, `car`

| Rule | Requirement |
|------|-------------|
| Accepted Values | `true`, `false`, `"yes"`, `"no"` |
| Conversion | Boolean `true` is converted to string `"yes"` internally |

### Valid Examples
```json
{"smoke": false}
{"smoke": "no"}
{"pet": true}
{"pet": "yes"}
```

---

## String Fields (General)

**Applies to:** Most text fields not otherwise specified

| Rule | Requirement |
|------|-------------|
| Length | 1-256 characters |
| Character Set | UTF-8 |

---

## Array Fields

**Applies to:** `previous_addresses`, `pets`, `automobiles`, `co_occupants`

| Rule | Requirement |
|------|-------------|
| Format | JSON array |
| Items | Objects with specified schema |

### Example
```json
{
  "pets": [
    {"type": "dog", "breed": "Labrador"},
    {"type": "cat", "breed": "Siamese"}
  ]
}
```

---

## Validation Error Messages

When validation fails, the API returns specific error messages:

| Field Type | Error Message |
|------------|---------------|
| Email | `"Invalid email format"` |
| Phone | `"Phone number must be 10 digits with area code"` |
| DOB | `"Applicant must be at least 18 years old"` |
| Address | `"Address could not be validated"` |
| SIN/SSN | `"SIN/SSN must be exactly 9 digits"` |
| Required | `"[field_name] is required"` |

---

## Testing Validation

Use the `/api/purchase_errors/<screening_id>` endpoint to validate data before processing:

```bash
curl -X POST "https://platform.singlekey.com/api/purchase_errors/12345" \
  -H "Authorization: Token your_api_token"
```

Response with validation errors:
```json
{
  "success": false,
  "errors": [
    "Tenant email is required",
    "Phone number must be 10 digits with area code",
    "Applicant must be at least 18 years old"
  ]
}
```

---

## See Also

- [Required Fields Reference](./required-fields.md)
- [Optional Fields Reference](./optional-fields.md)
- [Error Codes Reference](../troubleshooting/error-codes.md)
