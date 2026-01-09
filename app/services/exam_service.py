"""Exam service for managing exam workflow."""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models import Exam, Question
from app.db.repo import ExamRepository, QuestionRepository, StudentRepository
from app.core.grading.generator import QuestionGenerator
from app.core.grading.grader import AnswerGrader
from app.core.grading.finalizer import FinalGradeCalculator
from app.core.grading.thresholds import should_ask_followup
from app.settings import get_settings
import logging

logger = logging.getLogger(__name__)

from app.core.grading.generator import QuestionGenerator

question_generator = QuestionGenerator()

class ExamService:
    """Service for managing exam sessions and workflow."""
    
    def __init__(self):
        self.settings = get_settings()
        self.question_generator = question_generator
        self.answer_grader = AnswerGrader()
        self.final_grade_calculator = FinalGradeCalculator()
    
    async def start_exam(self, db: Session, username: str) -> Exam:
        """Start a new exam session for a student."""
        student = StudentRepository.get_or_create(db, username)
        exam = ExamRepository.create(db, student.id)
        
        # Generate initial questions
        for i in range(1, self.settings.exam_question_count + 1):
            try:
                generated = await self.question_generator.generate_question(
                    topic="Computer Science",
                    difficulty="Intermediate",
                    question_number=i
                )
                QuestionRepository.create(
                    db,
                    exam.id,
                    i,
                    generated.question_text,
                    generated.context,
                    generated.rubric
                )
            except Exception as e:
                logger.warning(f"Error generating question {i} (likely no API key): {e}")
                # Create different fallback questions based on question number
                generated = await self.question_generator.generate_question(
                    topic="Computer Science",
                    difficulty="Intermediate",
                    question_number=i
                )

        return exam
    
    async def get_current_question(self, db: Session, exam_id: int) -> Optional[Question]:
        """Get the current unanswered question for an exam."""
        questions = QuestionRepository.get_by_exam(db, exam_id)
        for question in questions:
            if question.student_answer is None:
                return question
        return None
    
    async def submit_answer(self, db: Session, question_id: int, answer: str) -> Question:
        """Submit an answer for a question."""
        question = QuestionRepository.update_answer(db, question_id, answer)
        
        if question:
            # Grade the answer
            try:
                grading_result = await self.answer_grader.grade_answer(
                    question.question_text,
                    question.context or "",
                    question.rubric or "",
                    answer
                )
                QuestionRepository.update_grade(
                    db,
                    question_id,
                    grading_result.grade,
                    grading_result.feedback
                )
            except Exception as e:
                logger.error(f"Error grading answer: {e}")
        
        return question
    
    async def complete_exam(self, db: Session, exam_id: int) -> Exam:
        """Calculate final grade and complete the exam."""
        questions = QuestionRepository.get_by_exam(db, exam_id)
        
        # Collect scores and feedback
        scores = []
        feedbacks = []
        for q in questions:
            if q.grade is not None:
                scores.append(q.grade)
                feedbacks.append(q.feedback or "")
        
        # Calculate final grade
        try:
            final_result = await self.final_grade_calculator.calculate_final_grade(
                scores,
                feedbacks
            )
            
            ExamRepository.update_status(
                db,
                exam_id,
                "completed",
                final_result.final_grade,
                final_result.explanation
            )
        except Exception as e:
            logger.error(f"Error calculating final grade: {e}")
            # Fallback: simple average
            avg_grade = sum(scores) / len(scores) if scores else 0.0
            ExamRepository.update_status(
                db,
                exam_id,
                "completed",
                avg_grade,
                f"Final grade calculated as average: {avg_grade:.1f}"
            )
        
        exam = ExamRepository.get(db, exam_id)
        return exam
    
    def get_exam_status(self, db: Session, exam_id: int) -> dict:
        """Get current status of an exam."""
        exam = ExamRepository.get(db, exam_id)
        if not exam:
            return None
        
        questions = QuestionRepository.get_by_exam(db, exam_id)
        answered_count = sum(1 for q in questions if q.student_answer is not None)
        
        return {
            "exam_id": exam.id,
            "status": exam.status,
            "questions_completed": answered_count,
            "total_questions": len(questions),
            "current_question": answered_count + 1 if exam.status == "in_progress" else None
        }

