# Environments

SingleKey provides two environments for API integration.

## Available Environments

| Environment | Base URL | Purpose |
|-------------|----------|---------|
| **Sandbox** | `https://sandbox.singlekey.com` | Testing and development |
| **Production** | `https://platform.singlekey.com` | Live operations |

## Sandbox Environment

Use sandbox for development and testing:

- No real charges
- No real credit checks
- Test data returned
- Safe for experimentation

### Sandbox Features

| Feature | Behavior |
|---------|----------|
| Payments | Simulated (use test cards) |
| Credit checks | Returns mock data |
| Background checks | Returns mock data |
| Webhooks | Sent to your callback URL |
| Data retention | Cleared periodically |

### Test Cards (Sandbox)

| Card Number | Result |
|-------------|--------|
| `4242424242424242` | Success |
| `4000000000000002` | Declined |
| `4000000000009995` | Insufficient funds |

Use any future expiration date and any 3-digit CVC.

### Test Tenant IDs

For free test screenings in sandbox:

```json
{
  "external_tenant_id": "test-tenant-001",
  // ... other fields
}
```

IDs `test-tenant-001` through `test-tenant-100` return mock data without charges.

## Production Environment

Use production for live operations:

- Real charges applied
- Real credit bureau data
- Real background checks
- All data retained

### Production Checklist

Before going live:

- [ ] Tested all flows in sandbox
- [ ] Production API token configured
- [ ] Webhook endpoint deployed and tested
- [ ] Error handling implemented
- [ ] Payment method added (or monthly billing enabled)
- [ ] SSL certificate valid on webhook endpoint

## Environment-Specific Configuration

### Python

```python
import os

ENV = os.environ.get('ENVIRONMENT', 'sandbox')

if ENV == 'production':
    BASE_URL = "https://platform.singlekey.com"
    API_TOKEN = os.environ.get('SINGLEKEY_PROD_TOKEN')
else:
    BASE_URL = "https://sandbox.singlekey.com"
    API_TOKEN = os.environ.get('SINGLEKEY_SANDBOX_TOKEN')
```

### JavaScript

```javascript
const ENV = process.env.ENVIRONMENT || 'sandbox';

const config = {
  production: {
    baseUrl: 'https://platform.singlekey.com',
    apiToken: process.env.SINGLEKEY_PROD_TOKEN
  },
  sandbox: {
    baseUrl: 'https://sandbox.singlekey.com',
    apiToken: process.env.SINGLEKEY_SANDBOX_TOKEN
  }
}[ENV];
```

### Environment Variables

```bash
# .env.development
ENVIRONMENT=sandbox
SINGLEKEY_SANDBOX_TOKEN=sk_test_abc123...

# .env.production
ENVIRONMENT=production
SINGLEKEY_PROD_TOKEN=sk_live_xyz789...
```

## Switching Environments

| Change | Sandbox to Production |
|--------|----------------------|
| Base URL | `sandbox.singlekey.com` → `platform.singlekey.com` |
| API Token | Sandbox token → Production token |
| Payment cards | Test cards → Real cards |
| Data | Mock data → Real data |

## Data Isolation

- Sandbox and production data are completely separate
- Tokens only work in their respective environment
- No data transfers between environments

## Rate Limits

| Environment | Rate Limit |
|-------------|------------|
| Sandbox | 100 requests/minute |
| Production | 1000 requests/minute |

Contact support if you need higher limits.

---

## See Also

- [Authentication](./authentication.md)
- [Quickstart Guide](./quickstart.md)
