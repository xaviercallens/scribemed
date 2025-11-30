# Windsurf AI-Assisted Development: Advanced Tips & Patterns

## 🎯 Maximizing Windsurf Efficiency for Medical Scribe Project

---

## 1. Prompt Engineering Patterns

### ⭐ The "Complete Context" Pattern

**Instead of:**
```
Create an upload endpoint
```

**Do this:**
```
Create FastAPI endpoint POST /api/recordings/upload that:
- Accepts multipart file upload (UploadFile)
- Validates: max 25MB, formats WAV/MP3/M4A
- Saves to ./uploads/ with UUID filename
- Creates Recording DB entry (status='uploaded')
- Returns: {recording_id, filename, status}
- Requires authentication via get_current_user
- Handles errors: file too large, invalid format
- Place in: backend/app/routers/recordings.py
```

**Why:** Specific requirements prevent back-and-forth and reduce revisions.

---

### ⭐ The "Layered Implementation" Pattern

Break complex features into layers:

**Layer 1: Core Logic**
```
Create a function transcribe_audio(file_path: str) -> dict that:
1. Opens audio file
2. Calls OpenAI Whisper API
3. Returns {"text": str, "duration": float, "language": str}
4. Handles errors with proper exceptions
Place in: backend/app/services/transcription.py
```

**Layer 2: API Integration**
```
Create endpoint POST /api/recordings/{id}/transcribe that:
1. Gets Recording from DB
2. Calls transcribe_audio(recording.file_path)
3. Updates Recording.transcript and status
4. Returns transcript data
Uses existing transcribe_audio function
```

**Layer 3: Error Handling**
```
Add to /api/recordings/{id}/transcribe:
1. Try-except for API failures
2. Retry logic (3 attempts, exponential backoff)
3. Log errors to logger
4. Return proper HTTP status codes
5. Update Recording.status on failure
```

**Why:** Each layer can be tested independently. Easier to debug.

---

### ⭐ The "Reference Existing" Pattern

**When adding similar functionality:**
```
Create endpoint POST /api/notes/generate similar to /api/recordings/{id}/transcribe but:
- Takes recording_id
- Calls generate_medical_note(transcript) service function
- Creates MedicalNote DB entry
- Returns structured SOAP note
Follow same error handling pattern as transcribe endpoint
```

**Why:** Maintains consistency across codebase. Reuses proven patterns.

---

### ⭐ The "Specify Stack" Pattern

**Always mention your tech stack:**
```
Create React component AudioUploader using:
- TypeScript
- react-hook-form for validation
- axios for upload
- TailwindCSS for styling
- @heroicons/react for icons
Show upload progress with progress bar
```

**Why:** AI chooses appropriate libraries and patterns for your stack.

---

## 2. Iterative Refinement Workflow

### Step 1: Generate Baseline
```
Create a basic login form with email and password fields
```

### Step 2: Add Validation
```
Add to login form:
- Email format validation
- Password min length 8 chars
- Show error messages below fields
Use react-hook-form
```

### Step 3: Style It
```
Style login form with TailwindCSS:
- Modern gradient background (indigo to blue)
- Centered card with shadow
- Rounded inputs with focus states
- Primary button with hover effect
```

### Step 4: Add Features
```
Add to login form:
- Loading state during submission
- "Remember me" checkbox
- "Forgot password" link
- Toggle password visibility icon
```

**Why:** Easier to review and test incremental changes than one massive component.

---

## 3. Common Pitfalls & Solutions

### ❌ Pitfall: Vague Requests
```
Make the API better
```
**Result:** AI doesn't know what to improve

### ✅ Solution: Specific Improvements
```
Improve /api/recordings/upload endpoint:
1. Add rate limiting (10 uploads per hour per user)
2. Add file type detection (not just extension)
3. Add request logging
4. Return upload speed metrics
```

---

### ❌ Pitfall: No Context
```
Add error handling
```
**Result:** Generic error handling that may not fit your needs

### ✅ Solution: Domain-Specific Context
```
Add error handling to transcription service:
- OpenAI API rate limit → return 429 with retry-after
- Invalid audio format → return 400 with format requirements
- File not found → return 404
- API key invalid → log error, return 500
Log all errors with recording_id for debugging
```

---

### ❌ Pitfall: Everything at Once
```
Create the entire frontend
```
**Result:** Overwhelming output, hard to review

