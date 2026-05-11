import paramiko
import getpass

def connect(host,username,password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host,username=username,password=password)
    return client

def shell(client):
    while True:
        command = input("ssh>")
        if command.lower() == "exit":
            break
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())

def main():
    host = input("Host: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    client = connect(host,username,password)
    shell(client)
    client.close()
main()