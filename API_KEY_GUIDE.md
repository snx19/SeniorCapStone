# API Key Guide - What You Need to Run the App

## TL;DR - Quick Answer

**You DON'T need an API key to run the basic demo!** The app works right now without one.

However, **if you want AI-generated questions and AI grading**, you'll need a Together.ai API key.

---

## Two Modes of Operation

### Mode 1: Demo Mode (No API Key Required) ✅ **YOU ARE HERE**

**What you have NOW:**
- ✅ App runs and works perfectly
- ✅ 3 pre-written questions (different for each question)
  - Question 1: Data Structures (arrays vs linked lists)
  - Question 2: Algorithm Complexity (Big O notation)
  - Question 3: Recursion
- ✅ Basic grading (based on answer length)
- ✅ All features work: login, questions, answers, grading, final results
- ✅ Perfect for demos and testing

**Limitations:**
- Questions are fixed (not AI-generated)
- Grading is simple (length-based, not AI-evaluated)

---

### Mode 2: Full AI Mode (API Key Required)

**What you get WITH an API key:**
- ✅ AI-generated questions (unique each time, tailored to topics)
- ✅ AI-powered grading with detailed feedback
- ✅ Intelligent final grade calculation with explanations
- ✅ More sophisticated evaluation

**Requirements:**
- Together.ai API key (free tier available)
- Internet connection for API calls

---

## How to Get a Together.ai API Key (Optional)

If you want the full AI-powered experience:

1. **Sign up at Together.ai:**
   - Go to: https://together.ai/
   - Create a free account
   - Navigate to API keys section

2. **Get your API key:**
   - Copy your API key from the dashboard
   - Free tier usually includes credits to get started

3. **Set up the API key:**

   **Option A: Environment Variable (Recommended)**
   ```powershell
   # Windows PowerShell (current session only)
   $env:TOGETHER_API_KEY="your_api_key_here"
   ```

   **Option B: Create .env file (Persistent)**
   ```bash
   # Create a file named .env in the project root
   TOGETHER_API_KEY=your_api_key_here
   DATABASE_URL=sqlite:///./exam_grader.db
   ```

4. **Restart the server:**
   ```bash
   python run.py
   ```

---

## Current Setup Status

**You currently have:**
- ✅ Python dependencies installed
- ✅ Database initialized
- ✅ Server running
- ✅ App working in demo mode

**You DON'T need to do anything else unless you want AI features!**

---

## Testing Both Modes

### Test Demo Mode (Current):
1. Just use the app as-is: http://localhost:8000
2. Everything works without any API key

### Test AI Mode (Optional):
1. Get Together.ai API key
2. Set it as environment variable or in .env file
3. Restart server
4. Questions and grading will now use AI

---

## Summary

- **For demos/tests:** No API key needed ✅
- **For production/AI features:** API key recommended
- **The app works perfectly in both modes!**

The current setup is perfect for demonstrating the concept. You can always add an API key later if you want the AI features.

