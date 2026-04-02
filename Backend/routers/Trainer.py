from fastapi import BackgroundTasks, FastAPI,HTTPException,Request,APIRouter,Depends, UploadFile, File,Form,Path,Query,status
from sqlalchemy.orm import Session
from services.TrainerService import TrainerService
from Database.DB import get_db
from fastapi.responses import JSONResponse
from services.AuthService import trainer_Authorization

router_trainer= APIRouter()

@router_trainer.get("/trainer_course_ids", summary="Get Trainer Course IDs", description="Fetches all course IDs assigned to a specific trainer.")
async def get_trainer_course_ids(
    db: Session = Depends(get_db),
    token: dict = Depends(trainer_Authorization())
):
    return await TrainerService().Trainer_have_course_ids(db, token)
