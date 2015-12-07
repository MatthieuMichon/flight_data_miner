#!/usr/bin/python3

"""
extract.geojson_reader
~~~~~~~~~~~~~~~~~~~~~~

This module handles flight data represented as a list of positions in a format
compliant with the Geo JSON specification.

- longitude
- latitude
- altitude as well as a time in
seconds.
"""

import json
import logging


class GeoJsonReader:

    def __init__(self, verbose=False):
        if verbose:
            logging.basicConfig(
                filename='GeoJsonReader.log', level=logging.DEBUG)
        self.trails = []

    def map_coordinates(self, points):
        return [{
            'lon': point[0],
            'lat': point[1],
            'alt': point[2],
            'time': point[3],
            'gs': point[4]
            } for point in points]

    def load_feature(self, feature):
        retval = {}
        retval['metadata'] = feature['properties']
        retval['points'] = self.map_coordinates(
            feature['geometry']['coordinates'])
        logging.debug('Loaded {} points'.format(len(retval['points'])))
        return retval

    def load_json(self, json_):
        logging.debug('Decoding Geo JSON data, '
                      'size: {} bytes'.format(len(json_)))
        jdata = json.loads(json_)

        # Depending on the value of the 'type' element, the GeoJSON data may
        # either be a single LineString or a collection of LineString.
        if jdata['type'] == 'Feature':
            trail = self.load_feature(jdata)
            self.trails.append(trail)
        elif jdata['type'] == 'FeatureCollection':
            for feature in jdata['features']:
                if feature['type'] == 'Feature':
                    trail = self.load_feature(feature)
                    self.trails.append(trail)


def test(verbose):
    jdata = '''{"type": "Feature", "properties": \
    {"title": "NH216", "stroke": "#012"}, \
    "geometry": {"type": "LineString", "coordinates": \
    [[139.7726, 35.54811, 0, 1448349714, 9], \
    [139.77328, 35.54843, 0, 1448349699, 8], \
    [139.77411, 35.5489, 0, 1448349678, 25] \
    ]}}'''
    reader = GeoJsonReader(verbose=verbose)
    reader.load_json(json_=jdata)

    if not len(reader.trails):
        print('FAIL')

    print(reader.trails)

if __name__ == '__main__':
    test(verbose=True)
