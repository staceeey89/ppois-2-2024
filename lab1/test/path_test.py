import unittest
from geo_coordinate import GeoCoordinate
from speed_of_movement import SpeedOfMovement
from path import Path


class TestPath(unittest.TestCase):

    def test_init(self):
        start = GeoCoordinate(40.7128, 74.0060)
        finish = GeoCoordinate(34.0522, 118.2437)
        path = Path(start, finish)

        self.assertEqual(path.coordinate_start, start)
        self.assertEqual(path.coordinate_finish, finish)

        expected_distance = (start.geo_latitude - finish.geo_longitude + 360) * 20
        self.assertEqual(path.distance, expected_distance)

        expected_time_on_foot = expected_distance / SpeedOfMovement.on_foot
        self.assertEqual(path.time_movement_on_foot, expected_time_on_foot)

        expected_time_on_bike = expected_distance / SpeedOfMovement.on_bike
        self.assertEqual(path.time_movement_on_bike, expected_time_on_bike)

        expected_time_on_bus = expected_distance / SpeedOfMovement.on_bus
        self.assertEqual(path.time_movement_on_bus, expected_time_on_bus)

        expected_time_on_motorbike = expected_distance / SpeedOfMovement.on_motorbike
        self.assertEqual(path.time_movement_on_motorbike, expected_time_on_motorbike)

        expected_time_on_car = expected_distance / SpeedOfMovement.on_car
        self.assertEqual(path.time_movement_on_car, expected_time_on_car)


if __name__ == '__main__':
    unittest.main()
