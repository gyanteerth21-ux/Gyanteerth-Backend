# Gyanteerth LMS Backend

A FastAPI-based Learning Management System backend with:
- JWT Authentication (Email + Google OAuth)
- Course management (Recorded & Live)
- Auto Google Meet link generation for live sessions
- Supabase PostgreSQL database
- Cloudinary for media uploads

## Tech Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy + Alembic
- **Auth**: JWT (python-jose) + Google OAuth2
- **Email**: aiosmtplib (SMTP)
- **Storage**: Cloudinary

## Setup

```bash
cd Backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python init_db.py      # Create tables on fresh DB
uvicorn main:app --reload
```

## Environment Variables
Set these in `.env` (see `.env.example`):
- `DATABASE_URL`
- `SECRET_KEY`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_TOKEN_JSON`
- `CLOUDINARY_*`
