#!env python3

import socket
import time

UDP_IP = "192.168.10.101"
UDP_PORT = 52011
MESSAGE = " ".join(["Hello, World!" for x in range(1)])

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM) # UDP
sock.bind(("192.168.200.1", UDP_PORT))

try:
    no = 1
    while True:
        print("Sending pkt ", no)
        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
        time.sleep(10)
        no += 1
except KeyboardInterrupt:
    print("Quitting ...")
