from geo_coordinate import GeoCoordinate
from speed_of_movement import SpeedOfMovement


class Path:
    def __init__(self, coordinate_start: GeoCoordinate, coordinate_finish: GeoCoordinate):

        self.coordinate_start = coordinate_start
        self.coordinate_finish = coordinate_finish

        self.distance = (coordinate_start.geo_latitude-coordinate_finish.geo_longitude+360)*20

        self.time_movement_on_foot = self.distance / SpeedOfMovement.on_foot
        self.time_movement_on_bike = self.distance / SpeedOfMovement.on_bike
        self.time_movement_on_bus = self.distance / SpeedOfMovement.on_bus
        self.time_movement_on_motorbike = self.distance / SpeedOfMovement.on_motorbike
        self.time_movement_on_car = self.distance / SpeedOfMovement.on_car
