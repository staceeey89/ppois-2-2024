import xml.etree.ElementTree as ET

from models.filter_criteria import FilterCriteria

from datetime import datetime


class XMLParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tree: ET.ElementTree = None
        self.root: ET.Element = None
        self.parse()

    def parse(self):
        try:
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()
        except FileNotFoundError:
            print("File not found.")
        except ET.ParseError as e:
            print("Error parsing XML:", e)

    def get_all_train_trips(self):
        result = []
        for event, elem in ET.iterparse(self.file_path, events=("start",)):
            if elem.tag == "train-trip":
                train_id_elem = elem.find("train-id")
                travel_time_elem = elem.find("travel-time")

                if train_id_elem is not None and travel_time_elem is not None:
                    train_id = int(train_id_elem.text)
                    departure_station = elem.find("departure-station").text if elem.find(
                        "departure-station") is not None else None
                    arrival_station = elem.find("arrival-station").text if elem.find(
                        "arrival-station") is not None else None
                    departure_datetime = elem.find("departure-datetime").text if elem.find(
                        "departure-datetime") is not None else None
                    arrival_datetime = elem.find("arrival-datetime").text if elem.find(
                        "arrival-datetime") is not None else None
                    travel_time = int(travel_time_elem.text)

                    current = (
                    train_id, departure_station, arrival_station, departure_datetime, arrival_datetime, travel_time)
                    result.append(current)

                elem.clear()
        return result

    def get_page_train_trips(self, page, page_size):
        result = []
        for elem in self.root.find("train-trips").findall("train-trip"):
            current = [int(elem.find("train-id").text), elem.find("departure-station").text,
                       elem.find("arrival-station").text, elem.find("departure-datetime").text,
                       elem.find("arrival-datetime").text, int(elem.find("travel-time").text)]
            result.append(tuple(current))
        return result[(page - 1) * page_size:page * page_size]

    def get_all_trains(self):
        result = []
        for elem in self.root.find("trains").findall("train"):
            current = [int(elem.get("id")), elem.text]
            result.append(tuple(current))
        return result

    def get_all_stations(self):
        result = []
        for elem in self.root.find("stations").findall("station"):
            current = [int(elem.get("id")), elem.text]
            result.append(tuple(current))
        return result

    def add_train_trip(self, train_trip):
        train_trip_root = self.root.find("train-trips")
        new_train_trip = ET.Element("train-trip")

        train_id = ET.SubElement(new_train_trip, "train-id")
        for train in self.get_all_trains():
            if train[1] == train_trip.train.name:
                train_id.text = str(train[0])
                break

        departure_station = ET.SubElement(new_train_trip, "departure-station")
        departure_station.text = train_trip.departure_station.city

        arrival_station = ET.SubElement(new_train_trip, "arrival-station")
        arrival_station.text = train_trip.arrival_station.city

        departure_datetime = ET.SubElement(new_train_trip, "departure-datetime")
        departure_datetime.text = train_trip.departure_datetime.strftime('%Y-%m-%d %H:%M:%S')

        arrival_datetime = ET.SubElement(new_train_trip, "arrival-datetime")
        arrival_datetime.text = train_trip.arrival_datetime.strftime('%Y-%m-%d %H:%M:%S')

        travel_time = ET.SubElement(new_train_trip, "travel-time")
        travel_time.text = str(((train_trip.arrival_datetime - train_trip.departure_datetime).seconds +
                            (train_trip.arrival_datetime - train_trip.departure_datetime).days * 24 * 60 * 60))

        train_trip_root.append(new_train_trip)

    def select_by_filter(self, filter_criteria: FilterCriteria):
        result = self.get_all_train_trips()
        if filter_criteria.train_id is not None:
            result = set(result) & set([elem for elem in result if elem[0] == filter_criteria.train_id])
        if filter_criteria.departure_station is not None:
            result = set(result) & set([elem for elem in result if elem[1] == filter_criteria.departure_station])
        if filter_criteria.arrival_station is not None:
            result = set(result) & set([elem for elem in result if elem[2] == filter_criteria.arrival_station])
        if filter_criteria.departure_datetime_start is not None and filter_criteria.departure_datetime_finish is not None:
            result = set(result) & set([elem for elem in result if filter_criteria.departure_datetime_start <= elem[3] <= filter_criteria.departure_datetime_finish])
        if filter_criteria.arrival_datetime_start is not None and filter_criteria.arrival_datetime_finish is not None:
            result = set(result) & set([elem for elem in result if filter_criteria.arrival_datetime_start <= elem[4] <= filter_criteria.arrival_datetime_finish])
        if filter_criteria.travel_time_start is not None and filter_criteria.travel_time_finish is not None:
            result = set(result) & set([elem for elem in result if filter_criteria.travel_time_start <= elem[5] <= filter_criteria.travel_time_finish])

        return list(result)

    def delete_by_filter(self, filter_criteria: FilterCriteria):
        elements_to_delete = [elem for elem in self.root.find("train-trips").findall("train-trip")]
        if filter_criteria.train_id is not None:
            elements_to_delete = set(elements_to_delete) & set([elem for elem in elements_to_delete if elem.find("train-id").text == str(filter_criteria.train_id)])
        if filter_criteria.departure_station is not None:
            elements_to_delete = set(elements_to_delete) & set([elem for elem in elements_to_delete if elem.find("departure-station").text == filter_criteria.departure_station])
        if filter_criteria.arrival_station is not None:
            elements_to_delete = set(elements_to_delete) & set([elem for elem in elements_to_delete if elem.find("arrival-station").text == filter_criteria.arrival_station])
        if filter_criteria.departure_datetime_start is not None and filter_criteria.departure_datetime_finish is not None:
            elements_to_delete = set(elements_to_delete) & set([elem for elem in elements_to_delete if datetime.strptime(filter_criteria.departure_datetime_start, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(elem.find("departure-datetime").text, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(filter_criteria.departure_datetime_finish, "%Y-%m-%d %H:%M:%S")])
        if filter_criteria.arrival_datetime_start is not None and filter_criteria.arrival_datetime_finish is not None:
            elements_to_delete = set(elements_to_delete) & set([elem for elem in elements_to_delete if datetime.strptime(filter_criteria.arrival_datetime_start, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(elem.find("departure-datetime").text, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(filter_criteria.arrival_datetime_finish, "%Y-%m-%d %H:%M:%S")])
        if filter_criteria.travel_time_start is not None and filter_criteria.travel_time_finish is not None:
            elements_to_delete = set(elements_to_delete) & set([elem for elem in elements_to_delete if filter_criteria.travel_time_start <= int(elem.find("travel-time").text) <= filter_criteria.travel_time_finish])

        for elem in elements_to_delete:
            self.root.find("train-trips").remove(elem)

        return len(elements_to_delete)

    def select_by_filter_page(self, filter_criteria, page, page_size):
        return self.select_by_filter(filter_criteria)[(page - 1) * page_size:page * page_size]

    def commit(self):
        self.tree.write(self.file_path)
