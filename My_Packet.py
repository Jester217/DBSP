from scapy import packet

class My_Packet:
    def __init__(self, dip, dport, dns):
        self.dip = dip
        self.dport = dport
        self.dns = dns


def main():
    """
    Add Documentation here
    """
    p = packet.BasePacket()
    print p


if __name__ == '__main__':
    main()