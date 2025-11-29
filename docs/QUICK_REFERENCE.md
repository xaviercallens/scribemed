# Medical Scribe AI - 2-Day Quick Reference

## ⏰ Time-Boxed Checklist

### DAY 1: Backend (8 hours)

#### Morning Session (4 hours)
- [ ] **H1-2: Setup** (2h)
  - [ ] Project structure created
  - [ ] Dependencies installed
  - [ ] FastAPI running on :8000
  - [ ] React dev server on :3000

- [ ] **H3-4: Database** (2h)
  - [ ] User, Recording, MedicalNote models
  - [ ] Pydantic schemas created
  - [ ] Database initialized

#### Afternoon Session (4 hours)
- [ ] **H5-6: Auth** (2h)
  - [ ] `/api/auth/register` working
  - [ ] `/api/auth/login` returns JWT
  - [ ] Token validation working

- [ ] **H7-8: Upload** (2h)
  - [ ] `/api/recordings/upload` accepts audio
  - [ ] Files saved to ./uploads/
  - [ ] Database records created

#### Evening Session (2 hours)
- [ ] **H9-10: Transcription** (2h)
  - [ ] Whisper API integrated
  - [ ] `/api/recordings/{id}/transcribe` working
  - [ ] Transcripts saved to DB

**Day 1 Goal:** Backend API with auth, upload, and transcription ✅

---

### DAY 2: Frontend + AI (10 hours)

#### Morning Session (4 hours)
- [ ] **H11-12: AI Notes** (2h)
  - [ ] GPT-4 prompt engineered
  - [ ] `/api/notes/generate` working
  - [ ] SOAP notes structured correctly

- [ ] **H13-14: API Complete** (2h)
  - [ ] GET /api/recordings (list)
  - [ ] GET /api/recordings/{id} (detail)
  - [ ] GET /api/notes/{id}
  - [ ] POST /api/recordings/{id}/process

#### Afternoon Session (4 hours)
- [ ] **H15-16: React Setup** (2h)
  - [ ] Routing configured
  - [ ] TailwindCSS working
  - [ ] API client with auth

- [ ] **H17-18: Auth UI** (2h)
  - [ ] Login page beautiful
  - [ ] Registration page
  - [ ] Auth context working

#### Evening Session (4 hours)
- [ ] **H19-20: Upload UI** (2h)
  - [ ] Drag-drop file upload
  - [ ] Upload progress shown
  - [ ] Redirects after upload

- [ ] **H21-22: Dashboard** (2h)
  - [ ] Stats cards displayed
  - [ ] Recording list shown
  - [ ] Navigation working

- [ ] **H23-24: Detail View** (2h)
  - [ ] Transcript displayed
  - [ ] SOAP note formatted
  - [ ] Process button functional

**Day 2 Goal:** Full demo-ready application ✅

---

## 🚨 Critical Path Items

Must work for demo:
1. ✅ User can login
2. ✅ Upload audio file
3. ✅ See transcription
4. ✅ View SOAP note
5. ✅ Professional UI

---

## 🔑 Environment Variables

```bash
# .env
OPENAI_API_KEY=sk-...
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./medical_scribe.db
```

---

## 🧪 Quick Test Commands

```bash
# Backend health
curl http://localhost:8000/

# Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

---

## 💡 Windsurf Power Prompts

### Backend
```
Create FastAPI endpoint [METHOD] /api/[path] that:
1. [specific behavior]
2. [validation rules]
3. [error handling]
4. [returns X format]
Requires authentication. Add to routers/[name].py
```

### Frontend
```
Create React component [ComponentName] that:
1. [displays X]
2. [handles Y interaction]
3. [styled with TailwindCSS]
4. [uses Z state/props]
Mobile responsive. Save to src/components/[file].tsx
```

### Complete Feature
```
Implement end-to-end [feature name]:
- Backend: [endpoint details]
- Frontend: [UI details]
- Integration: [how they connect]
```

---

## 📊 Demo Metrics to Highlight

| Metric | Value |
|--------|-------|
| Processing time | <30 sec |
| Time saved | 95% |
| Accuracy | >90% |
| Cost per note | ~$0.15 |

---

## 🎯 If Behind Schedule

**Cut these first:**
- [ ] Registration (use hard-coded login)
- [ ] Recording list (show only latest)
- [ ] Edit/delete functions
- [ ] Mobile responsiveness polish

**Never cut:**
- [x] Upload audio
- [x] Transcription
- [x] SOAP note generation
- [x] Basic UI

---

## 📱 Demo Checklist

**30 min before demo:**
- [ ] Backend running
- [ ] Frontend running
- [ ] Sample audio ready
- [ ] Test account created
- [ ] API keys valid
- [ ] Internet stable

**During demo:**
- [ ] Show problem (manual documentation)
- [ ] Show solution (upload → note)
- [ ] Show results (formatted SOAP)
- [ ] Show metrics (time/cost savings)
- [ ] Show roadmap (scale-up plan)

---

## 🆘 Common Issues

**"Module not found"**
```bash
pip install -r requirements.txt
npm install
```

**"API key invalid"**
- Check .env file
- Verify key on OpenAI dashboard
- Restart server after changing .env

**"CORS error"**
- Check FastAPI CORS middleware
- Verify origin matches frontend URL

**"Upload fails"**
- Check ./uploads/ directory exists
- Verify file size < 25MB
- Check file format (WAV/MP3)

---

## 💰 Cost Tracking

| Item | Prototype | 100 users | 1K users |
|------|-----------|-----------|----------|
| Dev | $1,250 | - | - |
| Hosting | $0 | $800/mo | $3K/mo |
| AI APIs | $100/mo | $2K/mo | $20K/mo |
| **Total** | **$1,350** | **$3K/mo** | **$23K/mo** |

---

## ✅ Definition of Done

**Prototype Complete When:**
- [ ] User can register/login
- [ ] Audio upload works
- [ ] Transcription generates
- [ ] SOAP note displays
- [ ] UI is professional
- [ ] Demo script ready
- [ ] Docs completed
- [ ] Code committed
- [ ] Costs documented

---

**Print this page and check off items as you build!** 📋
