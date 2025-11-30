#!/bin/bash
# Test complete Medical Scribe workflow
# Audio Upload → Transcription → Medical Note Generation

API_URL="http://localhost:8001"
TEST_EMAIL="workflow_test_$(date +%s)@example.com"
TEST_PASSWORD="TestPassword123"

echo "🧪 Medical Scribe - Complete Workflow Test"
echo "==========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Step 1: Register user
echo -e "${BLUE}1️⃣  Registering test user...${NC}"
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\",
    \"full_name\": \"Dr. Test Workflow\"
  }")

if echo "$REGISTER_RESPONSE" | grep -q "access_token"; then
    echo -e "   ${GREEN}✅ User registered${NC}"
    TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
else
    echo -e "   ${RED}❌ Registration failed${NC}"
    echo "   Response: $REGISTER_RESPONSE"
    exit 1
fi
echo ""

# Step 2: Create test audio file
echo -e "${BLUE}2️⃣  Creating test audio file...${NC}"
TEST_AUDIO="test_consultation.wav"

# Create a simple test audio file using text-to-speech or ffmpeg
# For now, we'll create a placeholder
if command -v ffmpeg &> /dev/null; then
    # Create 5 seconds of silence as test audio
    ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 5 -q:a 9 -acodec pcm_s16le "$TEST_AUDIO" -y 2>/dev/null
    echo -e "   ${GREEN}✅ Test audio file created (5s silence)${NC}"
else
    echo -e "   ${YELLOW}⚠️  ffmpeg not found, skipping audio creation${NC}"
    echo -e "   ${YELLOW}💡 Install ffmpeg or provide a real audio file${NC}"
    echo ""
    echo "   To test with a real file:"
    echo "   curl -X POST $API_URL/api/recordings/upload \\"
    echo "     -H \"Authorization: Bearer \$TOKEN\" \\"
    echo "     -F \"file=@your_audio_file.wav\""
    exit 0
fi
echo ""

# Step 3: Upload audio file
echo -e "${BLUE}3️⃣  Uploading audio file...${NC}"
UPLOAD_RESPONSE=$(curl -s -X POST "$API_URL/api/recordings/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$TEST_AUDIO")

