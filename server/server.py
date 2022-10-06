import socket
import time
import sys
import os

sys.path.append('../motor')
import motor

# CONSTANTS
json_template = b'{ \"message\" : \"Dispensed for %s second(s)!\" }'
OK_response = b'HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n'

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

motor = motor.Motor()

print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        value = b'1' # Default value (Hello, world!)
        get_message = request.find('/dispense')

        if get_message == 6:
            print("Dispensing food...")
            motor.dispenseFood(1)

        payload = json_template % value

        cl.send(OK_response)
        cl.send(payload)
        cl.close()

    except (OSError, KeyboardInterrupt) as e:
        cl.close()
        print('connection closed')
        try:
            sys.exit(0)
        except:
            os._exit(0)
