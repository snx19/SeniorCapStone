#!/bin/bash
# Setup script for Mac/Linux
# Run this script to set up the AI Oral Exam Grader

echo "========================================"
echo "AI Oral Exam Grader - Setup Script"
echo "========================================"
echo ""

# Check Python
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found! Please install Python 3.9+ first."
    exit 1
fi
python_version=$(python3 --version)
echo "  Found: $python_version"

# Install dependencies
echo ""
echo "[2/4] Installing dependencies..."
pip install -e .
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies!"
    exit 1
fi
echo "  Dependencies installed successfully!"

# Initialize database
echo ""
echo "[3/4] Initializing database..."
python3 -m app.db.init_db
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to initialize database!"
    exit 1
fi
echo "  Database initialized successfully!"

# Success message
echo ""
echo "[4/4] Setup complete!"
echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  python3 run.py"
echo ""
echo "Then open http://localhost:8000 in your browser"
echo ""
