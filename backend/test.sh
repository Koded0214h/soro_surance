#!/bin/bash

set -e  # exit on error

HOST="http://localhost:8000"

# --- Generate unique phone numbers using a timestamp ---
TIMESTAMP=$(date +%s)
CUSTOMER_REG_PHONE="+23480000${TIMESTAMP}"
CUSTOMER_REG_PASSWORD="testpassword123"
ADMIN_REG_PHONE="+23480001${TIMESTAMP}"
ADMIN_REG_PASSWORD="admintest123"

CUSTOMER_PHONE="${CUSTOMER_REG_PHONE}"
CUSTOMER_PASSWORD="${CUSTOMER_REG_PASSWORD}"
ADMIN_PHONE="${ADMIN_REG_PHONE}"
ADMIN_PASSWORD="${ADMIN_REG_PASSWORD}"

# Placeholders
CUSTOMER_TOKEN=""
ADMIN_TOKEN=""
PRODUCT_ID=""
POLICY_ID=""
CLAIM_ID=""
PAYMENT_REFERENCE=""

# Helper: print JSON if valid, otherwise raw text
pretty_print() {
    if echo "$1" | jq . >/dev/null 2>&1; then
        echo "$1" | jq .
    else
        echo "$1"
    fi
}

# Create dummy audio file
echo "Creating dummy.wav for voice claim test..."
echo "fake audio data" > dummy.wav
echo "dummy.wav created."
echo ""

# --- User Registration ---
echo "--- Registering Customer User (${CUSTOMER_REG_PHONE}) ---"
response=$(curl -s -X POST "${HOST}/api/register/" \
    -H "Content-Type: application/json" \
    -d "{\"phone_number\": \"${CUSTOMER_REG_PHONE}\", \"email\": \"customer-${TIMESTAMP}@example.com\", \"first_name\": \"Test\", \"last_name\": \"Customer\", \"password\": \"${CUSTOMER_REG_PASSWORD}\", \"password2\": \"${CUSTOMER_REG_PASSWORD}\", \"user_type\": \"customer\", \"date_of_birth\": \"1990-01-01\"}")
pretty_print "$response"
echo ""

echo "--- Registering Admin User (${ADMIN_REG_PHONE}) ---"
response=$(curl -s -X POST "${HOST}/api/register/" \
    -H "Content-Type: application/json" \
    -d "{\"phone_number\": \"${ADMIN_REG_PHONE}\", \"email\": \"admin-${TIMESTAMP}@example.com\", \"first_name\": \"Test\", \"last_name\": \"Admin\", \"password\": \"${ADMIN_REG_PASSWORD}\", \"password2\": \"${ADMIN_REG_PASSWORD}\", \"user_type\": \"admin\", \"date_of_birth\": \"1985-05-15\"}")
pretty_print "$response"
echo ""

# --- 1. Customer Login ---
echo "--- 1. Customer Login ---"
response=$(curl -s -X POST "${HOST}/api/token/" \
    -H "Content-Type: application/json" \
    -d "{\"phone_number\": \"${CUSTOMER_PHONE}\", \"password\": \"${CUSTOMER_PASSWORD}\"}")
CUSTOMER_TOKEN=$(echo "$response" | jq -r '.access')
echo "Customer Token: ${CUSTOMER_TOKEN}"
pretty_print "$response"
echo ""

# --- 2. List Products ---
echo "--- 2. List Products ---"
response=$(curl -s -X GET "${HOST}/api/products/" -H "Authorization: Bearer ${CUSTOMER_TOKEN}")
PRODUCT_ID=$(echo "$response" | jq -r '.results[0].id')
if [ -z "$PRODUCT_ID" ] || [ "$PRODUCT_ID" = "null" ]; then
    echo "ERROR: No products found. Please create at least one product via Django admin or shell."
    exit 1
fi
echo "Product ID: ${PRODUCT_ID}"
pretty_print "$response"
echo ""

# --- 3. Calculate Premium ---
echo "--- 3. Calculate Premium ---"
response=$(curl -s -X POST "${HOST}/api/products/${PRODUCT_ID}/calculate_premium/" \
    -H "Authorization: Bearer ${CUSTOMER_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"soro_score\": 60}")
pretty_print "$response"
echo ""

# --- 4. Create Policy (send product ID as integer) ---
echo "--- 4. Create Policy ---"
response=$(curl -s -X POST "${HOST}/api/policies/" \
    -H "Authorization: Bearer ${CUSTOMER_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"product\": ${PRODUCT_ID}, \"start_date\": \"2026-02-14\", \"end_date\": \"2027-02-14\", \"status\": \"draft\"}")
POLICY_ID=$(echo "$response" | jq -r '.id')
if [ -z "$POLICY_ID" ] || [ "$POLICY_ID" = "null" ]; then
    echo "ERROR: Policy creation failed."
    pretty_print "$response"
    exit 1
