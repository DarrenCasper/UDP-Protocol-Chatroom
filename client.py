import socket
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

username = input("Enter your username: ")

client.sendto(
    f"REQUEST_ACCESS:{username}".encode("utf-8"),
    (SERVER_IP, SERVER_PORT)
)

print("Waiting for server approval...")

response, _ = client.recvfrom(1024)
response = response.decode("utf-8")

if response == "ACCESS_DENIED":
    print("Access denied by server.")
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
            print("\n" + data.decode("utf-8"))
            print("You: ", end="")
        except:
            break


thread = threading.Thread(target=receive_messages)
thread.daemon = True
thread.start()

while True:
    message = input("You: ")

    if message.lower() == "/quit":
        client.sendto("LEAVE".encode("utf-8"), (SERVER_IP, SERVER_PORT))
        break

    client.sendto(message.encode("utf-8"), (SERVER_IP, SERVER_PORT))

client.close()
print("Disconnected.")