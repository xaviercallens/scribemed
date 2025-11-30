# 🧪 Medical Scribe API - User Test Guide

## ✅ Server Status

**Server is running!** 🎉

- **API Base URL**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **Alternative Docs**: http://localhost:8001/redoc
- **Health Check**: http://localhost:8001/health

---

## 🚀 Quick Test Scenarios

### 1. Test API Documentation (Interactive)

**Visit**: http://localhost:8001/docs

This opens the **Swagger UI** where you can:
- See all available endpoints
- Test endpoints directly in the browser
- View request/response schemas
- No coding required!

### 2. Test Health Check

**URL**: http://localhost:8001/health

**Expected Response**:
```json
{"status": "healthy"}
```

### 3. Test Root Endpoint

**URL**: http://localhost:8001/

**Expected Response**:
```json
{
  "message": "Welcome to Medical Scribe API",
  "version": "0.1.0",
  "status": "operational"
}
```

---

## 👤 User Registration & Login Flow

### Step 1: Register a New User

**Using Swagger UI** (Recommended):
1. Go to http://localhost:8001/docs
2. Find `POST /api/auth/register`
3. Click "Try it out"
4. Enter:
   ```json
   {
     "email": "doctor@clinic.com",
     "password": "SecurePass123",
     "full_name": "Dr. Smith"
   }
   ```
5. Click "Execute"
6. Copy the `access_token` from the response

**Using curl**:
```bash
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@clinic.com",
    "password": "SecurePass123",
    "full_name": "Dr. Smith"
  }'
```

### Step 2: Login

**Using Swagger UI**:
1. Find `POST /api/auth/login`
2. Click "Try it out"
3. Enter:
   ```json
   {
     "email": "doctor@clinic.com",
     "password": "SecurePass123"
   }
   ```
4. Click "Execute"
5. Copy the `access_token`

**Using curl**:
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@clinic.com",
    "password": "SecurePass123"
  }'
```

### Step 3: Get Your Profile (Protected Route)

**Using Swagger UI**:
1. Click the "Authorize" button at the top
2. Enter: `Bearer YOUR_TOKEN_HERE`
3. Click "Authorize"
4. Find `GET /api/auth/me`
5. Click "Try it out" → "Execute"

**Using curl**:
```bash
curl http://localhost:8001/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🧪 Test Scenarios

### ✅ Scenario 1: Happy Path
1. Register a new user ✅
2. Login with credentials ✅
3. Access protected route with token ✅
4. View user profile ✅

### ❌ Scenario 2: Error Handling
1. Try to register with invalid email → Should fail
2. Try to login with wrong password → Should fail
3. Access protected route without token → Should fail
4. Register with existing email → Should fail

### 🔐 Scenario 3: Security
1. Try accessing `/api/auth/me` without token → Blocked ✅
2. Try with invalid token → Blocked ✅
3. Password should be hashed in database ✅
4. Token should expire after 24 hours ✅

---

## 📊 What to Test

### Authentication Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/auth/register` | POST | Create new user | No |
| `/api/auth/login` | POST | Login and get token | No |
| `/api/auth/me` | GET | Get current user | Yes |

### System Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/` | GET | Welcome message | No |
| `/health` | GET | Health check | No |
| `/docs` | GET | API documentation | No |

---

## 🎯 Expected Behaviors

### ✅ Should Work
- Register with valid email and password (8+ chars)
- Login with correct credentials
- Access `/api/auth/me` with valid token
- View API documentation
- Health check returns "healthy"

### ❌ Should Fail
- Register with invalid email format
- Register with password < 8 characters
- Login with wrong password
- Access protected routes without token
- Register duplicate email

---

## 🐛 Troubleshooting

### Server Not Responding
```bash
# Check if server is running
curl http://localhost:8001/health

# If not, restart
cd backend
python -m uvicorn app.main:app --reload --port 8001
```

### "Unauthorized" Error
- Make sure you're using the token from login/register
- Token format: `Bearer YOUR_TOKEN_HERE`
- Token expires after 24 hours

### Database Issues
```bash
# Check if database exists
ls -lh medical_scribe.db

# Reset database (WARNING: deletes all data)
rm medical_scribe.db
# Restart server to recreate
```

---

## 📝 Sample Test Data

### Valid Users
```json
{
  "email": "doctor1@clinic.com",
  "password": "SecurePass123",
  "full_name": "Dr. John Smith"
}

{
  "email": "nurse@hospital.com",
  "password": "NursePass456",
  "full_name": "Jane Doe RN"
}
```

### Invalid Data (Should Fail)
```json
// Invalid email
{"email": "not-an-email", "password": "password123"}

// Short password
{"email": "test@test.com", "password": "short"}

// Missing fields
{"email": "test@test.com"}
```

---

## 🎨 Interactive Testing with Swagger UI

**Best for non-technical users!**

1. **Open**: http://localhost:8001/docs
2. **Explore**: All endpoints are listed with descriptions
3. **Test**: Click "Try it out" on any endpoint
4. **Authenticate**: Use the "Authorize" button for protected routes
5. **View**: See request/response examples

### Swagger UI Features
- ✅ No coding required
- ✅ Visual interface
- ✅ Automatic validation
- ✅ Example values provided
- ✅ Response codes explained

---

## 📊 Test Checklist

### Basic Functionality
- [ ] Server starts without errors
- [ ] Health endpoint responds
- [ ] API docs load at `/docs`
- [ ] Root endpoint returns welcome message

### User Management
- [ ] Can register new user
- [ ] Receives JWT token on registration
- [ ] Can login with credentials
- [ ] Can access profile with token
- [ ] Cannot access profile without token

### Security
- [ ] Passwords are not visible in responses
- [ ] Invalid credentials are rejected
- [ ] Tokens are required for protected routes
- [ ] Email validation works
- [ ] Password length validation works

### Error Handling
- [ ] Invalid email format rejected
- [ ] Short passwords rejected
- [ ] Duplicate emails rejected
- [ ] Wrong passwords rejected
- [ ] Missing fields rejected

---

## 🎉 Success Criteria

Your test is successful if:
1. ✅ You can register a user
2. ✅ You can login and get a token
3. ✅ You can access your profile with the token
4. ✅ Invalid requests are properly rejected
5. ✅ API documentation is accessible

---

## 📞 Need Help?

### Check Server Logs
The terminal running the server shows all requests and errors.

### Common Issues
1. **Port in use**: Kill process with `lsof -ti:8001 | xargs kill -9`
2. **Module not found**: Run `pip install -r requirements.txt`
3. **Database error**: Delete `medical_scribe.db` and restart

### Test Files
- Run unit tests: `python3 test_api.py`
- Run endpoint tests: `./test_endpoints.sh`

---

**Happy Testing!** 🚀

The server is running and ready for your tests at:
- **API**: http://localhost:8001
- **Docs**: http://localhost:8001/docs
