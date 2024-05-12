from datetime import datetime
from icalendar import Calendar, Event
from Presentation import Presentation
from Speaker import Speaker
class Conference:
    def __init__(self, name, location, start_date, end_date, max_participants, application_deadline, coffee_breaks, lunch_break):
        self.__name = name
        self.__location = location
        self.__start_date = start_date
        self.__end_date = end_date
        self.__max_participants = max_participants
        self.__application_deadline = application_deadline
        self.__coffee_breaks = coffee_breaks
        self.__lunch_break = lunch_break
        self.__participants = []
        self.__presentations = []

    def get_name(self):
        return self.__name

    def get_location(self):
        return self.__location

    def get_start_date(self):
        return self.__start_date

    def get_end_date(self):
        return self.__end_date

    def get_max_participants(self):
        return self.__max_participants

    def get_application_deadline(self):
        return self.__application_deadline

    def get_coffee_breaks(self):
        return self.__coffee_breaks

    def get_lunch_break(self):
        return self.__lunch_break

    def set_name(self, name):
        self.__name = name

    def set_location(self, location):
        self.__location = location

    def set_start_date(self, start_date):
        try:
            self.__start_date = start_date
        except ValueError:
            print("Ошибка: Дата начала должна быть объектом datetime.")

    def set_end_date(self, end_date):
        try:
            if end_date < self.__start_date:
                self.__end_date = end_date
        except ValueError:
            print("Дата окончания не может быть раньше даты начала.")
        except TypeError:
            print("Ошибка: Дата конца должна быть объектом datetime.")

    def set_max_participants(self, max_participants):
        try:
            self.__max_participants = max_participants
        except ValueError:
            print("Ошибка: Максимальное количество участников должно быть положительным целым числом.")

    def set_application_deadline(self, application_deadline):
        try:
            self.__application_deadline = application_deadline
        except ValueError:
            print("Ошибка: Срок подачи заявок должен быть объектом datetime.")

    def set_coffee_breaks(self, coffee_breaks):
        try:
            self.__coffee_breaks = coffee_breaks
        except ValueError:
            print("Ошибка: Перерывы на кофе должны быть списком кортежей (начальное_время, конечное_время).")

    def set_lunch_break(self, lunch_break):
        try:
            self.__lunch_break = lunch_break
        except ValueError:
            print("Ошибка: Перерыв на обед должен быть кортежем (начальное_время, конечное_время).")

    def add_presentation(self, title, speaker, topic):
        presentation = Presentation(title, speaker, topic)
        self.__presentations.append(presentation)

    def add_participant(self, participant):
        try:
            self.__participants.append(participant)
        except TypeError:
            print("Аргумент participant должен быть экземпляром класса Speaker.")

    def accept_application(self, participant):
        try:
            if datetime.now() > self.__application_deadline:
                print("Срок подачи заявок истек.")
                return
            if participant not in self.__participants:
                self.__participants.append(participant)
                print(f"Заявка от {participant.get_name()} принята.")
            else:
                print(f"{participant.get_name()} уже зарегистрирован.")
        except TypeError:
            print("Ошибка: Участник должен быть экземпляром класса Person.")

    def add_speaker(self, speaker):
        try:
            self.__participants.append(speaker)
            print(f"Спикер {speaker.get_name()} добавлен на конференцию.")
        except TypeError:
            print("Ошибка: Участник должен быть экземпляром класса Speaker.")

    def select_presentation(self, presentation):
        try:
            if any(p.get_topic() == presentation.get_topic() for p in self.__presentations):
                print(f"Тема '{presentation.get_topic()}' уже выбрана для другой презентации.")
                return
            if presentation.get_speaker().get_experience_level() < 'Сеньор':
                print(
                    f"Докладчик {presentation.get_speaker().get_name()} не имеет достаточного опыта или квалификации.")
                return
            self.__presentations.append(presentation)
            print(f"Презентация '{presentation.get_title()}' выбрана для конференции.")
        except TypeError:
            print("Ошибка: Презентация должна быть экземпляром класса Presentation.")

    def organize_program(self):
        print(f"{self.__name}: Организовываем программу конференции.")
        schedule = {}
        current_time = 9
        for presentation in sorted(self.__presentations, key=lambda p: p.get_speaker().get_preferred_time()):
            while any(start <= str(current_time) < end for start, end in self.__coffee_breaks) or (self.__lunch_break[0] <= str(current_time) < self.__lunch_break[1]):
                current_time += 1
            schedule[f"{current_time}:00 - {current_time+1}:00"] = presentation.get_title() + ", Спикер: " + presentation.get_speaker().get_name()
            current_time += 1
        return schedule

    def register_participant(self, participant):
        if len(self.__participants) < self.__max_participants:
            if participant in self.__participants:
                print(f"{participant.name} уже зарегистрирован на конференцию.")
            else:
                self.__participants.append(participant)
                print(f"{participant.name} зарегистрирован на конференцию.")
        else:
            print("Регистрация закрыта. Достигнуто максимальное количество участников.")

    def prepare_conference(self):
        print("Подготовка к конференции...")
        for presentation in self.__presentations:
            if presentation.get_speaker() not in self.__participants:
                print(f"Докладчик {presentation.get_speaker().get_name()} не зарегистрирован на конференцию.")
                return False
        if self.check_projector() is False or self.check_microphones() is False or self.check_sound_system() is False:
            print("Не все технические средства работают.")
            return False
        else:
            print("Все условия для начала конференции выполнены.")
            return True

    def conduct_conference(self):
        print(f"Проведение конференции '{self.__name}'...")
        if not self.prepare_conference():
            print("Конференция не может быть проведена из-за невыполнения некоторых условий.")
            return
        for time, presentation in self.organize_program().items():
            print(f"{time}: {presentation}")

    def check_projector(self):
        projector_status = input("Проектор работает? (true/false): ")
        if projector_status.lower() == 'true':
            print("Проектор работает.")
            return True
        else:
            print("Проектор не работает.")
            return False

    def check_microphones(self):
        microphones_status = input("Микрофоны работают? (true/false): ")
        if microphones_status.lower() == 'true':
            print("Микрофоны работают.")
            return True
        else:
            print("Микрофоны не работают.")
            return False

    def check_sound_system(self):
        sound_system_status = input("Звуковая система работает? (true/false): ")
        if sound_system_status.lower() == 'true':
            print("Звуковая система работает.")
            return True
        else:
            print("Звуковая система не работает.")
            return False

    def handle_unprepared_speaker(self, speaker):
        if self.can_reschedule_presentation(speaker):
            print(f"Презентация докладчика {speaker.get_name()} была перенесена.")
        elif self.can_replace_speaker(speaker):
            print(f"Докладчик {speaker.get_name()} был заменен.")
        else:
            self.cancel_presentation(speaker)
            print(f"Презентация докладчика {speaker.get_name()} была отменена.")

    def can_reschedule_presentation(self, speaker):
        free_slots = [slot for slot, presentation in self.organize_program().items() if presentation is None]
        if free_slots:
            print(f"Презентация докладчика {speaker.get_name()} может быть перенесена.")
            return True
        else:
            print(f"Нет свободных слотов для переноса презентации докладчика {speaker.get_name()}.")
            return False

    def can_replace_speaker(self, speaker):
        replacement_speakers = [p.get_speaker() for p in self.__presentations if p.get_speaker() != speaker and p.get_speaker().is_expert_on(speaker.get_presentation_topic())]
        if replacement_speakers:
            print(f"Докладчик {speaker.get_name()} может быть заменен.")
            return True
        else:
            print(f"Нет подходящих докладчиков для замены {speaker.get_name()}.")
            return False

    def cancel_presentation(self, speaker):
        speaker_name = input("Введите имя докладчика, чью презентацию вы хотите отменить: ")
        index_to_remove = None
        for i, presentation in enumerate(self.__presentations):
            if presentation.get_speaker().get_name() == speaker_name:
                index_to_remove = i
                break
        if index_to_remove is not None:
            removed_presentation = self.__presentations.pop(index_to_remove)
            print(f"Презентация '{removed_presentation.get_title()}' докладчика {speaker_name} была отменена.")
        else:
            print(f"Презентация докладчика {speaker_name} не была найдена.")

    def generate_icalendar(self):
        cal = Calendar()
        cal.add('prodid', '-//My Conference//Example//')
        cal.add('version', '2.0')

        for presentation in self.__presentations:
            event = Event()
            event.add('резюме', f"{presentation.speaker.name}: {presentation.title}")
            cal.add_component(event)

        with open('conference_schedule.ics', 'wb') as f:
            f.write(cal.to_ical())

    def collect_feedback(self):
        feedback = {}
        for presentation in self.__presentations:
            rating = input(
                f"Пожалуйста, оцените презентацию '{presentation.get_title()}' от {presentation.get_speaker().get_name()} (1-5): ")
            comment = input("Какие-то комментарии или предложения: ")
            feedback[presentation.get_title()] = {'оценка': rating, 'комментарий': comment}
        return feedback

    def notify_participants(self, message):
        for participant in self.__participants:
            print(f"Отправка сообщения {participant.get_name()}: {message}")