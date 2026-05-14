import getpass
from pyssh.ssh_client import connect
from pyssh.terminal import shell

def main():
    print("Welcome to PySSH-Console (beta).\n")
    host = input("Host: ")
    userinfo = input("Username: ")
    password = getpass.getpass("Password: ")

    try:
        print("\nConnecting to " + host + "...")
        client = connect(host, userinfo, password)
        print("Connected Successfully to " + host + ".")
    except Exception as e:
        print(e)
        return

    shell(client,userinfo)
    client.close()
main()