"""Authentication routes."""
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.exam_service import ExamService

router = APIRouter()


@router.post("/login")
async def login(request: Request, username: str = Form(...), db: Session = Depends(get_db)):
    """Login and start exam session."""
    if not username:
        return RedirectResponse(url="/?error=username_required", status_code=302)
    
    # Start exam
    exam_service = ExamService()
    exam = await exam_service.start_exam(db, username)
    
    # Store exam_id in session (for POC, we'll use cookies)
    response = RedirectResponse(url=f"/api/exam/{exam.id}", status_code=302)
    response.set_cookie(key="exam_id", value=str(exam.id))
    response.set_cookie(key="username", value=username)
    
    return response

