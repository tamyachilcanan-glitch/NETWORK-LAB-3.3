import socket                                      # TCP socket communication
import json                                        # JSON parsing and serialization
import logging                                     # Server logging

HOST = "0.0.0.0"                                   # Listen on all network interfaces
PORT = 12345                                       # Server port

# Configure server log

logging.basicConfig(            
    filename="server.log",                          # Save logs in server.log
    level=logging.INFO,                             # Save informational messages
    format="%(asctime)s - %(message)s"
)


def handle_request(data):                          # Process one client request
    try:
        payload = json.loads(data)                 # Convert JSON string into dictionary

        a = payload.get("a")                       # Get first value
        b = payload.get("b")                       # Get second value
        operation = payload.get("operation")       # Get requested operation

        # TODO 1: Check if any required parameter is missing or empty
        if (
            a is None or
            b is None or
            operation is None or
            a == "" or
            b == "" or
            operation == ""
        ):
            return {
                "error": "Missing parameters",                     # If it is missing, it returns code 400.
                "code": 400
            }

        # TODO 2: Validate that a and b are valid numbers
        # The dummy client sends what the user writes (text)
        # The SERVER performs the validation.
        try:
            a = float(a)                                             #The server converts them into numbers.
            b = float(b)

        except (ValueError, TypeError):                              #If it is not a number, the server returns “Invalid input”
            return {
                "error": "Invalid input",
                "code": 422
            }

        # TODO 3: Implement the supported operations
        if operation == "add":
            return {
                "result": a + b,
                "code": 200                                     # Valid operations
            }

        elif operation == "sub":
            return {
                "result": a - b,
                "code": 200
            }

        elif operation == "mul":
            return {
                "result": a * b,
                "code": 200
            }

        elif operation == "div":

            # TODO 4: Handle division by zero
            if b == 0:
                return {
                    "error": "Division by zero",
                    "code": 422
                }

            return {
                "result": a / b,
                "code": 200
            }

        # TODO 5: Handle unsupported operations
        else:
            return {
                "error": "Invalid operation",
                "code": 400
            }

    except json.JSONDecodeError:

        # TODO 6: Invalid JSON                            # Return error if received JSON is invalid
        return {
            "error": "Invalid JSON",
            "code": 400
        }

    except Exception:                                      # Handle unexpected server errors                                                       
        return {
            "error": "Server error",
            "code": 500
        }


# # Create the server socket
server_socket = socket.socket()                    # Create IPv4 TCP socket

server_socket.setsockopt(                          # Allow reuse of the same address and port
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server_socket.bind((HOST, PORT))                   # Bind socket to IP and port
server_socket.listen(5)                            # Start listening for connections

print(f"Calculator server running on {HOST}:{PORT}")        # Show that the server is running


while True:                                        # Keep server running

    conn, addr = server_socket.accept()            # Accept incoming connection

    print(f"\nConnection from {addr}")             # Show the client address

    data = conn.recv(1024).decode()                # Receive client data

    response = handle_request(data)                # Process request on server

    # Information used ONLY for server logging
    client_ip = addr[0]                            # Get the client IP for the log
    server_ip = conn.getsockname()[0]              # Get the server IP for the log

    try:                                            # Get request data for the log
        payload = json.loads(data)

        a = payload.get("a")
        b = payload.get("b")
        operation = payload.get("operation")

    except (json.JSONDecodeError, AttributeError):    # Use N/A if the request data cannot be read
        a = "N/A"
        b = "N/A"
        operation = "N/A"

    
    # Status message for the SERVER log
    
    if response["code"] == 200:
        status_message = "Successful operation"

    elif response["code"] == 400:
        status_message = "Invalid request"

    elif response["code"] == 422:
        status_message = "Invalid input"

    else:
        status_message = "Server error"

    # Result or error for the log
    
    if "result" in response:                                #This checks if the response contains a result or an error.
        result_text = f"Result: {response['result']}"

    else:
        result_text = f"Error: {response['error']}"

    # Log stays ONLY on the server
    log_message = (                                        # Build the complete server log message
        f"Client IP: {client_ip} | "
        f"Server IP: {server_ip} | "
        f"a: {a} | "
        f"b: {b} | "
        f"Operation: {operation} | "
        f"{result_text} | "
        f"Code: {response['code']} | "
        f"Status: {status_message}"
    )

    print(log_message)                             # Show log in AWS terminal
    logging.info(log_message)                      # Save log in server.log

    response_json = json.dumps(response)           # Convert response to JSON

    conn.send(response_json.encode())              # Send ONLY response to client

    conn.close()                                   # Close client connection
