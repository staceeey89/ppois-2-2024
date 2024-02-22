import datetime
import json
import random

from config.constants import MAX_CRIMES_PER_DAY, EVENTS_PATH
from src.event import Event, Crime, Call
from src.law import Law
from src.officer import OfficerGenerator, Rank, Position


class Loader:
    def __init__(self):
        pass

    @staticmethod
    def load_officers(path):
        with open(path, 'r') as file:
            data = json.load(file)
        officers = []
        for i in data:
            officer = OfficerGenerator(i["name"],
                                       Position.from_string(i["position"]),
                                       Rank.from_string(i["rank"]),
                                       i["experience"],
                                       datetime.datetime(2024, 2, 20)
                                       )
            officers.append(officer)
        return officers

    @staticmethod
    def load_events(path):
        with open(path, 'r') as file:
            data = json.load(file)

        events = []
        crimes = []
        calls = []
        for item in data:
            if item['type'] == 'Event':
                event = Event(item['title'], item['description'], item['slots'])
                events.append(event)
            elif item['type'] == 'Crime':
                law_dict = item['law']
                law = Law(law_dict['name'], law_dict['jurisdiction'], law_dict['description'], law_dict['penalty'])
                crime = Crime(item['title'], item['description'], item['slots'], item['difficulty'], law)
                crimes.append(crime)
            elif item['type'] == 'Call':
                call = Call(item['title'], item['description'], item['slots'], item['difficulty'], item['address'])
                calls.append(call)
        return events, crimes, calls


class EventGenerator:
    def __init__(self):
        events, crimes, calls = Loader.load_events(EVENTS_PATH)
        self.crimes_counter = random.randint(0, MAX_CRIMES_PER_DAY)
        self.events = events
        self.crimes = crimes
        self.calls = calls

    def generate_duty_event(self):
        if self.crimes_counter > 0:
            self.crimes_counter -= 1
            return random.choice([self._generate_call_event(), self._generate_crime_event()])
        return self._generate_call_event()

    def generate_public_security_event(self):
        return random.choice(self.events)

    def _generate_crime_event(self):
        return random.choice(self.crimes)

    def _generate_call_event(self):
        return random.choice(self.calls)


def time_calculation(difficulty, officers: list):
    default_time_per_slot = {
        'easy': 1,
        'medium': 2,
        'hard': 3
    }

    total_time = 0

    for officer in officers:
        time_multiplier = officer.experience * officer.rank.value
        total_time += time_multiplier * 1 / default_time_per_slot[difficulty]

    return 84 * 1 / total_time
