# Troubleshooting & FAQ

Common issues and their solutions when integrating with the SingleKey API.

## Quick Troubleshooting

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| 401 Unauthorized | Invalid token | Check token, include "Token " prefix |
| 400 Bad Request | Validation error | Check `errors` array in response |
| 404 Not Found | Wrong token/ID | Verify purchase_token or screening_id |
| Empty response | Wrong content-type | Set `Content-Type: application/json` |
| HTML instead of JSON | Blocked by WAF | Contact support |
| Timeout | Large request | Increase timeout, check network |

---

## Frequently Asked Questions

### Authentication

#### Q: I'm getting "Invalid token" but my token is correct?

**A:** Common causes:

1. **Missing prefix:** Use `Token your_token`, not just `your_token`
   ```
   ✗ Authorization: abc123...
   ✓ Authorization: Token abc123...
   ```

2. **Wrong header name:** Use `Authorization`, not `Auth` or `X-API-Key`
   ```
   ✗ Auth: Token abc123...
   ✓ Authorization: Token abc123...
   ```

3. **Extra whitespace:** No leading/trailing spaces
   ```
   ✗ Authorization: Token  abc123...
   ✓ Authorization: Token abc123...
   ```

4. **Environment mismatch:** Production token on sandbox or vice versa

#### Q: How do I get an API token?

**A:** Contact your SingleKey account manager or request access at `support@singlekey.com`. You'll receive separate tokens for sandbox and production environments.

---

### Request Issues

#### Q: My request returns empty or malformed response?

**A:** Ensure you're setting the correct headers:

```bash
curl -X POST "https://platform.singlekey.com/api/request" \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{"your": "json data"}'
```

Missing `Content-Type: application/json` can cause parsing issues.

#### Q: I'm getting validation errors but my data looks correct?

**A:** Common validation issues:

1. **Phone as integer:**
   ```json
   ✗ "ten_tel": 5551234567
   ✓ "ten_tel": "5551234567"
   ```

2. **DOB formatting:**
   ```json
   ✗ "ten_dob": "1990-06-15"
   ✓ "ten_dob_year": 1990, "ten_dob_month": 6, "ten_dob_day": 15
   ```

3. **Address without commas:**
   ```json
   ✗ "ten_address": "123 Main St Toronto ON Canada M5V1A1"
   ✓ "ten_address": "123 Main St, Toronto, ON, Canada, M5V 1A1"
   ```

4. **SIN with formatting:**
   ```json
   ✗ "ten_sin": "123-456-789"
   ✓ "ten_sin": "123456789"
   ```

#### Q: What's the difference between `external_customer_id` and `external_tenant_id`?

**A:**
- `external_customer_id`: Your unique identifier for the **landlord/property manager**
- `external_tenant_id`: Your unique identifier for the **tenant/applicant**

These help you correlate SingleKey records with your system. Use consistent IDs across requests.

---

### Screening Process

#### Q: How long does a screening take?

**A:** Typical processing times:

| Stage | Time |
|-------|------|
| Request received | Immediate |
| Credit check | 30-60 seconds |
| Background check | 30-60 seconds |
| Report generation | 30 seconds |
| **Total** | **2-3 minutes** |

Complex cases may take up to 5 minutes. If longer, contact support.

#### Q: My screening is stuck in "processing"?

**A:** If a screening hasn't completed after 10 minutes:

1. Check if there are validation errors: `GET /api/report/{token}`
2. Verify payment was captured
3. Contact support with the `purchase_token`

#### Q: Can I cancel a screening request?

**A:** Screenings cannot be cancelled once submitted. If the tenant hasn't completed the form, you can let it expire naturally.

#### Q: What happens if I submit the same tenant twice?

**A:**
- **Within 60 seconds:** Duplicate detection returns existing `purchase_token`
- **Within 30 days:** Cached credit data may be reused (no additional charge)
- **After 30 days:** Full new screening (new charge)

To force a new report within 30 days, use `"update": true`:

```json
{
  "external_tenant_id": "tenant-123",
  "update": true,
  // ... other fields
}
```

---

### Reports

#### Q: The `report_url` doesn't work or is expired?

**A:** Report URLs (S3 pre-signed URLs) expire after **5 days**. To get a fresh URL:

```bash
# Call the report endpoint again
curl -X GET "https://platform.singlekey.com/api/report/{token}" \
  -H "Authorization: Token your_token"
```

Each call returns a new URL valid for 5 days.

#### Q: What does `singlekey_score` represent?

**A:** The SingleKey Score is a proprietary score (300-900) that predicts tenant reliability. Higher is better:

| Score Range | Interpretation |
|-------------|----------------|
| 750+ | Excellent |
| 700-749 | Good |
| 650-699 | Fair |
| 600-649 | Below Average |
| <600 | Poor |

Note: Score may be `null` if credit bureau data is unavailable.

#### Q: The report shows `partial: true`. What does that mean?

**A:** A partial report indicates some components couldn't be retrieved:

- Credit bureau temporarily unavailable
- Background check incomplete
- Identity verification pending

