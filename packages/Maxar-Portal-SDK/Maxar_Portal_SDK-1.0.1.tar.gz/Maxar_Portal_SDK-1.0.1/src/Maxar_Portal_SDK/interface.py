from Maxar_Portal_SDK.ogc.interface import Interface as ogc_interface
from Maxar_Portal_SDK.account_service.interface import Interface as account_interface
from Maxar_Portal_SDK.auth.auth import Auth


class Interface:

    def __init__(self, *args):

        if len(args) > 0:
            try:
                base_url = args[0]
                username = args[1]
                password = args[2]
            except:
                raise Exception("MPS-config file not formatted correctly")
            self.auth = Auth(base_url, username, password)
        else:
            self.auth = Auth()

        self.ogc = ogc_interface(self.auth)
        self.account_service = account_interface(self.auth)

