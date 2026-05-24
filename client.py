import socket
import threading

# 1. Ask the user how they want to connect
print("--- Connection Setup ---")
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
    print("Invalid choice. Defaulting to local (127.0.0.1).")
    SERVER_IP = "127.0.0.1"

SERVER_PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

username = input("Enter your username: ")

# Send access request
client.sendto(
    f"REQUEST_ACCESS:{username}".encode("utf-8"), (SERVER_IP, SERVER_PORT)
)

print(f"Waiting for server approval at {SERVER_IP}:{SERVER_PORT}...")

try:
    response, _ = client.recvfrom(1024)
    response = response.decode("utf-8")
except Exception as e:
    print(f"Failed to connect to server: {e}")
    client.close()
    exit()

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
            data, _ = client.recvfrom(1024)
            # A small fix here: clear the line slightly for better formatting
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
        client.sendto("LEAVE".encode("utf-8"), (SERVER_IP, SERVER_PORT))
        break

    # Prevent sending empty messages
    if message.strip():
        client.sendto(message.encode("utf-8"), (SERVER_IP, SERVER_PORT))

client.close()
print("Disconnected.")