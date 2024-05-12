from enum import Enum
from typing import List, Type
from anytree import Node

from constants import PAGE_SIZE
from db import Lecturer
from empty_list_storage import EmptyListStorage
from model import Model
from sql_storage import SqlStorage
from view import View
from xml_storage import XmlStorage
from table import Table


class Fields(Enum):
    FACULTY = "Faculty"
    DEPARTMENT = "Department"
    NAME = "FullName"
    ATITLE = "AcademicTitle"
    ADEGREE = "AcademicDegree"
    EXPERIENCE = "YearsOfExperience"


class Storages(Enum):
    SQL = SqlStorage
    XML = XmlStorage
    EMPTY_LIST = EmptyListStorage


class Controller:
    def __init__(self, view):
        self.storages: Type[Storages] = Storages
        self.model: Model = self.storages.EMPTY_LIST.value()
        self.view: View = view

    def open(self, storage: Storages, file=None):
        self.model = storage.value(file)
        self.print_table()

    def generate_edge_list(self):
        lecturers: List[Lecturer] = self.model.get_all_lecturers()
        root = 'Лекторы'
        edges = []
        labels = {root: root}

        for i in lecturers:
            labels[i.id] = i.id
            edges.append((root, i.id))
            edges.append((i.id, str(i.id) + i.faculty))
            labels[str(i.id) + i.faculty] = i.faculty
            edges.append((i.id, str(i.id) + i.department))
            labels[str(i.id) + i.department] = i.department
            edges.append((i.id, str(i.id) + i.full_name))
            labels[str(i.id) + i.full_name] = i.full_name
            edges.append((i.id, str(i.id) + i.academic_title))
            labels[str(i.id) + i.academic_title] = i.academic_title
            edges.append((i.id, str(i.id) + i.academic_degree))
            labels[str(i.id) + i.academic_degree] = i.academic_degree
            edges.append((i.id, f"E{str(i.id) + str(i.years_of_experience)}"))
            labels[f"E{str(i.id)}{str(i.years_of_experience)}"] = f"Стаж: {i.years_of_experience} лет"

        if len(edges) == 0:
            labels = {}
        self.view.render_graph(edges, labels)

    def generate_tree(self):
        root = Node("Лекторы")
        lecturers: List[Lecturer] = self.model.get_all_lecturers()

        for i in lecturers:
            child = Node(str(i.id), parent=root)
            Node(i.faculty, parent=child)
            Node(i.department, parent=child)
            Node(i.full_name, parent=child)
            Node(i.academic_title, parent=child)
            Node(i.academic_degree, parent=child)
            Node(f"Стаж: {i.years_of_experience}", parent=child)

        self.view.render_tree(root)

    def connect_model(self, model: Model):
        self.model = model

    def connect_view(self, view):
        self.view = view

    def _verify(self):
        if self.view is None or self.model is None:
            raise ValueError("View or model is not connected.")

    def print_table(self):
        lecturers = self.model.get_lecturers_by_index(0, PAGE_SIZE)
        length = self.model.get_len()

        self.view.show_table(lecturers, length)

    def get_lecturers_by_index(self, start_index, limit):
        lecturers = self.model.get_lecturers_by_index(start_index, limit)
        length = self.model.get_len()
        self.view.table.show_table(lecturers, length)
        return lecturers

    def _view_mainloop(self):
        self.view.main_window.mainloop()

    def start(self):
        self._verify()
        self.view.controller = self
        self.print_table()
        self._view_mainloop()

    def insert(self, lecturer: Lecturer):
        self.model.insert(lecturer)
        self.print_table()

    def search_by_full_name(self,
                            full_name: str,
                            table: Table,
                            offset=0,
                            limit=PAGE_SIZE):
        result, length = self.model.search_by_name(full_name, offset, limit)
        table.show_table(result, length)

    def delete_by_full_name(self, full_name, window):
        result = self.model.delete_by_name(full_name)
        self.view.show_delete_results(result, full_name, window)
        if result != 0:
            self.print_table()

    def search_by_department(self,
                             department,
                             table: Table,
                             offset=0,
                             limit=PAGE_SIZE):
        result, length = self.model.search_by_department(department, offset, limit)
        table.show_table(result, length)

    def delete_by_department(self, department, window):
        result = self.model.delete_by_department(department)
        self.view.show_delete_results(result, department, window)
        if result != 0:
            self.print_table()

    def search_by_academic_title_faculty(self,
                                         academic_title: str,
                                         faculty: str,
                                         table: Table,
                                         offset: int = 0,
                                         limit: int = PAGE_SIZE):
        result, length = self.model.search_by_academic_title_and_faculty(academic_title, faculty, offset, limit)
        table.show_table(result, length)

    def delete_by_academic_title_faculty(self, academic_title: str, faculty: str, window):
        title = f"{academic_title} {faculty}"
        result = self.model.delete_by_academic_title_and_faculty(academic_title, faculty)
        self.view.show_delete_results(result, title, window)
        if result != 0:
            self.print_table()

    def search_by_experience(self,
                             lower_limit: int,
                             upper_limit: int,
                             table: Table,
                             offset: int = 0,
                             limit: int = PAGE_SIZE):
        result, length = self.model.search_by_experience(lower_limit, upper_limit, offset, limit)
        table.show_table(result, length)

    def delete_by_experience(self, lower_limit: int, upper_limit: int, window: int):
        title = f"от {lower_limit} до {upper_limit} лет"
        result = self.model.delete_by_experience(lower_limit, upper_limit)
        self.view.show_delete_results(result, title, window)
        if result != 0:
            self.print_table()

    def collect_departments(self):
        return self.model.collect(Fields.DEPARTMENT.value)

    def collect_academic_titles(self):
        return self.model.collect(Fields.ATITLE.value)

    def collect_faculty(self):
        return self.model.collect(Fields.FACULTY.value)

    def collect_academic_degrees(self):
        return self.model.collect(Fields.ADEGREE.value)

    def save(self):
        self.model.save()
