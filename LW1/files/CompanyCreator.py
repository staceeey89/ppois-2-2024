from ITCompany import ITCompany
from Printer import Printer
import os


class CompanyCreator:
    @staticmethod
    def create_company():
        name = input("Введите название новой IT-компании: ")
        initial_budget = float(input("Введите начальный бюджет компании: "))
        location = input("Введите место дислокации IT-компании: ")
        return ITCompany(name, initial_budget, location)

    @staticmethod
    def delete_company(file_name):
        try:
            os.remove(file_name)
            Printer.print_company_was_deleted()
        except FileNotFoundError:
            Printer.print_file_not_found()
