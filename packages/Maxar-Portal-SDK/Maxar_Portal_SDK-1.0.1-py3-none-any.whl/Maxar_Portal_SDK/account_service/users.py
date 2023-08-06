import requests
import json
import Maxar_Portal_SDK.process as process


class Users:

    def __init__(self, auth):
        self.base_url = auth.base_url
        self.response = None
        self.version = auth.version
        self.auth = auth

    def Search(self, search):
        """
        Function searches through all users and lists users that match the search term
        Args:
            search (string) = Search term. Searches through usernames, roles, activation numbers, and account numbers
        Returns:
            Dictionary of the found user or users
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/users?search={}'.format(search)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        if len(response.json()["users"]) < 1:
            raise Exception("No search results for {}. Please try another search term".format(search))
        return response.json()

    def GetUsers(self, userId=None, username=None):
        """
        Function lists a users details
        Args:
            userId (string) = Id of the desired user. Defaults to None
            username (string) = Username of the desired user. Defaults to None
        Returns:
            Dictionary of the desired user's details
        """

        authorization = process.authorization(self.auth)
        if userId:
            url = self.base_url + "/accountservice/api/v1/users/{}".format(userId)
        elif username:
            url = self.base_url + "/accountservice/api/v1/users/username/{}".format(username)
        else:
            url = self.base_url + "/accountservice/api/v1/users"
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def UpdateUser(self, userId, **kwargs):
        """
        Function updates requested user based on payload. Payload can be retrieved using GetUsers function and then edited.
        args:
            userId: "f:b1d8a1c8-a7d8-46b0-831c-2bb9185857a2:26"
        kwargs:
            username
            firstName
            lastName
            phone

        full payload:
                {'userId': 'f:b1d8a1c8-a7d8-46b0-831c-2bb9185857a2:1',
                 'username': 'system-admin-swph@maxar.com',
                 'firstName': 'System',
                 'lastName': 'SW_PH',
                 'emailAddress': 'system-admin-swph@maxar.com',
                 'createdDate': '2022-06-14T21:17:17.932579Z',
                 'updatedDate': '2022-07-12T19:35:45.943487Z',
                 'isActive': True,
                 'emailVerified': True,
                 'password': None,
                 'userType': 'SYSTEM_ADMIN',
                 'accountId': None,
                 'account': None,
                 'activationId': None,
                 'activation': None,
                 'country': None,
                 'phone': '7777777777',
                 'suspensionReason': None,
                 'notifySuspension': False,
                 'status': 'ACTIVE',
                 'totalCreditsUsed': 0.0}

        Returns:
            payload of changed user
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/accountservice/api/v1/users"
        payload = self.GetUsers(userId=userId)
        for item in kwargs.keys():
            payload.update({item: kwargs[item]})
        payload = json.dumps(payload)
        response = requests.request("PUT", url, headers=authorization, data=payload, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def CreateUser(self, user_type, accountId, activationId, emailAddress, firstName, lastName, clientID = 'mds-account-ui', **kwargs):
        """
        Function accepts payload for new user and returns response JSON of created user.
        Args:
            user_type = 'BASE_USER'
            accountId = str
            activationId = str
            emailAddress = str
            firstName =str
            lastName = str
            country = str
            phone = str
            clientID = string

        payload: dict

            {"notifySuspension":false,
            "userType":"BASE_USER",
            "accountId":1,
            "activationId":1,
            "emailAddress":"w.k@maxar.com",
            "firstName":"will",
            "lastName":"k",
            "country":"United States",
            "phone":"1234567890",
            "isActive":true}

        Returns:
            JSON of created user

        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/accountservice/api/v1/users/{}".format(clientID)

        payload = {"notifySuspension": False,
            "userType": user_type,
            "accountId": accountId,
            "activationId": activationId,
            "emailAddress": emailAddress,
            "firstName": firstName,
            "lastName": lastName,
            "country": '',
            "phone": '',
            "isActive": True}

        for item in kwargs.keys():
            payload.update({item: kwargs[item]})

        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=authorization, data=payload, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def UpdateUserRoles(self, userId, rolesToUpdate, delete=False):
        """
        Args:
            userId: string: 'f:b1d8a1c8-a7d8-46b0-831c-2bb9185857a2:42'
            rolesToUpdate: list: ['ARCHIVE_ORDERING']
            delete: boolean

        Returns:
            JSON if delete=False
            Response object if delete=True
        """

        authorization = process.authorization(self.auth)
        if type(rolesToUpdate) != list:
            raise Exception('rolesToUpdate must be a list')

        #use the roles class to create list of all roles
        roleList= self.GetUserAvailableRoles(userId)
        # roleList = roleClass.GetRoles()
        roleArray = []

        #loop through roles you want to add
        for i in range(len(rolesToUpdate)):
            #loop through all available roles
            for role in roleList:
                if role['name'] == rolesToUpdate[i]:
                    id = role['id']
                    roleArray.append({"id": id, "name": role['name']})

        #Check if it found all the roles you wanted to add
        if len(rolesToUpdate) != len(roleArray):
            raise Exception('One or more selected roles not available for this user.')
        payload = json.dumps(roleArray)

        if not delete:
            url = self.base_url + "/accountservice/api/v1/users/{}/assignroles".format(userId)
            response = requests.request("POST", url, headers=authorization, data=payload, verify=False)
            process_response = process._response_handler(response)
            return response.json()
        else:
            url = self.base_url + "/accountservice/api/v1/users/{}/removeroles".format(userId)
            response = requests.request("POST", url, headers=authorization, data=payload, verify=False)
            process_response = process._response_handler(response)
            return response

    def GetUserRoles(self, userId):
        """
        Finds the roles a user has.
        Returns:
            json of roles
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/accountservice/api/v1/users/roles/assigned/{}".format(userId)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process._response_handler(response)
        if response.status_code == 204:
            return {}
        else:
            return response.json()

    def GetUserAvailableRoles(self, userId):
        """
        Finds the roles available for a user to have.
        Returns:
            json of roles
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/accountservice/api/v1/users/roles/assigned-available/{}".format(userId)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def DeleteUser(self, userId):
        """
        Deletes a user
        Args:
            userId:

        Returns:
            response object
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/accountservice/api/v1/users?userId={}".format(userId)
        response = requests.request("DELETE", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return "User {} successfully deleted".format(userId)