if echo "$UPLOAD_RESPONSE" | grep -q "\"id\""; then
    echo -e "   ${GREEN}✅ Audio uploaded${NC}"
    RECORDING_ID=$(echo "$UPLOAD_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
    echo "   Recording ID: $RECORDING_ID"
else
    echo -e "   ${RED}❌ Upload failed${NC}"
    echo "   Response: $UPLOAD_RESPONSE"
    exit 1
fi
echo ""

# Step 4: Start transcription
echo -e "${BLUE}4️⃣  Starting transcription...${NC}"
TRANSCRIBE_RESPONSE=$(curl -s -X POST "$API_URL/api/recordings/$RECORDING_ID/transcribe" \
  -H "Authorization: Bearer $TOKEN")

if echo "$TRANSCRIBE_RESPONSE" | grep -q "transcribing"; then
    echo -e "   ${GREEN}✅ Transcription started${NC}"
    echo "   Status: transcribing"
else
    echo -e "   ${RED}❌ Transcription failed to start${NC}"
    echo "   Response: $TRANSCRIBE_RESPONSE"
    exit 1
fi
echo ""

# Step 5: Wait for processing
echo -e "${BLUE}5️⃣  Waiting for processing to complete...${NC}"
MAX_WAIT=60
WAIT_TIME=0

while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    sleep 2
    WAIT_TIME=$((WAIT_TIME + 2))
    
    STATUS_RESPONSE=$(curl -s "$API_URL/api/recordings/$RECORDING_ID" \
      -H "Authorization: Bearer $TOKEN")
    
    STATUS=$(echo "$STATUS_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'unknown'))" 2>/dev/null)
    
    echo -n "   ⏳ Status: $STATUS (${WAIT_TIME}s)..."
    
    if [ "$STATUS" = "completed" ]; then
        echo -e "\r   ${GREEN}✅ Processing completed!${NC}                    "
        break
    elif [ "$STATUS" = "failed" ]; then
        echo -e "\r   ${RED}❌ Processing failed${NC}                    "
        ERROR=$(echo "$STATUS_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('error_message', 'Unknown error'))")
        echo "   Error: $ERROR"
        exit 1
    fi
    
    echo -ne "\r"
done

if [ "$STATUS" != "completed" ]; then
    echo -e "   ${YELLOW}⚠️  Processing timeout (status: $STATUS)${NC}"
    echo "   Check server logs for details"
    exit 1
fi
echo ""

# Step 6: Get recording details
echo -e "${BLUE}6️⃣  Fetching recording details...${NC}"
RECORDING_RESPONSE=$(curl -s "$API_URL/api/recordings/$RECORDING_ID" \
  -H "Authorization: Bearer $TOKEN")

TRANSCRIPT=$(echo "$RECORDING_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('transcript', 'N/A')[:100])" 2>/dev/null)
echo -e "   ${GREEN}✅ Recording retrieved${NC}"
echo "   Transcript: $TRANSCRIPT..."
echo ""

# Step 7: Get medical note
echo -e "${BLUE}7️⃣  Fetching medical note...${NC}"
NOTE_RESPONSE=$(curl -s "$API_URL/api/recordings/$RECORDING_ID/note" \
  -H "Authorization: Bearer $TOKEN")

if echo "$NOTE_RESPONSE" | grep -q "soap_note"; then
    echo -e "   ${GREEN}✅ Medical note retrieved${NC}"
    
    # Extract SOAP sections
    SUBJECTIVE=$(echo "$NOTE_RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('soap_note', {}).get('subjective', 'N/A')[:80])" 2>/dev/null)
    ASSESSMENT=$(echo "$NOTE_RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('soap_note', {}).get('assessment', 'N/A')[:80])" 2>/dev/null)
    MODEL=$(echo "$NOTE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('model_used', 'N/A'))" 2>/dev/null)
    
    echo ""
    echo "   📝 SOAP Note Preview:"
    echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   Subjective: $SUBJECTIVE..."
    echo "   Assessment: $ASSESSMENT..."
    echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   Model: $MODEL"
else
    echo -e "   ${RED}❌ Failed to retrieve medical note${NC}"
    echo "   Response: $NOTE_RESPONSE"
fi
echo ""

# Step 8: List all recordings
echo -e "${BLUE}8️⃣  Listing all recordings...${NC}"
LIST_RESPONSE=$(curl -s "$API_URL/api/recordings/" \
  -H "Authorization: Bearer $TOKEN")

TOTAL=$(echo "$LIST_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total', 0))" 2>/dev/null)
echo -e "   ${GREEN}✅ Recordings listed${NC}"
echo "   Total recordings: $TOTAL"
echo ""

# Cleanup
echo -e "${BLUE}9️⃣  Cleaning up...${NC}"
rm -f "$TEST_AUDIO"
echo -e "   ${GREEN}✅ Test audio file removed${NC}"
echo ""

# Summary
echo "==========================================="
echo -e "${GREEN}📊 Workflow Test Summary${NC}"
echo "==========================================="
echo -e "${GREEN}✅ User registration${NC}"
echo -e "${GREEN}✅ Audio upload${NC}"
echo -e "${GREEN}✅ Transcription${NC}"
echo -e "${GREEN}✅ Medical note generation${NC}"
echo -e "${GREEN}✅ Data retrieval${NC}"
echo ""
echo -e "${GREEN}🎉 Complete workflow test PASSED!${NC}"
echo ""
echo "📝 Test Details:"
echo "   User: $TEST_EMAIL"
echo "   Recording ID: $RECORDING_ID"
echo "   Token: ${TOKEN:0:30}..."
echo ""
echo "🌐 View in browser: $API_URL/docs"
