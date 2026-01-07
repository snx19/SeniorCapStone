"""Guardrails for validating LLM responses."""
from typing import Type, TypeVar, Optional
from pydantic import BaseModel, ValidationError
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)


def validate_response(response_dict: dict, schema: Type[T]) -> Optional[T]:
    """Validate LLM response against a Pydantic schema."""
    try:
        return schema(**response_dict)
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        logger.error(f"Response dict: {response_dict}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during validation: {e}")
        return None

