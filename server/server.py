import socket
import time
import sys
import os
from HTTPRequest import HTTPRequest
from urllib.parse import parse_qs
sys.path.append('../motor')
sys.path.append('../statusLight')
import motor
import led

# Debug flag
DEBUG = True

# A simple socket-based server to listen for commands via local network
class Server:
    # Constants for network communications
    # JSON responses
    success_true_json = '{\"success\":true}'
    success_false_json = '{\"success\":false}'
    # Status codes
    OK_status = 'HTTP/1.1 200 OK\n'
    error_status = 'HTTP/1.1 500 Internal Server Error\n'
    not_implemented_status = 'HTTP/1.1 501 Not Implemented\n'
    # Headers
    app_json = 'Content-Type: application/json\n'
    text_html = 'Content-Type: text/html\n'
    end_headers = '\n'
    # Networking  stuff
    address = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    request_buf_size = 1024
    default_rev_value = 1
    # Endpoints
    connection_test_endpoint = '/connection-test'
    dispense_endpoint = '/dispense'
    led_on_endpoint = '/led-on'
    led_off_endpoint = '/led-off'

    def __init__(self):
        # Init hardware
        self.motor = motor.Motor()
        self.statusLight = led.LED()

        # Get html for index.html
        index = open("index.html")
        self.html = index.read()
        index.close()

        # Init socket and begin listening for requests
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.address)
        self.sock.listen(1)
        if DEBUG:
            print("listening on", self.address)

    # Listen for requests via local network
    def listenForRequests(self):
        while True:
            try:
                # Default revolutions value
                revolutions = self.default_rev_value
                # Connect to client
                connection, address = self.sock.accept()
                if DEBUG:
                    print("client connected from", address)
                # Receive data from client
                req = connection.recv(self.request_buf_size)
                # Decode request
                request = HTTPRequest(req)
                try: 
                    # Check for path
                    path = request.path
                except AttributeError as e: 
                    # No path, no options requested
                    response = self.not_implemented_status + self.end_headers
                    connection.send(response.encode())
                    connection.close()
                    break

                if DEBUG:
                    print(path)
                # Check request for `/connection-test` endpoint.
                connection_test_requested = path.find(self.connection_test_endpoint)
                # Check for `/dispense`
                dispense_requested = path.find(self.dispense_endpoint)
                # Check for `/led-on`
                led_on_requested = path.find(self.led_on_endpoint)
                # Check for `/led-off`
                led_off_requested = path.find(self.led_off_endpoint)

                # Perform requested action
                if connection_test_requested == 0:
                    # Send back OK response
                    response = self.OK_status\
                            + self.end_headers
                    connection.send(response.encode())
                    connection.close()
                elif dispense_requested == 0:
                    # Parse path for query param `revolutions`
                    split_path = path.split("?")
                    if len(split_path) > 1: # Query params present
                        query_params = split_path[1]
                        rev_value_str = query_params.split("=")[1]
                        print(rev_value_str)
                        revolutions = int(rev_value_str)
                        self.motor.dispenseFood(revolutions)
                    else:
                        # No query params, dispense default amount
                        self.motor.dispenseFood(revolutions)
                    # Send status to client
                    response = self.OK_status\
                            + self.app_json\
                            + self.end_headers\
                            + self.success_true_json
                    connection.send(response.encode())
                    connection.close()
                elif led_on_requested == 0:
                    # Parse path for query param `revolutions`
                    split_path = path.split("?")
                    if len(split_path) > 1: # Query params present
                        query_params = split_path[1]
                        colors = query_params.split("&")
                        if len(colors) > 2:
                            r_str = colors[0].split("=")[1]
                            g_str = colors[1].split("=")[1]
                            b_str = colors[2].split("=")[1]
                            print("R" + r_str + "G" + g_str + "B" + b_str)
                            self.statusLight.setValue(int(r_str), int(g_str), int(b_str))
                    else:
                        # Turn on LED
                        self.statusLight.setValue(100, 100, 100)
                    # Send status to client
                    response = self.OK_status\
                            + self.app_json\
                            + self.end_headers\
                            + self.success_true_json
                    connection.send(response.encode())
                    connection.close()
                elif led_off_requested == 0:
                    # Turn off LED
                    self.statusLight.setValue(0, 0, 0)
                    # Send status to client
                    response = self.OK_status\
                            + self.app_json\
                            + self.end_headers\
                            + self.success_true_json
                    connection.send(response.encode())
                    connection.close()
                else:
                    # Not implemented
                    response = self.not_implemented_status + self.end_headers
                    connection.send(response.encode())
                    connection.close()

            except (OSError, KeyboardInterrupt) as e:
                connection.close()
                self.statusLight.cleanup()
                if DEBUG:
                    print("connection closed due to exception")
                try: 
                    sys.exit(0)
                except:
                    os._exit(0)
               
if DEBUG:
    if __name__ == "__main__":
        serv = Server()
        serv.listenForRequests()
