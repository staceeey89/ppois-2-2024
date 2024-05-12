class InformationBoard():
    def __init__(self, train_number: int, departure_station: str, departure_time: str,
                 arrival_station: str, arrival_time: str, travel_time: str):
        self._train_number: int = train_number
        self._departure_station: str = departure_station
        self._departure_time: str = departure_time
        self._arrival_station: str = arrival_station
        self._arrival_time: str = arrival_time
        self._travel_time: str = travel_time

    def __str__(self):
        print(self.train_number, self.departure_station, self.departure_time,
              self.arrival_station, self.arrival_time, self.travel_time)

    def get_list_of_data(self):
        row: list = []
        row.append(self._train_number)
        row.append(self._departure_station)
        row.append(self._departure_time)
        row.append(self._arrival_station)
        row.append(self._arrival_time)
        row.append(self._travel_time)
        return row