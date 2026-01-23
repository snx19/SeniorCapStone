"""Notification routes."""
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User, Notification
from app.services.notification_service import NotificationService

router = APIRouter()


@router.get("/notification/{notification_id}/read")
async def mark_notification_read(
    request: Request,
    notification_id: int,
    redirect: str = "/student/dashboard",
    db: Session = Depends(get_db)
):
    """Mark a notification as read."""
    # Get user from cookie
    email = request.cookies.get("username")
    if not email:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    notification_service = NotificationService()
    success = notification_service.mark_as_read(db, notification_id, user.id)
    
    if not success:
        # Notification not found or doesn't belong to user
        return RedirectResponse(url=f"{redirect}?error=Notification not found", status_code=302)
    
    return RedirectResponse(url=redirect, status_code=302)


@router.post("/notifications/mark-all-read")
async def mark_all_notifications_read(
    request: Request,
    db: Session = Depends(get_db)
):
    """Mark all notifications as read for the current user."""
    # Get user from cookie
    email = request.cookies.get("username")
    if not email:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    notification_service = NotificationService()
    count = notification_service.mark_all_as_read(db, user.id)
    
    # Determine redirect based on user role
    if user.role == "teacher":
        redirect_url = "/api/teacher/dashboard"
    else:
        redirect_url = "/student/dashboard"
    
    return RedirectResponse(url=f"{redirect_url}?success={count} notifications marked as read", status_code=302)
