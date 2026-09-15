import socket
import json

HOST = "18.117.252.35"
PORT = 12345

while True:                                            #  allows multiple operations in one session

    print("\nSimple Calculator")                        # displays information to the user.
    print("Operations: add, sub, mul, div")
    print("Type exit to finish")

    operation = input("Enter operation: ")                # gets the operation from the user, but it does not validate it.

    if operation == "exit":                               # It is used to close the program.
        print("Goodbye!")
        break

    a = input("Enter first number: ")
    b = input("Enter second number: ")

    payload = {
        "a": a,
        "b": b,
        "operation": operation
    }

    s = socket.socket()
    s.connect((HOST, PORT))

    s.send(json.dumps(payload).encode())

    response = s.recv(1024).decode()

    print("Server response:", response)

    s.close()
