import socket
import json

HOST = "18.117.252.35"
PORT = 12345

while True:

    print("\nSimple Calculator")
    print("Operations: add, sub, mul, div")
    print("Type exit to finish")

    operation = input("Enter operation: ")

    if operation == "exit":
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
