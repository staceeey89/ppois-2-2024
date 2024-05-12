class OrganizingCommittee:
    def __init__(self, chairperson, members):
        self.__chairperson = chairperson
        self.__members = members

    def get_chairperson(self):
        return self.__chairperson

    def get_members(self):
        return self.__members

    def set_chairperson(self, chairperson):
        try:
            self.__chairperson = chairperson
        except ValueError:
            print("Председатель комитета должен быть строкой.")

    def set_members(self, members):
        try:
            self.__members = members
        except ValueError:
            print("Члены комитета должны быть списком.")

    def add_member(self, new_member):
        try:
            self.__members.append(new_member)
        except ValueError:
            print("Новый член комитета должен быть строкой.")

    def remove_member(self, member_to_remove):
        if member_to_remove not in self.__members:
            raise ValueError("Удаляемый член комитета не найден.")
        else:
            self.__members.remove(member_to_remove)