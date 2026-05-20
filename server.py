import socket

HOST = "0.0.0.0"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

approved_clients = {}

print(f"UDP Chat Server running on {HOST}:{PORT}")
print("Waiting for clients...\n")

while True:
    data, address = server.recvfrom(1024)
    message = data.decode("utf-8")

    if message.startswith("REQUEST_ACCESS:"):
        username = message.split(":", 1)[1]

        print(f"\nAccess request from {username} at {address}")
        choice = input(f"Allow {username} to join chat room? (y/n): ")

        if choice.lower() == "y":
            approved_clients[address] = username
            server.sendto("ACCESS_GRANTED".encode("utf-8"), address)

            print(f"{username} has been allowed.")

            join_message = f"[SERVER] {username} joined the chat room"
            for client_address in approved_clients:
                server.sendto(join_message.encode("utf-8"), client_address)

        else:
            server.sendto("ACCESS_DENIED".encode("utf-8"), address)
            print(f"{username} has been denied.")

    elif message == "LEAVE":
        if address in approved_clients:
            username = approved_clients[address]
            del approved_clients[address]

            leave_message = f"[SERVER] {username} left the chat room"
            print(leave_message)

            for client_address in approved_clients:
                server.sendto(leave_message.encode("utf-8"), client_address)

    else:
        if address not in approved_clients:
            server.sendto(
                "ACCESS_DENIED:You have not been allowed by the server".encode("utf-8"),
                address
            )
            continue

        username = approved_clients[address]
        chat_message = f"{username}: {message}"

        print(chat_message)

        for client_address in approved_clients:
            if client_address != address:
                server.sendto(chat_message.encode("utf-8"), client_address)