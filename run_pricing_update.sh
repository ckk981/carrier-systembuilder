#!/bin/bash

# Clear any broken venv from previous attempts
if [ -d "venv" ]; then
    echo "Removing previous virtual environment to ensure a clean slate..."
    rm -rf venv
fi

echo "Creating new virtual environment..."
python3 -m venv venv

# Verify venv python exists
if [ ! -f "venv/bin/python3" ]; then
    echo "Error: Virtual environment creation failed."
    exit 1
fi

echo "Installing dependencies using local venv pip..."
# Use explicit path to ensure we don't accidentally use system pip
./venv/bin/pip install selenium webdriver-manager

echo "Starting Pricing Scraper..."
# Use explicit path to python
./venv/bin/python3 update_prices.py

echo "Updating Expanded Equipment List..."
python3 expand_equipment.py

echo "Updating Index HTML..."
python3 update_index_equipment.py

echo "Done! Refresh the application to see the new prices."
