"""Thresholds for grading decisions."""
from typing import Tuple


# Minimum grade threshold for considering a follow-up question
FOLLOWUP_THRESHOLD = 70.0

# Grade thresholds for quality assessment
EXCELLENT_THRESHOLD = 90.0
GOOD_THRESHOLD = 80.0
ACCEPTABLE_THRESHOLD = 70.0


def should_ask_followup(grade: float) -> bool:
    """Determine if a follow-up question should be asked based on grade."""
    return grade < FOLLOWUP_THRESHOLD


def get_grade_category(grade: float) -> str:
    """Get grade category description."""
    if grade >= EXCELLENT_THRESHOLD:
        return "Excellent"
    elif grade >= GOOD_THRESHOLD:
        return "Good"
    elif grade >= ACCEPTABLE_THRESHOLD:
        return "Acceptable"
    else:
        return "Needs Improvement"

