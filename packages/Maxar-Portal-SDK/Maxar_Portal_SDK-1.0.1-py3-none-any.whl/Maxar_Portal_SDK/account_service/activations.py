import Maxar_Portal_SDK.account_service.roles as roles
import requests
import json
import Maxar_Portal_SDK.process as process

class Activations:

    def __init__(self, auth):
        self.base_url = auth.base_url
        self.response = None
        self.version = auth.version
        self.auth = auth

    def Search(self, search):
        """
        Function searches through all activations and lists activations that match the search term
        Args:
            search (string) = Search term. Searches through activation numbers, SAP contract identifiers, SAP line items,
            start dates, end dates, account numbers, and account ids
        Returns:
            Dictionary of the found activation or activations
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/activations?search={}'.format(search)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        if len(response.json()["activations"]) < 1:
            raise Exception("No search results for {}. Please try another search term".format(search))
        return response.json()

    def GetActivations(self, activationId=None):
        """
        Get all activations or activation by Id.
        Args:
            activationId (int): 1

        Returns:
            json
        """

        authorization = process.authorization(self.auth)
        if activationId:
            url = self.base_url + '/accountservice/api/v1/activations/{}'.format(activationId)
        elif not activationId:
            url = self.base_url + '/accountservice/api/v1/activations'
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def GetActivationsForAccount(self, accountId):
        """
        Gets activations for an account
        Args:
            AccountId (int): 1

        Returns:
            json
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/activations/available?accountId={}'.format(accountId)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def GetRolesForActivation(self, activationId): #RETURNS 500 ERROR. API BUG.
        """
        Args:
            activationId (int): 1
        Returns:
            json
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/activations/roles/{}'.format(activationId)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def GetActivationTypes(self):
        """
        Gets all activation types
        Returns:
            json
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/activations/types'
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def CreateActivation(self, accountId, activationTypeId, rateTableId, startDate, creditLimit, sapContractId, sapLineItem, **kwargs):
        """
        Creates an activation
        Args:
            name (string): 'test'
            AccountId (int): 1
            activationTypeId (string): "15001"
            startDate (string): "2022-07-19"
            sapContractId (string): '1234567890' (10 digits)
            sapLineItem (string): '123456' (6 digits)
            rateTableId (int):
            **kwargs:
                name (string): (must be unique)
                creatorName (string):
                endDate (string): "2022-07-19"
                roles (list): ['ARCHIVE_ORDERING']
                notes (string):
                imageryHoldbackValue (string) (co-dependent with imageryHoldbackUnits): '24'
                imageryHoldbackUnits (int) (co-dependent with imageryHoldbackValue): 0
                    0 = hours
                    1 = days
                    2 = months
                    3 = years
                creatorName (str) = 'Willy' (immutable once created)

        Returns:
            json of created account
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/activations'

        types = self.GetActivationTypes()
        for type in types:
            if type['id'] == activationTypeId:
                activationDict = type

        payload = {
            "accountId": accountId,
            "activationNumber": "string",
            "activationType": {
                "id": activationTypeId,
                "name": activationDict['name'],
                "description": activationDict['description']
            },
            "creditLimit": creditLimit,
            "isActive": True,
            "sapContractIdentifier": sapContractId,
            "sapLineItem": sapLineItem,
            "startDate": startDate,
            "rateTableId": rateTableId
        }

        for item in kwargs.keys():
            if item == 'roles':
                roleClass = roles.Roles(self.auth)
                roleList = roleClass.GetRoles()
                roleArray = []
                # loop through roles you want to add
                for i in range(len(kwargs['roles'])):
                    # loop through all available roles
                    for role in roleList:
                        if role['name'] == kwargs['roles'][i]:
                            id = role['id']
                            roleArray.append({"name": role['name'], "id": id})
                payload[item] = roleArray
            #Ensure that holdback units and values are both provided if one is. Set holdback display value.
            elif item == 'imageryHoldbackValue':
                payload[item] = kwargs[item]
                payload['imageryHoldbackDisplayValue'] = kwargs['imageryHoldbackValue']
                if 'imageryHoldbackUnits' not in kwargs.keys():
                    raise Exception('Must declare Holdback Units if declaring Holdback Value')
            elif item == 'imageryHoldbackUnits':
                payload[item] = kwargs[item]
                if 'imageryHoldbackValue' not in kwargs.keys():
                    raise Exception('Must declare Holdback Value if declaring Holdback Units')
            else:
                payload[item] = kwargs[item]

        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=authorization, data=payload, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def UpdateActivation(self, activationId, **kwargs):
        """
        Updates an activation.
        Args:
            activationId (int): 1
            **kwargs:
                name (string):
                endDate (string): "2022-07-19"
                roles (list): ['ARCHIVE_ORDERING']
                notes (string):
                imageryHoldbackValue (string) (co-dependent with imageryHoldbackUnits): '24'
                imageryHoldbackUnits (int) (co-dependent with imageryHoldbackValue): 0
                    0 = hours
                    1 = days
                    2 = months
                    3 = years
                name (string): 'test'
                AccountId (int): 1
                activationTypeId (string): "15001"
                startDate (string): "2022-07-19"
                sapContractId (string): '1234567890' (10 digits)
                sapLineItem (string): '123456' (6 digits)
                rateTableId (int): 1

        Returns:
            json of created account
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/activations'
        payload = self.GetActivations(activationId=activationId)

        for item in kwargs.keys():
            if item == 'roles':
                roleClass = roles.Roles(self.auth)
                roleList = roleClass.GetRoles()
                roleArray = []
                # loop through roles you want to add
                for i in range(len(kwargs['roles'])):
                    # loop through all available roles
                    for role in roleList:
                        if role['name'] == kwargs['roles'][i]:
                            id = role['id']
                            roleArray.append({"name": role['name'], "id": id})
                payload[item] = roleArray
            #Ensure that holdback units and values are both provided if one is. Set holdback display value.
            elif item == 'imageryHoldbackValue':
                payload[item] = kwargs[item]
                payload['imageryHoldbackDisplayValue'] = kwargs['imageryHoldbackValue']
                if 'imageryHoldbackUnits' not in kwargs.keys():
                    raise Exception('Must declare Holdback Units if declaring Holdback Value')
            elif item == 'imageryHoldbackUnits':
                payload[item] = kwargs[item]
                if 'imageryHoldbackValue' not in kwargs.keys():
                    raise Exception('Must declare Holdback Value if declaring Holdback Units')
            else:
                payload[item] = kwargs[item]

        payload = json.dumps(payload)
        response = requests.request("PUT", url, headers=authorization, data=payload, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def DeleteActivation(self, activationId):
        """
        Args:
            activationId (int): 1

        Returns:
            response object
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/activations?id={}'.format(activationId)
        response = requests.request("DELETE", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return "Activation {} successfully deleted".format(activationId)
