"""Final grade calculation logic."""
from typing import List
from app.core.llm.client import LLMClient
from app.core.llm.prompts import load_prompt, format_prompt
from app.core.llm.guardrails import validate_response
from app.core.schemas.llm_contracts import FinalGrade
import logging

logger = logging.getLogger(__name__)


class FinalGradeCalculator:
    """Calculates final exam grades using LLM."""
    
    def __init__(self):
        self.llm_client = LLMClient()
        self.prompt_template = None
        self._load_template()
    
    def _load_template(self):
        """Load the final grade prompt template."""
        try:
            self.prompt_template = load_prompt("final_grade_v1.txt")
        except FileNotFoundError:
            logger.warning("Final grade prompt not found, using default")
            self.prompt_template = self._get_default_template()
    
    def _get_default_template(self) -> str:
        """Default template if file not found."""
        return """Calculate the final exam grade based on the following question scores and feedback.

Question Scores: {question_scores}

Feedback Summary: {feedback_summary}

Please provide:
1. A final grade (0-100)
2. A comprehensive explanation of the final grade
3. The individual question scores as a list

Respond in JSON format:
{{
    "final_grade": 85.0,
    "explanation": "Overall explanation of performance",
    "question_scores": [85.0, 90.0, 80.0]
}}"""
    
    async def calculate_final_grade(self, question_scores: List[float], 
                                   feedback_summary: List[str]) -> FinalGrade:
        """Calculate final grade using LLM analysis."""
        scores_str = ", ".join([f"{s:.1f}" for s in question_scores])
        feedback_str = "\n".join([f"- {f}" for f in feedback_summary])
        
        prompt = format_prompt(
            self.prompt_template,
            question_scores=scores_str,
            feedback_summary=feedback_str
        )
        
        system_prompt = "You are an expert evaluator calculating final exam grades. Be fair and comprehensive. Always respond with valid JSON."
        
        try:
            response_dict = await self.llm_client.generate_json(prompt, system_prompt)
            result = validate_response(response_dict, FinalGrade)
            
            if not result:
                # Fallback: simple average if validation fails
                logger.warning("LLM response validation failed, using average calculation")
                avg_grade = sum(question_scores) / len(question_scores) if question_scores else 0.0
                return FinalGrade(
                    final_grade=avg_grade,
                    explanation=f"Final grade calculated as average of {len(question_scores)} questions.",
                    question_scores=question_scores
                )
            
            return result
        except Exception as e:
            logger.error(f"Error calculating final grade: {e}")
            # Fallback: simple average on error
            avg_grade = sum(question_scores) / len(question_scores) if question_scores else 0.0
            return FinalGrade(
                final_grade=avg_grade,
                explanation=f"Final grade calculated as average of individual question scores due to calculation error.",
                question_scores=question_scores
            )

