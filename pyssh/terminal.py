import sys
import os
import time
import select
import signal
import socket
import threading
import logging

logger = logging.getLogger(__name__)
audit_logger = logging.getLogger("pyssh.audit")

_HAS_SIGWINCH = hasattr(signal, "SIGWINCH")


def _reader(channel):
    while not channel.closed and not channel.eof_received:
        try:
            if channel.recv_ready():
                data = channel.recv(1024)
                if not data:
                    break
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
            else:
                time.sleep(0.01)
        except (socket.error, OSError, EOFError):
            logger.debug("reader stopped: channel closed")
            break


def _input_posix(channel):
    import tty
    import termios

    old = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())

    try:
        while not channel.closed and not channel.eof_received:
            r, _, _ = select.select([sys.stdin], [], [], 0.1)
            if sys.stdin in r:
                data = os.read(sys.stdin.fileno(), 1024)
                if not data:
                    break
                channel.sendall(data)
                audit_logger.info(data.decode("utf-8", errors="replace").strip())
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)


def _input_win(channel):
    import msvcrt

    keys = {"H": "\x1b[A", "P": "\x1b[B", "M": "\x1b[C", "K": "\x1b[D"}
    buffer = ""

    while not channel.closed and not channel.eof_received:
        if msvcrt.kbhit():
            ch = msvcrt.getwch()
            if ch in ("\x00", "\xe0"):
                data = keys.get(msvcrt.getwch(), "")
            elif ch in ("\r", "\n"):
                data = "\r"
                if buffer.strip():
                    audit_logger.info(buffer.strip())
                buffer = ""
            elif ch == "\x08":  # Backspace
                data = "\x08"
                buffer = buffer[:-1]
            else:
                data = ch
                buffer += ch

            if data:
                channel.sendall(data.encode("utf-8"))
        else:
            time.sleep(0.01)


class InteractiveShell:
    def __init__(self, channel):
        self.channel = channel

    def _resize(self, *_):
        try:
            cols, rows = os.get_terminal_size()
            self.channel.resize_pty(width=cols, height=rows)
        except (OSError, ValueError):
            logger.debug("resize skipped: no tty")

    def start(self):
        self._resize()
        if _HAS_SIGWINCH:
            signal.signal(signal.SIGWINCH, self._resize)

        threading.Thread(target=_reader, args=(self.channel,), daemon=True).start()

        try:
            if os.name == "nt":
                _input_win(self.channel)
            else:
                _input_posix(self.channel)
        except KeyboardInterrupt:
            pass
        finally:
            self.channel.close()
            print("\r\n\033[92mSession closed.\033[0m")