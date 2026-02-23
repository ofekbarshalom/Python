# ReliableRelay - Sliding Window Communication Protocol in Python

This project implements a simplified reliable transport mechanism on top of TCP sockets using Python. It includes a client and a server that communicate with packet indexing, acknowledgments (ACK), sliding window transmission, and timeout-based retransmission.

## Files in the Project

- **`server.py`**: Implements the server logic, receives packets, tracks in-order delivery, and sends cumulative ACK responses.
- **`client.py`**: Splits messages into packets, sends them using a sliding window approach, handles ACKs, and retransmits packets on timeout.

## Core Features

- **Packet Segmentation**: The client splits long messages into numbered packets (`M0-`, `M1-`, ...).
- **UTF-8 Safe Splitting**: Packet chunking avoids breaking multi-byte UTF-8 characters.
- **Sliding Window**: Multiple packets can be in flight before waiting for the window to advance.
- **Cumulative ACKs**: The server acknowledges the highest contiguous packet received.
- **Timeout Retransmission**: Unacknowledged packets are resent when timeout is reached.
- **Interactive or File-Based Input**: Client parameters can be entered manually or loaded from a text file.

## Requirements

- Python 3.8 or higher
- No external libraries required (standard library only)

## Running the Program

To run the system, start the server and client in separate terminals.

### 1. Start the Server

Run the following command in the terminal:

```bash
python server.py
```

The server listens on port `13000`.

### 2. Start the Client

Run the following command in another terminal:

```bash
python client.py
```

The client connects to `localhost:13000`.

### 3. Choose Input Mode

When the client starts, choose one of the following:

- `yes` → load values from a file.
- `no` → enter values interactively.

If you choose file mode, provide a path to a text file with this format:

```text
message: your message here
maximum_msg_size: 8
window_size: 3
timeout: 2
```

If you choose interactive mode, the server asks for maximum packet size, then the client asks for:

- message
- window size
- timeout

## Example Flow

1. Start `server.py`.
2. Start `client.py`.
3. Enter client input values (file mode or interactive mode).
4. Client sends packets within the window.
5. Server sends ACKs (`ACK0`, `ACK1`, ...).
6. Client advances the window and retransmits on timeout if needed.
7. Server reconstructs and prints the full message.

## Additional Notes

- Packet header format is `M<packet_number>-<payload>`.
- Server prints each received packet and packet size for visibility/debugging.
- The implementation is educational and demonstrates reliable-delivery concepts such as ordering, acknowledgment, and retransmission.

## Authors

This project was developed as part of a university Computer Networks assignment.

## License

This project is for educational purposes.