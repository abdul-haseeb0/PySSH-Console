def shell(client,userinfo):
    try:
        while True:

            command = input(f"[{userinfo}@Pyssh]:~$ ")

            if not command:
                continue

            if command.lower() in ["exit", "quit"]:
                print("Closing session...")
                break

            stdin, stdout, stderr = client.exec_command(command)

            print(stdout.read().decode())
            print(stderr.read().decode())


    except KeyboardInterrupt:
        print("\nSession interrupted. Exiting...")