### ✅ Solution: Component-by-Component
```
Session 1: Create basic App.tsx with routing (/, /login, /dashboard)
Session 2: Create Login page component
Session 3: Create Dashboard layout with navigation
Session 4: Create RecordingList component
Session 5: Integrate all components
```

---

## 4. Testing Strategy with Windsurf

### Unit Test Generation

```
Generate pytest unit tests for backend/app/services/transcription.py:
1. Test transcribe_audio with valid audio file
2. Test with invalid file path
3. Test with unsupported format
4. Mock OpenAI API responses
5. Test error handling
Use pytest-mock for mocking
```

### Integration Test Generation

```
Generate FastAPI integration test for /api/recordings/upload:
1. Test successful upload
2. Test with invalid file format
3. Test file size limit
4. Test without authentication
5. Test database record creation
Use TestClient from fastapi.testclient
```

---

## 5. Documentation Generation

### API Documentation
```
Add comprehensive docstring to transcribe_audio function:
- Description of what it does
- Args with types
- Returns with structure
- Raises with exception types
- Example usage
Use Google-style docstrings
```

### Component Documentation
```
Add JSDoc comments to AudioUploader component:
- Component description
- Props with types and descriptions
- Example usage
- Any important notes
```

---

## 6. Debugging with Windsurf

### When Something Breaks

**Step 1: Isolate**
```
The /api/recordings/upload endpoint returns 500 error.
Show me the current implementation of:
1. The endpoint handler
2. The file saving logic
3. The database insertion code
```

**Step 2: Analyze**
```
The error is "IntegrityError: NOT NULL constraint failed".
Check Recording model for required fields and show which field might be missing in the upload handler.
```

**Step 3: Fix**
```
Fix the upload handler to provide all required fields:
- user_id (from current_user)
- audio_file_path
- status (default 'uploaded')
- created_at (use datetime.utcnow)
```

---

## 7. Performance Optimization Requests

```
Optimize /api/recordings endpoint:
1. Add pagination (page, per_page params)
2. Add select loading (only needed fields)
3. Add index on user_id and created_at
4. Add caching for list response (5 min TTL)
5. Eager load medical_note relationship
Show before/after query analysis
```

---

## 8. Security Enhancement Requests

```
Enhance security for audio file upload:
1. Validate file content (not just extension)
2. Scan for malware using python-magic
3. Generate random filenames (UUID)
4. Set proper file permissions (0644)
5. Add rate limiting per user
6. Log all upload attempts
7. Validate file signature matches extension
```

---

## 9. Medical Domain-Specific Patterns

### SOAP Note Prompt Engineering

```
Create GPT-4 prompt for medical note generation:
Requirements:
1. Extract from conversation:
   - Chief complaint
   - History of present illness
   - Review of systems
   - Past medical history
   - Medications
   - Allergies
   - Physical exam findings
   - Assessment/diagnosis
   - Treatment plan
2. Format as structured JSON
3. Use proper medical terminology
4. Flag missing information as "Not documented"
5. Include ICD-10 codes if diagnosis mentioned
6. List contraindications if any
Return prompt template with example
```

### Medical Validation Rules

```
Create validation function for generated medical notes:
1. Check all SOAP sections present
2. Verify medications match discussion
3. Flag if prescription contradicts allergy
4. Ensure vital signs if mentioned
5. Check for required fields per regulation
6. Validate ICD-10 code format
Return validation report with pass/fail/warnings
```

---

## 10. Scaling Considerations Prompts

### Async Task Queue Setup

```
Refactor transcription to use Celery:
1. Create Celery app configuration
2. Convert transcribe_audio to Celery task
3. Update endpoint to return task_id immediately
4. Create status endpoint GET /api/recordings/{id}/status
5. Update frontend to poll for completion
Show Redis setup for task queue
```

### Caching Strategy

```
Implement Redis caching for:
1. User sessions (30 min TTL)
2. Recording list per user (5 min TTL)
3. Generated notes (until recording updated)
Show cache key patterns and invalidation logic
```

---

## 11. Frontend State Management Patterns

### Context-Based State

```
Create recording context (RecordingContext) that:
1. Manages list of recordings
2. Handles upload state
3. Tracks processing status
4. Provides refresh function
5. Auto-polls for status updates
Export useRecordings hook
```

### Form State Management

```
Create medical note editor form using react-hook-form:
1. Editable SOAP sections
2. Validation rules per section
3. Auto-save draft every 30 seconds
4. Track changes since last save
5. Confirm before leaving with unsaved changes
```

