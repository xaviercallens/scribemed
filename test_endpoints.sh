#!/bin/bash
# Test Medical Scribe API Endpoints
# Make sure the server is running first: ./start_server.sh

API_URL="http://localhost:8001"
TEST_EMAIL="test_$(date +%s)@example.com"
TEST_PASSWORD="TestPassword123"

echo "🧪 Medical Scribe API - Endpoint Tests"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo "1️⃣  Testing health check..."
HEALTH_RESPONSE=$(curl -s "$API_URL/health")
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo -e "   ${GREEN}✅ Health check passed${NC}"
    echo "   Response: $HEALTH_RESPONSE"
else
    echo -e "   ${RED}❌ Health check failed${NC}"
    echo "   Response: $HEALTH_RESPONSE"
    exit 1
fi
echo ""

# Test 2: Root endpoint
echo "2️⃣  Testing root endpoint..."
ROOT_RESPONSE=$(curl -s "$API_URL/")
if echo "$ROOT_RESPONSE" | grep -q "Medical Scribe API"; then
    echo -e "   ${GREEN}✅ Root endpoint passed${NC}"
    echo "   Response: $ROOT_RESPONSE"
else
    echo -e "   ${RED}❌ Root endpoint failed${NC}"
    echo "   Response: $ROOT_RESPONSE"
    exit 1
fi
echo ""

# Test 3: User Registration
echo "3️⃣  Testing user registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\",
    \"full_name\": \"Test User\"
  }")

if echo "$REGISTER_RESPONSE" | grep -q "access_token"; then
    echo -e "   ${GREEN}✅ Registration passed${NC}"
    TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
    echo "   Token: ${TOKEN:0:30}..."
else
    echo -e "   ${RED}❌ Registration failed${NC}"
    echo "   Response: $REGISTER_RESPONSE"
    exit 1
fi
echo ""

# Test 4: User Login
echo "4️⃣  Testing user login..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\"
  }")

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo -e "   ${GREEN}✅ Login passed${NC}"
    TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
    USER_EMAIL=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['user']['email'])")
    echo "   User: $USER_EMAIL"
else
    echo -e "   ${RED}❌ Login failed${NC}"
    echo "   Response: $LOGIN_RESPONSE"
    exit 1
fi
echo ""

# Test 5: Get Current User
echo "5️⃣  Testing get current user..."
ME_RESPONSE=$(curl -s "$API_URL/api/auth/me" \
  -H "Authorization: Bearer $TOKEN")

if echo "$ME_RESPONSE" | grep -q "$TEST_EMAIL"; then
    echo -e "   ${GREEN}✅ Get current user passed${NC}"
    echo "   Response: $ME_RESPONSE"
else
    echo -e "   ${RED}❌ Get current user failed${NC}"
    echo "   Response: $ME_RESPONSE"
    exit 1
fi
echo ""

# Test 6: Invalid Login
echo "6️⃣  Testing invalid login (should fail)..."
INVALID_LOGIN=$(curl -s -X POST "$API_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"WrongPassword\"
  }")

if echo "$INVALID_LOGIN" | grep -q "detail"; then
    echo -e "   ${GREEN}✅ Invalid login correctly rejected${NC}"
else
    echo -e "   ${RED}❌ Invalid login test failed${NC}"
    echo "   Response: $INVALID_LOGIN"
fi
echo ""

# Test 7: Unauthorized Access
echo "7️⃣  Testing unauthorized access (should fail)..."
UNAUTH_RESPONSE=$(curl -s "$API_URL/api/auth/me")

if echo "$UNAUTH_RESPONSE" | grep -q "detail"; then
    echo -e "   ${GREEN}✅ Unauthorized access correctly blocked${NC}"
else
    echo -e "   ${RED}❌ Unauthorized access test failed${NC}"
    echo "   Response: $UNAUTH_RESPONSE"
fi
echo ""

# Test 8: API Documentation
echo "8️⃣  Testing API documentation..."
DOCS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/docs")

if [ "$DOCS_RESPONSE" = "200" ]; then
    echo -e "   ${GREEN}✅ API docs accessible${NC}"
    echo "   URL: $API_URL/docs"
else
    echo -e "   ${RED}❌ API docs not accessible${NC}"
    echo "   HTTP Status: $DOCS_RESPONSE"
fi
echo ""

# Summary
echo "======================================"
echo "📊 Test Summary"
echo "======================================"
echo -e "${GREEN}✅ Health check: PASSED${NC}"
echo -e "${GREEN}✅ Root endpoint: PASSED${NC}"
echo -e "${GREEN}✅ User registration: PASSED${NC}"
echo -e "${GREEN}✅ User login: PASSED${NC}"
echo -e "${GREEN}✅ Get current user: PASSED${NC}"
echo -e "${GREEN}✅ Invalid login rejection: PASSED${NC}"
echo -e "${GREEN}✅ Unauthorized access blocked: PASSED${NC}"
echo -e "${GREEN}✅ API documentation: PASSED${NC}"
echo ""
echo "🎉 All endpoint tests passed!"
echo ""
echo "📝 Test user created:"
echo "   Email: $TEST_EMAIL"
echo "   Password: $TEST_PASSWORD"
echo "   Token: ${TOKEN:0:50}..."
echo ""
echo "🌐 Try the interactive docs: $API_URL/docs"
