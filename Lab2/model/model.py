import psycopg2 as ps
from psycopg2 import *
import datetime
from datetime import datetime
import re

class ModelBase:
    def __init__(self, host, dbname, user, password, port):
        if not port or not dbname or not user or not password:
            print("Ошибка: не все переменные окружения установлены корректно.")
            exit(1)

        try:
            self._connection = ps.connect(
                host=host,
                dbname=dbname,
                user=user,
                password=password,
                port=port
            )
            print("Успешное подключение к базе данных PostgreSQL")
            self._cursor = self._connection.cursor()

        except ps.Error as e:
            print(f"base open error: {e}")

    def create_table(self):
        medical_card = ''' 
            CREATE TABLE IF NOT EXISTS medical_cards(
                patient_surname VARCHAR(70),
                patient_name VARCHAR(70),
                registration_address VARCHAR(40),
                birthday_date date,
                appointment_date date,
                doctor_surname VARCHAR(70),
                doctor_name VARCHAR(70),
                doctor_statement VARCHAR(70)
            );
        '''

        self._cursor.execute(medical_card)
        self._connection.commit()

    def new_entry(self, entry: tuple):
        (patient_surname, patient_name, registration_address, birthday_date, appointment_date, doctor_surname,
         doctor_name, doctor_statement) = entry

        try:
            date_birth = datetime.strptime(birthday_date, '%m/%d/%y')
            date_birth = date_birth.replace(day=date_birth.day, month=date_birth.month)
            birthday_date = date_birth.date()
            print(date_birth)

            date_appointment = datetime.strptime(appointment_date, '%m/%d/%y')
            date_appointment = date_appointment.replace(day=date_appointment.day, month=date_appointment.month)
            appointment_date = date_appointment.date()
            print(date_appointment)
        except:
            pass

        request_to_insert_data = '''
        INSERT INTO medical_cards (patient_surname, patient_name, registration_address, birthday_date, appointment_date,
        doctor_surname, doctor_name, doctor_statement) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        self._cursor.execute(
            request_to_insert_data, (patient_surname, patient_name, registration_address, birthday_date,
                                     appointment_date, doctor_surname, doctor_name, doctor_statement)
        )
        self._connection.commit()

        '''request_to_read_data = "SELECT * FROM medical_cards"

        self._cursor.execute(request_to_read_data)
        data = self._cursor.fetchall()
        return data[-1]'''

    def loading(self, offset=0, limit=None):
        if limit is None:
            request_to_read_data = "SELECT * FROM medical_cards"
        else:
            request_to_read_data = f"SELECT * FROM medical_cards OFFSET {offset} LIMIT {limit}"

        self._cursor.execute(request_to_read_data)
        data = self._cursor.fetchall()
        return data

    def help_search(self, param):
        dist_request = f"SELECT DISTINCT {param} FROM medical_cards"
        self._cursor.execute(dist_request)
        data = self._cursor.fetchall()
        return data

    def search(self, num: int, searching1="", searching2=""):
        request_to_search = "SELECT * FROM medical_cards"
        match num:
            case 1:
                request_to_search = f"SELECT * FROM medical_cards WHERE patient_surname = '{searching1}' OR registration_address = '{searching2}';"
            case 2:
                request_to_search = f"SELECT * FROM medical_cards WHERE birthday_date = '{searching1}';"
            case 3:
                request_to_search = f"SELECT * FROM medical_cards WHERE doctor_name = '{searching1}' OR appointment_date = '{searching2}';"
        self._cursor.execute(request_to_search)
        data = self._cursor.fetchall()
        return data

    def delete(self, num: int, searching1="", searching2=""):
        request_to_delete = None
        match num:
            case 1:
                request_to_delete = f"DELETE FROM medical_cards WHERE patient_surname = '{searching1}' OR registration_address = '{searching2}';"
            case 2:
                request_to_delete = f"DELETE FROM medical_cards WHERE birthday_date = '{searching1}';"
            case 3:
                request_to_delete = f"DELETE FROM medical_cards WHERE doctor_name = '{searching1}' OR appointment_date = '{searching2}';"
        if request_to_delete:
            self._cursor.execute(request_to_delete)
            num_deleted = self._cursor.rowcount
            self._connection.commit()
            return num_deleted

    def check_surname_name(self, s: str):
        pattern = r'^[А-Я][а-я]+$'
        match = re.match(pattern, s)
        if match:
            pass
        else:
            raise Exception("Неправильно введены фамилия или имя")

    def check_registration(self, s: str):
        pattern = r'^ул\.[А-Я][а-я]+,\sд\.(?!0)\d+,\sкв\.(?!0)\d+$'
        match = re.match(pattern, s)
        if match:
            pass
        else:
            raise Exception("Неправильно введён адрес прописки\n\nПравильный вид \"ул.*, д.*, кв.*\"")

    def check_statement(self, s: str):
        pattern = r'^[А-Я]'
        match = re.match(pattern, s)
        if match:
            pass
        else:
            raise Exception("Неправильно введено заключение")

    def check_date(self, s: str):
        pattern = r'^([1-9]|[1][0-2])/([1-9]|[12][0-9]|3[01])/([0-9][0-9])$'
        match = re.match(pattern, s)
        if match:
            pass
        else:
            raise Exception("Неправильно введена дата")

    def clean_data_base(self):
        request_clean = "DELETE FROM medical_cards"
        self._cursor.execute(request_clean)
        self._connection.commit()

    def close_connection(self):
        self._cursor.close()
        self._connection.close()
