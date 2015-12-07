#!/usr/bin/python3


import logging
from pathlib import Path

from extract.geojson_reader import GeoJsonReader
from transform.scrubber import Scrubber
from load.chart_drawer import ChartDrawer


def get_file_contents(filename):
    p = Path('./../data')
    file_ = open(str(p / filename))
    return file_.read()


def main(verbose=False):
    logging.basicConfig(
                filename='main.log', level=logging.DEBUG)
    contents = get_file_contents('list.geo.json')
    greader = GeoJsonReader(verbose=verbose)
    greader.load_json(json_=contents)
    logging.debug('Loaded {} trails'.format(len(greader.trails)))
    trail = greader.trails[0]
    for pt in trail['points']:
        pt['alt'] = 10 * pt['alt']
    scrubber = Scrubber(trail)
    # print([pt for pt in scrubber.segments[0]])
    # print([pt for pt in scrubber.segments[1]])
    cd = ChartDrawer(scrubber.segments[2])


if __name__ == "__main__":
    main(verbose=True)
