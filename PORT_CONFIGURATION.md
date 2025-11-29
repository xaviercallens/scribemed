# Port Configuration Guide

## 🔌 Default Ports

| Service | Port | URL |
|---------|------|-----|
| **Backend API** | 8001 | http://localhost:8001 |
| **API Docs** | 8001 | http://localhost:8001/docs |
| **Frontend** | 3000 | http://localhost:3000 |

## 🔄 Why Port 8001?

Port **8000** is commonly used by many services and often conflicts with:
- Other FastAPI/Django applications
- Development tools
- System services

We use **8001** as the default to avoid these conflicts.

## 🛠️ Changing the Port

### Method 1: Environment Variable (Recommended)

Edit your `.env` file:
```bash
API_PORT=8002  # or any available port
```

Then start the server:
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8002
```

### Method 2: Command Line

Start with a custom port directly:
```bash
cd backend
python -m uvicorn app.main:app --reload --port YOUR_PORT
```

### Method 3: Use the Start Script

The `start_server.sh` script automatically checks if port 8001 is available:
```bash
./start_server.sh
```

## 🔍 Check Port Availability

### Check if a port is in use:
```bash
lsof -i :8001
```

### Find what's using a port:
```bash
lsof -ti:8001
```

### Kill process using a port:
```bash
lsof -ti:8001 | xargs kill -9
```

### Check multiple ports:
```bash
lsof -i :8000 -i :8001 -i :8002
```

## 🚨 Troubleshooting

### "Address already in use" Error

**Problem**: Port is already occupied

**Solution 1** - Kill the existing process:
```bash
lsof -ti:8001 | xargs kill -9
```

**Solution 2** - Use a different port:
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8002
```

**Solution 3** - Find and stop the conflicting service:
```bash
# Find what's using the port
lsof -i :8001

# Example output:
# COMMAND   PID   USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
# python  12345  user    3u  IPv4  0x1234    0t0  TCP *:8001 (LISTEN)

# Stop it gracefully
kill 12345
```

### Port Changes Not Taking Effect

**Problem**: Server still using old port

**Solution**:
1. Stop all running uvicorn processes:
   ```bash
   pkill -f uvicorn
   ```

2. Clear any cached settings:
   ```bash
   rm -rf backend/__pycache__
   rm -rf backend/app/__pycache__
   ```

3. Restart the server:
   ```bash
   ./start_server.sh
   ```

## 📝 Frontend Configuration

If you change the backend port, update the frontend API client:

**File**: `frontend/src/services/api.ts`
```typescript
const api = axios.create({
  baseURL: 'http://localhost:8001/api',  // Update this
});
```

Or use environment variables in frontend:

**File**: `frontend/.env`
```
REACT_APP_API_URL=http://localhost:8001
```

## 🔐 Production Considerations

In production, you typically:
- Use port **80** (HTTP) or **443** (HTTPS)
- Put the API behind a reverse proxy (Nginx, Traefik)
- Use environment variables for configuration
- Never expose the port directly

Example production setup:
```
Internet → Load Balancer (443) → Nginx (80) → FastAPI (8001)
```

## 📚 Quick Reference

```bash
# Start with default port (8001)
./start_server.sh

# Start with custom port
cd backend && python -m uvicorn app.main:app --reload --port 8002

# Check if port is available
lsof -i :8001

# Kill process on port
lsof -ti:8001 | xargs kill -9

# View all listening ports
lsof -iTCP -sTCP:LISTEN -n -P
```

## ✅ Best Practices

1. **Always check port availability** before starting the server
2. **Use environment variables** for port configuration
3. **Document any port changes** in your team
4. **Use the start script** (`./start_server.sh`) for consistent startup
5. **Keep frontend and backend ports in sync**

---

**Need help?** Check the [QUICKSTART.md](./QUICKSTART.md) or [DAY1_PROGRESS.md](./DAY1_PROGRESS.md) for more information.
