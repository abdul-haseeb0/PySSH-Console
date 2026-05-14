import getpass
from pyssh.ssh_client import connect
from pyssh.terminal import shell

def main():
    print("Welcome to PySSH-Console (beta).")
    host = input("Host: ")
    userinfo = input("Username: ")
    password = getpass.getpass("Password: ")
    client = connect(host,userinfo,password)
    shell(client,userinfo)
    client.close()
main()