#!/bin/bash

# discord message fetcher - setup and run script
# this script handles virtual environment setup, dependency installation, and execution

set -e  # exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # no color

echo "================================================================================"
echo "Discord Message Fetcher - Setup & Run"
echo "================================================================================"

# check if python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 found: $(python3 --version)"

# check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠${NC} .env file not found"
    
    if [ -f ".env.example" ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo -e "${YELLOW}⚠${NC} Please edit .env file and add your DISCORD_TOKEN and CHANNEL_ID"
        echo "Then run this script again."
        exit 1
    else
        echo -e "${RED}Error: .env.example not found${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✓${NC} .env file found"

# create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment exists"
fi

# activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# install/upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt > /dev/null 2>&1
    echo -e "${GREEN}✓${NC} Dependencies installed"
else
    echo -e "${RED}Error: requirements.txt not found${NC}"
    exit 1
fi

echo ""
echo "================================================================================"
echo "Starting Discord Message Fetcher..."
echo "================================================================================"
echo ""

# run the main script with all passed arguments
python3 main.py "$@"

# deactivate virtual environment
deactivate
