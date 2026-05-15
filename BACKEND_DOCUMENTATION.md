# JobPortal Backend Documentation (Django + DRF + Channels)

This document describes the backend architecture, data model, workflows, and API surface for the JobPortal application.

## 1. High-level architecture

The backend is a Django project (`jobProtalBackend`) with two main apps:

1. `accounts`
   - Custom user model (`accounts.models.User`)
   - Authentication flows (OTP-based login + JWT refresh)
   - Profile read/update endpoints
   - Password reset flow
2. `jobs`
   - Job posting, job listing, job application
   - HR dashboards (HR-only endpoints + application status updates)
   - Websocket notifications for job/application events

Key technologies:
- Django 5.x
- Django REST Framework (DRF)
- Simple JWT (JWT authentication + refresh)
- Channels (websockets)
- SQLite for local dev (`jobProtalBackend/settings.py` uses sqlite3 by default)
- CORS headers (`corsheaders`)

## 2. Repository layout (backend)

Important paths:
- `project/Backend/jobProtalBackend/jobProtalBackend/`
  - `settings.py` (installed apps, DB, CORS, JWT config)
  - `urls.py` (mounts `accounts` and `jobs`)
  - `asgi.py` (HTTP + websocket routing)
  - `jwt_auth_middleware.py` (JWT auth for websocket)
  - `routing.py` (channels routing, websocket URL patterns)
- `project/Backend/jobProtalBackend/accounts/`
  - `models.py` (User/OTP/PasswordResetToken)
  - `serializers.py` (`UserProfileSerializer`, `UserProfileUpdateSerializer`, etc.)
  - `views.py` (`ProfileView`, register/login/refresh/password-reset)
  - `urls.py` (account endpoints)
- `project/Backend/jobProtalBackend/jobs/`
  - `models.py` (Job, JobSkill, JobApplication, etc.)
  - `serializers.py` (`JobApplicationSerializer`, `JobListSerializer`, etc.)
  - `views.py` (job + application endpoints + HR endpoints)
  - `consumers.py` (websocket consumer)
  - `urls.py` (job endpoints)

## 3. Configuration and environment

### 3.1 Base URL assumptions
- Frontend expects the backend at `http://127.0.0.1:8000` by default (see frontend `src/connector/api.js`).

### 3.2 Environment variables
Example provided in `project/Backend/jobProtalBackend/.env.example`:
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- Email settings:
  - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, etc.
- `FRONTEND_URL` (used to build password reset links)

> Note: local DB is SQLite in `settings.py` unless you override it.

### 3.3 JWT settings
In `jobProtalBackend/settings.py`:
- `SIMPLE_JWT.ACCESS_TOKEN_LIFETIME`: 15 minutes
- `SIMPLE_JWT.REFRESH_TOKEN_LIFETIME`: 10 days
- JWT identifies users via `userId` (`USER_ID_FIELD` and `USER_ID_CLAIM`).

## 4. Data model

### 4.1 `accounts.User`
Core fields:
- `userId` (primary key, BigAutoField)
- `uid` (generated short unique string)
- `email` (unique)
- `role`: `"HR"` or `"SEEKER"`
- Profile fields:
  - `fullname`
  - `company` (HR uses it; seekers may be null)
  - `profile_picture` (ImageField)
  - `bio`, `phone`, `location`
  - `experience` (JSON list of objects)
  - `skills` (JSON list of strings)
  - `job_preferences` (JSON object; includes job types and locations)
- `resume` (FileField; used for applications)

Associated OTP/Reset:
- `OTP`: OTP code, expiry, attempts
- `PasswordResetToken`: reset token, expiry, used flag

### 4.2 `jobs` models
Jobs:
- `Job`
  - `title`, `company`, `location`, `experience` (string label)
  - `type` (job type choices)
  - `salary` (string)
  - `about_company`, `apply_source`, `url`
  - `posted_by` (FK to accounts.User)
  - `posted_at`, `job_code`
- `JobSkill`: FK to Job, stores single `skill` string (skills list is derived)
- `JobDescription` and `JobResponsibility`: store ordered text points

Applications:
- `JobApplication`
  - `job` (FK)
  - `applicant` (FK to accounts.User)
  - `resume` (FileField)
  - `applied_at`
  - `status`: pending/reviewed/accepted/rejected

## 5. Backend workflows

### 5.1 OTP login + JWT authentication
1. User calls `POST /user/login` with `email` and `password` (OTP is optional on the first attempt).
2. Backend checks password via `LoginSerializer`.
3. If OTP is not provided:
   - OTP is generated/stored via `OTPService`
   - Email is sent
   - Response: OTP required (`otp_required: true`)
4. User calls `POST /user/login` again including `otp`:
   - OTP is verified
   - OTP record is deleted
   - Backend returns:
     - `accessToken`
     - `refreshToken`
     - `role`
     - `user` (serialized via `UserProfileSerializer`)

