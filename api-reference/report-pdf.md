# Download Report PDF

`GET /api/report_pdf/<purchase_token>`

Downloads the screening report as a PDF file. This endpoint returns the actual PDF binary data as a file attachment.

## Authentication

| Header | Value |
|--------|-------|
| `Authorization` | `Token <your_api_token>` |

## Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `purchase_token` | string | Yes | The 32-character purchase token from the screening request |

## Request

```bash
curl -X GET "https://platform.singlekey.com/api/report_pdf/abc123def456ghi789jkl012mno345pq" \
  -H "Authorization: Token your_api_token" \
  -o screening_report.pdf
```

## Response

### Success

Returns a PDF file with the following headers:

```
Content-Type: application/pdf
Content-Disposition: attachment; filename="John_Doe_screening.pdf"
```

The filename is formatted as `{tenant_first_name}_{tenant_last_name}_screening.pdf`.

### Error - Report Not Ready

```json
{
  "success": false,
  "detail": "Report is not ready yet"
}
```

### Error - Not Found

```json
{
  "detail": "Report does not exist"
}
```

## HTTP Status Codes

| Status | Description |
|--------|-------------|
| `200` | Success - PDF file returned |
| `400` | Report not ready or processing |
| `401` | Invalid or missing authentication token |
| `404` | Screening not found |
| `500` | Internal server error |

## Usage Examples

### Python - Download and Save

```python
import requests

def download_report_pdf(purchase_token, api_token, output_path="report.pdf"):
    response = requests.get(
        f"https://platform.singlekey.com/api/report_pdf/{purchase_token}",
        headers={"Authorization": f"Token {api_token}"},
        stream=True
    )

    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Report saved to {output_path}")
        return True
    else:
        print(f"Error: {response.json()}")
        return False

# Usage
download_report_pdf("abc123...", "your_token", "tenant_report.pdf")
```

### JavaScript - Download in Browser

```javascript
async function downloadReportPdf(purchaseToken) {
  const response = await fetch(
    `https://platform.singlekey.com/api/report_pdf/${purchaseToken}`,
    {
      headers: {
        'Authorization': `Token ${API_TOKEN}`
      }
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  // Get filename from Content-Disposition header
  const contentDisposition = response.headers.get('Content-Disposition');
  const filename = contentDisposition
    ? contentDisposition.split('filename=')[1].replace(/"/g, '')
    : 'screening_report.pdf';

  // Create blob and download
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  a.remove();
}
```

### cURL - Save to File

```bash
# Download and save with automatic filename
curl -X GET "https://platform.singlekey.com/api/report_pdf/abc123..." \
  -H "Authorization: Token your_api_token" \
  -OJ

# Download and save to specific path
curl -X GET "https://platform.singlekey.com/api/report_pdf/abc123..." \
  -H "Authorization: Token your_api_token" \
  -o "/path/to/reports/tenant_screening.pdf"
```

## Best Practices

### Check Report Status First

Before attempting to download the PDF, verify the report is ready:

```python
def get_report_when_ready(purchase_token, api_token):
    # First check if report is ready
    status_response = requests.get(
        f"https://platform.singlekey.com/api/report/{purchase_token}",
        headers={"Authorization": f"Token {api_token}"}
    )

    status = status_response.json()

    if not status.get("success") or not status.get("pdf_report_ready"):
        return {"ready": False, "status": status.get("detail", "Report not ready")}

    # Report is ready, download PDF
    return download_report_pdf(purchase_token, api_token)
```

### Handle Large Files

For large reports, use streaming to avoid memory issues:

```python
# Good - streaming download
response = requests.get(url, stream=True)
with open(output_path, 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

# Avoid - loading entire file into memory
response = requests.get(url)
with open(output_path, 'wb') as f:
    f.write(response.content)
```

## Related Endpoints

| Endpoint | Description |
|----------|-------------|
| [`GET /api/report/<token>`](./report.md) | Get report data and status (includes S3 URL) |
| [`GET /api/applicant/<token>`](./applicant.md) | Get applicant information |

## Notes

- The PDF includes all screening results: credit report, background check, and SingleKey score
- PDF generation may take a few seconds after screening completion
- Check `pdf_report_ready` in the report status before downloading
- PDFs are generated on-demand and may vary slightly in formatting
