import Communicator
import Handler
from DBSP import dbsp_key_check
import Request
import Client_List
import Client
import logging
import socket


class Server:
    def __init__(self, dns_server_ip):
        """
        function constructs server
        args:
            ip: string
            port: int
        """
        self.dns_server_ip = dns_server_ip
        self.communicator = Communicator.Communicator()
        self.dbsp_client_list = Client_List.Client_List()
        self.banned_ip_list = []

    def update_request_type(self, request):
        """
        function determine and update request type
        args:
            request
        """
        if request.address[0] in self.banned_ip_list:
            request.set_type("DNS")

        b, c = self.dbsp_client_list.get_client_by_address(request.address)  # b: is client in list, c: client/None
        k = dbsp_key_check(request)
        if k:  # if request is dbsp key
            request.set_type("DBSP_KEY")
            if b:
                self.dbsp_client_list.remove_client(c)
                return
            c = Client.Client(request.address)
            self.dbsp_client_list.add_client(c)
            logging.info("new dbsp client, ip: {}".format(request.address[0]))
            return

        if b:
            request.set_type("DBSP")
            return

        request.set_type("DNS")

    def run(self):
        """
        function opereates server work
        """
        while True:
            request = self.communicator.get_request()
            if request is None:
                continue

            self.update_request_type(request)
            try:
                handler = Handler.Handler(self.communicator, request, self.dns_server_ip, self.dbsp_client_list)
                handler.start()
            except Exception as e:
                logging.error(e)