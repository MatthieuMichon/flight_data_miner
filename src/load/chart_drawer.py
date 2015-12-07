#!/usr/bin/python3

"""
load.chart_drawer
~~~~~~~~~~~~~~~~~

This module outputs a given trail in graphic charts.
"""

import matplotlib.pyplot as plt
import math
import logging


class ChartDrawer:

    def __init__(self, coordinates, verbose=False):
        if verbose:
            logging.basicConfig(
                filename='ChartDrawer.log', level=logging.DEBUG)
        self.data = self.conv_ld_to_dl(ld=coordinates)
        self.plot_all(dict_lists=self.data)

    def conv_ld_to_dl(self, ld):
        dl = {}
        for dict_ in ld:
            for k in dict_.keys():
                if k in dl:
                    dl[k].append(dict_[k])
                else:
                    dl[k] = [dict_[k]]
        return dl

    def plot_all(self, dict_lists):
        fig = 1
        plt.figure(fig)
        for k, v in dict_lists.items():
            print(100*len(dict_lists) + 10 + fig)
            plt.subplot(100*len(dict_lists) + 10 + fig)
            plt.plot(v)
            fig += 1
        plt.show()


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
    cd = ChartDrawer(coordinates=trail, verbose=True)
    print(cd.data)

if __name__ == '__main__':
    main()
