import requests
import os

class Auth:
    """
    This class handles authentication for the MPS SDK. When a config file is not present the user must pass the args below.
    Please create .MPS-config in home directory. For example: "C:/Users/will/.MPS-config"
    MPS-config contents:        [mps]
                                user_name=username
                                user_password=password
                                url=https://marianas-demo.dev.gcsdev.com
    """

    def __init__(self, base_url=None, username=None, password=None):
        """
        Function initializes the MPS environment and generates an access and refresh token
        Args:
            base_url (string) = Url of the desired environment
            username (string) = Username
            password (string) = Password
        """

        self.base_url = base_url  # host name "https://marianas-test.dev.gcsdev.com/"
        self.username = username
        self.password = password
        self.access = None
        self.refresh = None
        self.version = "1.0.0"
        self.SSL = False

        if not self.base_url: #checks if url is provided as argument to class. If not, look for .MPS-config
            dir_path = os.path.expanduser('~')
            file = '.MPS-config'
            full_path = os.path.join(dir_path, file)
            if os.path.isfile(full_path):
                self.base_url, self.username, self.password = self._get_environment(full_path)
            else:
                raise ValueError("Please create .MPS-config in home dir.")
        # else:
        #     acceptable_urls = ['https://marianas-test.dev.gcsdev.com']
        #     if self.base_url not in acceptable_urls:
        #         raise ValueError("Base_url must match acceptable SecureWatch 3 URL.")

        #checks for auth when the class is instantiated and assigns tokens to the self.access and self.refresh
        self.refresh_token()

    @staticmethod
    def _get_environment(file):
        """
        Determines tenant and data from config file, passes data into init
        """

        with open(file) as config_file:
            cred_dict = {}
            for line in config_file.readlines():
                if '=' in line:
                    key, value = line.split('=')
                    key = key.strip()
                    value = value.strip()
                    if '\n' in value:
                        value = value.replace('\n', '')
                    cred_dict.update({key: value})
        if 'user_name' not in cred_dict.keys() or 'user_password' not in cred_dict.keys() or 'url' not in cred_dict.keys():
            raise Exception('.MPS-config not formatted properly')
        else:
            user_name = cred_dict['user_name']
            password = cred_dict['user_password']
            url = cred_dict['url']
            return url, user_name, password



    def get_auth(self):
        """
        Function generates an access token and refresh token based on a username and password combination
        """

        url = "{}/auth/realms/mds/protocol/openid-connect/token".format(self.base_url)
        payload = 'client_id=mds-internal-service&username={}&password={}&grant_type=password'.format(self.username, self.password)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        if response.status_code != 200:
            raise Exception('Unable to connect. Status code equals {}'.format(response.status_code))
        else:
            self.access = response.json()['access_token']
            self.refresh = response.json()['refresh_token']
            return self.access

    def refresh_token(self):
        """
        Function takes in refresh token and generates a new access token and refresh token
        """

        if self.refresh:
            url = "{}/auth/realms/mds/protocol/openid-connect/token".format(self.base_url)

            payload = 'grant_type=refresh_token&refresh_token={}&client_id=mds-internal-service'.format(self.refresh)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)

            if response.status_code == 400 and response.json()['error_description'] == 'Token is not active':
                self.get_auth()
            elif response.status_code != 200:
                raise Exception('Error. Status code = {}'.format(response.status_code))
            else:
                self.access = response.json()['access_token']
                self.refresh = response.json()['refresh_token']
                return self.access
        else:
            self.get_auth()
