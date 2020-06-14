import sys

i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *
import socket
import Request
import logging

sys.stdin, sys.stdout, sys.stderr = i, o, e


class Communicator:
    def __init__(self):
        """
        function constructs server
        args:
            ip: string
            port: int
        """
        try:
            self.ip = socket.gethostbyname(socket.gethostname())
            self.port = 53
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("0.0.0.0", self.port))
        except socket.error as e:
            logging.critical("Comunicator is not able to generate server")
            print repr(e)


    def get_request_scapy(self):
        pack = sniff(count=1, lfilter = lambda p: p.haslayer(IP) and p.haslayer(UDP) and p.haslayer(DNS) and p[IP].dst == self.ip)[0]

        return pack[Raw].load

    def get_request(self):
        """
        function returns Request object
        Request:
            data = socket payload
            address = (ip, port)
                ip = string
                port = int
        """
        try:
            client_request, client_address = self.sock.recvfrom(1024)
            return Request.Request(client_request, client_address)
        except socket.error:
            return None

    def send_response(self, data, address):
        """
        function send response to requester
        args:
            data = string
            address = (ip, port)
                ip = string
                port = int
        """
        try:
            self.sock.sendto(data, address)
            return True
        except socket.error:
            return False

    def send_response_scapy(self, data, address):
        pack = IP(src=self.ip, dst=address[0]) / UDP(sport=self.port, dport=address[1]) / data
        send(pack)