fi
echo "Policy ID: ${POLICY_ID}"
pretty_print "$response"
echo ""

# --- 5. Initiate Payment ---
echo "--- 5. Initiate Payment ---"
response=$(curl -s -X POST "${HOST}/api/payments/initiate_payment/" \
    -H "Authorization: Bearer ${CUSTOMER_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"amount\": 10000.00, \"payment_type\": \"premium\", \"currency\": \"NGN\", \"policy_id\": ${POLICY_ID}}")
PAYMENT_REFERENCE=$(echo "$response" | jq -r '.payment_reference')
echo "Payment Reference: ${PAYMENT_REFERENCE}"
pretty_print "$response"
echo ""

# --- 6. Verify Payment ---
echo "--- 6. Verify Payment ---"
if [ -n "$PAYMENT_REFERENCE" ] && [ "$PAYMENT_REFERENCE" != "null" ]; then
    response=$(curl -s -X POST "${HOST}/api/payments/verify_payment/" \
        -H "Authorization: Bearer ${CUSTOMER_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{\"reference\": \"${PAYMENT_REFERENCE}\"}")
    pretty_print "$response"
else
    echo "No valid payment reference to verify."
fi
echo ""

# --- 7. File a Claim with Audio ---
echo "--- 7. File a Claim ---"
response=$(curl -s -X POST "${HOST}/api/claims/" \
    -H "Authorization: Bearer ${CUSTOMER_TOKEN}" \
    -F "policy=${POLICY_ID}" \
    -F "claim_type=accident" \
    -F "description=My car was involved in a minor fender bender." \
    -F "incident_date=2026-02-13" \
    -F "incident_time=10:30:00" \
    -F "incident_location=Main Street, Lagos" \
    -F "estimated_loss=50000" \
    -F "claimed_amount=45000" \
    -F "audio_file=@dummy.wav")
CLAIM_ID=$(echo "$response" | jq -r '.id')
if [ -z "$CLAIM_ID" ] || [ "$CLAIM_ID" = "null" ]; then
    echo "ERROR: Claim creation failed."
    pretty_print "$response"
    exit 1
fi
echo "Claim ID: ${CLAIM_ID}"
pretty_print "$response"
echo ""

# --- 8. Process Voice Claim ---
echo "--- 8. Submit Voice Claim ---"
response=$(curl -s -X POST "${HOST}/api/claims/${CLAIM_ID}/submit_voice_claim/" \
    -H "Authorization: Bearer ${CUSTOMER_TOKEN}")
pretty_print "$response"
echo ""

# --- 9. Customer Views Policies ---
echo "--- 9. Customer Views Policies ---"
response=$(curl -s -X GET "${HOST}/api/policies/" -H "Authorization: Bearer ${CUSTOMER_TOKEN}")
pretty_print "$response"
echo ""

# --- 10. Admin Login ---
echo "--- 10. Admin Login ---"
response=$(curl -s -X POST "${HOST}/api/token/" \
    -H "Content-Type: application/json" \
    -d "{\"phone_number\": \"${ADMIN_PHONE}\", \"password\": \"${ADMIN_PASSWORD}\"}")
ADMIN_TOKEN=$(echo "$response" | jq -r '.access')
echo "Admin Token: ${ADMIN_TOKEN}"
pretty_print "$response"
echo ""

# --- 11. Admin Dashboard ---
echo "--- 11. Admin Views Dashboard ---"
response=$(curl -s -X GET "${HOST}/api/admin/dashboard/" -H "Authorization: Bearer ${ADMIN_TOKEN}")
pretty_print "$response"
echo ""

# --- 12. Admin Reviews Claim ---
echo "--- 12. Admin Reviews Claim ---"
if [ -n "$CLAIM_ID" ] && [ "$CLAIM_ID" != "null" ]; then
    response=$(curl -s -X POST "${HOST}/api/claims/${CLAIM_ID}/review/" \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{\"action\": \"approve\", \"notes\": \"Claim appears legitimate after review.\", \"approved_amount\": 45000.00}")
    pretty_print "$response"
else
    echo "No valid claim to review."
fi
echo ""

# --- 13. USSD Request ---
echo "--- 13. USSD Request ---"
response=$(curl -s -X POST "${HOST}/api/ussd/" \
    -H "Content-Type: application/json" \
    -d "{\"session_id\": \"test_session_123\", \"phone_number\": \"+2348000000000\", \"service_code\": \"*384*7676#\", \"text\": \"0\"}")
echo "$response"
echo ""

# --- 14. Send Voice Notification ---
echo "--- 14. Send Voice Notification ---"
response=$(curl -s -X POST "${HOST}/api/notifications/voice/" \
    -H "Authorization: Bearer ${CUSTOMER_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"type\": \"claim_update\", \"message\": \"Your claim has been approved and payment is being processed.\", \"claim_id\": ${CLAIM_ID}}")
echo "$response"
echo ""

echo "--- Test script completed ---"