JWT refresh:
- `POST /user/refresh/` with `refresh_token` returns a new `accessToken`.

### 5.2 Profile update (SEEKER + HR)
Endpoint: `PATCH /user/profile/<id>/`
- Protected by `JWTAuthentication` + `IsAuthenticated`.
- Accepts `multipart/form-data`.

Payload fields:
- `fullname`, `company`, `phone`, `bio`, `location`
- `profile_picture` (optional file)
- `experience` (JSON string)
- `skills` (JSON string)
- `job_preferences` (JSON string)

Backend behavior:
- `UserProfileUpdateSerializer` parses JSON strings for:
  - `experience`, `skills`, `job_preferences`
- Saves updated user model and returns:
  - `user` (full updated profile via `UserProfileSerializer`)
  - `stats` (computed from job applications / posted jobs depending on role)

### 5.3 Job posting (HR-only)
Endpoint: `POST /job/post/`
- Protected by HR permission (`IsHR`).
- Uses `JobSerializer` to create a job record and bulk-create:
  - `JobSkill`
  - `JobDescription`
  - `JobResponsibility`

### 5.4 Applying to a job (SEEKER)
Endpoint: `POST /job/<job_id>/apply/`
- Protected by `IsAuthenticated`.
- Payload includes at least:
  - `resume` (FileField, multipart upload)
  - (job-related fields are not written here; application links to job via URL param)

Backend behavior:
- Creates `JobApplication` for `(job, applicant)`
- Sends notifications:
  - WS notification to HR
  - Email to seeker
  - Email to HR

### 5.5 HR application status updates
Endpoint: `PATCH /job/application/<application_id>/status/`
- Protected by HR permission (`IsHR`).
- Backend validates that HR owns the job (`application.job.posted_by == request.user`).
- Valid statuses: `pending`, `reviewed`, `accepted`, `rejected`.

Backend behavior:
- Updates application status
- Sends:
  - WS notifications to applicant and HR
  - Email to applicant

## 6. Websocket notifications

Websocket endpoint:
- `ws/notifications/?token=<accessToken>`

Backend:
- `jobs.consumers.NotificationConsumer`
  - Accepts connection only when `scope['user']` is authenticated
  - Users are grouped into `user_<userId>` groups
  - Server sends:
    - `event`
    - `payload`

Frontend client:
- `src/connector/socket.js` connects using the access token from IndexedDB.

## 7. API reference (paths)

Base mounts:
- `jobProtalBackend/urls.py`
  - `/user/` → `accounts.urls`
  - `/job/` → `jobs.urls`

### 7.1 Accounts (`/user/`)
- `GET /user/health`
  - returns `{ status: "Working" }`
- `POST /user/register`
  - registers a user (HR requires company name)
- `POST /user/login`
  - OTP flow + returns tokens + user profile
- `POST /user/refresh/`
  - refresh access token
- `POST /user/password-reset/request`
  - sends reset email (frontend URL used to build reset link)
- `GET /user/password-reset/validate/<token>`
  - validates reset token
- `POST /user/password-reset/confirm`
  - confirms reset and sets new password
- `PATCH /user/profile/<id>/`
  - updates profile (multipart/form-data)
- `GET /user/profile/` and `GET /user/profile/<user_id>/`
  - reads profile + computed stats

### 7.2 Jobs (`/job/`)
- `POST /job/post/` (HR-only)
  - creates job + skills + descriptions
- `GET /job/all/`
  - returns list of jobs + job details (skills/descriptions)
- `GET /job/<job_id>/`
  - returns job by id (with details)
- `POST /job/<job_id>/apply/`
  - creates job application (multipart includes resume)
- `GET /job/hr/jobs/` (HR-only)
  - returns HR jobs with applications
  - **Includes candidate profile info** in `applications[].applicant`
- `GET /job/hr/stats/` (HR-only)
  - returns job/application stats for charts
- `GET /job/seeker/dashboard/` (SEEKER)
  - returns seeker dashboard application list + stats rows
- `PATCH /job/application/<application_id>/status/` (HR-only)
  - updates application status

## 8. HR candidate profile fields

For HR visibility, `jobs.serializers.JobApplicationSerializer` includes:
- `applications[].applicant.profile_picture`
- `applications[].applicant.experience`
- `applications[].applicant.skills`
- `applications[].applicant.job_preferences`
- plus basic profile fields (fullname/email/location/bio/etc.)

This enables the frontend HR dashboard to render candidate profile details directly in the applications list.

## 9. Notes / known considerations
- Websocket JWT middleware uses query parameter `token` and reads `userId` claim from SimpleJWT configuration.
- For profile_picture URLs returned by DRF serializers, responses depend on request context to build absolute URLs.

