"""
Fix For Scapy Changing Input Output In Pycharm
"""
import sys  # For standard I/O

i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *
import socket
import hashlib
import dns_proxy
import logging

sys.stdin, sys.stdout, sys.stderr = i, o, e

DNS_SERVER_ADDRESS = ("8.8.8.8", 53)


def dns_request_generator(request_name):
    return IP(dst=DNS_SERVER_ADDRESS[0]) / UDP(dport=DNS_SERVER_ADDRESS[1]) / DNS(rd=1, qd=DNSQR(
        qname=request_name))


def dbsp_get_response(request, dns_answer):
    s = 'she sells sea shells by the sea shore'
    int(hashlib.sha1(s).hexdigest(), 16) % (10 ** 8)
    abs(hash(s)) % (10 ** 8)


def get_dns_service(request):
    dns_response = dns_handle_request(dns_request_generator(request[DNS].qd[DNSQR].qname))
    return dns_response[DNS].an[DNSRR].rdata


def push(sender_address, data):
    return sender_address[0] + ":" + data


def pull(sender_address, data):
    return sender_address[0] + ":" + data


def camouflage(request, response):
    dns_response = dns_handle_request(dns_request_generator(request[DNS].qd[DNSQR].qname))
    response[DNS].an[DNSRR].rdata = dns_response[DNS].an[DNSRR].rdata
    return response

def encapsulation(response):
    return DNS()

def decapsulation(request):
    return "PULL", "10.10.10.2", "hello, how are you?"


def dbsp_handle_request(request, dns_server_ip):
    client_address = request.get_address()
    request = request.get_data()
    state, sender, data = decapsulation(request)
    if state == "PUSH":
        response = push(sender, data)
    if state == "PULL":
        response = push(sender, data)
    else:
        response = dns_proxy.dns_request_generator(request[DNS].qd[DNSQR].qname, dns_server_ip)
    response = encapsulation(response)
    response = camouflage(request, response)
    return response

def ancient_dbsp_handle_request(request, dns_server_ip):
    """
    function returns dbsp response packet (only DNS part)
    """
    client_address = request.get_address()
    request = request.get_data()
    #request = IP(dst='8.8.8.8').src / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname='www.thepacketgeek.com'))
    request = DNS(rd=1, qd=DNSQR(qname='www.thepacketgeek.com'))
    response = DNS()
    response[DNS].an[DNSRR].rdata = get_dns_service(request)
    dbsp_response = dns_response[IP] / request
    return dns_response


def dbsp_key_check(request):
    """
    check if request is DBSP key
    return True if len(qname) % qtype == qclass
    :param request: Request
    """
    request = request.data
    name = len(str(request[DNS].qd[DNSQR].qname))
    mdl = int(request[DNS].qd[DNSQR].qtype)
    anr = int(request[DNS].qd[DNSQR].qclass)
    try:
        if name % mdl != anr:
            return False, name
        return True, None
    except ZeroDivisionError as zero:
        logging.debug(zero)  #if happens user probably is trying to interept dbsp, add to banned clients