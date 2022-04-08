#!/usr/bin/env python3

# Python DNS query client
#
# Example usage:
#   ./dns.py --type=A --name=www.pacific.edu --server=8.8.8.8
#   ./dns.py --type=AAAA --name=www.google.com --server=8.8.8.8

# Should provide equivalent results to:
#   dig www.pacific.edu A @8.8.8.8 +noedns
#   dig www.google.com AAAA @8.8.8.8 +noedns
#   (note that the +noedns option is used to disable the pseduo-OPT
#    header that dig adds. Our Python DNS client does not need
#    to produce that optional, more modern header)


from dns_tools import dns, dns_header_bitfields  # Custom module for boilerplate code

import argparse
import ctypes
import random
import socket
import struct
import sys

def main():

    # Setup configuration
    parser = argparse.ArgumentParser(description='DNS client for ECPE 170')
    parser.add_argument('--type', action='store', dest='qtype',
                        required=True, help='Query Type (A or AAAA)')
    parser.add_argument('--name', action='store', dest='qname',
                        required=True, help='Query Name')
    parser.add_argument('--server', action='store', dest='server_ip',
                        required=True, help='DNS Server IP')

    args = parser.parse_args()
    qtype = args.qtype
    qname = args.qname
    server_ip = args.server_ip
    port = 53
    server_address = (server_ip, port)

    if qtype not in ("A", "AAAA"):
        print("Error: Query Type must be 'A' (IPv4) or 'AAAA' (IPv6)")
        sys.exit()

    # Create UDP socket
    # ---------
    # STUDENT TO-DO
    # ---------
    try:
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print("Error, couldn't make UDP socket")
        sys.exit()

    # Generate DNS request message
    # ---------
    # STUDENT TO-DO
    # ---------
    message = bytearray()
    message += struct.pack('!H', random.randint(0,65535)) #msg id some random 16 bit integer

    #setting flags
    flags = dns_header_bitfields()
    flags.qr = 0
    flags.opcode = 0
    flags.aa = 0
    flags.tc = 0
    flags.rd = 1
    flags.ra = 0
    flags.reserved = 0
    flags.rcode = 0
    
    message += bytes(flags)
    
    message += struct.pack('!H', 1) #input = amount of question
    message += struct.pack('!H', 0) #input = entries in answer sectino
    message += struct.pack('!H', 0) #input = entries in authority section
    message += struct.pack('!H', 0) #input = entries in additional section
    
    #split url
    names = qname.split('.')
    for x in names:
        message += struct.pack('!B', len(x))
        message += x.encode()
    message += struct.pack('!B', 0)
    if qtype == 'A':
        message += struct.pack('!H', 1)
    else:
        message += struct.pack('!H', 28)
    message += struct.pack('!H', 1)
    # Send request message to server
    # (Tip: Use sendto() function for UDP)
    # ---------
    # STUDENT TO-DO
    # ---------
    udp.sendto(message, server_address)

    # Receive message from server
    # (Tip: use recvfrom() function for UDP)
    # ---------
    # STUDENT TO-DO
    # ---------
    #buffer size 4096
    raw_bytes = udp.recvfrom(4096)[0]

    # Close socket
    # ---------
    # STUDENT TO-DO
    # ---------
    udp.close()
    # Decode DNS message and display to screen
    dns.decode_dns(raw_bytes)


if __name__ == "__main__":
    sys.exit(main())