---

## 12. Windsurf Workflows for Common Tasks

### Adding a New Feature End-to-End

**Step 1: Backend Model**
```
Add to Recording model:
- summary field (Text, nullable)
- confidence_score field (Float, nullable)
Update schema accordingly
```

**Step 2: Backend Service**
```
Create service function generate_summary(transcript: str) -> dict:
- Uses GPT-4 to create 2-sentence summary
- Returns summary and confidence score
Place in backend/app/services/summary.py
```

**Step 3: Backend Endpoint**
```
Add POST /api/recordings/{id}/summarize that:
- Calls generate_summary
- Updates Recording.summary
- Returns summary data
```

**Step 4: Frontend API Client**
```
Add to src/services/api.ts:
- summarizeRecording(id: number) function
- Returns promise with summary
- Handles errors
```

**Step 5: Frontend UI**
```
Add to RecordingDetail component:
- "Generate Summary" button
- Display summary with confidence score
- Loading state during generation
- Error handling with retry
```

---

## 13. Code Review Prompts

```
Review the transcription service for:
1. Error handling completeness
2. Resource cleanup (file handles)
3. Security issues (path traversal)
4. Performance bottlenecks
5. Missing type hints
6. Documentation quality
Provide specific improvement suggestions
```

---

## 14. Migration & Refactoring

```
Refactor upload endpoint to use:
1. Separate validation function
2. Separate file storage service
3. Separate database service
4. Proper dependency injection
5. Type hints everywhere
Show before/after comparison
```

---

## 15. Production Readiness Checklist

```
Audit the application for production readiness:
1. All endpoints have rate limiting
2. All passwords are hashed
3. All secrets in environment variables
4. All errors logged properly
5. All database queries optimized
6. All API calls have timeouts
7. All file uploads validated
8. All responses include proper CORS headers
Provide detailed report with priorities
```

---

## 🎯 Quick Reference: Prompt Templates

### Backend Endpoint
```
Create [METHOD] /api/[path] endpoint:
- Purpose: [what it does]
- Input: [request body/params]
- Output: [response structure]
- Auth: [required/optional/none]
- Validation: [rules]
- Errors: [specific error cases]
- Place in: [file path]
```

### Frontend Component
```
Create [ComponentName] component:
- Purpose: [what it displays/does]
- Props: [list with types]
- State: [what state it manages]
- API calls: [which endpoints]
- Styling: [TailwindCSS specifics]
- Interactions: [user actions]
- Place in: [file path]
```

### Service Function
```
Create [function_name] service:
- Purpose: [business logic]
- Input: [parameters with types]
- Output: [return type]
- External APIs: [which ones]
- Error handling: [specific cases]
- Side effects: [DB, files, etc.]
- Place in: [file path]
```

---

## 💡 Pro Tips

1. **Always specify file paths** - Prevents AI from creating files in wrong locations
2. **Request type hints** - Makes code more maintainable
3. **Ask for error handling explicitly** - AI won't always add it by default
4. **Request tests alongside code** - Easier to verify correctness
5. **Specify styling frameworks** - Prevents mixing CSS approaches
6. **Reference existing code** - Maintains consistency
7. **Break down complex features** - Easier to review and test
8. **Ask for documentation** - Future-you will thank present-you
9. **Request before/after examples** - Helps understand changes
10. **Iterate incrementally** - Build confidence in each step

---

## 🚀 Advanced: Chaining Prompts

**Scenario:** Building a complex feature

**Prompt 1:** Architecture
```
Design architecture for medical note editing feature:
- Database schema changes
- API endpoints needed
- Frontend components
- State management approach
Provide high-level overview
```

**Prompt 2:** Backend Implementation
```
Based on the architecture, implement backend:
[paste architecture from above]
Start with database models
```

**Prompt 3:** Frontend Implementation
```
Based on the architecture, implement frontend:
[paste architecture]
Use the existing API client pattern
```

---

## 📝 Summary

**Effective Windsurf usage = Clear context + Specific requirements + Iterative refinement**

**Key Principles:**
- Be specific about what you want
- Provide technical context
- Break down complex tasks
- Review and iterate
- Document as you go
- Test incrementally

**Remember:** Windsurf is a tool to accelerate development, not replace thinking. You still need to:
- Understand the business requirements
- Design the architecture
- Review generated code critically
- Test thoroughly
- Make final decisions

---

*Use this guide to build faster, better, and more maintainable code with AI assistance.*
