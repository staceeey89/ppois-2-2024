from check_data_type import check_data_type


class GeoCoordinate:
    def __init__(self, geo_latitude: float, geo_longitude: float):

        if geo_latitude < 0.0 or geo_longitude < 0.0:
            raise ValueError("Negative degrees")

        if geo_latitude > 180 or geo_longitude > 180:
            raise ValueError("Wrong coordinate")

        self.geo_latitude = geo_latitude
        self.geo_longitude = geo_longitude
