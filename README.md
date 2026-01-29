# AI Complaint System (Flask Backend)

## Requirements
- Python 3.11+ (recommended)
- Virtualenv (recommended)

## Setup (Windows)
1. Create venv
	- `python -m venv venv`
	- `venv\Scripts\activate`
2. Install deps
	- `pip install -r requirements.txt`
	- (optional dev) `pip install -r requirements-dev.txt`
3. Configure env
	- Copy `.env.example` → `.env`
	- Set `SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL`
4. Migrate DB
	- `flask db upgrade`
5. Run
	- `python run.py`


## API Quickstart
### Register
POST `/auth/register`
```json
{ "name": "Alice", "email": "alice@example.com", "password": "pass1234" }
```

### Login
POST `/auth/login`
```json
{ "email": "alice@example.com", "password": "pass1234" }
```

### Create complaint
POST `/complaints` (Bearer token required)
```json
{ "title": "Internet down", "description": "WiFi not working in room" }
```

### My complaints
GET `/complaints/my` (Bearer token required)

### Health check
GET `/health`
