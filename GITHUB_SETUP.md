# GitHub Repository Setup Guide

## Steps to Push to GitHub

### 1. Create a New Repository on GitHub

1. Go to https://github.com and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Repository name: `ai-oral-exam-grader` (or your preferred name)
4. Description: "AI-powered oral exam grading system - POC demo"
5. Choose **Public** or **Private**
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click **"Create repository"**

### 2. Push Your Code to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ai-oral-exam-grader.git

# Or if using SSH:
git remote add origin git@github.com:YOUR_USERNAME/ai-oral-exam-grader.git

# Stage all files
git add .

# Commit with a message
git commit -m "Initial commit: AI Oral Exam Grader POC"

# Push to GitHub (main branch)
git branch -M main
git push -u origin main
```

### 3. Verify on GitHub

1. Refresh your GitHub repository page
2. You should see all files uploaded
3. The README.md will display on the repository homepage

---

## Sharing with Your Team

### Option 1: Make Repository Public
- Anyone with the link can clone it
- Best for open projects

### Option 2: Add Team Members as Collaborators
1. Go to repository → **Settings** → **Collaborators**
2. Click **"Add people"**
3. Enter GitHub usernames or emails
4. They'll receive an invitation

### Option 3: Use GitHub Organizations
- Create an organization
- Add team members to the organization
- They'll have access to all org repositories

---

## What Your Team Will See

### Repository Structure
```
ai-oral-exam-grader/
├── README.md              # Project overview
├── TEAM_SETUP.md          # Setup instructions for team
├── API_KEY_GUIDE.md       # Optional AI features guide
├── setup.ps1              # Windows setup script
├── setup.sh               # Mac/Linux setup script
├── pyproject.toml         # Python dependencies
├── run.py                 # Application entry point
├── app/                   # Application code
├── prompts/               # LLM prompt templates
└── ...
```

### Key Files for Team
- **TEAM_SETUP.md** - Start here! Complete setup guide
- **README.md** - Project architecture and overview
- **setup.ps1 / setup.sh** - One-command setup scripts

---

## Team Members: How to Get Started

Your team members should:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-oral-exam-grader.git
   cd ai-oral-exam-grader
   ```

2. **Run the setup script:**
   - Windows: `.\setup.ps1`
   - Mac/Linux: `chmod +x setup.sh && ./setup.sh`

3. **Start the app:**
   ```bash
   python run.py
   ```

4. **Open browser:** http://localhost:8000

That's it! The app works immediately in demo mode.

---

## Best Practices

### .gitignore
✅ Already configured to exclude:
- Python cache files (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- Database files (`*.db`, `*.sqlite`)
- Environment files (`.env`)
- IDE files (`.vscode/`, `.idea/`)

### Commits
- Use descriptive commit messages
- Commit working code
- Don't commit `.env` files with API keys

### Branches (Optional)
```bash
# Create a feature branch
git checkout -b feature-name

# Work on features
# ...

# Merge back to main
git checkout main
git merge feature-name
```

---

## Troubleshooting

**Problem: "Repository not found"**
- Check repository URL is correct
- Verify you have access (for private repos)
- Try: `git remote -v` to check remote URL

**Problem: "Permission denied"**
- Make sure you're authenticated with GitHub
- Use `gh auth login` (GitHub CLI) or set up SSH keys

**Problem: Team members can't clone**
- Check repository visibility (public vs private)
- Add them as collaborators (for private repos)

---

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Push code
3. ✅ Share repository URL with team
4. ✅ Team clones and runs setup
5. 🎉 Everyone can demo the app!

---

**Need help?** Check GitHub documentation or ask your team lead.

