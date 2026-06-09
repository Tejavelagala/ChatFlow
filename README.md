# ChatFlow

ChatFlow is a full-stack real-time chat application with a Django REST + Channels backend and a Vue 3 + Vite frontend. It supports JWT authentication, chat rooms, live WebSocket messaging, message delivery/seen states, reactions, typing indicators, online presence, media uploads, pinned messages, user profiles, and room moderation tools.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Running the App](#running-the-app)
- [API Reference](#api-reference)
- [WebSocket Reference](#websocket-reference)
- [Testing](#testing)
- [Media and Uploads](#media-and-uploads)
- [Security Notes](#security-notes)
- [Production Notes](#production-notes)
- [Troubleshooting](#troubleshooting)

## Features

- User registration, login, JWT access tokens, and refresh tokens through Djoser and Simple JWT.
- Authenticated chat rooms with room ownership and membership.
- Real-time messaging over Django Channels WebSockets.
- REST endpoints for room creation, joining, message history, uploads, profiles, moderation, and message actions.
- Message reactions, replies, editing, deletion, delivery state, seen state, and pinned messages.
- Image, audio, and document/file sharing with server-side size/type checks.
- Online users per room, typing indicators, and basic presence lookup.
- Room moderation with owner/admin/moderator roles, promotion, ban, mute, leave-room, and delete-room flows.
- Vue 3 frontend with Pinia stores, Vue Router, Axios token refresh, toast notifications, virtualized message lists, dark mode, and responsive UI.
- Local SQLite development database by default, with optional PostgreSQL configuration.

## Tech Stack

### Backend

- Python
- Django 5.2
- Django REST Framework
- Django Channels
- Channels Redis
- Djoser
- Simple JWT
- django-cors-headers
- django-ratelimit
- WhiteNoise
- SQLite by default, PostgreSQL optional

### Frontend

- Vue 3
- Vite
- Pinia
- Vue Router
- Axios
- Vue Toastification
- Vue Virtual Scroller
- Browser Image Compression
- Vitest

### Realtime Infrastructure

- WebSockets are served by Django Channels.
- Redis is used as the Channels backing layer.
- Daphne is included in backend dependencies for ASGI serving.

## Architecture

```text
Browser
  |
  | HTTP REST
  v
Vue 3 Frontend  --->  Django REST API
  |                         |
  | WebSocket               | ORM
  v                         v
Django Channels  --->  SQLite/PostgreSQL
  |
  v
Redis Channel Layer
```

The frontend talks to the backend through:

- REST API base URL: `VITE_API_BASE_URL`
- WebSocket base URL: `VITE_WS_BASE_URL`

The backend exposes:

- Auth endpoints under `/auth/`
- Chat REST endpoints under `/api/chat/`
- WebSocket endpoint under `/ws/chat/<room_id>/<username>/`
- Media files under `/media/`

## Project Structure

```text
ChatFlow/
+-- backend/
|   +-- chats/
|   |   +-- consumers.py              # WebSocket consumer
|   |   +-- middleware.py             # JWT auth for WebSockets
|   |   +-- models.py                 # Rooms, messages, reactions, profiles, presence
|   |   +-- ratelimit.py              # Login/register rate limit middleware
|   |   +-- routing.py                # WebSocket routes
|   |   +-- serializers.py            # DRF serializers
|   |   +-- urls.py                   # Chat API routes
|   |   +-- validators.py             # Upload validation
|   |   +-- views.py                  # Chat REST API views
|   +-- config/
|   |   +-- asgi.py                   # ASGI app with Channels
|   |   +-- settings.py               # Django settings
|   |   +-- urls.py                   # Root URL routes
|   |   +-- wsgi.py
|   +-- users/
|   +-- media/                        # Uploaded development media
|   +-- db.sqlite3                    # Local development database
|   +-- manage.py
|   +-- requirements.txt
|
+-- frontend/
|   +-- public/
|   +-- src/
|   |   +-- components/
|   |   |   +-- chat/                 # Chat UI components
|   |   |   +-- common/               # Reusable UI components
|   |   +-- composables/
|   |   +-- config/
|   |   +-- pages/
|   |   +-- router/
|   |   +-- services/
|   |   +-- stores/
|   |   +-- tests/
|   |   +-- utils/
|   |   +-- App.vue
|   |   +-- main.js
|   +-- package.json
|   +-- vite.config.js
|   +-- vitest.config.js
|
+-- README.md
```

## Prerequisites

- Python 3.11 or newer recommended.
- Node.js 20 or newer recommended.
- npm.
- Redis server running on `127.0.0.1:6379` for WebSocket group messaging.

On Windows, Redis can be run through Docker, WSL, Memurai, or another compatible local Redis distribution.

## Environment Variables

### Backend

Create `backend/.env`:

```env
DJANGO_SECRET_KEY=replace-this-with-a-long-random-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Optional. SQLite is used when DB_ENGINE is omitted.
DB_ENGINE=django.db.backends.sqlite3

# Optional PostgreSQL configuration.
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=chatflow
# DB_USER=postgres
# DB_PASSWORD=postgres
# DB_HOST=localhost
# DB_PORT=5432
```

Important: `DJANGO_SECRET_KEY` is required. The app will not start without it.

### Frontend

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_WS_BASE_URL=ws://127.0.0.1:8000
```

The repository also includes `frontend/.env.example` with these frontend defaults.

## Backend Setup

From the project root:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

If you already use the root `.venv` in this workspace, activate that environment instead:

```bash
..\.venv\Scripts\activate
```

Start Redis before running the ASGI server. Then start the backend:

```bash
python manage.py runserver 127.0.0.1:8000
```

For WebSocket-heavy development, you can also run Daphne directly:

```bash
daphne -b 127.0.0.1 -p 8000 config.asgi:application
```

## Frontend Setup

From the project root:

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server normally runs at:

```text
http://127.0.0.1:5173
```

## Running the App

Run these processes in separate terminals:

1. Redis on `127.0.0.1:6379`.
2. Django backend on `http://127.0.0.1:8000`.
3. Vite frontend on `http://127.0.0.1:5173`.

Then open the frontend in the browser, register or log in, create a room, and join it from another account or browser session to test realtime messaging.

## API Reference

All chat endpoints are mounted under:

```text
/api/chat/
```

Most endpoints require:

```http
Authorization: Bearer <access_token>
```

### Authentication

Djoser and Simple JWT expose auth endpoints under `/auth/`.

Common endpoints:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/auth/users/` | Register a user |
| POST | `/auth/jwt/create/` | Log in and receive access/refresh tokens |
| POST | `/auth/jwt/refresh/` | Refresh an access token |
| POST | `/auth/jwt/verify/` | Verify a JWT |

### Chat Rooms

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/chat/create-room/` | Create a room. Body: `{"room_name":"General"}` |
| POST | `/api/chat/join-room/<room_id>/` | Join an existing room |
| GET | `/api/chat/room/<room_id>/` | Get room details |
| GET | `/api/chat/all-rooms/` | List rooms where the current user is a member |
| DELETE | `/api/chat/delete-room/<room_id>/` | Delete a room. Owner only |
| POST | `/api/chat/leave-room/<room_id>/` | Leave a room. Owners cannot leave their own room |
| GET | `/api/chat/room-members/<room_id>/` | List room members |

### Messages

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/chat/send-message/<room_id>/` | Send a text message |
| GET | `/api/chat/room-messages/<room_id>/` | Paginated room message history |
| DELETE | `/api/chat/delete-message/<message_id>/` | Delete your own message |
| PUT | `/api/chat/edit-message/<message_id>/` | Edit your own message |
| POST | `/api/chat/react-message/<message_id>/` | Toggle an emoji reaction |
| POST | `/api/chat/pin-message/<message_id>/` | Pin a message. Room owner only |
| POST | `/api/chat/unpin-message/<message_id>/` | Unpin a message. Room owner only |
| GET | `/api/chat/pinned-messages/<room_id>/` | List pinned messages in a room |

Message history uses page-number pagination:

```text
GET /api/chat/room-messages/<room_id>/?page=1&page_size=30
```

The maximum page size is `100`.

### Uploads

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/chat/upload-image/` | Upload an image message. Multipart: `room_id`, `image` |
| POST | `/api/chat/upload-audio/` | Upload an audio message. Multipart: `room_id`, `audio` |
| POST | `/api/chat/upload-file/` | Upload a file message. Multipart: `room_id`, `file` |

Upload limits:

- Images: 5 MB.
- Audio: 10 MB.
- Files: 10 MB.

Allowed file extensions:

```text
pdf, doc, docx, txt, zip, rar, xlsx, pptx, csv
```

### Profiles and Presence

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/chat/profile/` | Get the current user's profile |
| PUT | `/api/chat/profile/` | Update profile fields such as avatar, bio, and cover image |
| GET | `/api/chat/presence/<username>/` | Get a user's online/last-seen presence |

### Moderation

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/chat/promote-user/<room_id>/` | Promote a user. Owner only. Body: `username`, `role` |
| POST | `/api/chat/ban-user/<room_id>/` | Ban a user. Owner/admin only |
| POST | `/api/chat/mute-user/<room_id>/` | Mute a user. Owner/admin/moderator only |

Supported roles:

```text
owner, admin, moderator, member
```

## WebSocket Reference

Connect to:

```text
ws://127.0.0.1:8000/ws/chat/<room_id>/<username>/?token=<access_token>
```

The WebSocket middleware also supports a bearer token in the `Authorization` header when the client environment can send it.

### Connection Rules

The socket is rejected when:

- The JWT is missing or invalid.
- The JWT user is inactive.
- The `<username>` path value does not exactly match the token user.
- The room does not exist.
- The user is not a room member.
- The user is banned from the room.
- Redis/channel-layer group join fails.

Close codes used by the consumer include:

| Code | Meaning |
| --- | --- |
| `4401` | Authentication failed |
| `4403` | Forbidden, username mismatch, not a member, or banned |
| `4500` | Server/channel-layer failure |

### Client-to-Server Events

Send JSON messages through the socket.

#### Ping

```json
{
  "type": "ping"
}
```

Response:

```json
{
  "type": "pong"
}
```

#### Text Message

```json
{
  "type": "message",
  "message": "Hello from ChatFlow"
}
```

Broadcast payload:

```json
{
  "message": "Hello from ChatFlow",
  "username": "alice",
  "message_id": 123,
  "created_at": "2026-06-04 12:00:00+00:00"
}
```

Muted users cannot send messages.

#### Typing

```json
{
  "type": "typing"
}
```

Broadcast payload:

```json
{
  "type": "typing",
  "username": "alice"
}
```

#### Delivered

```json
{
  "type": "delivered",
  "message_id": 123
}
```

Broadcast payload:

```json
{
  "type": "delivered",
  "message_id": 123,
  "delivered_at": "2026-06-04 12:00:00+00:00"
}
```

#### Seen

```json
{
  "type": "seen",
  "message_id": 123
}
```

Broadcast payload:

```json
{
  "type": "seen",
  "message_id": 123,
  "seen_by": "alice",
  "seen_at": "2026-06-04 12:00:00+00:00"
}
```

#### Reaction

```json
{
  "type": "reaction",
  "message_id": 123,
  "emoji": ":thumbs_up:"
}
```

Broadcast payload:

```json
{
  "type": "reaction",
  "message_id": 123,
  "reactions": {
    ":thumbs_up:": 2
  }
}
```

### Server-to-Client Events

The server can also send:

```json
{
  "type": "online_users",
  "users": ["alice", "bob"]
}
```

Errors are sent as:

```json
{
  "type": "error",
  "message": "Message content required"
}
```

## Testing

### Backend

From `backend/`:

```bash
python manage.py test
```

The backend includes Django tests for REST and WebSocket behavior in:

```text
backend/chats/tests.py
backend/chats/tests_websocket.py
```

### Frontend

From `frontend/`:

```bash
npm run test
```

Build the production bundle:

```bash
npm run build
```

Preview the production bundle:

```bash
npm run preview
```

## Media and Uploads

In development, uploaded files are stored under:

```text
backend/media/
```

The Django root URL config serves media files when running locally. For production, serve media files through your web server, object storage, or another production-grade file storage setup.

## Security Notes

- `DJANGO_SECRET_KEY` must be unique and private for every deployed environment.
- Keep `DJANGO_DEBUG=False` in production.
- Restrict `DJANGO_ALLOWED_HOSTS` to real hostnames in production.
- Update `CORS_ALLOWED_ORIGINS` in `backend/config/settings.py` for deployed frontend origins.
- Use HTTPS in production and set frontend `VITE_WS_BASE_URL` to `wss://...`.
- WebSocket connections must include a valid JWT and match the requested username.
- Login is rate-limited to 5 attempts per minute per IP.
- Registration is rate-limited to 3 attempts per minute per IP.
- Message and upload endpoints also use user-based rate limits.
- Server-side validation is present for uploaded file size and extension.

## Production Notes

Before deploying:

1. Set `DJANGO_DEBUG=False`.
2. Use a strong `DJANGO_SECRET_KEY`.
3. Configure `DJANGO_ALLOWED_HOSTS`.
4. Configure production CORS origins.
5. Use PostgreSQL or another durable production database.
6. Run Redis as a managed or supervised service.
7. Serve the ASGI app with Daphne/Uvicorn behind a reverse proxy.
8. Serve static files from `STATIC_ROOT` after `python manage.py collectstatic`.
9. Serve media files outside the Django development static helper.
10. Use `https://` and `wss://` URLs.
11. Review cookie security settings if session/CSRF flows are used.

Collect static files:

```bash
cd backend
python manage.py collectstatic
```

Build frontend assets:

```bash
cd frontend
npm run build
```

The frontend build output is written to:

```text
frontend/dist/
```

## Troubleshooting

### `DJANGO_SECRET_KEY must be set`

Create `backend/.env` and add `DJANGO_SECRET_KEY`.

### WebSocket closes immediately with `4401`

The access token is missing, invalid, expired, or not being passed in the WebSocket URL/header.

Use:

```text
?token=<access_token>
```

### WebSocket closes with `4403`

Check that:

- The URL username exactly matches the JWT user's username.
- The user joined the room.
- The user is not banned.
- The room UUID is correct.

### WebSocket closes with `4500`

Check that Redis is running at:

```text
127.0.0.1:6379
```

Also check backend logs for channel-layer errors.

### Frontend cannot reach backend

Check `frontend/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_WS_BASE_URL=ws://127.0.0.1:8000
```

Restart the Vite dev server after changing `.env`.

### CORS errors

Add the frontend origin to `CORS_ALLOWED_ORIGINS` in `backend/config/settings.py`. The current local defaults include:

```text
http://localhost:5173
http://127.0.0.1:5173
```

### Upload rejected

Check file size and extension. Files are limited to 10 MB and only the configured document/archive formats are allowed.

## Useful Commands

```bash
# Backend
cd backend
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
python manage.py test

# Frontend
cd frontend
npm install
npm run dev
npm run build
npm run test
```

## License

No license file is currently included at the project root. Add one before distributing or publishing the project.
