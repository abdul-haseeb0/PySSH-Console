def shell(client,userinfo):
    while True:
        command = input(f"[{userinfo}@Pyssh]:~$ ")
        if command.lower() == "exit":
            break
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())