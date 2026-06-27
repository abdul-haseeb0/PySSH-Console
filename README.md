<div align="center">

# 🔐 PySSH Console

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/paramiko-powered-0A9EDC?style=flat-square" alt="paramiko">
  <img src="https://img.shields.io/badge/status-beta-F59E0B?style=flat-square" alt="Beta">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-0078D4?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/license-Open%20Source-22C55E?style=flat-square" alt="License">
</p>

<p align="center">
  A lightweight interactive SSH client in Python — connect, authenticate, and execute remote commands straight from your terminal.
</p>

</div>

---

## Overview

**PySSH Console** is a functional SSH client built with [`paramiko`](https://www.paramiko.org/). It establishes a real interactive shell session on a remote machine using `invoke_shell()` — giving you live, bidirectional communication with the server rather than just one-off command execution.

Designed for developers, students, and sysadmins who want a minimal, readable SSH client they can understand, extend, and make their own — without relying on PuTTY, OpenSSH, or any external SSH binary.

> Currently in **beta**. Core functionality is stable; additional features are actively being added.

---

## Features

| Feature | Description |
|---|---|
| 🔑 **Password Authentication** | Securely prompts for credentials using `getpass` — no plaintext passwords |
| 🖥️ **True Interactive Shell** | Opens a real PTY shell via `invoke_shell()` for bidirectional session handling |
| 📡 **Live Output Streaming** | Polls the channel with `recv_ready()` and streams output in real time |
| 🧹 **Clean Output Filtering** | Strips command echo and bare prompt lines from displayed output |
| ⏱️ **Connection Timeout** | Configurable 10-second timeout — fails fast on unreachable hosts |
| 🛑 **Graceful Exit** | Type `exit` or `quit` to cleanly close the channel and session |
| ⌨️ **Keyboard Interrupt Handling** | `Ctrl+C` exits the shell loop cleanly with a status message |
| ⚠️ **Advanced Error Handling** | Connection failures surface clear, descriptive error messages |
| 🔒 **Agent & Key Forwarding Disabled** | Explicit `look_for_keys=False`, `allow_agent=False` for controlled auth flow |

---

## Requirements

- **Python** 3.8+
- **pip**

Dependencies (`requirements.txt`):

```
paramiko
```

Install:

```bash
pip install -r requirements.txt
```

---

## Installation

```bash
git clone https://github.com/your-username/PySSH-Console.git
cd PySSH-Console
pip install -r requirements.txt
```

---

## Usage

```bash
python3 main.py
```

You will be prompted for connection details:

```
Welcome to PySSH Console (beta).

Host: 192.168.1.10
Username: john
Password:

Connecting to 192.168.1.10...
Connected Successfully to 192.168.1.10.
```

An interactive shell session starts immediately after:

```
[john@server]:~$ whoami
john
[john@server]:~$ ls /var/www
html  logs
[john@server]:~$ exit
Closing session...
```

Type `exit` or `quit` to close the session cleanly. Press `Ctrl+C` at any time to interrupt and exit.

---

## How It Works

PySSH Console uses `paramiko`'s `invoke_shell()` to open a true PTY-backed channel on the remote server — the same underlying mechanism used by full SSH clients. This means the remote machine sees a real terminal, not a scripted exec session.

**Connection flow:**

```
main.py
  │
  ├── Prompts for host / username / password
  ├── Calls connect() → ssh_client.py
  │     └── paramiko.SSHClient.connect() with timeout + strict auth flags
  │
  └── On success, calls shell() → terminal.py
        └── invoke_shell() → opens PTY channel
              ├── Initial banner / MOTD drained on connect
              ├── Input loop: reads command → channel.send()
              ├── Output loop: polls recv_ready() → filters and prints
              └── exit / quit / KeyboardInterrupt → channel.close()
```

---

## Project Structure

```
PySSH-Console/
│
├── main.py                  # Entry point — prompts, connects, launches shell
├── requirements.txt         # Python dependencies
├── README.md
├── LICENSE
│
├── pyssh/
│   ├── ssh_client.py        # SSH connection handler (paramiko client setup)
│   └── terminal.py          # Interactive shell loop (invoke_shell, I/O polling)
│
└── screenshots/
    └── ...                  # Terminal session screenshots
```

---

## Security Notice

> ⚠️ PySSH Console uses `AutoAddPolicy` for host key verification, meaning it **does not verify the remote server's identity**. This is intentional for lab and development use, but exposes you to **man-in-the-middle attacks** on untrusted networks.

**Safe usage guidelines:**

- Only connect to servers you own or explicitly trust
- Avoid use over public Wi-Fi or untrusted networks without a VPN
- Do not use in production environments where host integrity must be verified
- SSH key authentication (planned in roadmap) will improve this significantly

---

## Current Limitations

- Password authentication only — no SSH key support yet
- No custom port support (defaults to `22`)
- No known hosts verification
- No SFTP / file transfer capability
- Single session only — no multiplexing

---

## Roadmap

- [ ] SSH key-based authentication
- [ ] Custom port support (`-p` flag or prompt)
- [ ] Known hosts verification
- [ ] SFTP file transfer
- [ ] Config file support (`~/.pyssh/config`)

---

## Disclaimer

PySSH Console is intended for **educational and personal use only**. Always follow responsible security practices when connecting to remote servers. The author assumes no liability for misuse.

---

## License

This project is open source. See [`LICENSE`](./LICENSE) for details.
