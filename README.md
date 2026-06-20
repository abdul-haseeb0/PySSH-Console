# PySSH Console

A lightweight interactive SSH client built in Python — connect to any remote server and execute shell commands straight from your terminal.

---

## What is PySSH Console?

PySSH Console is a simple yet functional SSH client written in Python using the `paramiko` library. It lets you connect to a remote machine via SSH using password authentication and interact with it through a live shell — all from your terminal, without needing a full SSH client like PuTTY or OpenSSH.

This project started as a single-script tool and is being gradually refactored into a clean, structured Python package.

---

## Features

- Password-based SSH authentication
- Interactive shell with real-time command execution
- Live output streaming from remote server
- Clean session handling with graceful exit
- Basic error reporting for failed connections
- Custom prompt displaying connected username

---

## Requirements

- Python 3.x
- [Paramiko](https://www.paramiko.org/)

Install dependencies:

```bash
pip install paramiko
```

---

## Usage

```bash
python3 main.py
```

You will be prompted for:

```
Host: 192.168.1.10
Username: john
Password: ********
```

Once connected, an interactive shell starts:

```
[john@PySSH]:~$ ls
[john@PySSH]:~$ cd /var/www
[john@PySSH]:~$ exit
```

Type `exit` or `quit` to close the session cleanly.

---

## Project Structure

```
PySSH-Console/
│
├── main.py              # Entry point
└── pyssh/
    ├── ssh_client.py    # SSH connection handler
    └── terminal.py      # Interactive shell loop
```

---

## Security Notice

> ⚠️ This tool uses `AutoAddPolicy` for host key verification, which means it **does not verify the remote server's identity**. This is acceptable for personal/lab use but is **not recommended for production environments** as it exposes you to man-in-the-middle attacks.

For secure usage:
- Only connect to servers you own or trust
- Avoid using over public/untrusted networks without a VPN

---

## Limitations

- Password authentication only (no SSH key support yet)
- No port forwarding
- No SFTP / file transfer
- No multi-session support

---

## Roadmap

- [ ] SSH key-based authentication
- [ ] Custom port support
- [ ] Known hosts verification
- [ ] SFTP file transfer
- [ ] Config file support (`~/.pyssh/config`)

---

## Disclaimer

This tool is intended for **educational and personal use only**. Always follow proper security practices when connecting to remote servers.
