#!/bin/bash

echo "🎓 Starting Alphabet Learning App..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python from https://python.org"
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found in current directory"
    exit 1
fi

# Run the application
echo "🚀 Launching the app..."
python3 main.py

# Check if there was an error
if [ $? -ne 0 ]; then
    echo
    echo "❌ An error occurred while running the app"
    read -p "Press Enter to continue..."
fi 