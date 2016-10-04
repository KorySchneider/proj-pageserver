"""
  A trivial web server in Python. 

  Based largely on https://docs.python.org/3.4/howto/sockets.html
  This trivial implementation is not robust:  We have omitted decent
  error handling and many other things to keep the illustration as simple
  as possible. 
"""

import CONFIG    # Configuration options. Create by editing CONFIG.base.py
import argparse  # Command line options (may override some configuration options)
import socket    # Basic TCP/IP communication on the internet
import _thread   # Response computation runs concurrently with main program 

def listen(portnum):
    """
    Create and listen to a server socket.
    Args:
       portnum: Integer in range 1024-65535; temporary use ports
           should be in range 49152-65535.
    Returns:
       A server socket, unless connection fails (e.g., because
       the port is already in use).
    """
    # Internet, streaming socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to port and make accessible from anywhere that has our IP address
    serversocket.bind(('', portnum))
    serversocket.listen(1)    # A real server would have multiple listeners
    return serversocket

def serve(sock, func):
    """
    Respond to connections on sock.
    Args:
       sock:  A server socket, already listening on some port.
       func:  a function that takes a client socket and does something with it
    Returns: nothing
    Effects:
        For each connection, func is called on a client socket connected
        to the connected client, running concurrently in its own thread.
    """
    while True:
        print("Attempting to accept a connection on {}".format(sock))
        (clientsocket, address) = sock.accept()
        _thread.start_new_thread(func, (clientsocket,))

## HTTP response codes
##   See:  https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
##   or    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
## 
STATUS_OK = "HTTP/1.0 200 OK\n\n"
STATUS_FORBIDDEN = "HTTP/1.0 403 Forbidden\n\n"
STATUS_NOT_FOUND = "HTTP/1.0 404 Not Found\n\n"
STATUS_NOT_IMPLEMENTED = "HTTP/1.0 401 Not Implemented\n\n"

def isValidURL(string):
    valid = False
    if string.endswith('.html') or string.endswith('.css'):
        if not '..' in string and not '~' in string and not '//' in string:
            valid = True
    return valid

def respond(sock):
    """
    This server responds only to GET requests (not PUT, POST, or UPDATE).
    Any valid GET request is answered with an ascii graphic of a cat. 
    """
    request = sock.recv(1024)  # We accept only short requests
    request = str(request, encoding='utf-8', errors='strict')
    print("\nRequest was {}\n".format(request))

    parts = request.split()
    if len(parts) > 1 and parts[0] == "GET":
        response = None
        if isValidURL(parts[1]):
            try:
                responseFile = open('pages'+parts[1], 'r')
                response = responseFile.read()
            except FileNotFoundError:
                transmit(STATUS_NOT_FOUND, sock)
                transmit('404', sock)
        else:
            transmit(STATUS_FORBIDDEN, sock)
            transmit('403', sock)

        if response is not None:
            transmit(STATUS_OK, sock)
            transmit(response, sock)
            responseFile.close()
    else:
        transmit(STATUS_NOT_IMPLEMENTED, sock)        
        transmit("\nI don't handle this request: {}\n".format(request), sock)

    sock.close()
    return

def transmit(msg, sock):
    """It might take several sends to get the whole message out"""
    sent = 0
    while sent < len(msg):
        buff = bytes( msg[sent: ], encoding="utf-8")
        sent += sock.send( buff )
    

###
#
# Run from command line
#
###

def get_options():
    """
    Options from command line or configuration file.
    Returns namespace object with option value for port
    """
    parser = argparse.ArgumentParser(description="Run trivial web server.")
    parser.add_argument("--port", "-p",  dest="port", 
                        help="Port to listen on; default is {}".format(CONFIG.PORT),
                        type=int, default=CONFIG.PORT)
    options = parser.parse_args()
    if options.port <= 1000:
        print("Warning: Ports 0..1000 are reserved by the operating system")
    return options
    

def main():
    options = get_options()
    port = options.port
    sock = listen(port)
    print("Listening on port {}".format(port))
    print("Socket is {}".format(sock))
    serve(sock, respond)

main()
    
