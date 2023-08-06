import requests
import json
import MPS_Portal_SDK.process as process


class Roles:

    def __init__(self, auth):
        self.base_url = auth.base_url
        self.response = None
        self.version = auth.version
        self.auth = auth

    def GetRoles(self):
        """

        Returns: All roles

        """
        authorization = process.authorization(self.auth)
        url = self.base_url + "/accountservice/api/v1/roles"
        payload = {}
        response = requests.request("GET", url, headers=authorization, data=payload, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def CreateRole(self, name):
        """
        args:
            name = str
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/accountservice/api/v1/roles"
        payload = {
            "id": "",
            "name": name,
            "displayName": "{\"type\":\"STRING\",\"value\":[\"" + name + "\"]}",
            "isComposite": False,
            "isAssigned": False,
            "inheritedFrom": None,
            "composites": None,
            "attributes": [
                {
                    "name": "displayName",
                    "content": {
                        "type": "STRING",
                        "value": [
                            name
                        ]
                    }
                }
            ]
        }

        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=authorization, data=payload, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def UpdateRole(self, id, name, displayName):
        """
        args:
            id = str
            name = str
            displayName = str
        Accepts payload in the following format. Fill id and name with role you want to change. Name is immutable.
        payload = {
            "id": "",
            "name": "test",
            "displayName": "{\"type\":\"STRING\",\"value\":[\"test\"]}",
            "isComposite": False,
            "isAssigned": False,
            "inheritedFrom": None,
            "composites": None,
            "attributes": [
                {
                    "name": "displayName",
                    "content": {
                        "type": "STRING",
                        "value": [
                            "test"
                        ]
                    }
                }
            ]
        }
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/accountservice/api/v1/roles"
        payload = {
            "id": id,
            "name": name,
            "displayName": "{\"type\":\"STRING\",\"value\":[\"" + displayName + "\"]}",
            "isComposite": False,
            "isAssigned": False,
            "inheritedFrom": None,
            "composites": None,
            "attributes": [
                {
                    "name": 'displayName',
                    "content": {
                        "type": "STRING",
                        "value": [
                            displayName
                        ]
                    }
                }
            ]
        }
        payload = json.dumps(payload)
        response = requests.request("PUT", url, headers=authorization, data=payload, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def DeleteRole(self, roleName):

        authorization = process.authorization(self.auth)
        url = self.base_url + "/accountservice/api/v1/roles/{}".format(roleName)
        response = requests.request("DELETE", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return "Role {} successfully deleted".format(roleName)
