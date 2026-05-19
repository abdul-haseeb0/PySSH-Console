import time

def shell(client):
    try:
        channel = client.invoke_shell()

        deadline = time.time() + 3
        while time.time() < deadline:
            if channel.recv_ready():
                print(channel.recv(65535).decode(errors="ignore"), end="")
                break
            time.sleep(0.1)

        while True:
            command = input("")

            if not command:
                continue

            if command.lower() in ["exit", "quit"]:
                print("Closing session...")
                channel.close()
                break

            channel.send(command + "\n")

            deadline = time.time() + 5
            while time.time() < deadline:
                if channel.recv_ready():
                    time.sleep(0.2)
                    output = ""

                    while channel.recv_ready():
                        output += channel.recv(65535).decode(errors="ignore")

                    lines = output.splitlines()
                    filtered = [
                        l for l in lines
                        if l.strip()
                           and command.strip() not in l
                           and not l.strip().endswith("$")
                    ]
                    print("\n".join(filtered))
                    break
                time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nSession interrupted. Exiting...")