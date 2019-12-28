#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Binding...")
    s.bind((HOST, PORT))
    print("Listening...")
    s.listen()
    conn, addr = s.accept()
    print("Got new socket!")
    with conn:
        print('Connected by', addr)
        msg=str('')
        while True:
            data = conn.recv(1024)
            print("Received data")
            if not data:
                break
            print(data)
            msg += str(data, "utf-8")
        print(msg)
