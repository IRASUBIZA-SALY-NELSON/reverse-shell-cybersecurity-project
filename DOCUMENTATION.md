# 🎓 Rwanda Coding Academy - Cybersecurity Assignment
## Educational Backdoor Demonstration - Group Project

### 📋 Assignment Overview
This project demonstrates advanced cybersecurity concepts through an educational backdoor implementation. All activities are conducted with explicit user consent and for educational purposes only.

### 🎯 Grading Criteria (50 Points Total)

#### ✅ 1. Game Functionality (25 points)
- **User Notification (5 points)**: Comprehensive consent dialog explaining all features
- **Dependency Installation (5 points)**: Automatic checking and installation of required apps
- **Uninterrupted Gaming (10 points)**: Hidden C2 operations don't interfere with gameplay
- **Shell Access (10 points)**: Reliable reverse shell with full command execution

#### ✅ 2. Persistence & Security (5 points)
- Cross-platform persistence mechanisms:
  - **Linux/Mac**: Crontab entries
  - **Windows**: Startup folder scripts

#### ✅ 3. User Protection (5 points)
- Comprehensive cleanup tool that removes:
  - All persistence mechanisms
  - Game files and processes
  - Startup entries
  - Related processes

#### ✅ 4. Documentation (5 points)
- Complete technical documentation
- Ethical considerations
- Installation and usage instructions

#### ✅ 5. Innovation & Creativity (5 points)
- Hidden PowerShell execution
- Multi-session C2 management
- Cross-platform compatibility
- Educational transparency

---

## 🔧 Technical Implementation

### Core Components

#### 1. Main Game (`guessing_game.py`)
- **Number guessing game** as frontend distraction
- **Hidden C2 operations** running in background threads
- **Cross-platform reverse shell** implementation
- **Persistence mechanisms** for system reboot survival
- **Comprehensive consent system** with activity logging

#### 2. C2 Server (`listener.py`)
- **Dual-port management**: Shell (4444) + Notifications (4445)
- **Multi-session support** for multiple targets
- **Interactive shell interface** with command execution
- **Session tracking** and management

#### 3. Cleanup Tool (`cleanup.py`)
- **Complete persistence removal**
- **Process termination**
- **File cleanup**
- **User safety confirmation**

---

## 🚀 Installation & Usage

### For Presenters (C2 Operators)

1. **Start the listener:**
```bash
python3 listener.py
```

2. **Configure target IP:**
   - Update `C2_HOST` in `guessing_game.py` to your listener IP
   - Default ports: 4444 (shell), 4445 (notifications)

3. **Deploy game to targets:**
   - Copy `guessing_game.py` to target systems
   - Run with: `python guessing_game.py`

### For Target Users

1. **Run the game:**
```bash
python guessing_game.py
```

2. **Review consent dialog** - all features are disclosed
3. **Play the number guessing game** - C2 runs invisibly
4. **Use cleanup tool** when demo is complete:
```bash
python cleanup.py
```

---

## 🛡️ Security Features

### Ethical Safeguards
- **Explicit user consent** before any network activity
- **Educational purpose disclosure** in consent dialog
- **Activity logging** for transparency
- **Comprehensive cleanup** tool provided
- **No data exfiltration** or malicious behavior

### Technical Features
- **Hidden PowerShell execution** (Windows)
- **Cross-platform compatibility** (Windows/Linux/Mac)
- **Persistent C2 connections** with auto-reconnect
- **Multi-session management**
- **OS-native persistence**

---

## 📊 Demo Commands

Once connected, try these commands:
```bash
# System information
whoami
hostname
pwd

# File system
ls          # Linux/Mac
dir         # Windows

# Process management
ps          # Linux/Mac
tasklist    # Windows

# Network information
ipconfig    # Windows
ifconfig    # Linux/Mac
```

---

## ⚠️ Ethical Considerations

### Educational Purpose Only
- This tool is designed **exclusively for cybersecurity education**
- **Never use without explicit consent**
- **Only deploy in controlled environments**
- **Follow all institutional guidelines**

### Compliance Features
- **Full disclosure** of all capabilities
- **User consent logging**
- **Easy cleanup** mechanisms
- **No persistence after cleanup**
- **Educational branding** throughout

---

## 🎯 Presentation Tips

### Live Demo Steps
1. **Show consent dialog** - explain transparency
2. **Start listener** - show C2 server
3. **Deploy game** - demonstrate seamless operation
4. **Execute commands** - show shell access
5. **Demonstrate persistence** - reboot if possible
6. **Run cleanup** - show complete removal

### Key Talking Points
- **Educational transparency** vs malicious backdoors
- **Cross-platform capabilities**
- **Persistence mechanisms**
- **Ethical cybersecurity practices**
- **Real-world pentesting techniques**

---

## 🏆 Winning Features

This implementation exceeds requirements through:

1. **Superior User Experience**: Clean, professional interface
2. **Comprehensive Documentation**: Complete technical details
3. **Ethical Excellence**: Full transparency and consent
4. **Technical Innovation**: Hidden PowerShell, multi-session C2
5. **Cross-Platform Support**: Windows, Linux, Mac compatibility
6. **Professional Cleanup**: Complete system restoration

---

### 🎓 Rwanda Coding Academy - Defending Rwanda Cyberspace
*Educational Cybersecurity Demonstration*
