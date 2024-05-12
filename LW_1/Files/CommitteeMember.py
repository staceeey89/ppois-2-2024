from Person import Person
class CommitteeMember(Person):
    VALID_PRIORITIES = ["низкий", "средний", "высокий"]

    def __init__(self, name, affiliation):
        super().__init__(name, affiliation)
        self.__tasks = []
        self.__priority_map = {}
        self.__deadlines = {}

    def get_tasks(self):
        return self.__tasks

    def get_priority_map(self):
        return self.__priority_map

    def get_deadlines(self):
        return self.__deadlines

    def assign_task(self, task, priority="средний", deadline=None):
        try:
            self.__tasks.append(task)
        except ValueError:
            print("Задача должна быть строкой.")
        try:
            self.__priority_map[task] = priority
        except ValueError:
            print(f"Приоритет должен быть одним из {self.VALID_PRIORITIES}.")
        try:
            if deadline:
                self.__deadlines[task] = deadline
        except ValueError:
            print("Срок должен быть строкой или None.")
        print(f"{self.get_name()} получил задачу '{task}' с приоритетом '{priority}'.")

    def complete_task(self, task):
        try:
            self.__tasks.remove(task)
            print(f"{self.get_name()} выполнил задачу '{task}'.")
        except ValueError:
            print(f"Задача '{task}' не найдена в списке задач {self.get_name()}.")

    def review_paper(self, paper):
        try:
            print(f"{self.get_name()} рецензирует статью '{paper}'.")
        except ValueError:
            print("Статья должна быть строкой.")

    def vote(self, decision):
        try:
            print(f"{self.get_name()} голосует за '{decision}'.")
        except ValueError:
            print("Решение должно быть строкой.")

    def organize_meeting(self, meeting_time):
        try:
            print(f"{self.get_name()} организует встречу на {meeting_time}.")
        except ValueError:
            print("Время встречи должно быть строкой.")

    def send_reminder(self, reminder):
        try:
            print(f"{self.get_name()} отправляет напоминание: '{reminder}'.")
        except ValueError:
            print("Напоминание должно быть строкой.")

    def delegate_task(self, task, member):
        try:
            member.__tasks.append(task)
        except ValueError:
            print("Член комитета должен быть экземпляром класса CommitteeMember.")
        try:
            self.__tasks.remove(task)
        except ValueError:
            print(f"Задача '{task}' не найдена в списке задач {self.get_name()}.")
        print(f"{self.get_name()} делегировал задачу '{task}' {member.get_name()}.")

    def generate_task_report(self):
        completed_tasks = [task for task in self.__tasks if task not in self.__priority_map]
        pending_tasks = [task for task in self.__tasks if task in self.__priority_map]
        report = f"{self.get_name()} завершил следующие задачи:\n"
        for task in completed_tasks:
            report += f"  - {task}\n"
        report += f"{self.get_name()} имеет следующие невыполненные задачи:\n"
        for task in pending_tasks:
            priority = self.__priority_map.get(task, "средний")
            deadline = self.__deadlines.get(task, "без срока")
            report += f"  - {task} (Приоритет: {priority}, Срок: {deadline})\n"
        return report