import requests, warnings, json
warnings.filterwarnings("ignore")
import Maxar_Portal_SDK.process as process

class Products:

    def __init__(self, auth):
        self.base_url = auth.base_url
        self.response = None
        self.version = auth.version
        self.auth = auth

    def get_products(self):
        """
        Gets a list of all products
        Returns a list of dictionaries
        """

        authorization = process.authorization(self.auth)
        url = "{}/accountservice/api/v1/products".format(self.base_url)
        response = requests.request("GET", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return response.json()

    def filter_products(self, productCategory=None, usageType=None, age=None, catalogType=None):
        """
        filters products based on args passed in
        Args:
        productCategory = Str of the product Category that you are looking for.
        usageType = Str Download or Streaming
        age = Str of the age of the product. ex [3,91)
        catalogType = String of the catalog that the product belongs to Archive or Online
        returns: List of dictionaries of the products that you are filtering for.
        """

        all_products = self.get_products(self.auth)
        self._paramater_checker(productCategory, usageType, catalogType)
        filtered_products = [i for i in all_products if
        (i['productCategory'].lower() == str(productCategory).lower() or not productCategory)
                     and (i['usageType'] == str(usageType) or not usageType)
                     and (i['age'] == str(age) or not age)
                     and (i['catalogType'] == str(catalogType).lower() or not catalogType)]
        return filtered_products

    def _paramater_checker(self,productCategory, usageType, catalogType):
        if productCategory:
            acceptable_productCategory = ['Vivid Basic Tile Cache', 'Vivid Basic', 'OSM Tiles', 'Vivid Standard',
                              'Vivid Advanced', 'Vivid Premium', 'Online Imagery', 'Archive Imagery',
                              'Radarsat-2', 'Base Mosaic/TerraColor']
        if productCategory not in acceptable_productCategory:
            raise Exception('Please input correct Product category. {}'.format(acceptable_productCategory))
        if usageType:
            usageTypes = ['Streaming', 'Download']
        if usageType not in usageTypes:
            raise Exception('Please enter acceptable UsageType. {}'.format(usageTypes))
        if catalogType:
            catalogTypes = ['Online', 'Archive']
        if catalogType not in catalogTypes:
            raise Exception('Please enter acceptable UsageType. {}'.format(catalogTypes))

    def create_products(self, catalogType, productName, productCategory, usageType, age=None):
        """
        Function creates a new product.
        Args:
        productCategory = Str of the product Category that you are looking for.
        usageType = Str Download or Streaming
        age = Str of the age of the product.  ex [3,91), defaults to null
        catalogType = String of the catalog that the product belongs to Archive or Online
        Returns a json response object.
        """

        authorization = process.authorization(self.auth)
        url = "{}/accountservice/api/v1/products".format(self.base_url)
        self._paramater_checker(productCategory, usageType, catalogType)
        code = 'PRODUCT_' + productName.replace(' ', '_').upper()
        payload = json.dumps({
        "age": age,
        "catalogType": "{}".format(catalogType),
        "code": "{}".format(code),
        "fullProductName": "{}".format(productName),
        "id": "",
        "productCategory": "{}".format(productCategory),
        "productCategoryCode": "{}".format(code),
        "usageType": '{}'.format(usageType)
        })
        response = requests.request("POST", url, headers=authorization, data=payload, verify=False)
        process_response = process._response_handler(response)
        return response.json()


    def delete_products(self,productId):
        """
        Function soft deletes a product by id
        Args
            productid= Str of the id of the product that you are deleting.
        Returns a server response status code.
        """

        authorization = process.authorization(self.auth)
        url = "{}/accountservice/api/v1/products/{}".format(self.base_url, productId)
        response = requests.request("DELETE", url, headers=authorization, verify=False)
        process_response = process._response_handler(response)
        return "Product {} successfully deleted".format(productId)

