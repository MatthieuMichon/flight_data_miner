#!/usr/bin/python3

"""
load.geojson_writer
~~~~~~~~~~~~~~~~~~~

This module outputs a given trail in a format compatible with the Geo JSON
specifications.
"""


import json
import logging


class GeoJsonWriter:

    OPTIONNAL_ELEMENTS = ['alt', 'time', 'gs', 'rating']

    def __init__(self, properties, coordinates, verbose=False):
        """
        coordinates must included 'lat' and 'lon'
        """
        if verbose:
            logging.basicConfig(
                filename='GeoJsonReader.log', level=logging.DEBUG)
        self.data = self.generate_feature(
            properties=properties, coordinates=coordinates)
        self.json_ = json.dumps(self.data)

    def generate_feature(self, properties, coordinates):
        feature = {}
        feature['properties'] = properties
        feature['geometry'] = {
            'type': 'LineString',
            'coordinates': self.convert_coordinates(coordinates=coordinates)
        }

        return feature

    def convert_coordinates(self, coordinates):

        def point_dict_list(coordinates):
            list_ = []
            list_.extend([coordinates['lon'], coordinates['lat']])
            for element in self.OPTIONNAL_ELEMENTS:
                if element in coordinates:
                    list_.append(coordinates[element])
            return list_

        return [point_dict_list(point) for point in coordinates]


def main():
    trail = [
        {'lon': 2.53929, 'lat': 49.01516,
         'rating': 1, 'alt': 0, 'gs': 10, 'time': 1447961252},
        {'lon': 2.53953, 'lat': 49.01515,
         'rating': 1, 'alt': 0, 'gs': 9, 'time': 1447961269},
        {'lon': 2.53978, 'lat': 49.01508,
         'rating': 2, 'alt': 0, 'gs': 2, 'time': 1447961291},
        {'lon': 2.53994, 'lat': 49.01487,
         'rating': 1, 'alt': 0, 'gs': 9, 'time': 1447961318}
    ]
    properties = {'title': 'test'}
    gjw = GeoJsonWriter(properties=properties, coordinates=trail, verbose=True)
    print(gjw.json_)

if __name__ == '__main__':
    main()
