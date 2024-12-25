# import socket
from socket import *
import time


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
packetsACK = [False] * len(packets)
print("\n")

window_start = 0
start_time = time.time()
current_time = time.time() - start_time

window_moved = True

while window_start < len(packets):

    if window_moved:  # Send packets within the window
        for i in range(window_start, min(window_start + int(window_size), len(packets))):
            if i == 2:  # debug
                continue  # debug
            if not packetsACK[i]:  # Only send unacknowledged packets
                print(f"Sending packet {i}: {packets[i]}")
                clientSocket.send(packets[i].encode())  # Send the packet

                # Immediately receive the acknowledgment
                ack_from_server = clientSocket.recv(4096).decode()
                ack_number = int(ack_from_server[3:])  # Extract ACK number
                print(f"Received {ack_from_server}")
                packetsACK[ack_number] = True  # Mark the packet as acknowledged

    window_moved = False
    # Slide the window forward
    while window_start < len(packets) and packetsACK[window_start]:
        window_start += 1  # Slide window forward
        print(f"moving window to {window_start}")  #debug
        start_time = time.time()
        #print("new start time: " + str(start_time))
        window_moved = True

    current_time = time.time() - start_time
    # print("current time: " + str(current_time))

    # reached timeout and needs to send all the false packets
    if current_time >= float(timeout):
        for i in range(window_start, min(window_start + int(window_size), len(packets))):
            if not packetsACK[i]:
                print(f"Sending packet {i} again: {packets[i]}")
                clientSocket.send(packets[i].encode())  # Send the packet

                # Immediately receive the acknowledgment
                ack_from_server = clientSocket.recv(4096).decode()
                ack_number = int(ack_from_server[3:])  # Extract ACK number
                print(f"Received {ack_from_server}")
                for j in range(ack_number + 1):
                    packetsACK[j] = True  # Mark the packet as acknowledged

        start_time = time.time()

clientSocket.close()
