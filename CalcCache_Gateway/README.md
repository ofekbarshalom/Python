# Exercise 2 in computer network course - Application Layer Communication using Python

This project implements an application layer communication protocol using Python sockets. It includes a server, a proxy, and a client that communicate using a custom protocol. The server performs calculations, while the proxy handles caching of responses to reduce redundant requests.

## Files in the Project

- **`server.py`**: Implements the server logic, processes client requests, performs calculations, and sends responses.
- **`proxy.py`**: Acts as a middle layer between the client and the server. It caches responses to improve performance and reduce redundant communication.
- **`client.py`**: Represents the client that sends requests to the server (via the proxy) and displays the results.
- **`api.py`**: Defines the custom protocol and utility functions used for communication.
- **`calculator.py`**: Contains the logic for mathematical expression evaluation.

## Requirements

- Python 3.8 or higher
- PyCharm (optional, for ease of development)
- Ensure you have the following libraries if additional dependencies exist.

## Running the Program

To run the program, you need to start the server, the proxy, and the client in separate terminal instances. Follow these steps:

### 1. Start the Server

Run the following command in the terminal:

```bash
python server.py --host 127.0.0.1 --port 9999
```

This starts the server on the local machine at port `9999`.

### 2. Start the Proxy

Run the following command in a different terminal:

```bash
python proxy.py --proxy_host 127.0.0.1 --proxy_port 8888 --server_host 127.0.0.1 --server_port 9999
```

This starts the proxy on the local machine at port `8888` and links it to the server at port `9999`.

### 3. Start the Client

Run the following command in another terminal:

```bash
python client.py --host 127.0.0.1 --port 8888
```

This starts the client and connects it to the proxy on port `8888`. The client allows you to select predefined mathematical expressions for calculation.

### 4. Interaction

The client will display a menu with predefined mathematical expressions. Select an expression by entering the corresponding number and press Enter. The result will be displayed along with the steps.

To exit the client, enter `0` and press Enter.

## Additional Notes

- **Caching Behavior**: The proxy caches responses. If the same request is sent again, the proxy returns the cached response without contacting the server.
- **Protocol**: The communication protocol is defined in `api.py`. It uses a custom header structure for transmitting requests and responses, as in TCP.
- **Debugging**: All errors and logs are printed in the respective terminals for easier debugging.

## Example Usage

1. Start the server.
2. Start the proxy.
3. Start the client.
4. Choose a calculation (e.g., option `1`) in the client.
5. View the result and steps in the client terminal.
6. Send the same request again to observe caching behavior in the proxy terminal.

## Authors

This project was developed as part of a university assignment in the Computer Networks course.

## License

This project is for educational purposes and should not be reused or distributed without permission.
