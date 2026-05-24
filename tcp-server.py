import socket
import threading

HOST = "0.0.0.0"
PORT = 9999

# SOCK_STREAM tells the OS to use TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()  # TCP requires the server to actively listen for incoming connection requests

approved_clients = {}  # In TCP, we store the active connection object, not just the address

print(f"TCP Chat Server running on {HOST}:{PORT}")
print("Waiting for clients...\n")


def handle_client(client_socket, address):
    """Handles the continuous stream of data for a specific connected client."""
    username = ""
    try:
        while True:
            # In TCP, we use recv() directly on the client's specific socket pipe
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode("utf-8")

            if message.startswith("REQUEST_ACCESS:"):
                username = message.split(":", 1)[1]
                print(f"\nAccess request from {username} at {address}")

                # Prompt the server admin for approval
                choice = input(f"Allow {username} to join chat room? (y/n): ")

                if choice.lower() == "y":
                    approved_clients[client_socket] = username
                    client_socket.send("ACCESS_GRANTED".encode("utf-8"))
                    print(f"{username} has been allowed.")

                    # Broadcast join message
                    join_msg = f"[SERVER] {username} joined the chat room"
                    for sock in approved_clients:
                        sock.send(join_msg.encode("utf-8"))
                else:
                    client_socket.send("ACCESS_DENIED".encode("utf-8"))
                    print(f"{username} has been denied.")
                    break  # Break out to close this specific connection

            elif message == "LEAVE":
                break  # Break out to trigger the cleanup block below

            else:
                # Regular chat message
                if client_socket not in approved_clients:
                    client_socket.send(
                        "ACCESS_DENIED:You have not been allowed by the server".encode(
                            "utf-8"
                        )
                    )
                    continue

                chat_message = f"{username}: {message}"
                print(chat_message)

                # Broadcast message to everyone else
                for sock in approved_clients:
                    if sock != client_socket:
                        sock.send(chat_message.encode("utf-8"))

    except ConnectionResetError:
        pass  # Handles sudden client disconnections cleanly
    finally:
        # Cleanup when client leaves or gets disconnected
        if client_socket in approved_clients:
            username = approved_clients[client_socket]
            del approved_clients[client_socket]
            leave_msg = f"[SERVER] {username} left the chat room"
            print(leave_msg)
            for sock in approved_clients:
                sock.send(leave_msg.encode("utf-8"))

        client_socket.close()


while True:
    # accept() blocks until a client completes the 3-Way Handshake
    client_socket, address = server.accept()
    # Spin up a thread so the server can handle multiple TCP connections simultaneously
    thread = threading.Thread(
        target=handle_client, args=(client_socket, address)
    )
    thread.start()