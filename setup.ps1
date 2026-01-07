# Setup script for Windows (PowerShell)
# Run this script to set up the AI Oral Exam Grader

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Oral Exam Grader - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found! Please install Python 3.9+ first." -ForegroundColor Red
    exit 1
}
Write-Host "  Found: $pythonVersion" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "[2/4] Installing dependencies..." -ForegroundColor Yellow
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies!" -ForegroundColor Red
    exit 1
}
Write-Host "  Dependencies installed successfully!" -ForegroundColor Green

# Initialize database
Write-Host ""
Write-Host "[3/4] Initializing database..." -ForegroundColor Yellow
python -m app.db.init_db
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to initialize database!" -ForegroundColor Red
    exit 1
}
Write-Host "  Database initialized successfully!" -ForegroundColor Green

# Success message
Write-Host ""
Write-Host "[4/4] Setup complete!" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "  python run.py" -ForegroundColor White
Write-Host ""
Write-Host "Then open http://localhost:8000 in your browser" -ForegroundColor Cyan
Write-Host ""
