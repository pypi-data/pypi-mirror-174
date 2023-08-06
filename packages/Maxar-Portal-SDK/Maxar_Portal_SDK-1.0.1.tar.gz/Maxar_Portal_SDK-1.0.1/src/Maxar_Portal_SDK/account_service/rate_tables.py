import Maxar_Portal_SDK.account_service.products as products
import requests
import Maxar_Portal_SDK.process as process
import json


class Table_Info:

    def __init__(self, auth):
        self.base_url = auth.base_url
        self.response = None
        self.version = auth.version
        self.auth = auth

    def GetTable(self, table_id=None):
        """
        Function lists either all rate tables and their details or a single rate table and its details
        Args:
            table_id (int) = Id of the desired rate table
        Returns:
             Dictionary of all tables and their details or a single table and its details
        """

        authorization = process.authorization(self.auth)
        if table_id:
            url = self.base_url + '/accountservice/api/v1/ratetables/{}'.format(table_id)
        else:
            url = self.base_url + '/accountservice/api/v1/ratetables'
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def GetActivationsForTable(self, table_id):
        """
        Function lists all activations associated with a specific rate table
        Args:
            table_id (int) = Id of the desired rate table
        Returns:
            Dictionary of a list of all activations associated with the given rate table
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/ratetables/{}/activations'.format(table_id)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def GetCreditTypes(self):
        """
        Function lists all available credit types
        Returns:
            List of dictionaries of available credit types
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/ratetables/credittypes'
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def GetRateAmounts(self, table_id):
        """
        Function lists all rate amounts for a desired rate table
        Args:
            table_id (int) = Id of the desired rate table
        Returns:
            List of all rate amounts and their details for the specified rate table
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/ratetables/{}/productCredits'.format(table_id)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return response.json()

class RateTables:

    def __init__(self, auth):
        self.base_url = auth.base_url
        self.response = None
        self.version = auth.version
        self.auth = auth

    def CreateTable(self, name, tables):
        """
        Function creates a new rate table
        Args:
            name (string) = Name for the newly created table
            tables (list(lists)) = Desired credit ammount (int) and credit unit type id (int). List must include the
            same amount of tables as there are products. Must be in the following format:
                [[<credits>, <creditUnitTypeId>]]
        Returns:
            Dictionary of newly created table
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/ratetables'
        count = 0
        product_info = products.Products.get_products(self)
        credit_info = Table_Info.GetCreditTypes(self)
        product_ids = []
        for i in product_info:
            product_ids.append(i["id"])
        table_num = len(product_info)
        if len(tables) != table_num:
            raise Exception("Total number of rate amounts is not equal to the amount of products. Number of rate amounts "
                            "must be equal to {}".format(len(product_info)))
        credit_check = [i for i in credit_info for j in tables if i["id"] == j[1]]
        if len(credit_check) != table_num:
            raise Exception("One or more credit types are not valid. Please use valid credit types")
        payload = {
            "name": name,
            "rateAmounts": []
        }
        while count < table_num:
            test = payload["rateAmounts"].append(
                {
                    "productId": product_ids[count],
                    "credits": float(tables[count][0]),
                    "creditUnitTypeId": tables[count][1]
                }
            )
            count += 1
        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=authorization, data=payload, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def UpdateTable(self, table_id, product_id=None, **kwargs):
        """
        **NOTE: Currently no way to update rate amounts for a table. No current call to get rate amounts or associated
        values to prevent overwriting, adding, or removal**
        Function updates a desired table's details
        Args:
            table_id (int) = Id of the desired rate table
            product_id (int) = Id of the desired product to alter. Defaults to None
        Kwargs:
            name (string) = Name of the desired rate table
            credits (int) = Number of desired credits
        Returns:
            Dictionary of updated rate table
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/ratetables'
        table_info = Table_Info.GetTable(self, table_id)
        rate_info = Table_Info.GetRateAmounts(self, table_id)
        rate_variables = ["productId", "credits", "creditUnitTypeId"]
        credit_variables = [15000, 15001, 15002, 15003, 15004]
        rates = []
        for i in rate_info:
            rates.append({"productId": i["product"]["id"], "credits": i["credits"],
                          "creditUnitTypeId": i["creditUnitType"]["id"]})
        payload = {
            "id": table_id,
            "name": table_info['name'],
            "rateAmounts": rates
        }
        for item in kwargs.keys():
            if item in rate_variables:
                if item == "credits":
                    kwargs[item] = float(kwargs[item])
                if item == "creditUnitTypeId":
                    if kwargs[item] > 15005 or kwargs[item] < 15000:
                        raise Exception("{} is not a valid credit unit type id. "
                                        "Please enter a valid credit unit type id".format(kwargs[item]))
                if product_id:
                    if product_id > len(rate_info):
                        raise Exception(
                            "{} is not a valid product id. Please enter a valid product id".format(product_id)
                        )
                    payload.update(
                        {
                            "rateAmounts"[product_id - 1]: payload["rateAmounts"][product_id - 1].update(
                                {item: kwargs[item]}
                            )
                        }
                    )
            payload.update({item: kwargs[item]})
        payload = json.dumps(payload)
        response = requests.request("PUT", url, headers=authorization, data=payload, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def DeleteTable(self, table_id):
        """
        **WARNING: Only one available rate table at this time (7/19/2022) DO NOT test this call with only available rate
        table**
        Function deletes a desired rate table
        Args:
            table_id (int) = Id of the desired rate table
        Returns:
            Success message upon deletion
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/accountservice/api/v1/ratetables/{}'.format(table_id)
        response = requests.request("DELETE", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return "Rate table {} successfully deleted".format(table_id)
