import requests
import Maxar_Portal_SDK.process as process


class WMS:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = auth.base_url + "/geoserver/wms"
        self.response = None
        self.version = auth.version
        self.querystring = self._init_querystring()


    def return_image(self, **kwargs):
        """
        Function finds the imagery matching a bbox or feature id
        Kwargs:
            bbox = String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            filter = CQL filter used to refine data of search.
            height = Integer value representing the vertical number of pixels to return
            width = Integer value representing the horizontal number of pixels to return
            layers = String representing the called upon layer. Defaults to 'DigitalGlobe:Imagery'
            format = String of the format of the response image either jpeg, png or geotiff
            featureprofile = String of the desired stacking profile. Defaults to account Default
        Returns:
            requests response object of desired image
        """
        #Get Authorization
        token = self.auth.refresh_token()
        authorization = {'Authorization': 'Bearer {}'.format(token)}

        self.querystring = self._init_querystring()
        keys = list(kwargs.keys())
        if 'bbox' in keys:
            process._validate_bbox(kwargs['bbox'])
            if 'EPSG:3857' in kwargs['bbox']:
                self.querystring.update({'crs': 'EPSG:3857'})
                bbox_list = [i for i in kwargs['bbox'].split(',')]
                kwargs['bbox'] = ",".join([bbox_list[1], bbox_list[0], bbox_list[3], bbox_list[2], bbox_list[4]])
            self.querystring.update({'bbox': kwargs['bbox']})
        else:
            raise Exception('Search function must have a BBOX.')
        if 'filter' in keys:
            self.querystring.update({'cql_filter': kwargs['filter']})
            del (kwargs['filter'])
        for key, value in kwargs.items():
            self.querystring[key] = value
        request = requests.get(self.base_url, headers=authorization, params=self.querystring, verify=self.auth.SSL)
        self.response = request
        return process._response_handler(self.response)

    def _init_querystring(self):
        querystring = {'service': 'WMS',
                       'request': 'GetMap',
                       'version': '1.3.0',
                       'crs': 'EPSG:4326',
                       'height': '512',
                       'width': '512',
                       'layers': 'Maxar:Imagery',
                       'format': 'image/jpeg',
                       'SDKversion': '{}'.format(self.version)
                       }
        return querystring
