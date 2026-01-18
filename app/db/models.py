"""Database models."""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base



class User(Base):
    """User login model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(50), nullable=False)  # "student" or "teacher"
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    student_id = Column(String(50), nullable=True)  # Only for students
    instructor_id = Column(String(50), nullable=True)  # Only for teachers
    
    # Relationships
    courses = relationship("Course", back_populates="instructor")
    
class Student(Base):
    """Student model."""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    exams = relationship("Exam", back_populates="student")


class Exam(Base):
    """Exam session model."""
    __tablename__ = "exams"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    status = Column(String(50), default="in_progress")  # in_progress, completed
    final_grade = Column(Float, nullable=True)
    final_explanation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    student = relationship("Student", back_populates="exams")
    questions = relationship("Question", back_populates="exam")


class Question(Base):
    """Exam question model."""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    question_number = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    rubric = Column(Text, nullable=True)
    student_answer = Column(Text, nullable=True)
    grade = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    is_followup = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    exam = relationship("Exam", back_populates="questions")


class Course(Base):
    """Course model for instructors."""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_number = Column(String(20), nullable=False, index=True)  # e.g., "CSC376"
    section = Column(String(10), nullable=False)  # e.g., "424"
    quarter_year = Column(String(20), nullable=False)  # e.g., "Spring26"
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    instructor = relationship("User", back_populates="courses")
    
    # Composite unique constraint: same course_number + section + quarter_year should be unique per instructor
    __table_args__ = (
        UniqueConstraint('course_number', 'section', 'quarter_year', 'instructor_id', name='uq_course_instructor'),
    )

