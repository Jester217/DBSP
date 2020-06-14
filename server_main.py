import logging
import sys
import Server

LOGGING_STATE = logging.INFO
DNS_SERVER_IP = "8.8.8.8"


def get_args():
    """
    function get args needed for program
    port is const 53 (DNS port)
    ip can be supllied from command line or default ip (host)
    """
    try:
        dns_server_ip = sys.argv[1]
    except IndexError:
        logging.info("IP wasn't supplied on the command line, server uses default IP")
        dns_server_ip = DNS_SERVER_IP

    return dns_server_ip


def main():
    """
    this python file generates DBSP server
    """
    logging.basicConfig(format='%(levelname)s:%(message)s', level=LOGGING_STATE)
    args = get_args()
    dns_server_ip = args

    server = Server.Server(dns_server_ip)
    server.run()


if __name__ == '__main__':
    main()