class FilterCriteria:
    def __init__(self, train_id, departure_station, arrival_station, departure_datetime_start, departure_datetime_finish,
                 arrival_datetime_start, arrival_datetime_finish, travel_time_start, travel_time_finish):
        self.train_id = train_id
        self.departure_station = departure_station
        self.arrival_station = arrival_station
        self.departure_datetime_start = departure_datetime_start
        self.departure_datetime_finish = departure_datetime_finish
        self.arrival_datetime_start = arrival_datetime_start
        self.arrival_datetime_finish = arrival_datetime_finish
        self.travel_time_start = travel_time_start
        self.travel_time_finish = travel_time_finish
