class Client:

    def __init__(self, ip):
        self.ip = ip
        self.massages = []

    def add_massage(self, massage):
        """
        function add message to messages list
        args:
            message: string
        """
        self.massages.append(massage)