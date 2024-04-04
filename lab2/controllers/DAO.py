import mysql.connector

from models.filter_criteria import FilterCriteria


class TrainTripDAO:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="dmitry",
            password="28D01d2005D",
            database="railway_depot_database"
        )
        self.train_dao = TrainDAO()
        self.station_dao = StationDAO()

    def __del__(self):
        self.connection.close()

    def insert(self, train_trip):
        train_id = self.train_dao.get_train_id_by_name(train_trip.train.name)
        departure_station_id = self.station_dao.get_station_id_by_city(train_trip.departure_station.city)
        arrival_station_id = self.station_dao.get_station_id_by_city(train_trip.arrival_station.city)
        arrival_datetime_string = "%s-%s-%s %s:%s:%s" % (
            train_trip.arrival_datetime.year,
            train_trip.arrival_datetime.month,
            train_trip.arrival_datetime.day,
            train_trip.arrival_datetime.hour,
            train_trip.arrival_datetime.minute,
            train_trip.arrival_datetime.second
        )
        departure_datetime_string = "%s-%s-%s %s:%s:%s" % (
            train_trip.departure_datetime.year,
            train_trip.departure_datetime.month,
            train_trip.departure_datetime.day,
            train_trip.departure_datetime.hour,
            train_trip.departure_datetime.minute,
            train_trip.departure_datetime.second
        )
        travel_time = ((train_trip.arrival_datetime - train_trip.departure_datetime).seconds +
                       (train_trip.arrival_datetime - train_trip.departure_datetime).days * 24 * 60 * 60)
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO train_trips(train_id, departure_station_id, arrival_station_id, "
                           "departure_datetime, arrival_datetime, travel_time) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" %
                           (train_id, departure_station_id, arrival_station_id, departure_datetime_string,
                            arrival_datetime_string, travel_time))
            self.connection.commit()

    def get_rows_count(self):
        with self.connection.cursor(buffered=True) as cursor:
            cursor.execute("SELECT trains.id AS train_id, stations_1.city AS departure_station, stations_2.city "
                           "AS arrival_station, train_trips.departure_datetime AS departure_datetime, "
                           "train_trips.arrival_datetime AS arrival_datetime, train_trips.travel_time "
                           "AS travel_time FROM train_trips JOIN stations AS stations_1 ON "
                           "stations_1.id = train_trips.departure_station_id JOIN stations AS stations_2 "
                           "ON stations_2.id = train_trips.arrival_station_id JOIN trains "
                           "ON trains.id = train_trips.train_id")
            row_count = cursor.rowcount
        return row_count

    def get_rows_count_by_filter(self, filter_criteria: FilterCriteria):
        with self.connection.cursor(buffered=True) as cursor:
            cursor.execute(self.build_students_select_query(filter_criteria))
            rows_count = cursor.rowcount

        return rows_count

    def get_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT trains.id AS train_id, stations_1.city AS departure_station, stations_2.city "
                           "AS arrival_station, train_trips.departure_datetime AS departure_datetime, "
                           "train_trips.arrival_datetime AS arrival_datetime, train_trips.travel_time "
                           "AS travel_time FROM train_trips JOIN stations AS stations_1 ON "
                           "stations_1.id = train_trips.departure_station_id JOIN stations AS stations_2 "
                           "ON stations_2.id = train_trips.arrival_station_id JOIN trains "
                           "ON trains.id = train_trips.train_id ORDER BY departure_datetime ASC")
            train_trips = cursor.fetchall()
        return train_trips

    def get_page(self, page_number, page_size):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT trains.id AS train_id, stations_1.city AS departure_station, stations_2.city "
                           "AS arrival_station, train_trips.departure_datetime AS departure_datetime, "
                           "train_trips.arrival_datetime AS arrival_datetime, train_trips.travel_time "
                           "AS travel_time FROM train_trips JOIN stations AS stations_1 ON "
                           "stations_1.id = train_trips.departure_station_id JOIN stations AS stations_2 "
                           "ON stations_2.id = train_trips.arrival_station_id JOIN trains "
                           "ON trains.id = train_trips.train_id ORDER BY departure_datetime ASC LIMIT %d OFFSET %d" %
                           (page_size, (page_number - 1) * page_size))
            train_trips = cursor.fetchall()
        return train_trips

    def delete_by_filter(self, filter_criteria: FilterCriteria):
        with self.connection.cursor() as cursor:
            cursor.execute(self.build_students_delete_query(filter_criteria))
            deleted_rows = cursor.rowcount
            self.connection.commit()
        return deleted_rows

    def select_by_filter(self, filter_criteria: FilterCriteria, page, page_size):
        with self.connection.cursor() as cursor:
            cursor.execute(self.build_students_select_query_with_page(filter_criteria, page, page_size))
            train_trips = cursor.fetchall()
        return train_trips

    def build_students_delete_query(self, filter_criteria: FilterCriteria):
        query = "DELETE FROM train_trips "
        is_where_statement_in_query = False

        if filter_criteria.train_id is not None:
            if is_where_statement_in_query:
                query += " AND train_id = %d" % filter_criteria.train_id
            else:
                query += " WHERE train_id = %d" % filter_criteria.train_id
                is_where_statement_in_query = True

        if filter_criteria.departure_station is not None:
            if is_where_statement_in_query:
                query += " AND departure_station_id = %d" % self.station_dao.get_station_id_by_city(filter_criteria.departure_station)
            else:
                query += " WHERE departure_station_id = %d" % self.station_dao.get_station_id_by_city(filter_criteria.departure_station)
                is_where_statement_in_query = True

        if filter_criteria.arrival_station is not None:
            if is_where_statement_in_query:
                query += " AND arrival_station_id = %d" % self.station_dao.get_station_id_by_city(filter_criteria.arrival_station)
            else:
                query += " WHERE arrival_station_id = %d" % self.station_dao.get_station_id_by_city(filter_criteria.arrival_station)
                is_where_statement_in_query = True

        if filter_criteria.departure_datetime_start is not None and filter_criteria.departure_datetime_finish is not None:
            if is_where_statement_in_query:
                query += " AND departure_datetime BETWEEN '%s' and '%s'" % (
                    filter_criteria.departure_datetime_start, filter_criteria.departure_datetime_finish)
            else:
                query += " WHERE departure_datetime BETWEEN '%s' and '%s'" % (
                    filter_criteria.departure_datetime_start, filter_criteria.departure_datetime_finish)
                is_where_statement_in_query = True

        if filter_criteria.arrival_datetime_start is not None and filter_criteria.arrival_datetime_finish is not None:
            if is_where_statement_in_query:
                query += " AND arrival_datetime BETWEEN '%s' and '%s'" % (
                    filter_criteria.arrival_datetime_start, filter_criteria.arrival_datetime_finish)
            else:
                query += " WHERE arrival_datetime BETWEEN '%s' and '%s'" % (
                    filter_criteria.arrival_datetime_start, filter_criteria.arrival_datetime_finish)
                is_where_statement_in_query = True

        if filter_criteria.travel_time_start is not None and filter_criteria.travel_time_finish is not None:
            if is_where_statement_in_query:
                query += " AND travel_time BETWEEN '%s' AND '%s'" % (filter_criteria.travel_time_start, filter_criteria.travel_time_finish)
            else:
                query += " WHERE travel_time BETWEEN '%s' AND '%s'" % (filter_criteria.travel_time_start, filter_criteria.travel_time_finish)

        return query

    def build_students_select_query_with_page(self, filter_criteria: FilterCriteria, page, page_size):
        query = self.build_students_select_query(filter_criteria)
        query += " ORDER BY departure_datetime ASC LIMIT %d OFFSET %d" % (page_size, page_size * (page - 1))
        return query

    def build_students_select_query(self, filter_criteria: FilterCriteria):
        query = ("SELECT trains.id AS train_id, stations_1.city AS departure_station, stations_2.city "
                           "AS arrival_station, train_trips.departure_datetime AS departure_datetime, "
                           "train_trips.arrival_datetime AS arrival_datetime, train_trips.travel_time "
                           "AS travel_time FROM train_trips JOIN stations AS stations_1 ON "
                           "stations_1.id = train_trips.departure_station_id JOIN stations AS stations_2 "
                           "ON stations_2.id = train_trips.arrival_station_id JOIN trains "
                           "ON trains.id = train_trips.train_id")
        is_where_statement_in_query = False

        if filter_criteria.train_id is not None:
            if is_where_statement_in_query:
                query += " AND train_id = %d" % filter_criteria.train_id
            else:
                query += " WHERE train_id = %d" % filter_criteria.train_id
                is_where_statement_in_query = True

        if filter_criteria.departure_station is not None:
            if is_where_statement_in_query:
                query += " AND departure_station_id = %d" % self.station_dao.get_station_id_by_city(filter_criteria.departure_station)
            else:
                query += " WHERE departure_station_id = %d" % self.station_dao.get_station_id_by_city(filter_criteria.departure_station)
                is_where_statement_in_query = True

        if filter_criteria.arrival_station is not None:
            if is_where_statement_in_query:
                query += " AND arrival_station_id = %d" % self.station_dao.get_station_id_by_city(filter_criteria.arrival_station)
            else:
                query += " WHERE arrival_station_id = %d" % self.station_dao.get_station_id_by_city(filter_criteria.arrival_station)
                is_where_statement_in_query = True

        if filter_criteria.departure_datetime_start is not None and filter_criteria.departure_datetime_finish is not None:
            if is_where_statement_in_query:
                query += " AND departure_datetime BETWEEN '%s' and '%s'" % (
                    filter_criteria.departure_datetime_start, filter_criteria.departure_datetime_finish)
            else:
                query += " WHERE departure_datetime BETWEEN '%s' and '%s'" % (
                    filter_criteria.departure_datetime_start, filter_criteria.departure_datetime_finish)
                is_where_statement_in_query = True

        if filter_criteria.arrival_datetime_start is not None and filter_criteria.arrival_datetime_finish is not None:
            if is_where_statement_in_query:
                query += " AND arrival_datetime BETWEEN '%s' and '%s'" % (
                    filter_criteria.arrival_datetime_start, filter_criteria.arrival_datetime_finish)
            else:
                query += " WHERE arrival_datetime BETWEEN '%s' and '%s'" % (
                    filter_criteria.arrival_datetime_start, filter_criteria.arrival_datetime_finish)
                is_where_statement_in_query = True

        if filter_criteria.travel_time_start is not None and filter_criteria.travel_time_finish is not None:
            if is_where_statement_in_query:
                query += " AND travel_time BETWEEN '%s' AND '%s'" % (filter_criteria.travel_time_start, filter_criteria.travel_time_finish)
            else:
                query += " WHERE travel_time BETWEEN '%s' AND '%s'" % (filter_criteria.travel_time_start, filter_criteria.travel_time_finish)

        return query


class TrainDAO:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="dmitry",
            password="28D01d2005D",
            database="railway_depot_database"
        )

    def get_train_id_by_name(self, name):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id FROM trains WHERE name = '%s'" % name)
            return cursor.fetchone()[0]

    def get_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM trains")
            return cursor.fetchall()


class StationDAO:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="dmitry",
            password="28D01d2005D",
            database="railway_depot_database"
        )

    def get_station_id_by_city(self, city):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM stations WHERE city = '%s'" % (city))
            return cursor.fetchone()[0]

    def get_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM stations")
            return cursor.fetchall()
