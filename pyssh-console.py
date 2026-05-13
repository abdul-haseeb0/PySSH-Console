import paramiko
import getpass

def connect(host, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(
            hostname=host,
            username=username,
            password=password,
            timeout=10,
            look_for_keys=False,
            allow_agent=False
        )

        return client

    except Exception as e:
        print("Connection failed:", e)
        exit()

def shell(client,userinfo):
    while True:
        command = input(f"[{userinfo}@Pyssh]:~$ ")
        if command.lower() == "exit":
            break
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())

def main():
    print("Welcome to PySSH-Console (beta).")
    host = input("Host: ")
    userinfo = input("Username: ")
    password = getpass.getpass("Password: ")
    client = connect(host,userinfo,password)
    shell(client,userinfo)
    client.close()
main()