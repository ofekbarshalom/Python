#import socket
from socket import *

SERVER_ADDRESS = ('', 13000)
MAX_MSG_SIZE = 4
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(SERVER_ADDRESS)
serverSocket.listen(1)

print("The server is ready to receive client")
connectionSocket, addrClient = serverSocket.accept()

sentence = connectionSocket.recv(4096).decode()
if sentence == "what is the maximum number of bytes you are willing to receive?":
    connectionSocket.send(bytes(str(MAX_MSG_SIZE).encode()))

packets_received = []

# Modified while loop to handle packets
while True:
    msg_from_client = connectionSocket.recv(MAX_MSG_SIZE)

    if not msg_from_client:  # Break when the client stops sending
        break

    decoded_msg = msg_from_client.decode()  # Decode the received message
    packets_received.append(decoded_msg)  # Store the received packet

    # Send an acknowledgment back to the client
    ack_message = "ACK"
    connectionSocket.send(ack_message.encode())

    # Print the received packet and its length
    print(f"Received packet: {decoded_msg}")
    print(f"Packet size: {len(msg_from_client)} bytes\n")

print("All packets received:", packets_received)

connectionSocket.close()
