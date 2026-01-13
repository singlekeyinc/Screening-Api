#!/bin/bash
# SingleKey API cURL Examples
#
# Replace YOUR_API_TOKEN with your actual API token
# Replace placeholder values with real data
#
# Usage:
#   chmod +x examples.sh
#   ./examples.sh

API_TOKEN="YOUR_API_TOKEN"
BASE_URL="https://platform.singlekey.com"
# Use sandbox for testing:
# BASE_URL="https://sandbox.singlekey.com"

# ============================================================================
# 1. CREATE SCREENING - Direct API (run_now: true)
# ============================================================================
echo "=== Creating Direct API Screening ==="

curl -X POST "${BASE_URL}/api/request" \
  -H "Authorization: Token ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-456",
    "run_now": true,
    "ll_first_name": "John",
    "ll_last_name": "Smith",
    "ll_email": "landlord@example.com",
    "ll_tel": "5551234567",
    "ten_first_name": "Jane",
    "ten_last_name": "Doe",
    "ten_email": "tenant@example.com",
    "ten_tel": "5559876543",
    "ten_dob_year": 1990,
    "ten_dob_month": 6,
    "ten_dob_day": 15,
    "ten_address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
    "ten_sin": "123456789",
    "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
    "purchase_rent": 2000,
    "callback_url": "https://yoursite.com/webhooks/singlekey"
  }'

echo -e "\n"

# ============================================================================
# 2. CREATE SCREENING - Form-Based (Landlord Form)
# ============================================================================
echo "=== Creating Landlord Form Screening ==="

curl -X POST "${BASE_URL}/api/request" \
  -H "Authorization: Token ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-789",
    "ll_first_name": "John",
    "ll_last_name": "Smith",
    "ll_email": "landlord@example.com",
    "ll_tel": "5551234567",
    "ten_first_name": "Jane",
    "ten_last_name": "Doe",
    "ten_email": "tenant@example.com",
    "callback_url": "https://yoursite.com/webhooks/singlekey"
  }'

echo -e "\n"

# ============================================================================
# 3. CREATE SCREENING - Form-Based (Tenant Form)
# ============================================================================
echo "=== Creating Tenant Form Screening ==="

curl -X POST "${BASE_URL}/api/request" \
  -H "Authorization: Token ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "external_customer_id": "landlord-123",
    "external_tenant_id": "tenant-101",
    "tenant_form": true,
    "ten_email": "tenant@example.com",
    "purchase_address": "123 Main St, Toronto, ON, Canada, M5V 1A1",
    "callback_url": "https://yoursite.com/webhooks/singlekey"
  }'

echo -e "\n"

# ============================================================================
# 4. GET SCREENING REPORT
# ============================================================================
echo "=== Getting Screening Report ==="

PURCHASE_TOKEN="abc123def456ghi789jkl012mno345pq"  # Replace with actual token

curl -X GET "${BASE_URL}/api/report/${PURCHASE_TOKEN}" \
  -H "Authorization: Token ${API_TOKEN}"

echo -e "\n"

# ============================================================================
# 5. GET APPLICANT INFORMATION
# ============================================================================
echo "=== Getting Applicant Info ==="

curl -X GET "${BASE_URL}/api/applicant/${PURCHASE_TOKEN}" \
  -H "Authorization: Token ${API_TOKEN}"

echo -e "\n"

# With detailed info and credit score
echo "=== Getting Detailed Applicant Info ==="

curl -X GET "${BASE_URL}/api/applicant/${PURCHASE_TOKEN}?detailed=true&show_credit_score=true" \
  -H "Authorization: Token ${API_TOKEN}"

echo -e "\n"

# ============================================================================
# 6. VALIDATE SCREENING DATA
# ============================================================================
echo "=== Validating Screening Data ==="

SCREENING_ID="12345"  # Replace with actual screening ID

curl -X POST "${BASE_URL}/api/purchase_errors/${SCREENING_ID}" \
  -H "Authorization: Token ${API_TOKEN}"

echo -e "\n"

# ============================================================================
# 7. DOWNLOAD REPORT PDF
# ============================================================================
echo "=== Downloading Report PDF ==="

curl -X GET "${BASE_URL}/api/report_pdf/${PURCHASE_TOKEN}" \
  -H "Authorization: Token ${API_TOKEN}" \
  -o screening_report.pdf

echo "PDF saved to screening_report.pdf"
echo -e "\n"

# ============================================================================
# 8. CHECK PAYMENT STATUS
# ============================================================================
echo "=== Checking Payment Status ==="

curl -X GET "${BASE_URL}/api/payments" \
  -H "Authorization: Token ${API_TOKEN}"

echo -e "\n"

# ============================================================================
# 9. POLL FOR REPORT COMPLETION
# ============================================================================
echo "=== Polling for Report Completion ==="

poll_for_report() {
  local token=$1
  local max_attempts=30
  local delay=10

  for ((i=1; i<=max_attempts; i++)); do
    echo "Attempt $i of $max_attempts..."

    response=$(curl -s -X GET "${BASE_URL}/api/report/${token}" \
      -H "Authorization: Token ${API_TOKEN}")

    # Check if report is complete
    success=$(echo "$response" | grep -o '"success": *true')
    score=$(echo "$response" | grep -o '"singlekey_score": *[0-9]*')

    if [ -n "$success" ] && [ -n "$score" ]; then
      echo "Report ready!"
      echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
      return 0
    fi

    # Extract status
    detail=$(echo "$response" | grep -o '"detail": *"[^"]*"')
    echo "Status: $detail"

    sleep $delay
  done

  echo "Timeout waiting for report"
  return 1
}

# Uncomment to use:
# poll_for_report "$PURCHASE_TOKEN"

# ============================================================================
# 10. PRETTY PRINT RESPONSE
# ============================================================================
echo "=== Example with Pretty Print ==="

curl -s -X GET "${BASE_URL}/api/report/${PURCHASE_TOKEN}" \
  -H "Authorization: Token ${API_TOKEN}" | python3 -m json.tool

echo -e "\n"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

# Function to create screening and wait for result
create_and_wait() {
  echo "Creating screening..."

  response=$(curl -s -X POST "${BASE_URL}/api/request" \
    -H "Authorization: Token ${API_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{
      "external_customer_id": "landlord-123",
      "external_tenant_id": "tenant-'"$(date +%s)"'",
      "run_now": true,
      "ll_first_name": "John",
      "ll_last_name": "Smith",
      "ll_email": "landlord@example.com",
      "ten_first_name": "Jane",
      "ten_last_name": "Doe",
      "ten_email": "tenant@example.com",
      "ten_tel": "5559876543",
      "ten_dob_year": 1990,
      "ten_dob_month": 6,
      "ten_dob_day": 15,
      "ten_address": "456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
      "ten_sin": "123456789"
    }')

  echo "Response: $response"

  # Extract purchase token
  token=$(echo "$response" | grep -o '"purchase_token": *"[^"]*"' | cut -d'"' -f4)

  if [ -n "$token" ]; then
    echo "Purchase token: $token"
    echo "Waiting for report..."
    poll_for_report "$token"
  else
    echo "Failed to create screening"
  fi
}

# Uncomment to run full flow:
# create_and_wait

echo "=== Examples Complete ==="
