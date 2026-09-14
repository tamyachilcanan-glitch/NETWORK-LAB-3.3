import socket                                      # TCP socket communication
import json                                        # JSON parsing and serialization
import logging                                     # Server logging

HOST = "0.0.0.0"                                   # Listen on all network interfaces
PORT = 12345                                       # Server port

# Configure server log
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def handle_request(data):                          # Process one client request
    try:
        payload = json.loads(data)                 # Convert JSON string into dictionary

        a = payload.get("a")                       # Get first value
        b = payload.get("b")                       # Get second value
        operation = payload.get("operation")       # Get requested operation

        # TODO 1: Check if any required parameter is missing
        if a is None or b is None or operation is None:
            return {"error": "Missing parameters", "code": 400}

        # TODO 2: Validate that a and b are valid numbers
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            return {"error": "Invalid input", "code": 422}

        # TODO 3: Implement the supported operations
        if operation == "add":
            return {"result": a + b, "code": 200}

        elif operation == "sub":
            return {"result": a - b, "code": 200}

        elif operation == "mul":
            return {"result": a * b, "code": 200}

        elif operation == "div":

            # TODO 4: Handle division by zero
            if b == 0:
                return {"error": "Division by zero", "code": 422}

            return {"result": a / b, "code": 200}

        # TODO 5: Handle unsupported operations
        else:
            return {"error": "Invalid operation", "code": 400}

    except json.JSONDecodeError:
        # TODO 6: Return an appropriate error for invalid JSON
        return {"error": "Invalid JSON", "code": 400}

    except Exception:
        return {"error": "Server error", "code": 500}


# Create TCP socket
server_socket = socket.socket()                    # Create IPv4 TCP socket

server_socket.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server_socket.bind((HOST, PORT))                   # Bind socket to IP and port
server_socket.listen(5)                            # Start listening for connections

print(f"Calculator server running on {HOST}:{PORT}")


while True:                                        # Keep server running

    conn, addr = server_socket.accept()            # Accept incoming connection

    print(f"Connection from {addr}")               # Display client address

    data = conn.recv(1024).decode()                # Receive client data

    response = handle_request(data)                # Process request on server

    # Information for logging
    client_ip = addr[0]
    server_ip = conn.getsockname()[0]

    try:
        payload = json.loads(data)

        a = payload.get("a")
        b = payload.get("b")
        operation = payload.get("operation")

    except json.JSONDecodeError:
        a = "N/A"
        b = "N/A"
        operation = "N/A"

    # Build log information
    if "result" in response:
        result_text = f"Result: {response['result']}"
    else:
        result_text = f"Error: {response['error']}"

    log_message = (
        f"Client IP: {client_ip} | "
        f"Server IP: {server_ip} | "
        f"Operation: {operation} | "
        f"a: {a} | "
        f"b: {b} | "
        f"{result_text} | "
        f"Code: {response['code']}"
    )

    print(log_message)                             # Show log on server
    logging.info(log_message)                      # Save log in server.log

    response_json = json.dumps(response)           # Convert response to JSON

    conn.send(response_json.encode())              # Send response to client

    conn.close()                                   # Close client connection
