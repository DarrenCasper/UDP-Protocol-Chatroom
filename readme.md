# UDP Chat Room with Server Access Control

This project is a simple chat room application using the UDP protocol. The system consists of one server and multiple clients. Each client can request access to join the chat room by sending a username to the server.

The server acts as the access controller. When a client sends an access request, the server manually decides whether the client is allowed to join the chat room or not. If the server approves the request, the client can send and receive messages in the chat room. If the request is denied, the client cannot access the chat room.

## Main Features

- Uses UDP protocol instead of TCP
- Supports multiple clients connected to one server
- Client sends a username when requesting access
- Server manually allows or denies client access
- Approved clients can send messages to the chat room
- Server broadcasts messages to other approved clients
- Unauthorized clients are rejected by the server

## How the System Works

The communication flow starts when a client sends an access request to the server using the following format:

```text
REQUEST_ACCESS:username