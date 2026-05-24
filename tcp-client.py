import socket
import threading

print("--- TCP Connection Setup ---")
print("1. Same PC (Localhost)")
print("2. Another Device (Local Network)")
choice = input("Select connection type (1 or 2): ").strip()

if choice == "1":
    SERVER_IP = "127.0.0.1"
elif choice == "2":
    SERVER_IP = input(
        "Enter the Server's Local IP address (e.g., 192.168.1.X): "
    ).strip()
else:
    SERVER_IP = "127.0.0.1"

SERVER_PORT = 9999

# SOCK_STREAM initializes a TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

username = input("Enter your username: ")

try:
    # This line triggers the initial 3-way handshake in Wireshark!
    client.connect((SERVER_IP, SERVER_PORT))
except Exception as e:
    print(f"Could not establish a physical TCP connection to the server: {e}")
    exit()

# Once connected, we send the initial payload
client.send(f"REQUEST_ACCESS:{username}".encode("utf-8"))
print(f"Waiting for server approval at {SERVER_IP}:{SERVER_PORT}...")

response = client.recv(1024).decode("utf-8")

if response.startswith("ACCESS_DENIED"):
    print(f"Access denied by server. Reason: {response}")
    client.close()
    exit()

if response == "ACCESS_GRANTED":
    print("Access granted.")
    print("Connected to chat room.")
    print("Type /quit to leave.\n")


def receive_messages():
    while True:
        try:
            # We don't need recvfrom() because this socket pipe is tied directly to the server
            data = client.recv(1024)
            if not data:
                print("\nServer shut down the connection.")
                break
            print(f"\r{data.decode('utf-8')}\nYou: ", end="")
        except:
            break


thread = threading.Thread(target=receive_messages)
thread.daemon = True
thread.start()

while True:
    try:
        message = input("You: ")
    except (KeyboardInterrupt, EOFError):
        message = "/quit"

    if message.lower() == "/quit":
        client.send("LEAVE".encode("utf-8"))
        break

    if message.strip():
        # Using simple send() instead of sendto() because the destination is already locked in
        client.send(message.encode("utf-8"))

# Closing the socket gracefully handles the TCP teardown (FIN/ACK sequence)
client.close()
print("Disconnected.")