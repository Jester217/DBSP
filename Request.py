from DBSP import dbsp_key_check

class Request:
    """
    class collects all the information about a request
    """
    def __init__(self, data, address):
        self.data = data
        self.address = address
        self.type = None

    def get_data(self):
        """
        function returns data
        """
        return self.data

    def get_address(self):
        """
        function returns address
        """
        return self.address

    def set_type(self, t):
        """
        function set request type
        args:
            t: string
        """
        self.type = t

    def get_type(self):
        """
        function returns request type
        """
        return self.type