import requests
import warnings
import Maxar_Portal_SDK.process as process

warnings.filterwarnings('ignore')

class Usage:

    def __init__(self, auth):
        self.base_url = auth.base_url
        self.headers = process.authorization()
        self.auth = auth

    def get_usage(self, activation_id=None):
        """
        Function returns the usage for an activation.
        Args:
            activation_id: string of the activation you want to check. if not provided attempts to get it from your token.
            Needs the account admin permissions to get Activation Id from token. If using elevated permission from account admin. Activation ID is required.
        """
        authorization = process.authorization(self.auth)
        if activation_id:
            url = "{}/usageservice/api/v1/usage/activation/{}".format(self.base_url, activation_id)
        else:
            url = "{}/usageservice/api/v1/usage".format(self.base_url)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process._response_handler(response)
        return response.json()


    def get_usage_overview(self): # Account admin needed
        """
        this function gets aggregated usage information for the usage overview
        """
        authorization = process.authorization(self.auth)
        url = "{}/usageservice/api/v1/usage/activation/overview".format(self.base_url)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process._response_handler(response)
        return response.json()


    def get_usage_allowed(self, activation_id=None):
        """
        This function checks if there is usage left on the activation tied to your token.
        Returns 200 server status code if you have credit remaining.
        Args:
            activation_id: string of the activation you want to check. if not provided attempts to get it from your token.
            Needs the account admin permissions to get Activation Id from token. If using elevated permission from account admin. Activation ID is required.
        """
        authorization = process.authorization(self.auth)
        if activation_id:
            url = '{}/usageservice/api/v1/usage/activation/{}/allowed'.format(self.base_url, activation_id)
        else:
            url = "{}/usageservice/api/v1/usage/allowed".format(self.base_url)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process._response_handler(response)
        try:
            return response.json()
        except:
            return response.status_code

    def get_usage_allowed_download(self,bbox,productId,activation_id=None):
        """
        Function checks if there is enough usage left on your activation to download data.
        Args:
            bbox = Str of the area that you want to download. Is coverted to an area
            productId = String of the Id of product that you are trying to download
            activation_id: string of the activation you want to check. if not provided attempts to get it from your token.
            Needs the account admin permissions to get Activation Id from token. If using elevated permission from account admin. Activation ID is required.
        """
        authorization = process.authorization(self.auth)
        sqkm = process.area_sqkm(bbox)
        if activation_id:
            url = '{}/usageservice/api/v1/usage/activation/{}/allowed/download?sqKm={}&productId={}'.format(self.base_url,activation_id,sqkm,productId)
        else:
            url = "{}/usageservice/api/v1/usage/allowed/download?sqKm={}&productId={}".format(self.base_url,sqkm,productId)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process._response_handler(response)
        try:
            return response.json()
        except:
            return response.status_code