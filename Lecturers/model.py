class Lecturer:
    def __init__(self,
                 identifier, faculty, department, full_name, academic_title, academic_degree, years_of_experience):
        self.id = identifier
        self.faculty = faculty
        self.department = department
        self.full_name = full_name
        self.academic_title = academic_title
        self.academic_degree = academic_degree
        self.years_of_experience = years_of_experience

    def __str__(self):
        return (f"{self.id} {self.faculty} {self.department} {self.full_name} {self.academic_title}"
                f" {self.academic_degree} {self.years_of_experience}")


class Model:
    def __init__(self):
        pass

    def insert(self, lecturer: Lecturer):
        pass

    def get_all_lecturers(self):
        pass

    def get_len(self) -> int:
        pass

    def get_lecturers_by_index(self, offset, limit):
        pass

    def search_by_name(self, name, offset=0, limit=None):
        pass

    def delete_by_name(self, name):
        pass

    def collect(self, field):
        pass

    def retrieve(self, field):
        pass

    def search_by_department(self, department, offset=0, limit=None):
        pass

    def delete_by_department(self, department):
        pass

    def search_by_academic_title_and_faculty(self, academic_title, faculty, offset=0, limit=None):
        pass

    def delete_by_academic_title_and_faculty(self, academic_title, faculty):
        pass

    def search_by_experience(self, lower_limit, upper_limit, offset=0, limit=None):
        pass

    def delete_by_experience(self, lower_limit, upper_limit):
        pass

    def save(self):
        pass
