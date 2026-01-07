# Quick Start Guide

## Prerequisites

- Python 3.9 or higher
- pip package manager

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -e .
   ```

2. **Set up environment variables:**
   - Copy `.env.example` to `.env` (if you can create it)
   - Or set environment variables directly:
     ```bash
     # Windows PowerShell
     $env:TOGETHER_API_KEY="your_api_key_here"
     $env:DATABASE_URL="sqlite:///./exam_grader.db"
     
     # Linux/Mac
     export TOGETHER_API_KEY="your_api_key_here"
     export DATABASE_URL="sqlite:///./exam_grader.db"
     ```

3. **Initialize the database:**
   ```bash
   python -m app.db.init_db
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```
   Or:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the application:**
   - Open your browser to `http://localhost:8000`
   - Enter a username to start an exam
   - Answer the generated questions
   - View your final grade at the end

## Important Notes

- Make sure you have a valid Together.ai API key
- The database file (`exam_grader.db`) will be created automatically in the project root
- All prompt templates are in the `prompts/` directory
- The application generates 3 questions by default (configurable in settings)

## Troubleshooting

- If you get import errors, make sure you've installed the dependencies with `pip install -e .`
- If the LLM API fails, check that your API key is correct and that you have API credits
- If questions don't generate, check the console logs for errors - the app will use fallback questions if the LLM fails

