"""Main FastAPI application."""
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_
from datetime import datetime, timezone
from app.api.router import api_router
from app.db.base import Base, engine
from app.db.session import get_db
from app.db.models import User, Course, Exam, Student
from app.logging_config import setup_logging

# Import seeding function
from app.db.seed_users import seed_users

# Setup logging
setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed users if they don’t already exist
seed_users()

# Create FastAPI app
app = FastAPI(
    title="AI Oral Exam Grader",
    description="AI-powered oral exam grading system",
    version="0.1.0"
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
env = Environment(loader=FileSystemLoader("app/templates"))


def render_template(template_name: str, context: dict) -> HTMLResponse:
    """Render a Jinja2 template."""
    template = env.get_template(template_name)
    html_content = template.render(**context)
    return HTMLResponse(content=html_content)

@app.get("/student/dashboard", response_class=HTMLResponse)
async def student_dashboard(request: Request, db: Session = Depends(get_db)):
    """Student dashboard page with personalized welcome."""
    # Get email from cookie
    email = request.cookies.get("username")
    if not email:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Use first_name if available, otherwise fallback to "Student"
    first_name = user.first_name if user.first_name else "Student"
    
    return render_template("student_dashboard.html", {
        "request": request,
        "first_name": first_name
    })

@app.get("/teacher/dashboard", response_class=HTMLResponse)
async def teacher_dashboard(request: Request, db: Session = Depends(get_db)):
    """Teacher dashboard page with personalized welcome."""
    # Get email from cookie
    email = request.cookies.get("username")
    if not email:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Use first_name if available, otherwise fallback to "Teacher"
    first_name = user.first_name if user.first_name else "Teacher"
    
    # Query courses for this instructor from database
    courses = db.query(Course).filter(Course.instructor_id == user.id).all()
    
    # Query open exams for this instructor (published exams)
    # Join with Student to get student info, then try to match with User
    open_exams_query = db.query(Exam).outerjoin(
        Student, Exam.student_id == Student.id
    ).filter(
        Exam.instructor_id == user.id,
        Exam.date_published.isnot(None)  # Only published exams
    )
    
    # Build exam data with student info
    open_exams = []
    for exam in open_exams_query.all():
        student = None
        user_obj = None
        
        if exam.student_id:
            student = db.query(Student).filter(Student.id == exam.student_id).first()
            if student:
                # Try to find User by email (assuming username might be email)
                user_obj = db.query(User).filter(User.email == student.username).first()
        
        # Calculate percent if final_grade exists
        percent = exam.final_grade * 100 if exam.final_grade else None
        
        # Calculate letter grade
        grade = None
        if percent is not None:
            if percent >= 90:
                grade = "A"
            elif percent >= 80:
                grade = "B"
            elif percent >= 70:
                grade = "C"
            elif percent >= 60:
                grade = "D"
            else:
                grade = "F"
        
        open_exams.append({
            "exam_id": exam.exam_id,
            "student_id": user_obj.student_id if user_obj else (student.username if student else None),
            "first_name": user_obj.first_name if user_obj else None,
            "last_name": user_obj.last_name if user_obj else None,
            "status": exam.status,
            "percent": percent,
            "grade": grade,
            "date_started": exam.created_at if exam.student_id else None,
            "date_completed": exam.completed_at,
            "date_published": exam.date_published
        })
    
    return render_template("teacher_dashboard.html", {
        "request": request,
        "first_name": first_name,
        "courses": courses,
        "open_exams": open_exams
    })

@app.get("/teacher/register-course", response_class=HTMLResponse)
async def register_course_page(request: Request, db: Session = Depends(get_db)):
    """Display the register new course form."""
    # Get email from cookie
    email = request.cookies.get("username")
    if not email:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if not user or user.role != "teacher":
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Generate year options (20-35 for years 2020-2035 in short format)
    year_options = [str(year) for year in range(20, 36)]
    
    error = request.query_params.get("error", "")
    
    return render_template("register_course.html", {
        "request": request,
        "year_options": year_options,
        "error": error
    })

@app.post("/teacher/register-course")
async def register_course(
    request: Request,
    course_number: str = Form(...),
    quarter: str = Form(...),
    year: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle course registration form submission."""
    # Get email from cookie
    email = request.cookies.get("username")
    if not email:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if not user or user.role != "teacher":
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get sections from form (as list) - FastAPI form data
    form_data = await request.form()
    sections_raw = form_data.getlist("sections[]")
    # If getlist doesn't work, try getting as single value first
    if not sections_raw:
        # Fallback: check if it's a single value
        single_section = form_data.get("sections[]")
        sections = [single_section] if single_section else []
    else:
        sections = sections_raw
    
    # Validate input
    if not sections or len(sections) == 0:
        return RedirectResponse(url="/teacher/register-course?error=At least one section is required", status_code=302)
    
    # Convert course_number to uppercase
    course_number = course_number.upper().strip()
    
    # Build quarter_year string (e.g., "Spring26")
    quarter_year = f"{quarter}{year}"
    
    # Create a course record for each section
    created_courses = []
    errors = []
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        try:
            # Check if course already exists
            existing = db.query(Course).filter(
                Course.course_number == course_number,
                Course.section == section,
                Course.quarter_year == quarter_year,
                Course.instructor_id == user.id
            ).first()
            
            if existing:
                errors.append(f"Course {course_number} Section {section} for {quarter_year} already exists")
                continue
            
            # Create new course
            course = Course(
                course_number=course_number,
                section=section,
                quarter_year=quarter_year,
                instructor_id=user.id
            )
            db.add(course)
            created_courses.append(course)
            
        except IntegrityError as e:
            db.rollback()
            errors.append(f"Error creating {course_number} Section {section}: {str(e)}")
    
    # Commit all courses
    if created_courses:
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            return RedirectResponse(url=f"/teacher/register-course?error=Error saving courses: {str(e)}", status_code=302)
    
    # If there were errors but some courses were created, show success but note errors
    if errors and created_courses:
        # Redirect with success - courses were created despite some errors
        return RedirectResponse(url="/teacher/dashboard?warning=Some courses already existed", status_code=302)
    elif errors and not created_courses:
        # All failed
        error_msg = "; ".join(errors)
        return RedirectResponse(url=f"/teacher/register-course?error={error_msg}", status_code=302)
    
    # Success - redirect to dashboard
    return RedirectResponse(url="/teacher/dashboard?success=course_registered", status_code=302)

@app.get("/teacher/create-exam", response_class=HTMLResponse)
async def create_exam_page(request: Request, db: Session = Depends(get_db)):
    """Display the create new exam form."""
    # Get email from cookie
    email = request.cookies.get("username")
    if not email:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if not user or user.role != "teacher":
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get courses for this instructor
    courses = db.query(Course).filter(Course.instructor_id == user.id).all()
    
    error = request.query_params.get("error", "")
    
    return render_template("create_exam.html", {
        "request": request,
        "courses": courses,
        "error": error
    })

@app.post("/teacher/create-exam")
async def create_exam(
    request: Request,
    course_number: str = Form(...),
    section: str = Form(...),
    quarter_year: str = Form(...),
    exam_name: str = Form(...),
    llm_prompt: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle exam creation form submission."""
    # Get email from cookie
    email = request.cookies.get("username")
    if not email:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if not user or user.role != "teacher":
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Verify the course belongs to this instructor
    course = db.query(Course).filter(
        Course.course_number == course_number.upper(),
        Course.section == section,
        Course.quarter_year == quarter_year,
        Course.instructor_id == user.id
    ).first()
    
    if not course:
        return RedirectResponse(url="/teacher/create-exam?error=Course not found or access denied", status_code=302)
    
    # Generate exam_id: course_number-section-exam_name-quarter_year
    exam_id = f"{course_number.upper()}-{section}-{exam_name.lower().replace(' ', '-')}-{quarter_year}"
    
    # Check if exam with this ID already exists
    existing_exam = db.query(Exam).filter(Exam.exam_id == exam_id).first()
    if existing_exam:
        return RedirectResponse(url="/teacher/create-exam?error=An exam with this ID already exists. Please choose a different exam name.", status_code=302)
    
    # Get instructor name
    instructor_name = f"{user.first_name} {user.last_name}"
    
    # Create new exam (not published yet, status = "not_started")
    exam = Exam(
        exam_id=exam_id,
        course_number=course_number.upper(),
        section=section,
        exam_name=exam_name,
        quarter_year=quarter_year,
        instructor_name=instructor_name,
        instructor_id=user.id,
        status="not_started",  # Not yet published
        # Store LLM prompt in final_explanation field for now (or create a separate field later)
        # For now, we'll store it in final_explanation temporarily
        final_explanation=llm_prompt
    )
    
    try:
        db.add(exam)
        db.commit()
        db.refresh(exam)
        
        # Redirect to course page to see the new exam
        # TODO: Later redirect to exam preview/edit page for LLM generation
        return RedirectResponse(url=f"/teacher/course/{course_number.upper()}/{section}?exam_created={exam_id}", status_code=302)
        
    except IntegrityError as e:
        db.rollback()
        return RedirectResponse(url=f"/teacher/create-exam?error=Error creating exam: {str(e)}", status_code=302)
    except Exception as e:
        db.rollback()
        return RedirectResponse(url=f"/teacher/create-exam?error=Unexpected error: {str(e)}", status_code=302)

@app.get("/teacher/course/{course_number}/{section}", response_class=HTMLResponse)
async def course_page(
    request: Request,
    course_number: str,
    section: str,
    db: Session = Depends(get_db)
):
    """Display course page with exams."""
    # Get email from cookie
    email = request.cookies.get("username")
    if not email:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if not user or user.role != "teacher":
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get course from database (verify it belongs to this instructor)
    course = db.query(Course).filter(
        Course.course_number == course_number.upper(),
        Course.section == section,
        Course.instructor_id == user.id
    ).first()
    
    if not course:
        return RedirectResponse(url="/teacher/dashboard?error=course_not_found", status_code=302)
    
    # Query open exams for this course/section (published and not completed)
    open_exams = db.query(Exam).filter(
        Exam.course_number == course_number.upper(),
        Exam.section == section,
        Exam.quarter_year == course.quarter_year,
        Exam.date_published.isnot(None),  # Must be published
        Exam.status != "completed"  # Not completed
    ).order_by(Exam.date_published.desc()).all()
    
    # Query closed exams for this course/section (completed or past end date)
    now = datetime.now(timezone.utc)
    closed_exams = db.query(Exam).filter(
        Exam.course_number == course_number.upper(),
        Exam.section == section,
        Exam.quarter_year == course.quarter_year,
        or_(
            Exam.status == "completed",
            and_(Exam.date_end_availability.isnot(None), Exam.date_end_availability < now)
        )
    ).order_by(Exam.completed_at.desc()).all()
    
    return render_template("course_page.html", {
        "request": request,
        "course_number": course_number.upper(),
        "section": section,
        "quarter_year": course.quarter_year,
        "open_exams": open_exams,
        "closed_exams": closed_exams
    })

@app.get("/teacher/exam/{exam_id}", response_class=HTMLResponse)
async def exam_details_page(
    request: Request,
    exam_id: str,
    db: Session = Depends(get_db)
):
    """Display exam details page."""
    # Get email from cookie
    email = request.cookies.get("username")
    if not email:
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if not user or user.role != "teacher":
        return RedirectResponse(url="/?error=login_required", status_code=302)
    
    # Get exam from database (using exam_id string, not id integer)
    exam = db.query(Exam).filter(Exam.exam_id == exam_id).first()
    
    if not exam:
        return RedirectResponse(url="/teacher/dashboard?error=exam_not_found", status_code=302)
    
    # Verify exam belongs to this instructor
    if exam.instructor_id != user.id:
        return RedirectResponse(url="/teacher/dashboard?error=access_denied", status_code=302)
    
    return render_template("exam_details.html", {
        "request": request,
        "exam": exam
    })

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root page - login form."""
    error = request.query_params.get("error", "")
    success = request.query_params.get("success", "")
    return render_template("login.html", {"request": request, "error": error, "success": success})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Signup page - create new account."""
    error = request.query_params.get("error", "")
    return render_template("signup.html", {"request": request, "error": error})

@app.get("/teacher/login", response_class=HTMLResponse)
async def teacher_login_page(request: Request):
    """Teacher login page."""
    error = request.query_params.get("error", "")
    success = request.query_params.get("success", "")
    return render_template("teacher_login.html", {"request": request, "error": error, "success": success})


@app.get("/question/{question_id}", response_class=HTMLResponse)
async def question_page(request: Request, question_id: int):
    """Dummy question page for testing login."""
    # You can later render question.html template here
    return render_template("question.html", {"request": request, "question_id": question_id})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)