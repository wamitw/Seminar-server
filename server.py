#!/usr/bin/env python3

import socketserver, argparse, sys, threading, atexit, ssl
from io import StringIO

def execRCE(code):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    exec(code)
    sys.stdout = old_stdout
    return redirected_output.getvalue()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got request from {}".format(self.client_address[0]))
        output = execRCE(self.data)
        self.request.sendall(output.encode('utf-8'))

class SSLTCPServer(socketserver.TCPServer):
    def __init__(self,
                 server_address,
                 RequestHandlerClass,
                 certfile,
                 ssl_version=ssl.PROTOCOL_TLSv1,
                 bind_and_activate=True):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.certfile = certfile
        self.keyfile = certfile
        self.ssl_version = ssl_version

    def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        connstream = ssl.wrap_socket(newsocket,
                                 server_side=True,
                                 certfile = self.certfile,
                                 keyfile = self.certfile,
                                 ssl_version = self.ssl_version)
        return connstream, fromaddr

class ThreadedTCPServer(socketserver.ThreadingMixIn, SSLTCPServer):
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
        with ThreadedTCPServer((host, port), MyTCPHandler,"cert.pem") as server:
            host, port = server.server_address
            print("Server started on {}:{}".format(host, port))
            atexit.register(close_server, server)
            server.serve_forever()

    except IOError as e:
        print(e)
    except:
        print("Exiting...")
        exit
