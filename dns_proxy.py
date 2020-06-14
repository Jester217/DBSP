import sys

i, o, e = sys.stdin, sys.stdout, sys.stderr
import socket
import logging
from scapy.all import *
import socket

sys.stdin, sys.stdout, sys.stderr = i, o, e



def dns_request_generator(request_name, dns_server_address):
    return IP(dst=dns_server_address[0]) / UDP(dport=dns_server_address[1]) / DNS(rd=1, qd=DNSQR(
        qname=request_name))


def send_request(request, dns_server_ip):
    """
    send DNS request to a server
    args:
        request: string
    """
    try:
        dns_server_address = (dns_server_ip, 53)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(request.data, dns_server_address)
        response, address = sock.recvfrom(1024)
        response[IP].src = socket.gethostname()
        response[IP].dst = request.address[0]
        logging.debug("DNS request was received and handled")
        return response
    except socket.error:
        return None
