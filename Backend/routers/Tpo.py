from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database.DB import get_db
from services.AuthService import tpo_Authorization
from services.TpoService import TpoService

router_tpo = APIRouter()

@router_tpo.get("/students", summary="Get TPO Students", description="Returns a list of students for the TPO's college.")
async def get_tpo_students_api(db: Session = Depends(get_db), token: dict = Depends(tpo_Authorization())):
    tpo_id = token.get("user_id")
    if not tpo_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")
    return await TpoService().get_tpo_students(tpo_id, db)
