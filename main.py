import getpass
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from pathlib import Path

from pyssh.ssh_client import connect
from pyssh.terminal import InteractiveShell

from colorama import Fore, Style, init

init(autoreset=True)


def init_logging():
    log_dir = Path.home() / ".pyssh_logs"
    log_dir.mkdir(exist_ok=True)

    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    session_logger = logging.getLogger()
    session_logger.setLevel(logging.INFO)

    session_handler = RotatingFileHandler(log_dir / "pyssh.log", maxBytes=5 * 1024 * 1024, backupCount=5)
    session_handler.setFormatter(formatter)
    session_logger.addHandler(session_handler)

    audit_logger = logging.getLogger("pyssh.audit")
    audit_logger.setLevel(logging.INFO)
    audit_handler = RotatingFileHandler(log_dir / "audit.log", maxBytes=5 * 1024 * 1024, backupCount=5)
    audit_handler.setFormatter(formatter)
    audit_logger.addHandler(audit_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)
    session_logger.addHandler(console_handler)


def main():
    init_logging()
    logger = logging.getLogger(__name__)

    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        ██████╗ ██╗   ██╗███████╗███████╗██╗  ██╗          ║
    ║        ██╔══██╗╚██╗ ██╔╝██╔════╝██╔════╝██║  ██║          ║
    ║        ██████╔╝ ╚████╔╝ ███████╗███████╗███████║          ║
    ║        ██╔═══╝   ╚██╔╝  ╚════██║╚════██║██╔══██║          ║
    ║        ██║        ██║   ███████║███████║██║  ██║          ║
    ║        ╚═╝        ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝          ║
    ║                                                           ║
    ║              Professional SSH Console v1.0                ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """

    print(Fore.LIGHTMAGENTA_EX + banner + Style.RESET_ALL)
    print(Fore.GREEN + "Welcome to the PySSH Console." + Style.RESET_ALL)
    print(Fore.YELLOW + "Secure | Auditable | Cross-Platform" + Style.RESET_ALL)
    print()

    host = input("Host: ")
    userinfo = input("Username: ")
    password = getpass.getpass("Password: ")

    client = None
    try:
        print(f"\nConnecting to {host}...")
        client = connect(host, userinfo, password)
        print(Fore.GREEN + "Connected. Initiating PTY..." + Style.RESET_ALL)
        logger.info(f"Session started for {userinfo}@{host}")

        channel = client.invoke_shell()
        shell = InteractiveShell(channel)
        shell.start()

    except KeyboardInterrupt:
        print("\n\033[93mSession interrupted.\033[0m")
        logger.warning("Session interrupted by user.")
    except (ConnectionError, OSError) as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        if client:
            client.close()
            logger.info("SSH client closed.")
        print("Goodbye.")


if __name__ == "__main__":
    main()