import socket                                      # TCP socket communication
import json                                        # JSON serialization

HOST = "18.117.252.35"                             # Server IP address
PORT = 12345                                       # Server port

while True:

    print("\nSimple Calculator")
    print("Operations: add, sub, mul, div")
    print("Type exit to finish")

    operation = input("Enter operation: ")

    if operation == "exit":
        print("Goodbye!")
        break

    a_input = input("Enter first number: ")
    b_input = input("Enter second number: ")

    try:
        a = float(a_input)
    except ValueError:
        a = a_input

    try:
        b = float(b_input)
    except ValueError:
        b = b_input

    payload = {
        "a": a,
        "b": b,
        "operation": operation
    }

    s = socket.socket()                            # Create TCP socket

    s.connect((HOST, PORT))                        # Connect to server

    s.send(json.dumps(payload).encode())           # Send JSON request

    response = s.recv(1024).decode()               # Receive server response

    print("Server response:", response)

    s.close()                                      # Close connection
