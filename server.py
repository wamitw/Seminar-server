#!/usr/bin/env python3

import socket, argparse

#Default Values
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

parser = argparse.ArgumentParser(description='Server that accept python remote code execution and returns their result')
parser.add_argument('--host', default=HOST, action='store', type=str, help='Host to listen upon. default is ' + HOST + '.')
parser.add_argument('--port','-p', default=PORT, action='store', type=int, help='Port to listen upon')

args = parser.parse_args()

host = args.host
port = args.port

print("Starting server on host " + host + " on port " + str(port) + ".")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Binding...")
    s.bind((host, port))
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
