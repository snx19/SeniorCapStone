"""Pydantic schemas for API request/response models."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class LoginRequest(BaseModel):
    """Login request model."""
    username: str


class ExamStartResponse(BaseModel):
    """Response when starting an exam."""
    exam_id: int
    question_count: int


class QuestionResponse(BaseModel):
    """Response for a question."""
    question_id: int
    question_number: int
    question_text: str
    context: Optional[str] = None
    is_followup: bool = False


class AnswerSubmission(BaseModel):
    """Answer submission model."""
    question_id: int
    answer: str


class GradingResponse(BaseModel):
    """Response after grading."""
    question_id: int
    grade: float
    feedback: str


class ExamStatusResponse(BaseModel):
    """Exam status response."""
    exam_id: int
    status: str
    current_question: Optional[int] = None
    questions_completed: int
    total_questions: int


class FinalGradeResponse(BaseModel):
    """Final grade response."""
    exam_id: int
    final_grade: float
    explanation: str
    question_grades: List[float]