You can still proceed with available data or wait for a complete report.

---

### Forms

#### Q: What's the difference between `form_url` and `tenant_form_url`?

**A:**
- `form_url`: Landlord form - landlord fills in property and tenant details
- `tenant_form_url`: Tenant form - tenant completes their own application

Use `tenant_form_url` when you want the tenant to apply directly.

#### Q: Can I customize the form appearance?

**A:** Contact your account manager about white-labeling options. Limited CSS customization may be available.

#### Q: Form links aren't working?

**A:** Check:
1. URL wasn't truncated (especially in emails)
2. Token hasn't expired (7 days for most forms)
3. Form hasn't already been submitted

---

### Webhooks

#### Q: I'm not receiving webhooks?

**A:** Verify:

1. **URL is publicly accessible:**
   ```bash
   curl -X POST https://yoursite.com/webhooks/singlekey -d '{}'
   ```

2. **HTTPS is required** (HTTP won't work)

3. **Responding with 200:**
   ```python
   @app.route('/webhooks/singlekey', methods=['POST'])
   def webhook():
       # Process...
       return '', 200  # Must return 200
   ```

4. **No firewall blocking:** SingleKey IPs must be allowed

5. **callback_url is set in request:**
   ```json
   {
     "callback_url": "https://yoursite.com/webhooks/singlekey",
     // ... other fields
   }
   ```

#### Q: How do I test webhooks locally?

**A:** Use a tunneling service like ngrok:

```bash
# Start your local server
python app.py  # Running on port 5000

# In another terminal
ngrok http 5000

# Use ngrok URL as callback_url
# https://abc123.ngrok.io/webhooks/singlekey
```

#### Q: Webhooks are arriving out of order?

**A:** Webhook order is not guaranteed. Use timestamps and idempotent handlers:

```python
def handle_webhook(event):
    webhook_id = event.get('webhook_id')

    # Check if already processed
    if WebhookLog.objects.filter(webhook_id=webhook_id).exists():
        return  # Already handled

    # Process and log
    WebhookLog.objects.create(webhook_id=webhook_id)
    # ... handle event
```

---

### Payments

#### Q: I'm getting "Payment required" but I have monthly billing?

**A:** Verify with your account manager that:
1. Monthly billing is enabled for your account
2. Your billing is in good standing
3. You're using the correct API token

#### Q: How do I know if payment was successful?

**A:** Check the `payment_status` in the report response:

| Status | Meaning |
|--------|---------|
| `"paid"` | Payment captured |
| `"on hold, payment will be captured on submission"` | Authorized, pending |
| `"unpaid"` | Payment failed |
| `"landlord has not submitted"` | Waiting for form |

---

### Testing

#### Q: How do I test without real charges?

**A:** Use the sandbox environment:

```python
BASE_URL = "https://sandbox.singlekey.com"
```

Sandbox uses test data and doesn't charge real payments. Use test card: `4242424242424242`

#### Q: Are there test tenant IDs?

**A:** In sandbox, use these for free test screenings:
- `test-tenant-001` through `test-tenant-100`

```json
{
  "external_tenant_id": "test-tenant-001",
  // ... other fields
}
```

---

## Error Resolution Guide

### "Address could not be validated"

1. Check address format includes commas:
   ```
   "123 Main St, Toronto, ON, Canada, M5V 1A1"
   ```

2. Verify address exists (Google Maps)

3. Include all components:
   - Street number and name
   - City
   - Province/State
   - Country
   - Postal/ZIP code

4. Try variations:
   ```
   "123 Main Street" vs "123 Main St"
   "Ontario" vs "ON"
   ```

### "Applicant must be at least 18 years old"

1. Double-check DOB values:
   ```json
   {
     "ten_dob_year": 1990,   // Not 90
     "ten_dob_month": 6,     // Not "June"
     "ten_dob_day": 15
   }
   ```

2. Verify tenant is actually 18+

3. Check for transposed values (year vs day)

### "Phone must be 10 digits"

1. Remove all non-digit characters:
   ```python
   phone = ''.join(filter(str.isdigit, raw_phone))
   ```

2. Handle country code:
   ```python
   if len(phone) == 11 and phone.startswith('1'):
       phone = phone[1:]  # Remove leading 1
   ```

3. Pass as string, not integer

### "Credit bureau unavailable"

1. This is temporary - retry in 30 minutes
2. If persists, contact support
3. Can submit request with `run_now: false` to queue

---

## Getting Help

### Support Channels

| Issue Type | Contact |
|------------|---------|
| API questions | `api-support@singlekey.com` |
| Account/billing | `support@singlekey.com` |
| Urgent production issues | Contact your account manager |

### Information to Include

When contacting support, include:
- `purchase_token` or `screening_id`
- Timestamp of the request
- Full error message
- Request payload (redact sensitive data)
- Environment (sandbox/production)

### API Status

Check API status at: `https://status.singlekey.com`

---

## See Also

- [Error Codes Reference](./error-codes.md)
- [Field Validation Rules](../fields/validation-rules.md)
- [API Reference](../api-reference/)
