#Code Reference : http://www.bitforestinfo.com/2017/01/how-to-write-simple-packet-sniffer.html


# import modules
import socket 
import struct
import binascii
import os
import pye
from email_sender import *


# if operating system is windows
if os.name == "nt":
    s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_IP)
    s.bind(("192.168.56.1", 5000))
    s.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
    s.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

# if operating system is linux
else:
    s=socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))

# create loop 
while True:

    # Capture packets from network
    pkt=s.recvfrom(65565)

    # extract packets with the help of pye.unpack class 
    unpack=pye.unpack()

    message = ""

    print("\n\n------------ Ethernet Header ------------")
    # print data on terminal

    message += "------------ Ethernet Header ------------\n\n"
    for i in unpack.eth_header(pkt[0][0:14]).items():
        a,b=i
        print("{} : {} | ".format(a,b),)
        message += "{} : {} | ".format(a,b)

    print("\n------------ IP Header ------------")

    message += "\n\n------------ IP Header ------------\n\n"
    for i in unpack.ip_header(pkt[0][14:34]).items():
        a,b=i
        print("{} : {} | ".format(a,b),)
        message += "{} : {} | ".format(a,b)

    print("\n------------ Tcp Header ------------")

    message += "\n\n------------ Tcp Header ------------\n\n"
    for  i in unpack.tcp_header(pkt[0][34:54]).items():
        a,b=i
        print("{} : {} | ".format(a,b),)
        message += "{} : {} | ".format(a,b)

    send_mail("NETWORK SNIFFER", message)