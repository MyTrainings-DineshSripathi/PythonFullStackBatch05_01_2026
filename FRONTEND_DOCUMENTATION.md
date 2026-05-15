# JobPortal Frontend Documentation (React + Vite + Redux Toolkit)

This document describes the frontend architecture, routing, state management, key screens, and how the client communicates with the backend.

## 1. High-level architecture

Frontend is a React (Vite) application located at:
- `project/JobPortal/src`

Major parts:
- `src/UIBlocks/` — page-level UI blocks (Header, MyAccount, dashboards, etc.)
- `src/connector/` — network clients (axios wrapper + websocket)
- `src/data/` — Redux slices + IndexedDB persistence layer
- `src/components/Loaders/` — skeleton/loaders used during async work

The app is routed with `react-router-dom` and uses:
- Redux Toolkit for global state
- IndexedDB for storing access/refresh tokens and persisted user data
- Axios for HTTP requests
- Sonner (`toast`) for notifications

## 2. Project setup

Prerequisites:
- Node.js + npm

Common commands (from `project/JobPortal/`):
- `npm install`
- `npm run dev` (Vite dev server)
- `npm run build`

Backend base URL:
- The frontend axios wrapper assumes the backend at `http://127.0.0.1:8000` (see `src/connector/api.js`).

## 3. Core network + persistence layers

### 3.1 Axios API wrapper
File: `project/JobPortal/src/connector/api.js`

Responsibilities:
- Create a shared axios instance (`api`)
- Attach `Authorization: Bearer <accessToken>` via request interceptor
- Handle token refresh on `401` via `/user/refresh/`
- Update IndexedDB user cache after profile update (`saveUserData`)
- Track global “in-flight” request count to power the DB communication loader in the header

Base URL:
- `export const BASE = 'http://127.0.0.1:8000'`

### 3.2 IndexedDB auth persistence
File: `project/JobPortal/src/data/indexed/IndexedService.js`

Responsibilities:
- Store access/refresh tokens (`tokens` object store)
- Store the latest serialized user object (`tokens[].user`)
- Rehydrate auth state on page load

### 3.3 Auth bootstrap provider
File: `project/JobPortal/src/data/ExtraProviders/AuthProvider.jsx`

On mount:
- Reads refresh token + stored auth data from IndexedDB
- If refresh token is valid, dispatches `setUserData(...)` to Redux
- Until auth is ready, returns `undefined` (prevents rendering)

### 3.4 Websocket client
File: `project/JobPortal/src/connector/socket.js`

Builds the websocket URL:
- `ws://<backend-host>/ws/notifications/?token=<accessToken>`

Connects to:
- backend `NotificationConsumer`

### 3.5 Global loading (“DB communication”) line
Added:
- `src/data/slices/networkSlice.jsx`
- Header reads `state.network.inFlight`
- axios interceptors dispatch `requestStarted()` / `requestFinished()`

Header line:
- `DB communication: Loading...` appears when there are in-flight HTTP requests.

## 4. Global state (Redux)

Redux store:
- `src/data/slices/reduxStore.jsx`

Slices:
- `userSlice.jsx`
  - `state.user` holds logged-in user info and profile fields for header rendering
- `jobSlice.jsx`
  - job list + search + skeleton triggering
- `networkSlice.jsx`
  - in-flight request counter for header loader

## 5. Routing & layout

Entry point:
- `src/main.jsx`

Key layout pieces:
- `AppWrapper` (shows app-level loader)
- `AuthProvider` (rehydrates auth)
- `Header` (global)
- `RoutesComponent` (renders the routed pages)

Routes:
- Route for profile:
  - `src/UIBlocks/Header/RoutesComponent.jsx` includes `/myAccount/:id`

Header link:
- `Header.jsx` navigates to `/myAccount/<userId>`

## 6. Backend-driven screens / workflows

### 6.1 Authentication flow (OTP + JWT)
Backend:
- `POST /user/login`
Frontend:
- Login triggers OTP requirement (backend returns `otp_required: true`)
- On OTP entry, calls `POST /user/login` again with `otp` to receive:
  - `accessToken`, `refreshToken`, `role`, `user`
- Redux + IndexedDB are updated from `setUserData` and token storage.

Token refresh:
- handled automatically by `api.js` interceptors on `401`.

### 6.2 Profile: MyAccount page (view + edit)
Files:
- `src/UIBlocks/MyAccount/MyAccount.jsx`
- `src/UIBlocks/MyAccount/ProfileSections.jsx`

Fetch:
- On mount, `MyAccount` calls `GET_PROFILE_BY_ID` → `GET /user/profile/<id>/`
- Populates local component state used by the edit form and summary cards.

Editing:
- Main profile details (fullname, company, phone, bio, picture):
  - Toggle with “Edit Profile” button.
- SEEKER sub-parts (Experience, Skills, Looking For):
  - Edited inline inside the Profile Summary cards with per-section `Edit/Cancel`.

Immediate update behavior:
- Job preferences editor is fully controlled and avoids stale internal component state:
  - `JobPreferencesSection` derives `jobTypes/locations` directly from props.
- After clicking Save:
  - `PATCH /user/profile/<id>/` returns updated profile data
  - UI sets local state from response
  - Header avatar is updated from updated user data
  - Profile picture URL is cache-busted using a `?t=<timestamp>` query param to force immediate re-render.

### 6.3 Jobs browsing + applying
Key components:
- Browse/Search is driven by the `JobSlice` loading state.

Jobs API:
- `GET /job/all/` (used by the thunk in `src/data/slices/JobAsyncThunk.jsx`)

Applying:
- `POST /job/<job_id>/apply/` (multipart upload; resume file is sent)

### 6.4 HR dashboard (applications + candidate profile)
File:
- `src/UIBlocks/Dashboard/HrDashboard.jsx`

HR endpoints:
- `GET /job/hr/stats/`
- `GET /job/hr/jobs/` (includes job applications with candidate profile info in `applications[].applicant`)

Candidate profile shown:
- HR dashboard renders:
  - profile picture
  - fullname + email
  - location
  - skills snippet
  - looking-for info (job types + locations)
  - first experience item

HR status updates:
- `PATCH /job/application/<application_id>/status/`
- UI updates in-place and refreshes stats/jobs after success.

Realtime:
- HR dashboard listens to websocket events via `createNotificationSocket`.

## 7. Developer notes / important implementation details

1. Profile sub-part editors must be controlled
   - `JobPreferencesSection` uses checkboxes and text input controlled from `preferences` props to keep the summary consistent.

2. Global request loading indicator
   - The loader is driven by axios interceptors in `src/connector/api.js`.
   - Any requests routed through the `api` instance will be counted.

3. Websocket events
   - On new application or status update, dashboards refresh their job lists and stats.

## 8. Where to look in the codebase

Networking:
- `src/connector/api.js`
- `src/connector/socket.js`

Auth:
- `src/data/ExtraProviders/AuthProvider.jsx`
- `src/data/indexed/IndexedService.js`

Profile:
- `src/UIBlocks/MyAccount/MyAccount.jsx`
- `src/UIBlocks/MyAccount/ProfileSections.jsx`

HR:
- `src/UIBlocks/Dashboard/HrDashboard.jsx`

Loaders:
- `src/components/Loaders/*`

