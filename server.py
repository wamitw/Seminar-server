#!/usr/bin/env python3

import socketserver, argparse, sys, threading, atexit
from io import StringIO

def execRCE(code):
    old_stdout = sys.stdout
    print("Before code execution")
    redirected_output = sys.stdout = StringIO()
    st = exec(code)
    sys.stdout = old_stdout
    print("After code execution with status=" + str(st))
    return redirected_output.getvalue()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        output = execRCE(self.data)
        print("output is " + output)
        # just send back the same data, but upper-cased
        self.request.sendall(output.encode('utf-8'))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def close_server(server):
    server.shutdown()

#Default Values
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 0            # Port to listen on (0 is arbitary availabe port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server that accept python remote code execution and returns their result')
    parser.add_argument('--host', default=HOST, action='store', type=str, help='Host to listen upon. default is ' + HOST + '.')
    parser.add_argument('--port','-p', default=PORT, action='store', type=int, help='Port to listen upon')

    args = parser.parse_args()
    host, port = args.host, args.port

    print("Starting server on {}:{}".format(host, port))
    try:
        # Create the server, binding to localhost on port 9999
        with ThreadedTCPServer((host, port), MyTCPHandler) as server:
            host, port = server.server_address
            print("Server started on {}:{}".format(host, port))
            atexit.register(close_server, server)
            server.serve_forever()

    except IOError as e:
        print(e)
    except:
        print("Undefined Error")
        print("Exiting...")
        exit
