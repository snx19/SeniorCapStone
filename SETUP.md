# Setup Guide for Team Members

This guide will help you get the AI Oral Exam Grader running on your machine.

## Prerequisites

Before you begin, make sure you have:

- **Python 3.9 or higher** - Check with `python --version`
- **pip** - Python package manager (usually comes with Python)
- **Git** - For cloning the repository

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-oral-exam-grader
```

### 2. Install Dependencies

Install all required Python packages:

```bash
pip install -e .
```

This will install:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (database ORM)
- Pydantic (data validation)
- And other dependencies listed in `pyproject.toml`

### 3. Initialize the Database

Create the SQLite database and tables:

```bash
python -m app.db.init_db
```

You should see:
```
INFO - Creating database tables...
INFO - Database tables created successfully!
```

A file called `exam_grader.db` will be created in the project root.

### 4. Run the Application

Start the development server:

```bash
python run.py
```

Or:

```bash
uvicorn app.main:app --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 5. Access the Application

Open your web browser and navigate to:

```
http://localhost:8000
```

You should see the login page!

---

## Demo Mode vs. AI Mode

### Demo Mode (Default - No Setup Needed)

The app works **immediately** without any additional configuration:

- ✅ Pre-written questions (3 different questions)
- ✅ Basic grading (length-based evaluation)
- ✅ Full workflow: login → questions → answers → results
- ✅ Perfect for testing and demos

**No API key needed!**

### AI Mode (Optional)

To enable AI-generated questions and AI grading:

1. Get a free API key from [Together.ai](https://together.ai)
2. Set it as an environment variable:

   **Windows (PowerShell):**
   ```powershell
   $env:TOGETHER_API_KEY="your_api_key_here"
   ```

   **Windows (Command Prompt):**
   ```cmd
   set TOGETHER_API_KEY=your_api_key_here
   ```

   **Linux/Mac:**
   ```bash
   export TOGETHER_API_KEY="your_api_key_here"
   ```

3. Restart the server

See `API_KEY_GUIDE.md` for more details.

---

## Testing the Application

1. **Login:**
   - Enter any username (e.g., "test_student")
   - Click "Start Exam"

2. **Answer Questions:**
   - Read the question and context
   - Type your answer in the text box
   - Click "Submit Answer"
   - Repeat for all 3 questions

3. **View Results:**
   - After submitting all answers, you'll see your final grade
   - Review feedback for each question
   - See your overall performance summary

---

## Troubleshooting

### "Module not found" errors

**Solution:** Make sure you installed dependencies:
```bash
pip install -e .
```

### Port 8000 already in use

**Solution:** Either:
- Stop the other application using port 8000
- Or modify `run.py` to use a different port

### Database errors

**Solution:** Delete the database and reinitialize:
```bash
rm exam_grader.db  # Linux/Mac
del exam_grader.db  # Windows
python -m app.db.init_db
```

### Server won't start

**Solution:** Check that:
- Python 3.9+ is installed
- All dependencies are installed
- You're in the correct directory
- Port 8000 is available

---

## Project Structure

```
ai-oral-exam-grader/
├── app/              # Main application code
├── prompts/          # LLM prompt templates
├── run.py           # Quick start script
├── pyproject.toml   # Dependencies and project config
└── README.md        # Project overview
```

---

## Getting Help

If you run into issues:

1. Check the error messages in the terminal
2. Review this setup guide
3. Check `API_KEY_GUIDE.md` if using AI features
4. Ask your team lead

---

## Next Steps

Once you have the app running:

- Try different usernames to create multiple exam sessions
- Test the full exam workflow
- Explore the codebase to understand the architecture
- Check out the prompt templates in `prompts/` directory

Happy coding! 🚀

