from Person import Person

class Scientist(Person):
    def __init__(self, name, affiliation, field_of_study):
        super().__init__(name, affiliation)
        self.__field_of_study = field_of_study
        self.__collaborations = []
        self.__contacts = {}
        self.__achievements = []
        self.__research_publications = []
        self.__grant_proposals = []
        self.__conferences_attended = []
        self.__subscribed_journals = []

    def get_field_of_study(self):
        return self.__field_of_study

    def get_collaborations(self):
        return self.__collaborations

    def get_contacts(self):
        return self.__contacts

    def get_achievements(self):
        return self.__achievements

    def set_field_of_study(self, field_of_study):
        try:
            self.__field_of_study = field_of_study
        except ValueError:
            print("Поле области исследований должно быть строкой.")

    def publish_research(self, research):
        self.__research_publications.append(research)
        print(f"{self.get_name()} опубликовал исследование '{research}'.")

    def write_grant_proposal(self, grant_info):
        self.__grant_proposals.append(grant_info)
        print(f"{self.get_name()} написал предложение по гранту '{grant_info}'.")

    def attend_conference(self, conference_info):
        self.__conferences_attended.append(conference_info)
        print(f"{self.get_name()} принял участие в конференции '{conference_info}'.")

    def collaborate_with(self, other_scientist):
        try:
            self.__collaborations.append(other_scientist)
            print(f"{self.get_name()} начал сотрудничество с {other_scientist.get_name()}.")
        except ValueError:
            print("Коллаборатор должен быть экземпляром класса Scientist.")

    def track_achievements(self, achievement):
        try:
            self.__achievements.append(achievement)
            print(f"{self.get_name()} достиг: {achievement}")
        except ValueError:
            print("Достижение должно быть строкой.")

    def subscribe_to_journals(self, journal_list):
        try:
            self.__subscribed_journals.extend(journal_list)
            print(f"{self.get_name()} подписался на следующие научные журналы:")
            for journal in journal_list:
                if not isinstance(journal, str):
                    raise ValueError("Название журнала должно быть строкой.")
                print(f"  - {journal}")
        except ValueError:
            print("Список журналов должен быть списком.")

    def get_subscribed_journals(self):
        return self.__subscribed_journals