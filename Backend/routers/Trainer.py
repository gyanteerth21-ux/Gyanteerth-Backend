from fastapi import BackgroundTasks, FastAPI,HTTPException,Request,APIRouter,Depends, UploadFile, File,Form,Path,Query,status
from sqlalchemy.orm import Session
from services.TrainerService import TrainerService
from Database.DB import get_db
from fastapi.responses import JSONResponse
from services.AuthService import trainer_Authorization
from schemas.admin import CourseStudentsProgressResponse

router_trainer= APIRouter()

@router_trainer.get("/trainer_course_ids", summary="Get Trainer Course IDs", description="Fetches all course IDs assigned to a specific trainer.")
async def get_trainer_course_ids(
    db: Session = Depends(get_db),
    token: dict = Depends(trainer_Authorization())
):
    return await TrainerService().Trainer_have_course_ids(db, token)

@router_trainer.get("/course/{course_id}/students-progress", response_model=CourseStudentsProgressResponse, summary="Get Course Students Progress", description="Returns detailed progress for all students enrolled in a specific course.")
async def get_course_students_progress_api(course_id: str, db: Session = Depends(get_db), token: dict = Depends(trainer_Authorization())):
    return await TrainerService().get_course_students_progress(course_id, db, token)

@router_trainer.get("/assessment_results", summary="Get Assessment Results")
async def get_assessment_results(
    from_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: str = Query(None, description="End date (YYYY-MM-DD)"),
    course_id: str = Query(None, description="Filter by Course ID"),
    db: Session = Depends(get_db),
    token: object = Depends(trainer_Authorization())
):
    return await TrainerService().get_assessment_results(token, from_date, to_date, course_id, db)

@router_trainer.get("/export_assessment_results", summary="Export Assessment Results to Excel")
async def export_assessment_results(
    from_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: str = Query(None, description="End date (YYYY-MM-DD)"),
    course_id: str = Query(None, description="Filter by Course ID"),
    db: Session = Depends(get_db),
    token: object = Depends(trainer_Authorization())
):
    return await TrainerService().export_assessment_results(token, from_date, to_date, course_id, db)
