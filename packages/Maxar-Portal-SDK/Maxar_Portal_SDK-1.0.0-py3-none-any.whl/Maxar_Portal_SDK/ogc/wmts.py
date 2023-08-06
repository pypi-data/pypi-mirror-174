import requests
import MPS_Portal_SDK.process as process
from pyproj import Proj, transform
import math


class WMTS:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = auth.base_url + "/geoserver/gwc/service/wmts"
        self.response = None
        self.version = auth.version
        self.querystring = self._init_querystring()

    def wmts_convert(self, zoom_level, laty, longx, crs=None):
        """
        Function converts a lat long position to the tile column and row needed to return WMTS imagery over the area
        Args:
            zoom_level: Integer value of the desired zoom level
            laty: Integer value of the latitude
            longx: Integer value of the desired longitude
        Returns:
            String values of the Tile Row and the Tile Column
        """
        if crs == '4326' or not crs:
            querystring = self.querystring
            # GetCapablities call structure changed from SW2 to SW3, hardcoded TileMatrixSets instead of restructuring
            # the XML parser
            TileMatrixSet = {0: {'MatrixWidth': 2, 'MatrixHeight': 1}, 1: {'MatrixWidth': 4, 'MatrixHeight': 2}, 3:
                {'MatrixWidth': 16, 'MatrixHeight': 8}, 4: {'MatrixWidth': 32, 'MatrixHeight': 16}, 5:
                {'MatrixWidth': 64, 'MatrixHeight': 32}, 6: {'MatrixWidth': 128, 'MatrixHeight': 64}, 7:
                {'MatrixWidth': 256, 'MatrixHeight': 128}, 8: {'MatrixWidth': 512, 'MatrixHeight': 256}, 9:
                {'MatrixWidth': 1024, 'MatrixHeight': 512}, 10: {'MatrixWidth': 2048, 'MatrixHeight': 1024}, 11:
                {'MatrixWidth': 4096, 'MatrixHeight': 2048}, 12: {'MatrixWidth': 8192, 'MatrixHeight': 4096}, 13:
                {'MatrixWidth': 16384, 'MatrixHeight': 8192}, 14: {'MatrixWidth': 32769, 'MatrixHeight': 16384}, 15:
                {'MatrixWidth': 65536, 'MatrixHeight': 32768}, 16: {'MatrixWidth': 131072, 'MatrixHeight': 65536}, 17:
                {'MatrixWidth': 262144, 'MatrixHeight': 131072}, 18: {'MatrixWidth': 524288, 'MatrixHeight': 262144}, 19:
                {'MatrixWidth': 1048576, 'MatrixHeight': 524288}, 20: {'MatrixWidth': 2097152, 'MatrixHeight': 1048576}, 21:
                {'MatrixWidth': 4194304, 'MatrixHeight': 2097152}}

            for i in TileMatrixSet:
                if i == zoom_level:
                    matrixwidth = TileMatrixSet[i]['MatrixWidth']
                    matrixheight = TileMatrixSet[i]['MatrixHeight']
            if not matrixwidth or not matrixheight:
                raise Exception('Unable to determine Matrix dimensions from input coordinates')

            return str(round((float(longx) + 180) * (int(matrixwidth)/360))), str(round((90 - float(laty)) * (int(matrixheight)/180)))
        else:
            inProj = Proj(init='epsg:3857')
            outProj = Proj(init='epsg:4326')
            x2, y2 = transform(inProj, outProj, longx, laty)

            def deg2num(lat_deg, lon_deg, zoom):
                lat_rad = math.radians(lat_deg)
                n = 2.0 ** zoom
                xtile = int((lon_deg + 180.0) / 360.0 * n)
                ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
                return (str(xtile), str(ytile))

            tiles = deg2num(y2, x2, zoom_level)
            return tiles

    def wmts_get_tile(self, tilerow, tilecol, zoom_level, **kwargs):
        """
        Function executes the wmts call and returns a response object of the desired tile
        Args:
            tilerow: String value of the tile row.
            tilecol: String value of the tile column
            zoom_level: Integer value of the desired zoom level
        Returns:
            WMTS tiles for the input data
        """
        token = self.auth.refresh_token()
        authorization = {'Authorization': 'Bearer {}'.format(token)}

        querystring = self.querystring
        querystring['TileMatrix'] = querystring['TileMatrixSet'] + ':' + str(zoom_level)
        querystring['tilerow'] = tilerow
        querystring['tilecol'] = tilecol
        querystring['request'] = 'GetTile'
        response = requests.request("GET", self.base_url, headers=authorization, params=self.querystring, verify=self.auth.SSL)
        process_response = process._response_handler(response)
        return process_response

    def wmts_bbox_get_tile_list(self, zoom_level, bbox, **kwargs):
        """
        Function takes in a bbox and zoom level to return a list of WMTS calls that can be used to aquire all the wmts
        tiles. Projection defaults to EPSG:4326
        Args:
            zoom_level: Integer value of the desired zoom level
            bbox: String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
        Returns:
            List of WMTS calls.
        """

        process._validate_bbox(bbox)
        bbox_list = [i for i in bbox.split(',')]
        if len(bbox_list) == 4:
            miny = float(bbox_list[0])
            minx = float(bbox_list[1])
            maxy = float(bbox_list[2])
            maxx = float(bbox_list[3])
            crs = '4326'
        else:
            miny = float(bbox_list[0])
            minx = float(bbox_list[1])
            maxy = float(bbox_list[2])
            maxx = float(bbox_list[3])
            crs = '3857'

        min_tilerow, min_tilecol = self.wmts_convert(zoom_level, miny, minx, crs)
        max_tilerow, max_tilecol = self.wmts_convert(zoom_level, maxy, maxx, crs)

        if max_tilerow < min_tilerow:
            swap = max_tilerow
            max_tilerow = min_tilerow
            min_tilerow = swap
        if max_tilecol < min_tilecol:
            swap = max_tilecol
            max_tilecol = min_tilecol
            min_tilecol = swap
        tiles = []
        row_col = []

        for i in range(int(min_tilecol), int(max_tilecol) + 1):
            for j in range(int(min_tilerow), int(max_tilerow) + 1):
                querystring = self.querystring
                querystring['request'] = 'GetTile'
                querystring['TileMatrixSet'] = 'EPSG:' + crs
                querystring['TileMatrix'] = querystring['TileMatrixSet'] + ':' + str(zoom_level)
                querystring['TileRow'] = i
                querystring['TileCol'] = j
                tiles.append(self.base_url + '?' + "&".join("{}={}".format(key, value) for key,value in querystring.items()))
                row_col.append((querystring['TileRow'], querystring['TileCol'], zoom_level))
        combined = [tiles, row_col]
        return combined

    def _init_querystring(self):
        querystring = {
                       'service': 'WMTS',
                       'request': 'GetTile',
                       'version': '1.0.0',
                       'TileMatrixSet': 'EPSG:4326',
                       'Layer': 'Maxar:Imagery',
                       'Format': 'image/jpeg',
                       'SDKversion': '{}'.format(self.version)
                       }
        return querystring

