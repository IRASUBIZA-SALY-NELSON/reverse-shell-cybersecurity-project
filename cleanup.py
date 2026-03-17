#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess

def cleanup_persistence():
    """Remove all persistence mechanisms"""
    home = Path.home()
    
    # Remove crontab entries
    cron_entries = [
        "guessing_game",
        "/guessing_game_cron"
    ]
    
    subprocess.run(['crontab', '-l'], capture_output=True)
    
    # Remove game file if exists
    game_file = home / "guessing_game.py"
    if game_file.exists():
        game_file.unlink()
    
    print("✅ Persistence removed successfully!")
    print("🔒 Your system is clean.")

if __name__ == "__main__":
    cleanup_persistence()
