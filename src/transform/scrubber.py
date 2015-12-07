#!/usr/bin/python3

"""
transform.scrubber
~~~~~~~~~~~~~~~~~~

This module provides data cleansing methods.

A given set of points is analyzed, and separated in one or more list of points
if close enough to each other.
Each of those lists are then processed with individual points evaluated.
"""

import logging


class Scrubber:

    MAX_SEGMENT_TIMESTAMP_DIFF = 90
    REJECT_POINTS_ABOVE = 200

    def __init__(self, trail):
        logging.debug(
            'Scrubbing trail {}: found {} points'.format(
                trail['metadata']['title'], len(trail['points'])))
        self.metadata = trail['metadata']
        points = trail['points']
        points = self.sort_by_timestamp(points)
        segments = self.isolate_segments(points)
        segments = [self.rate_points(segment) for segment in segments]
        segments = [self.remove_weak_points(segment) for segment in segments]
        self.segments = segments

    def closest_neighbor(self, list_, index):
        list_len = len(list_)
        return min(
            abs(list_[(index+1) % list_len] - list_[index]),
            abs(list_[index] - list_[index-1]))

    def sort_by_timestamp(self, trail):
        return sorted(trail, key=lambda k: k['time'])

    def isolate_segments(self, points):
        """Converts a list of points into one or more segments depending on the
        time interval between groups of points"""
        timestamps = [pt['time'] for pt in points]

        # Assign a segment number for each point
        segment_indexes = [0] * len(timestamps)
        current_segment = 0
        for i in range(len(timestamps)):
            if i < (len(timestamps) - 1):
                if (timestamps[i+1] - timestamps[i] >
                        self.MAX_SEGMENT_TIMESTAMP_DIFF):
                    # New segment
                    current_segment += 1
            segment_indexes[i] = current_segment
        segment_count = current_segment

        segments = []
        for i in range(segment_count):
            # For each segment
            segments.append([points[j] for j in range(len(timestamps))
                             if segment_indexes[j] == i])
        return segments

    def rate_points(self, trail):
        """Apply a score against each individual points. The higher the score,
        the weaker the data quality.
        """
        timestamp_ratings = self.rate_timestamping(trail=trail)
        speed_ratings = self.rate_speed(trail=trail)
        altitude_ratings = self.rate_altitude(trail=trail)
        for i in range(len(trail)):
            trail[i]['rating'] = (
                timestamp_ratings[i] + speed_ratings[i] + altitude_ratings[i])
        return trail

    def rate_timestamping(self, trail):

        def rate_delay(delay):
            rating = [
                (15, 0), (30, 1), (45, 2), (60, 5),
                (90, 10), (120, 20), (3*60, 50), (4*60, 100),
                (6*60, 200), (8*60, 500), (12*60, 1000)]
            for rate in rating:
                if rate[0] > delay:
                    return rate[1]
            return 2000

        time_list = [point['time'] for point in trail]
        closest_point_time = [
            self.closest_neighbor(list_=time_list, index=i)
            for i in range(len(time_list))]
        ratings = [rate_delay(delay) for delay in closest_point_time]
        return ratings

    def rate_speed(self, trail):

        def rate_change(change):
            rating = [
                (5, 0),
                (10, 1),
                (20, 10),
                (50, 100),
                (100, 1000)]
            for rate in rating:
                if rate[0] > change:
                    return rate[1]
            return 2000

        speed_list = [point['gs'] for point in trail]
        smallest_speed_change_list = [
            self.closest_neighbor(list_=speed_list, index=i)
            for i in range(len(speed_list))]
        ratings = [rate_change(change)
                   for change in smallest_speed_change_list]
        return ratings

    def rate_altitude(self, trail):

        def rate_change(change):
            rating = [
                (5, 0),
                (10, 1),
                (20, 10),
                (50, 100),
                (100, 1000)]
            for rate in rating:
                if rate[0] > change:
                    return rate[1]
            return 2000

        altitude_list = [point['alt'] for point in trail]
        time_list = [point['time'] for point in trail]
        smallest_altitude_change_list = [
            self.closest_neighbor(list_=altitude_list, index=i)
            for i in range(len(altitude_list))]
        ratings = [rate_change(change)
                   for change in smallest_altitude_change_list]
        return ratings

    def remove_weak_points(self, trail):
        return [point for point in trail
                if point['rating'] <= self.REJECT_POINTS_ABOVE]
