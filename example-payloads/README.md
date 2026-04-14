# Example Payloads

Example request payloads for the SingleKey Screening API.

## Contents

| File | Description |
|------|-------------|
| [direct-api-request.md](./direct-api-request.md) | Immediate screening with all data (`run_now: true`) |
| [landlord-form-request.md](./landlord-form-request.md) | Request a landlord form |
| [tenant-form-request.md](./tenant-form-request.md) | Request a direct tenant form (`tenant_form: true`) |

## Quick Reference

| Request Type | Key Parameters | Result |
|--------------|----------------|--------|
| Direct API | `run_now: true` + all tenant data | Immediate processing |
| Landlord Form | Minimal data | Returns `form_url` for landlord |
| Tenant Form | `tenant_form: true` + `purchase_address` | Returns `tenant_form_url` |

## Endpoints

Use the endpoint that matches your integration type:

| Integration | Endpoint |
|-------------|----------|
| Form-based (Landlord/Tenant) | `POST /screen/embedded_flow_request` |
| Direct API (immediate screening) | `POST /api/request` |

Both endpoints accept the same fields. The difference is that `/api/request` automatically sets `run_now: true`, triggering immediate processing. For form-based flows where a landlord or tenant needs to complete a form first, use `/screen/embedded_flow_request`.

## Headers

```
Authorization: Token your_api_token
Content-Type: application/json
```
