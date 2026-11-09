<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,100:0ea5e9&height=180&section=header&text=PySSH%20Console&fontSize=48&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=A%20modern%20SSH%20client%20for%20your%20terminal%2C%20written%20in%20Python&descAlignY=58&descSize=16" alt="PySSH Console" width="100%"/>

<p>
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/paramiko-powered-0A9EDC?style=for-the-badge" alt="paramiko">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-0078D4?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/status-beta-F59E0B?style=for-the-badge" alt="Beta">
</p>

**Connect, verify, and work on remote machines with a real PTY shell, without PuTTY or OpenSSH.**

[Features](#-features) · [Quick Start](#-quick-start) · [How It Works](#-how-it-works) · [Security](#-security) · [Logging](#-logging--auditing) · [Roadmap](#-roadmap)

</div>

---

## ✨ Overview

**PySSH Console** is a lightweight, cross-platform SSH client built on [`paramiko`](https://www.paramiko.org/). It opens a true PTY-backed shell and passes raw bytes straight through, so what you see is exactly what the server sends: full colors, UTF-8, and interactive apps like `vim`, `htop` and `tmux`.

It is built for developers, students and sysadmins who want an SSH client that is small, readable and easy to extend.

> 🚧 **Beta:** the core is stable and new features are being added regularly.

---

## 🚀 Features

### 🔒 Security
| | Feature | Description |
|---|---|---|
| 🛡️ | **Strict Host Key Verification** | A custom policy replaces `AutoAddPolicy` and verifies SHA256 fingerprints |
| 🕵️ | **MITM Protection** | Unknown hosts prompt you to verify the fingerprint before connecting |
| 💾 | **Known Hosts Persistence** | Verified keys are saved to `~/.ssh/known_hosts` for future sessions |

### 🖥️ Terminal Experience
| | Feature | Description |
|---|---|---|
| ⚡ | **Raw PTY Pass-Through** | No blocking I/O or hardcoded timeouts, so interaction is instant |
| 🎨 | **Full ANSI Color Support** | Raw byte streaming preserves 256-color themes and UTF-8 |
| 📝 | **Interactive Apps** | `vim`, `nano`, `htop` and `tmux` work as they do in a native terminal |
| ⌨️ | **Native Command History** | Arrow keys use the server's shell history instead of local emulation |
| 📐 | **Dynamic Resizing** | A `SIGWINCH` handler sends new window dimensions to the server |

### 🌍 Cross-Platform
| | Feature | Description |
|---|---|---|
| 🪟 | **Windows Support** | Uses `msvcrt` for keyboard input, since `termios` is unavailable |
| 🧵 | **Threaded I/O** | A background reader thread handles output where `select()` can't watch stdin |
| ↕️ | **Arrow Key Translation** | Windows scan codes are mapped to ANSI sequences so history works |
| 📁 | **Pathlib Integration** | Cross-platform handling of `~/.ssh` and log directories |

### 📋 Logging & Auditing
| | Feature | Description |
|---|---|---|
| 🔄 | **Rotating Log Files** | 5 MB max size with 5 backups, so logs can't fill your disk |
| 🧾 | **Dual Loggers** | `pyssh.log` for system events and `audit.log` for command auditing |
| ✍️ | **Command Buffering** | On Windows, complete commands are logged instead of keystrokes |
| 🕐 | **Structured Format** | Timestamps, log levels and consistent formatting |

### 🧱 Code Quality
| | Feature | Description |
|---|---|---|
| 🎯 | **Narrow Exception Handling** | Specific catches (`socket.error`, `OSError`, `paramiko.SSHException`) |
| ♻️ | **Terminal State Restoration** | `finally` blocks restore terminal settings even after a crash |
| 🔌 | **Graceful Disconnects** | Channels are closed properly, so no zombie sessions remain on the server |
| 📦 | **Proper Packaging** | A `pyssh/` package with `__init__.py` |

### 💅 UI
| | Feature | Description |
|---|---|---|
| 🌈 | **Color-Coded Output** | Green for success, red for errors, yellow for warnings |
| 💬 | **Clean Error Messages** | Friendly messages instead of raw stack traces |

---

## ⚡ Quick Start

**Requirements:** Python 3.8+ and pip.

```bash
git clone https://github.com/abdul-haseeb0/PySSH-Console.git
cd PySSH-Console
pip install -r requirements.txt
python3 main.py
```

You'll be prompted for connection details:

```text
Host: 192.168.1.10
Username: john
Password:
```

On first contact with an unknown host, you'll be asked to verify its fingerprint:

```text
The authenticity of host '192.168.1.10' can't be established.
SHA256 fingerprint: SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Trust this host and continue connecting? (yes/no):
```

Once you accept, the key is saved and the shell starts. Type `exit` or press `Ctrl+D` to close the session cleanly.

---

## 🧠 How It Works

```text
main.py
  │
  ├── Prompts for host / username / password (getpass)
  ├── connect() → pyssh/ssh_client.py
  │     └── Strict host key policy → verify SHA256 → persist to known_hosts
  │
  └── shell() → pyssh/terminal.py
        └── invoke_shell() → PTY channel
              ├── Linux/macOS: raw tty mode + select() on stdin/channel
              ├── Windows:     msvcrt input + background reader thread
              ├── SIGWINCH → resize_pty() on terminal resize
              └── finally: restore terminal state, close channel
```

---

## 🛡️ Security

PySSH Console verifies every server before authenticating.

- **Unknown host:** you see the SHA256 fingerprint and must confirm it
- **Known host:** the key is checked against `~/.ssh/known_hosts`
- **Changed key:** the connection is refused, which protects you from man-in-the-middle attacks

**Good practice:**
- Compare fingerprints with the server administrator on first connection
- Only connect to servers you own or trust
- Avoid untrusted networks without a VPN

---

## 📋 Logging & Auditing

Logs are written to a dedicated log directory and rotate automatically (5 MB × 5 backups).

| File | Purpose |
|---|---|
| `pyssh.log` | Connection events, errors and system activity |
| `audit.log` | Commands executed during sessions |

---

## 📁 Project Structure

```text
PySSH-Console/
├── main.py              # Entry point: banner, prompts, connect, launch shell
├── requirements.txt     # Dependencies
├── README.md
├── LICENSE
├── pyssh/
│   ├── __init__.py      # Package init and __version__
│   ├── ssh_client.py    # Connection handling and host key policy
│   └── terminal.py      # PTY pass-through, resize handling, logging
└── screenshots/
```

---

## ⚠️ Current Limitations

- Password authentication only (no SSH keys yet)
- Default port `22` only
- No SFTP / file transfer
- Single session only (no multiplexing)

---

## 🗺️ Roadmap

- [x] Known hosts verification
- [x] Windows support
- [x] Rotating logs and command auditing
- [x] Interactive app support (`vim`, `tmux`, `htop`)
- [ ] SSH key-based authentication
- [ ] Custom port support (`-p` flag or prompt)
- [ ] SFTP file transfer
- [ ] Config file support (`~/.pyssh/config`)

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push and open a Pull Request

Found a bug or have an idea? [Open an issue](https://github.com/abdul-haseeb0/PySSH-Console/issues).

---

## 📜 Disclaimer

PySSH Console is intended for **educational and personal use**. Follow responsible security practices when connecting to remote servers. The author assumes no liability for misuse.

---

## 📄 License

This project is open source. See [`LICENSE`](./LICENSE) for details.

---

<div align="center">

**Built with 🐍 Python and ☕ by [Abdul Haseeb](https://github.com/abdul-haseeb0)**

If PySSH Console helped you, consider giving it a ⭐

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0ea5e9,100:0f172a&height=100&section=footer" alt="footer" width="100%"/>

</div>
