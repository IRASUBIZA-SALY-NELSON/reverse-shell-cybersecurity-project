#!/usr/bin/env python3
"""
Rwanda Coding Academy - Cybersecurity Assignment
Comprehensive Cleanup Tool
Removes all persistence mechanisms and traces
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def detect_os():
    system = platform.system().lower()
    if "linux" in system:
        return "linux"
    elif "windows" in system:
        return "windows"
    elif "darwin" in system:
        return "macos"
    else:
        return "unknown"

def cleanup_persistence():
    """Remove all persistence mechanisms completely"""
    os_type = detect_os()
    home = Path.home()

    print(f"🧹 Starting comprehensive cleanup for {os_type.upper()}...")
    print("=" * 60)

    removed_items = []

    # Linux/Mac cleanup
    if os_type in ["linux", "macos"]:
        try:
            # Remove crontab entries
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                filtered_lines = []
                for line in lines:
                    if not any(keyword in line.lower() for keyword in ['guessing_game', 'reverse_game', 'python3']):
                        filtered_lines.append(line)

                if len(filtered_lines) != len(lines):
                    new_crontab = '\n'.join(filtered_lines)
                    subprocess.run(['crontab', '-'], input=new_crontab, text=True)
                    removed_items.append("Crontab persistence entries")

        except Exception as e:
            print(f"⚠️  Crontab cleanup: {e}")

    # Windows cleanup
    elif os_type == "windows":
        try:
            # Remove startup scripts
            startup_paths = [
                os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup\\game.bat'),
                os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup\\reverse_game.bat'),
                os.path.join(os.getenv('PROGRAMDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\game.bat'),
            ]

            for startup_path in startup_paths:
                if os.path.exists(startup_path):
                    os.remove(startup_path)
                    removed_items.append(f"Startup script: {startup_path}")

        except Exception as e:
            print(f"⚠️  Windows startup cleanup: {e}")

    # Remove game files
    game_files = [
        home / "guessing_game.py",
        home / "reverse_game.py",
        home / "game.py",
        Path.cwd() / "guessing_game.py",
        Path.cwd() / "reverse_game.py",
    ]

    for game_file in game_files:
        if game_file.exists():
            try:
                game_file.unlink()
                removed_items.append(f"Game file: {game_file}")
            except PermissionError:
                print(f"⚠️  Cannot remove {game_file} (permission denied)")

    # Kill processes
    try:
        if os_type == "windows":
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True)
            subprocess.run(['taskkill', '/f', '/im', 'pythonw.exe'], capture_output=True)
        else:
            subprocess.run(['pkill', '-f', 'guessing_game'], capture_output=True)
            subprocess.run(['pkill', '-f', 'reverse_game'], capture_output=True)
        removed_items.append("Related processes")
    except:
        pass

    # Summary
    print("\n✅ CLEANUP SUMMARY:")
    print("=" * 60)
    if removed_items:
        for item in removed_items:
            print(f"  �️  Removed: {item}")
    else:
        print("  ℹ️  No persistence items found")

    print("\n🔒 System is now clean!")
    print("🎓 Rwanda Coding Academy - Cybersecurity Assignment")
    print("   Educational cleanup completed successfully")

if __name__ == "__main__":
    print("🎓 RWANDA CODING ACADEMY - CYBERSECURITY CLEANUP TOOL")
    print("This tool removes all persistence mechanisms from the educational demo")
    print()

    response = input("Do you want to proceed with cleanup? (y/N): ").lower().strip()
    if response in ['y', 'yes']:
        cleanup_persistence()
    else:
        print("Cleanup cancelled. No changes made.")
