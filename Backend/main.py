import sys
import os
# Fix for Vercel: add Backend/ directory to Python path so all local modules resolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from sqlalchemy import text
from Database.DB import SessionLocal
from routers.Auth import router_auth
from routers.user import router_user
from routers.Admin import router_admin
from routers.Trainer import router_trainer
import time
from Database.DB import query_times

app = FastAPI()

@app.on_event("startup")
def startup_db_sync():
    from Database.DB import engine
    from sqlalchemy import text
    from Models.Progress.AssessmentAnswerTable import AssessmentAnswerTable
    
    try:
        # Ensure new tables like AssessmentAnswerTable are created FIRST
        AssessmentAnswerTable.metadata.create_all(bind=engine)
        print("Database tables sync completed successfully on startup.")
    except Exception as e:
        print(f"Database tables sync failed: {str(e)}")
        
    try:
        with engine.connect() as conn:
            # Safely add the user_college column (may fail if dialect doesn't support IF NOT EXISTS, but won't block table creation)
            conn.execute(text("ALTER TABLE user_profile ADD COLUMN IF NOT EXISTS user_college VARCHAR(150);"))
            
            # Safely add the LiveAttendanceTable columns that might be missing if alembic upgrade isn't run
            conn.execute(text('ALTER TABLE live_attendance_table ADD COLUMN IF NOT EXISTS "Attended_Live" BOOLEAN DEFAULT FALSE;'))
            conn.execute(text('ALTER TABLE live_attendance_table ADD COLUMN IF NOT EXISTS "Watched_Recording" BOOLEAN DEFAULT FALSE;'))
            conn.execute(text('ALTER TABLE live_attendance_table ADD COLUMN IF NOT EXISTS "Is_Present" BOOLEAN DEFAULT FALSE;'))
            
            conn.commit()
    except Exception as e:
        print(f"ALTER TABLE skipped/failed: {str(e)}")

app.add_middleware(SessionMiddleware, secret_key="your_super_secret_key_here")
# Read allowed origins from environment
env_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://lms-vert-alpha.vercel.app",
    "https://gyanteerth.vercel.app",
    "https://gyanteerthlearning.online",
    "https://www.gyanteerthlearning.online",
]
# Add any extra origins from .env
origins.extend([o.strip() for o in env_origins if o.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="https://.*\\.amplifyapp\\.com/?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": f"HTTP {exc.status_code}",
            "message": exc.detail,
            "path": str(request.url)
        }
    )

@app.middleware("http")
async def add_process_time_header(request, call_next):

    start_time = time.time()

    response = await call_next(request)

    api_time = time.time() - start_time
    db_time = sum(query_times)
    query_count = len(query_times)

    response.headers["X-API-Time"] = str(round(api_time, 5))
    response.headers["X-DB-Time"] = str(round(db_time, 5))
    response.headers["X-Query-Count"] = str(query_count)

    query_times.clear()

    return response

app.include_router(router_auth,prefix="/gyantreeth/v1/auth_checkpoint",tags=["Authentication"])
app.include_router(router_user,prefix="/gyantreeth/v1/user",tags=["User"])
app.include_router(router_admin,prefix="/gyantreeth/v1/admin",tags=["Admin"])
app.include_router(router_trainer,prefix="/gyantreeth/v1/trainer",tags=["Trainer"])

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)