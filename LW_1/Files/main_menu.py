from datetime import datetime
from Speaker import Speaker
from Conference import Conference
from Presentation import Presentation
import re

class ConferenceCLI:
    def __init__(self):
        self.conference = None
        self.speakers = {}
        self.presentations = {}

    def help_menu(self):
        print("""
Доступные команды:
- help: Показать список команд
- create_conference: Создать конференцию
- show_info: Показать информацию о конференции
- add_participant: Зарегистрировать участника
- add_presentation: Добавить презентацию на конференцию для докладчика
- generate_schedule: Сгенерировать программу конференции
- prepare_conference: Подготовить конференцию
- conduct_conference: Провести конференцию
- collect_feedback: Собрать обратную связь о презентациях
- notify_participants <сообщение>: Отправить уведомление всем участникам
- exit: Выйти из программы
        """)

    def show_info(self):
        if not self.conference:
            print("Конференция не создана. Используйте команду create_conference для создания.")
            return
        conference = self.conference
        print(f"""
Название: {conference.get_name()}
Местоположение: {conference.get_location()}
Дата начала: {conference.get_start_date()}
Дата окончания: {conference.get_end_date()}
Максимальное количество участников: {conference.get_max_participants()}
Срок подачи заявок: {conference.get_application_deadline()}
Перерывы на кофе: {conference.get_coffee_breaks()}
Перерыв на обед: {conference.get_lunch_break()}
        """)

    def create_conference(self):
        name = input("Введите название конференции: ")
        location = input("Введите местоположение конференции: ")

        while True:
            try:
                start_date = datetime.strptime(input("Введите дату начала конференции в формате ГГГГ-ММ-ДД: "),
                                               "%Y-%m-%d")
                break
            except ValueError:
                print("Ошибка: Неверный формат даты. Попробуйте еще раз.")

        while True:
            try:
                end_date = datetime.strptime(input("Введите дату окончания конференции в формате ГГГГ-ММ-ДД: "),
                                             "%Y-%m-%d")
                if end_date < start_date:
                    print("Ошибка: Дата окончания не может быть раньше даты начала.")
                else:
                    break
            except ValueError:
                print("Ошибка: Неверный формат даты. Попробуйте еще раз.")

        while True:
            try:
                max_participants = int(input("Введите максимальное количество участников: "))
                if max_participants <= 0:
                    raise ValueError("Ошибка: Максимальное количество участников должно быть положительным числом.")
                break
            except ValueError as e:
                print(e)

        while True:
            try:
                application_deadline = datetime.strptime(input("Введите срок подачи заявок в формате ГГГГ-ММ-ДД: "),
                                                         "%Y-%m-%d")
                if application_deadline > start_date:
                    print("Ошибка: Срок подачи заявок не может быть позже начала конференции.")
                else:
                    break
            except ValueError:
                print("Ошибка: Неверный формат даты. Попробуйте еще раз.")

        while True:
            try:
                coffee_break_start = input("Введите время начала перерыва на кофе (часы:минуты): ")
                coffee_break_end = input("Введите время окончания перерыва на кофе (часы:минуты): ")

                if re.match(r"\d{1,2}:\d{2}", coffee_break_start) and re.match(r"\d{1,2}:\d{2}", coffee_break_end):
                    if coffee_break_start < coffee_break_end:
                        coffee_breaks = [(coffee_break_start, coffee_break_end)]
                        break
                    else:
                        raise ValueError("Ошибка: Время окончания перерыва должно быть позже времени начала.")
                else:
                    raise ValueError("Неверный формат времени.")
            except ValueError as e:
                print(e)

        while True:
            try:
                lunch_break_start = input("Введите время начала перерыва на обед (часы:минуты): ")
                lunch_break_end = input("Введите время окончания перерыва на обед (часы:минуты): ")

                if re.match(r"\d{1,2}:\d{2}", lunch_break_start) and re.match(r"\d{1,2}:\d{2}", lunch_break_end):
                    if lunch_break_start < lunch_break_end:
                        lunch_break = (lunch_break_start, lunch_break_end)
                        break
                    else:
                        raise ValueError("Ошибка: Время окончания перерыва должно быть позже времени начала.")
                else:
                    raise ValueError("Неверный формат времени.")
            except ValueError as e:
                print(e)

        self.conference = Conference(name, location, start_date, end_date, max_participants, application_deadline, coffee_breaks, lunch_break)

    def add_participant(self):
        if not self.conference:
            print("Конференция не создана. Используйте команду create_conference для создания.")
            return
        name = input("Введите ФИО докладчика: ")
        affiliation = input("Введите место работы: ")
        presentation_topic = input("Введите тему докладчика: ")
        while True:
            try:
                experience_level = input("Введите квалификацию докладчика ('Джуниор', 'Мидл' или 'Сеньор'): ")
                if experience_level not in ['Джуниор', 'Мидл', 'Сеньор']:
                    raise ValueError("Ошибка: Введите один из вариантов: 'Джуниор', 'Мидл' или 'Сеньор'.")
                break
            except ValueError as e:
                print(e)

        while True:
            try:
                preferred_time = input("Введите предпочтительное время выступления ('Утро', 'День', 'Вечер'): ")
                if preferred_time not in ['Утро', 'День', 'Вечер']:
                    raise ValueError("Ошибка: Введите один из вариантов: 'Утро', 'День' или 'Вечер'.")
                break
            except ValueError as e:
                print(e)

        speaker = Speaker(name, affiliation, presentation_topic, experience_level, preferred_time)
        self.conference.add_participant(speaker)
        self.speakers[name] = speaker
        print("Докладчик добавлен.")

    def add_presentation(self):
        if not self.conference:
            print("Конференция не создана. Используйте команду create_conference для создания.")
            return

        if not self.speakers:
            print("Нет докладчика. Используйте команду add_participant для создания.")
            return

        title = input("Введите название презентации: ")
        topic = input("Введите тему презентации: ")

        print("Доступные докладчики:")
        for index, speaker_name in enumerate(self.speakers.keys(), 1):
            print(f"{index}. {speaker_name}")

        while True:
            choice = input("Выберите докладчика по порядковому номеру: ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.speakers):
                break
            else:
                print("Неверный выбор. Введите число от 1 до", len(self.speakers))

        selected_speaker_name = list(self.speakers.keys())[int(choice) - 1]
        speaker = self.speakers[selected_speaker_name]
        presentation = Presentation(title, speaker, topic)
        self.presentations[title] = presentation
        self.conference.add_presentation(title, speaker, topic)
        print("Презентация добавлена.")

    def generate_schedule(self):
        if not self.conference:
            print("Конференция не создана. Используйте команду create_conference для создания.")
            return
        if not self.speakers:
            print("Нет докладчика. Используйте команду add_participant для создания.")
            return
        if not self.presentations:
            print("Нет презентации у докладчика. Используйте команду add_presentationc для создания.")
            return
        schedule = self.conference.organize_program()
        print("Программа конференции:")
        for time, presentation in schedule.items():
            print(f"{time}: {presentation}")

    def prepare_conference(self):
        if not self.conference:
            print("Конференция не создана. Используйте команду create_conference для создания.")
            return
        if not self.speakers:
            print("Нет докладчика. Используйте команду add_participant для создания.")
            return
        if not self.presentations:
            print("Нет презентации у докладчика. Используйте команду add_presentationc для создания.")
            return
        if self.conference.prepare_conference():
            print("Конференция готова к проведению.")
        else:
            print("Подготовка конференции не завершена из-за невыполнения некоторых условий.")

    def conduct_conference(self):
        if not self.conference:
            print("Конференция не создана. Используйте команду create_conference для создания.")
            return
        if not self.speakers:
            print("Нет докладчика. Используйте команду add_participant для создания.")
            return
        if not self.presentations:
            print("Нет презентации у докладчика. Используйте команду add_presentationc для создания.")
            return
        self.conference.conduct_conference()

    def collect_feedback(self):
        if not self.conference:
            print("Конференция не создана. Используйте команду create_conference для создания.")
            return
        if not self.speakers:
            print("Нет докладчика. Используйте команду add_participant для создания.")
            return
        if not self.presentations:
            print("Нет презентации у докладчика. Используйте команду add_presentationc для создания.")
            return
        feedback = self.conference.collect_feedback()
        print("Обратная связь о презентациях:")
        for presentation, data in feedback.items():
            print(f"Презентация '{presentation}': Оценка - {data['оценка']}, Комментарий - {data['комментарий']}")

    def notify_participants(self, message):
        if not self.conference:
            print("Конференция не создана. Используйте команду create_conference для создания.")
            return
        if not self.speakers:
            print("Нет докладчика. Используйте команду add_participant для создания.")
            return
        self.conference.notify_participants(message)

    def run(self):
        while True:
            command = input("Введите команду (help для справки): ").split()
            if command[0] == 'help':
                self.help_menu()
            elif command[0] == 'create_conference':
                self.create_conference()
            elif command[0] == 'show_info':
                self.show_info()
            elif command[0] == 'add_participant':
                self.add_participant()
            elif command[0] == 'add_presentation':
                self.add_presentation()
            elif command[0] == 'generate_schedule':
                self.generate_schedule()
            elif command[0] == 'prepare_conference':
                self.prepare_conference()
            elif command[0] == 'conduct_conference':
                self.conduct_conference()
            elif command[0] == 'collect_feedback':
                self.collect_feedback()
            elif command[0] == 'notify_participants':
                self.notify_participants(' '.join(command[1:]))
            elif command[0] == 'exit':
                print("До свидания!")
                break
            else:
                print("Неверная команда. Введите 'help' для списка команд.")


if __name__ == '__main__':
    cli = ConferenceCLI()
    cli.run()