import socket
import json

HOST = "18.117.252.35"                                 # Server IP and port
PORT = 12345

while True:                                            #  allows multiple operations in one session

    print("\nSimple Calculator")                        # displays information to the user.
    print("Operations: add, sub, mul, div")
    print("Type exit to finish")

    operation = input("Enter operation: ")                # gets the operation from the user, but it does not validate it.

    if operation == "exit":                               # It is used to close the program.
        print("Goodbye!")
        break

    a = input("Enter first number: ")                      # gets the number a y b 
    b = input("Enter second number: ")                     # without validation.

    payload = {
        "a": a,                                            # Collect the values ​​into a dictionary.
        "b": b,
        "operation": operation
    }

    s = socket.socket()                                    # This creates the client socket.
    s.connect((HOST, PORT))                                # The client connects to the server using the IP address and port.

    s.send(json.dumps(payload).encode())                   # converts the data to JSON and then to bytes.

    response = s.recv(1024).decode()                        # recv receives the server response, and decode converts the bytes to text.

    print("Server response:", response)                     # Display response

    s.close()                                               # Close connection
