#!/usr/bin/env python3
"""
Main entry point for the Lottery Analysis and Prediction System.
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from src.ui.lottery_app import run_app


if __name__ == "__main__":
    run_app()
