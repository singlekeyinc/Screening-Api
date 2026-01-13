# Authentication

All SingleKey API requests require authentication using a token in the request header.

## API Token

You'll receive two API tokens from your SingleKey account manager:
- **Sandbox Token**: For testing and development
- **Production Token**: For live operations

## Header Format

Include your token in the `Authorization` header with the `Token` prefix:

```
Authorization: Token your_api_token_here
```

## Example Request

```bash
curl -X GET "https://platform.singlekey.com/api/report/abc123" \
  -H "Authorization: Token sk_live_abc123def456..."
```

## Common Mistakes

| Mistake | Incorrect | Correct |
|---------|-----------|---------|
| Missing prefix | `Authorization: abc123` | `Authorization: Token abc123` |
| Wrong prefix | `Authorization: Bearer abc123` | `Authorization: Token abc123` |
| Missing header | (no Authorization header) | `Authorization: Token abc123` |
| Extra whitespace | `Authorization: Token  abc123` | `Authorization: Token abc123` |

## Security Best Practices

### Keep Tokens Secret

- Never commit tokens to source control
- Use environment variables:

```python
import os

API_TOKEN = os.environ.get('SINGLEKEY_API_TOKEN')
```

```javascript
const API_TOKEN = process.env.SINGLEKEY_API_TOKEN;
```

### Use Different Tokens Per Environment

```python
# config.py
import os

if os.environ.get('ENV') == 'production':
    API_TOKEN = os.environ.get('SINGLEKEY_PRODUCTION_TOKEN')
    BASE_URL = "https://platform.singlekey.com"
else:
    API_TOKEN = os.environ.get('SINGLEKEY_SANDBOX_TOKEN')
    BASE_URL = "https://sandbox.singlekey.com"
```

### Rotate Tokens Periodically

Contact support to rotate your API tokens if:
- A token may have been exposed
- An employee with access leaves
- Regular security policy requires rotation

## Token Scopes

All API tokens currently have full access to:
- Create screening requests
- Retrieve reports
- Access applicant data
- Manage payments

Contact your account manager if you need restricted-scope tokens.

## Authentication Errors

| Error | Status Code | Meaning |
|-------|-------------|---------|
| `"Invalid token."` | 401 | Token is incorrect or revoked |
| `"Authentication credentials were not provided."` | 401 | Missing Authorization header |
| `"Token has expired"` | 401 | Token needs renewal |

## Testing Authentication

Verify your token is working:

```bash
curl -X GET "https://platform.singlekey.com/api/payments" \
  -H "Authorization: Token your_token" \
  -w "\nStatus: %{http_code}\n"
```

Expected response for valid token:
```json
{
  "success": true,
  "has_payment_method": true,
  ...
}
```

---

## See Also

- [Environments](./environments.md)
- [Quickstart Guide](./quickstart.md)
