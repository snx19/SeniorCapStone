"""Question generation logic."""
from app.core.llm.client import LLMClient
from app.core.llm.prompts import load_prompt, format_prompt
from app.core.llm.guardrails import validate_response
from app.core.schemas.llm_contracts import GeneratedQuestion
import logging

logger = logging.getLogger(__name__)


class QuestionGenerator:
    """Generates exam questions using LLM."""
    
    def __init__(self):
        self.llm_client = LLMClient()
        self.prompt_template = None
        self._load_template()
    
    def _load_template(self):
        """Load the question generation prompt template."""
        try:
            self.prompt_template = load_prompt("question_gen_v1.txt")
        except FileNotFoundError:
            logger.warning("Question generation prompt not found, using default")
            self.prompt_template = self._get_default_template()
    
    def _get_default_template(self) -> str:
        """Default template if file not found."""
        return """Generate an essay-style exam question for a computer science course.

Topic: {topic}
Difficulty: {difficulty}
Question Number: {question_number}

Please provide:
1. A clear, thought-provoking question
2. Relevant background context
3. A detailed grading rubric

Respond in JSON format with the following structure:
{{
    "question_text": "The question text",
    "context": "Background context and information",
    "rubric": "Detailed grading rubric with criteria"
}}"""
    
    async def generate_question(self, topic: str = "Computer Science", difficulty: str = "Intermediate", 
                               question_number: int = 1) -> GeneratedQuestion:
        """Generate a question using the LLM."""
        prompt = format_prompt(
            self.prompt_template,
            topic=topic,
            difficulty=difficulty,
            question_number=question_number
        )
        
        system_prompt = "You are an expert computer science professor creating exam questions. Always respond with valid JSON."
        
        try:
            response_dict = await self.llm_client.generate_json(prompt, system_prompt)
            question = validate_response(response_dict, GeneratedQuestion)
            
            if not question:
                # Fallback to default question if validation fails
                logger.warning("LLM response validation failed, using fallback question")
                return self._get_fallback_question(question_number)
            
            return question
        except Exception as e:
            logger.warning(f"Error generating question (likely no API key): {e}")
            # Return fallback question on error
            return self._get_fallback_question(question_number)
    
    def _get_fallback_question(self, question_number: int) -> GeneratedQuestion:
        """Get a fallback question based on question number."""
        fallback_questions = {
            1: {
                "question_text": "Question 1: Explain the fundamental principles of data structures. Discuss the differences between arrays and linked lists, and when you would use each.",
                "context": "Data structures are fundamental to computer science. Arrays store elements in contiguous memory, while linked lists use nodes with pointers. Understanding when to use each is crucial for efficient programming.",
                "rubric": "Grading criteria: (1) Understanding of arrays - 25 points, (2) Understanding of linked lists - 25 points, (3) Comparison and differences - 25 points, (4) Use case examples - 25 points. Total: 100 points."
            },
            2: {
                "question_text": "Question 2: Describe the concept of algorithm time complexity (Big O notation). Provide examples of O(1), O(n), and O(n²) algorithms and explain why understanding complexity matters.",
                "context": "Algorithm complexity analysis helps developers understand how algorithms scale. Big O notation describes the worst-case time complexity. Efficient algorithms can make the difference between a usable and unusable program.",
                "rubric": "Grading criteria: (1) Explanation of Big O notation - 30 points, (2) O(1) example and explanation - 20 points, (3) O(n) example and explanation - 20 points, (4) O(n²) example and explanation - 20 points, (5) Importance discussion - 10 points. Total: 100 points."
            },
            3: {
                "question_text": "Question 3: Explain the concept of recursion in programming. Discuss its advantages and disadvantages, and provide an example of a problem that is naturally solved using recursion.",
                "context": "Recursion is a programming technique where a function calls itself to solve a problem. It's commonly used in tree traversal, divide-and-conquer algorithms, and problems with recursive structure like factorial or Fibonacci sequences.",
                "rubric": "Grading criteria: (1) Explanation of recursion concept - 25 points, (2) Advantages discussion - 20 points, (3) Disadvantages discussion - 20 points, (4) Appropriate example with explanation - 30 points, (5) Clarity and organization - 5 points. Total: 100 points."
            }
        }
        
        fallback = fallback_questions.get(question_number, fallback_questions[1])
        return GeneratedQuestion(
            question_text=fallback["question_text"],
            context=fallback["context"],
            rubric=fallback["rubric"]
        )

