# Team Setup Guide - AI Oral Exam Grader POC

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ai-oral-exam-grader
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

3. **Initialize the database:**
   ```bash
   python -m app.db.init_db
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Open your browser:**
   - Go to: http://localhost:8000
   - Enter any username (e.g., "test_user")
   - Start taking the exam!

**That's it!** The app works immediately in demo mode - no API keys needed.

---

## 📋 What You Get

### Demo Mode (Default - No Setup Required)
- ✅ 3 pre-written questions:
  - Question 1: Data Structures (arrays vs linked lists)
  - Question 2: Algorithm Complexity (Big O notation)
  - Question 3: Recursion
- ✅ Basic grading based on answer length
- ✅ Full workflow: Login → Questions → Answers → Grading → Results
- ✅ Perfect for demos and testing

### Full AI Mode (Optional - Requires API Key)
- 🤖 AI-generated questions
- 🤖 AI-powered grading with detailed feedback
- 🤖 Intelligent final grade calculation

See `API_KEY_GUIDE.md` for AI setup instructions.

---

## 🔧 Troubleshooting

### Common Issues

**Problem: `ModuleNotFoundError`**
```bash
# Solution: Reinstall dependencies
pip install -e .
```

**Problem: Port 8000 already in use**
```bash
# Solution 1: Stop the app using port 8000
# Solution 2: Change port in run.py
```

**Problem: Database errors**
```bash
# Solution: Delete and recreate database
rm exam_grader.db  # or del exam_grader.db on Windows
python -m app.db.init_db
```

**Problem: Import errors**
```bash
# Solution: Make sure you're in the project directory
cd ai-oral-exam-grader
pip install -e .
```

---

## 📁 Project Structure

```
ai-oral-exam-grader/
├── app/                 # Main application code
│   ├── api/            # API routes
│   ├── core/           # Core logic (LLM, grading)
│   ├── db/             # Database models and setup
│   ├── services/       # Business logic
│   ├── templates/      # HTML templates
│   └── static/         # CSS and static files
├── prompts/            # LLM prompt templates
├── pyproject.toml      # Python dependencies
└── run.py             # Application entry point
```

---

## 🎯 Testing the Demo

1. **Start the server:**
   ```bash
   python run.py
   ```

2. **In your browser:**
   - Go to http://localhost:8000
   - Enter username: "demo_student"
   - Click "Start Exam"

3. **Complete the exam:**
   - Answer Question 1 (about data structures)
   - Answer Question 2 (about Big O notation)
   - Answer Question 3 (about recursion)
   - View your final grade and feedback

---

## 📚 Additional Resources

- `README.md` - Project overview and architecture
- `API_KEY_GUIDE.md` - How to enable AI features (optional)
- `QUICKSTART.md` - Quick reference guide

---

## 💡 Tips for Team Members

1. **Development:**
   - The app auto-reloads when you save files (with `--reload` flag)
   - Database file: `exam_grader.db` (SQLite - no server needed)
   - Logs appear in the terminal where you run `python run.py`

2. **Testing:**
   - Each exam creates a new database entry
   - You can use any username - no authentication required for POC
   - Database persists between runs

3. **Customization:**
   - Questions: Edit `app/core/grading/generator.py` → `_get_fallback_question()`
   - Styling: Edit `app/static/styles.css`
   - Number of questions: Edit `app/settings.py` → `exam_question_count`

---

## 🆘 Need Help?

- Check the troubleshooting section above
- Review `README.md` for architecture details
- Ask your team lead if stuck

---

**Happy coding! 🎉**

