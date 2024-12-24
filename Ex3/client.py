# import socket
from socket import *

def split_message(message, max_size):
    message_bytes = message.encode()  # Encode the message in UTF-8
    result = []  # Array to store the split parts

    # Iterate through the message in chunks of max_size
    for i in range(0, len(message_bytes), max_size - 3):
        chunk = message_bytes[i:i + (max_size - 3)]  # Get the chunk of max_size or smaller
        packet_number = f"M{i // (max_size - 3)}-"  # Format packet number
        packet = f"{packet_number}{chunk.decode('utf-8', errors='ignore')}"  # Combine packet number and chunk
        result.append(packet)  # Decode and add to the result
    return result


def read_input_from_file(file_path):
    params = {}
    with open(file_path, 'r', encoding='utf-8') as file:  # Open the file
        for line in file:
            key, value = line.split(":", 1)  # Split each line into key and value
            params[key.strip()] = value.strip()  # Remove any extra whitespace

    # Extract values and return them in the correct types
    return (
        params["message"],
        int(params["maximum_msg_size"]),
        int(params["window_size"]),
        int(params["timeout"])
    )


#----------------------------------------------------------------------------------


serverName = 'localhost'
serverPort = 13000
SERVER_ADDRESS = (serverName, serverPort)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(SERVER_ADDRESS)

# Input handling
file_mode = input("Do you want to read inputs from a file? (yes/no): ").strip().lower()
if file_mode == 'yes':
    file_path = input("Enter the file path: ").strip()
    message, max_msg_size, window_size, timeout = read_input_from_file(file_path)

    max_ask_server = "what is the maximum number of bytes you are willing to receive?"
    clientSocket.send(max_ask_server.encode())
    maximum_msg_size = int(clientSocket.recv(4096).decode())

    if maximum_msg_size != max_msg_size:
        print("Not the same max size")

else:
    max_ask_server = "what is the maximum number of bytes you are willing to receive?"
    clientSocket.send(max_ask_server.encode())

    maximum_msg_size = int(clientSocket.recv(4096).decode())
    print('Hi client, I\'m willing to receive:', str(maximum_msg_size) + " bytes")

    message = input('Input a massage: ')

    window_size = input('enter the window size: ')

    timeout = input('enter the timeout: ')

packets = split_message(message, maximum_msg_size)
packetsACK = [len(packets)]
print("\n")

for i in range(len(packets)):
    print(f"Packet {i}: \'{packets[i]}\'")
    clientSocket.send(packets[i].encode())  # Encode the packet before sending
    ack_from_server = clientSocket.recv(4096).decode()
    ack_number = int(ack_from_server[3:])  # Extract the number after "ACK"
    packetsACK[ack_number] = True
    print(ack_from_server)

clientSocket.close()
