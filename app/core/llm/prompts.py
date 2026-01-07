"""Prompt template loading and formatting."""
from pathlib import Path
from typing import Dict


PROMPTS_DIR = Path(__file__).parent.parent.parent.parent / "prompts"


def load_prompt(filename: str) -> str:
    """Load a prompt template from file."""
    prompt_path = PROMPTS_DIR / filename
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8").strip()


def format_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with provided variables."""
    return template.format(**kwargs)

