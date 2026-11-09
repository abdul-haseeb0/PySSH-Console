import paramiko
from paramiko.hostkeys import HostKeys
import logging
import hashlib
import base64
import socket
from pathlib import Path

logger = logging.getLogger(__name__)


class CustomHostKeyPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        digest = hashlib.sha256(key.asbytes()).digest()
        fingerprint = "SHA256:" + base64.b64encode(digest).decode('utf-8').rstrip('=')

        print(f"\n\033[93mThe authenticity of host '{hostname}' can't be established.\033[0m")
        print(f"Key fingerprint: {fingerprint}")
        response = input("Are you sure you want to continue connecting (yes/no)? ").strip().lower()

        if response == 'yes':
            ssh_dir = Path.home() / ".ssh"
            ssh_dir.mkdir(exist_ok=True)
            known_hosts_path = ssh_dir / "known_hosts"

            host_keys = HostKeys()
            if known_hosts_path.exists():
                host_keys.load(str(known_hosts_path))

            host_keys.add(hostname, key.get_name(), key)
            host_keys.save(str(known_hosts_path))
            logger.info(f"Host key for {hostname} accepted.")
            return

        raise paramiko.AuthenticationException(f"Host key verification failed for {hostname}.")


def connect(host, username, password, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(CustomHostKeyPolicy())

    known_hosts_path = Path.home() / ".ssh" / "known_hosts"
    if known_hosts_path.exists():
        client.load_host_keys(str(known_hosts_path))

    try:
        logger.info(f"Connecting to {host}:{port} as {username}")
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=10,
            look_for_keys=False,
            allow_agent=False
        )
        logger.info(f"Connected to {host}")
        return client
    except (paramiko.SSHException, paramiko.AuthenticationException, socket.timeout, OSError) as e:
        logger.error(f"SSH connection failed: {e}")
        raise ConnectionError(f"SSH connection failed: {e}")