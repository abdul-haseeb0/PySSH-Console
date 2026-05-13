PySSH Console (Beta)

PySSH Console is a simple interactive SSH client built in Python using the paramiko library. It allows users to securely connect to a remote server via SSH and execute shell commands directly from a terminal-like interface.

The program prompts for host credentials, establishes an SSH connection, and provides an interactive shell where commands can be executed in real time. It also handles basic error reporting and ensures a clean session flow with proper connection handling.

This project is currently in a development phase and is being gradually refactored from a single-script tool into a more structured and scalable Python application.

Features
Secure SSH connection using username and password
Interactive command execution shell
Basic error handling for connection failures
Clean session management with graceful exit support
Tech Stack
Python 3
Paramiko (SSH library)
Getpass (secure password input)

Usage
Run the script and enter your server credentials when prompted:

--> python pyssh.py

Then execute shell commands directly on the connected remote machine. Type exit to close the session.

Note!
This tool is intended for educational and personal use. Proper SSH security practices are recommended when using in real environments.
