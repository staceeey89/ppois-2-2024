import datetime
import random
import time
import src

from typing import List, Optional
from duty import Duty
from event import Event, Crime, Call
from investigation import Investigation
from officer import Officer
from public_security import PublicSecurity
from config.constants import DUTY_DURATION, WEEKEND
from utils.ccolors import ccolors
from utils.utils import EventGenerator


class Police:
    def __init__(self, city: str, chief_officer: str, officers: list):
        self.city = city
        self.chief_officer = chief_officer
        self.duty: Optional[Event, None] = None

        self.officer_list = officers
        self.active_cases: List[Investigation] = []

    def assign(self, officers: List[Officer], event: Optional[Event] = None, mandatory: bool = False) -> List[Officer]:
        selected_officers: List[Officer] = []
        dict_officers = {}
        counter = 1
        print(f"{ccolors.UNDERLINE}"
              f"№      Тип офицера       Имя                Звание              Опыт          Будет свободен"
              f"{ccolors.DEFAULT}")
        for officer in officers:
            if officer.unavailable_until > self.duty.timenow:
                print(ccolors.STRIKE + "{:<3} {}".format('', officer) + ccolors.DEFAULT)
            else:
                print("{:<3} {}".format(counter, officer))
                dict_officers[counter] = officer
                counter += 1

        while len(selected_officers) < len(dict_officers) and (not event or len(selected_officers) < event.slots):
            if mandatory:
                choice = int(input("Введите номер офицера: "))
            else:
                choice = int(input("Введите номер офицера, введите -1, чтобы закончить выбор: "))
                if choice == -1:
                    print("Офицеры отправлены")
                    break
            if 1 <= choice <= len(dict_officers) and (dict_officers[choice] not in self.duty.patrol):
                selected_officers.append(dict_officers[choice])
            else:
                print("Повторите ввод.")
                continue
        return selected_officers

    def prepare_duty(self, date: datetime):
        self.case_analysis()
        self.duty = Duty(date)
        print(f"{ccolors.WARNING}Вы начинаете смену {date}{ccolors.DEFAULT}\nсегодня офицеры нужны для:")
        event_generator = EventGenerator()
        patrol_event = event_generator.generate_public_security_event()

        patrol_list: List[Officer] = []
        for i in self.officer_list:
            if isinstance(i, src.officer.PatrolOfficer):
                patrol_list.append(i)

        detective_list = []
        for i in self.officer_list:
            if isinstance(i, src.officer.Detective):
                detective_list.append(i)

        print(patrol_event)
        print(f"Назначьте офицеров на патруль:")
        self.duty.patrol = self.assign(patrol_list, patrol_event, True)

        print(f"Назначьте детективов сегодня:")
        self.duty.detective = self.assign(detective_list)

        print(f"Назначьте офицеров, которые будут отвечать на вызовы:")
        public_security_list = list(set(patrol_list) - set(self.duty.patrol))
        self.duty.public_security_team = self.assign(public_security_list)

        print(self.duty)

    def penalty(self):
        print("Вызов проигнорирован.\n")
        self.duty.score -= 10

    def case_analysis(self):
        cases_to_remove = []
        for i in self.active_cases:
            if i.until < self.duty.timenow:
                print(i.report)
                cases_to_remove.append(i)
            elif i.until <= self.duty.timenow + datetime.timedelta(hours=DUTY_DURATION):
                print(f"Дело:\n{i}\n...будет передано в суд, детективы освободятся сегодня.)")
            else:
                print(f"Дело:\n{i}\n...ещё расследуется.\n")

        for i in cases_to_remove:
            self.active_cases.remove(i)

    def investigate(self, event: Crime):
        officers = self.duty.detective
        investigation = Investigation(event, self.assign(officers, event))
        if len(investigation.officers) == 0:
            self.penalty()
        else:
            investigation.investigate(self.duty.timenow)
            self.active_cases.append(investigation)

    def respond(self, event: Call):
        officers = self.duty.public_security_team
        public_security = PublicSecurity(event, self.assign(officers, event))
        if len(public_security.officers) == 0:
            self.penalty()
        else:
            public_security.public_security_operation(self.duty.timenow)
            self.duty.score += 10

    def on_duty(self):
        event_generator = EventGenerator()

        print(f"{ccolors.WARNING}Доброе утро, {self.chief_officer}."
              f"Ваша смена началась. {ccolors.DEFAULT} {self.duty.timenow}")
        duty_end = self.duty.timenow + datetime.timedelta(hours=DUTY_DURATION)
        time.sleep(random.randint(3, 5))
        while self.duty.timenow < duty_end:
            self.duty.timenow += datetime.timedelta(minutes=random.randint(15, 60))
            print("Текущее время: ", self.duty.timenow, "\nСчёт: ", self.duty.score, "\n")
            event = event_generator.generate_duty_event()
            print(event)

            if isinstance(event, src.event.Crime):
                self.investigate(event)
            elif isinstance(event, src.event.Call):
                self.respond(event)
            time.sleep(random.randint(3, 5))
        self.duty.timenow = duty_end

    def off_duty(self):
        print(f"{ccolors.FAIL}Смена закончена. Счёт: {self.duty.score}{ccolors.DEFAULT}")
        print(f"Счёт: {self.duty.score}")
        for i in self.duty.public_security_team:
            i.unavailable_until = self.duty.timenow + datetime.timedelta(days=WEEKEND, hours=-DUTY_DURATION)
