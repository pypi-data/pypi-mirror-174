import requests
import MPS_Portal_SDK.process as process


class WFS:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = auth.base_url + "/geoserver/wfs"
        self.response = None
        self.version = auth.version
        self.querystring = self._init_querystring()

    def search(self, typename='FinishedFeature',  **kwargs):
        """
        Function searches using the wfs method.
        Args:
            typename = String of the typename. Defaults to 'FinishedFeature'. Example input 'MaxarCatalogMosaicProducts'
        Kwargs:
            bbox = String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            filter = CQL filter used to refine data of search.
            outputformat = String of the format of the response object. Defaults to json.
            featureprofile = String of the desired stacking profile. Defaults to account Default
            typename = String of the typename. Defaults to FinishedFeature. Example input MaxarCatalogMosaicProducts
            srsname (string) = Desired projection. Defaults to EPSG:4326
        Returns:
            Response object of the search
        """

        token = self.auth.refresh_token()
        authorization = {'Authorization': 'Bearer {}'.format(token)}
        self.querystring = self._init_querystring()
        process._check_typeName(typename)
        self.querystring.update({'typenames': 'Maxar:{}'.format(typename)})
        keys = list(kwargs.keys())
        if 'filter' in keys and kwargs['filter']:
            if 'bbox' in keys and kwargs['bbox']:
                if "EPSG:3857" in kwargs['bbox']:
                    process._validate_bbox(kwargs['bbox'])
                    bbox_list = [i for i in kwargs['bbox'].split(',')]
                    kwargs['bbox'] = ",".join([bbox_list[1], bbox_list[0], bbox_list[3], bbox_list[2], bbox_list[4]])
                    kwargs['bbox'] = kwargs['bbox'].replace(",EPSG:3857", ",'EPSG:3857'")
                    self._combine_bbox_and_filter(kwargs['filter'], kwargs['bbox'], typename)
                    self.querystring['srsname'] = "EPSG:3857"
                    del (kwargs['filter'])
                    del (kwargs['bbox'])
                else:
                    process._validate_bbox(kwargs['bbox'])
                    self._combine_bbox_and_filter(kwargs['filter'], kwargs['bbox'], typename)
                    del(kwargs['filter'])
                    del(kwargs['bbox'])
            else:
                if "EPSG:3857" in kwargs['filter']:
                    self.querystring['srsname'] = "EPSG:3857"
                self.querystring.update({'cql_filter': kwargs['filter']})
                del (kwargs['filter'])
                if 'srsname' in kwargs.keys():
                    self.querystring['srsname'] = kwargs['srsname']
        elif kwargs['bbox']:
            process._validate_bbox(kwargs['bbox'])
            if "EPSG:3857" in kwargs['bbox']:
                bbox_list = [i for i in kwargs['bbox'].split(',')]
                kwargs['bbox'] = ",".join([bbox_list[1], bbox_list[0], bbox_list[3], bbox_list[2], bbox_list[4]])
                self.querystring['srsname'] = "EPSG:3857"
            self.querystring.update({'bbox': kwargs['bbox']})
        elif 'request' in keys:
            if kwargs['request'] == 'DescribeFeatureType':
                self.querystring.update({'request': kwargs['request']})
                del(kwargs['filter'])
                del(kwargs['bbox'])
                del(self.querystring['outputformat'])
        else:
            raise Exception('Search function must have a BBOX or a Filter.')
        for key, value in kwargs.items():
            self.querystring[key] = value

        query_string = process._remove_cache(self.querystring)
        request = requests.get(self.base_url, headers=authorization, params=query_string, verify=self.auth.SSL)
        self.response = request
        return process._response_handler(self.response)

    def _combine_bbox_and_filter(self, filter, bbox, typename):

        # if 'MaxarCatalogMosaic' in typename:
        #     bbox_geometry = 'BBOX(shape,{})'.format(bbox)
        #     combined_filter = bbox_geometry + 'AND' + '(' + filter + ')'
        # else:
        bbox_geometry = 'BBOX(featureGeometry,{})'.format(bbox)
        combined_filter = bbox_geometry + 'AND' + '(' + filter + ')'
        self.querystring.update({'cql_filter': filter})
        self.querystring.update({'cql_filter': combined_filter})

    def _init_querystring(self):
        querystring = {
                       'service': 'WFS',
                       'request': 'GetFeature',
                       'typenames': 'Maxar:FinishedFeature',
                       'version': '1.1.0',
                       'srsname': 'EPSG:4326',
                       'outputformat': 'json',
                       'SDKversion' : '{}'.format(self.version)
                       }
        return querystring
