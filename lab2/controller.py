from view import View
from anytree import Node, RenderTree
from model import Record, SQLModel, XMLModel
from typing import List
from pubsub import pub


class PageInfo:
    def __init__(self, items_per_page, items_offset, current_page, items_size):
        self.items_per_page = items_per_page
        self.items_offset = items_offset
        self.current_page = current_page
        self.items_size = items_size
        self.total_pages = -(-self.items_size // self.items_per_page)
        self.on_page = 0
        self.condition = ""
        self.is_sql = True

    def on_new_SQL(self, items_size):
        result = PageInfo(self.items_per_page, 0, 0, items_size)

        if result.items_per_page > result.items_size:
            result.items_per_page = 1
        return result

    def on_new_XML(self, items_size):
        result = PageInfo(self.items_per_page, 0, 0, items_size)
        result.is_sql = False

        if result.items_per_page > result.items_size:
            result.items_per_page = 1
        return result

    def get_other_page_info(self, items_size, condition):
        result = PageInfo(self.items_per_page, 0, 0, items_size)
        if self.items_per_page > items_size:
            result.items_per_page = items_size

        result.condition = condition
        return result

    def set_on_page(self, on_page):
        self.on_page = on_page

    def update_total_pages(self):
        if self.items_per_page == 0:
            self.total_pages = 0
            return
        self.total_pages = -(-self.items_size // self.items_per_page)


class Controller:
    def __init__(self):
        self.model = None
        self.mainPageInfo = PageInfo(10, 0, 0, 0)
        self.otherPageInfo = None
        self.view = View()
        self.subscribe_events()
        self.is_saved = True
        self.mainFrame = self.view.get_mainFrame()
        self.update_ui(self.mainFrame)
        self.view.main_loop()

    def subscribe_events(self):
        pub.subscribe(self.go_next_page, "press next")
        pub.subscribe(self.go_prev_page, "press prev")
        pub.subscribe(self.go_first_page, "press first")
        pub.subscribe(self.go_last_page, "press last")
        pub.subscribe(self.dec_on_page, "press minus")
        pub.subscribe(self.inc_on_page, "press plus")
        pub.subscribe(self.enter_on_page, "press page enter")
        pub.subscribe(self.add_entry_dialog, "press add entry")
        pub.subscribe(self.add_new_entry, "add new entry dialog")
        pub.subscribe(self.open_find_dialog, "open find dialog")
        pub.subscribe(self.open_remove_dialog, "open remove dialog")
        pub.subscribe(self.open_find_full_name_window, "open find full name window")
        pub.subscribe(self.open_find_salary_window, "open find salary window")
        pub.subscribe(self.open_find_brothers_window, "open find brothers window")
        pub.subscribe(self.open_find_sisters_window, "open find sisters window")
        pub.subscribe(self.open_remove_full_name_window, "open remove full name window")
        pub.subscribe(self.open_remove_salary_window, "open remove salary window")
        pub.subscribe(self.open_remove_brothers_window, "open remove brothers window")
        pub.subscribe(self.open_remove_sisters_window, "open remove sisters window")
        pub.subscribe(self.remove_entries, "remove entries")
        pub.subscribe(self.open_file_open_dialog_SQL, "open file open dialog SQL")
        pub.subscribe(self.open_file_open_dialog_XML, "open file open dialog XML")
        pub.subscribe(self.save_changes, "save changes")
        pub.subscribe(self.open_tree_view, "open tree view")

    def open_tree_view(self, evt_object):
        if self.model is None:
            self.view.error_message("You have to select a database!")
            evt_object.Enable()
            return
        if evt_object == self.mainFrame:
            all_items = self.model.get_all_items()
        elif self.otherPageInfo is not None:
            all_items = self.model.get_all_items_condition(self.otherPageInfo.condition)
        else:
            return
        student_node = Node("Students")
        for ind, item in enumerate(all_items, 1):
            id_node = Node(str(ind), parent=student_node)
            Node("Full name: " + str(item.full_name), parent=id_node)
            Node("Father full name: " + str(item.father_name), parent=id_node)
            Node("Father salary: " + str(item.father_salary), parent=id_node)
            Node("Mother full name: " + str(item.mother_name), parent=id_node)
            Node("Mother salary: " + str(item.mother_salary), parent=id_node)
            Node("Brothers amount: " + str(item.brothers_amount), parent=id_node)
            Node("Sisters amount: " + str(item.sisters_amount), parent=id_node)
        string = ""
        for pre, fill, node in RenderTree(student_node):
            string += "%s%s" % (pre, node.name) + "\n"

        self.view.info_message("Tree view", string)

    def open_file_open_dialog_SQL(self):
        self.mainFrame.Disable()
        pathname = self.view.open_file_open_dialog_SQL(self.is_saved)
        if pathname is None:
            self.mainFrame.Enable()
            return

        self.model = SQLModel(pathname)
        self.mainPageInfo = self.mainPageInfo.on_new_SQL(self.model.get_items_size())
        self.mainFrame.Enable()
        self.mainPageInfo.items_size = self.model.get_items_size()
        self.mainPageInfo.update_total_pages()
        self.is_saved = True
        self.update_ui(self.mainFrame)

    def open_file_open_dialog_XML(self):
        self.mainFrame.Disable()
        pathname = self.view.open_file_open_dialog_XML(self.is_saved)
        if pathname is None:
            self.mainFrame.Enable()
            return

        self.model = XMLModel(pathname)
        self.mainPageInfo = self.mainPageInfo.on_new_XML(self.model.get_items_size())
        self.mainPageInfo.is_sql = False
        self.mainFrame.Enable()
        self.mainPageInfo.items_size = self.model.get_items_size()
        self.mainPageInfo.update_total_pages()
        self.is_saved = True
        self.update_ui(self.mainFrame)

    def save_changes(self):
        if self.model is not None:
            self.is_saved = True
            self.model.save()
        self.mainFrame.Enable()
        self.update_ui(self.mainFrame)

    def form_condition_full_name_SQL(self, full_name) -> str:
        if full_name[1] == 0:
            field = "student_full_name"
        elif full_name[1] == 1:
            field = "father_full_name"
        else:
            field = "mother_full_name"

        if full_name[0] == 0:
            return f"WHERE {field} LIKE '{full_name[2]} %'"
        elif full_name[0] == 1:
            return f"WHERE {field} LIKE '% {full_name[2]} %'"
        else:
            return f"WHERE {field} LIKE '% {full_name[2]}'"

    def form_condition_salary_SQL(self, salary) -> str:
        if salary[0] == 0:
            field = "father_salary"
        else:
            field = "mother_salary"
        if salary[1][0] != "" and salary[1][1] != "":
            return f"WHERE {field} BETWEEN  {salary[1][1]} AND {salary[1][0]}"
        if salary[1][0] != "":
            return f"WHERE {field} <= {salary[1][0]}"
        return f"WHERE {field} >= {salary[1][1]}"

    def form_condition_brothers_SQL(self, brothers):
        return f"WHERE brothers_amount={brothers}"

    def form_condition_sisters_SQL(self, sisters):
        return f"WHERE sisters_amount={sisters}"

    def form_condition_full_name_XML(self, full_name):
        if full_name[0] == 0:
            field = "first"
        elif full_name[0] == 1:
            field = "middle"
        else:
            field = "last"

        if full_name[1] == 0:
            return ("full_name", field, "student", full_name[2])
        elif full_name[1] == 1:
            return ("full_name", field, "father", full_name[2])
        else:
            return ("full_name", field, "mother", full_name[2])

    def form_condition_salary_XML(self, salary):
        if salary[0] == 0:
            return ("father_salary", (salary[1][0], salary[1][1]))
        else:
            return ("mother_salary", (salary[1][0], salary[1][1]))

    def form_condition_brothers_XML(self, brothers):
        return ("brothers_amount", int(brothers))

    def form_condition_sisters_XML(self, sisters):
        return ("sisters_amount", int(sisters))

    def open_find_full_name_window(self, full_name):
        if self.mainPageInfo.is_sql:
            condition = self.form_condition_full_name_SQL(full_name)
        else:
            condition = self.form_condition_full_name_XML(full_name)
        self.open_find_window(condition)

    def open_find_salary_window(self, salary):
        if self.mainPageInfo.is_sql:
            condition = self.form_condition_salary_SQL(salary)
        else:
            condition = self.form_condition_salary_XML(salary)
        self.open_find_window(condition)

    def open_find_brothers_window(self, brothers):
        if self.mainPageInfo.is_sql:
            condition = self.form_condition_brothers_SQL(brothers)
        else:
            condition = self.form_condition_brothers_XML(brothers)
        self.open_find_window(condition)

    def open_find_sisters_window(self, sisters):
        if self.mainPageInfo.is_sql:
            condition = self.form_condition_sisters_SQL(sisters)
        else:
            condition = self.form_condition_sisters_XML(sisters)
        self.open_find_window(condition)

    def open_remove_full_name_window(self, full_name):
        if self.mainPageInfo.is_sql:
            condition = self.form_condition_full_name_SQL(full_name)
        else:
            condition = self.form_condition_full_name_XML(full_name)
        self.open_remove_window(condition)

    def open_remove_salary_window(self, salary):
        if self.mainPageInfo.is_sql:
            condition = self.form_condition_salary_SQL(salary)
        else:
            condition = self.form_condition_salary_XML(salary)
        self.open_remove_window(condition)

    def open_remove_brothers_window(self, brothers):
        if self.mainPageInfo.is_sql:
            condition = self.form_condition_brothers_SQL(brothers)
        else:
            condition = self.form_condition_brothers_XML(brothers)
        self.open_remove_window(condition)

    def open_remove_sisters_window(self, sisters):
        if self.mainPageInfo.is_sql:
            condition = self.form_condition_sisters_SQL(sisters)
        else:
            condition = self.form_condition_sisters_XML(sisters)
        self.open_remove_window(condition)

    def remove_entries(self):
        if self.model is None:
            return
        if self.otherPageInfo is not None:
            removed_entries_count = self.model.remove_items_condition(
                self.otherPageInfo.condition
            )
            self.view.open_removed_info(removed_entries_count)
            self.mainPageInfo.items_size = self.model.get_items_size()
            self.mainPageInfo.update_total_pages()
            self.is_saved = False
            self.mainPageInfo.update_total_pages()
            if self.mainPageInfo.current_page > self.mainPageInfo.total_pages - 1:
                self.mainPageInfo.current_page = self.mainPageInfo.total_pages - 1

            self.mainPageInfo.items_offset = (
                self.mainPageInfo.current_page * self.mainPageInfo.items_per_page
            )
        self.update_ui(self.mainFrame)

    def open_find_window(self, condition):
        if self.model is None:
            return
        self.otherPageInfo = self.mainPageInfo.get_other_page_info(
            self.model.get_items_size_condition(condition), condition
        )
        find_window = self.view.open_find_window()
        find_window.Show()
        self.update_ui(find_window)

    def open_remove_window(self, condition):
        if self.model is None:
            return
        self.otherPageInfo = self.mainPageInfo.get_other_page_info(
            self.model.get_items_size_condition(condition), condition
        )
        remove_window = self.view.open_remove_window()
        remove_window.Show()
        self.update_ui(remove_window)

    def open_find_dialog(self):
        if self.model is None:
            self.view.error_message("You have to open a database!")
            return
        self.view.call_find_dialog()

    def open_remove_dialog(self):
        if self.model is None:
            self.view.error_message("You have to open a database!")
            return
        self.view.call_remove_dialog()

    def add_new_entry(self, new_data):
        if self.model is None:
            return
        self.is_saved = False
        self.model.add_item(*new_data)
        page_info = self.mainPageInfo
        page_info.items_size = self.model.get_items_size()
        page_info.update_total_pages()
        self.update_ui(self.view.get_mainFrame())

    def add_entry_dialog(self):
        if self.model is None:
            self.view.error_message("You have to open a database!")
            return
        self.view.call_add_entry_dialog()

    def make_current_table_request(self, page_info: PageInfo):
        if self.model is None:
            return None
        if page_info.condition == "":
            return self.model.get_items(
                page_info.items_offset, page_info.items_per_page
            )
        return self.model.get_items_condition(
            page_info.condition, page_info.items_offset, page_info.items_per_page
        )

    def get_page_info_evt(self, evt_object):
        if evt_object == self.mainFrame or self.otherPageInfo is None:
            return self.mainPageInfo
        else:
            return self.otherPageInfo

    def dec_on_page(self, evt_object):
        page_info = self.get_page_info_evt(evt_object)

        if page_info.items_per_page - 1 <= 0:
            return

        page_info.items_per_page -= 1
        page_info.update_total_pages()
        page_info.items_offset = page_info.current_page * page_info.items_per_page
        self.update_ui(evt_object)

    def inc_on_page(self, evt_object):
        page_info = self.get_page_info_evt(evt_object)

        if page_info.items_per_page + 1 > page_info.items_size:
            self.view.error_message("View items exceeded items available")
            return

        page_info.items_per_page += 1
        page_info.update_total_pages()
        if page_info.current_page > page_info.total_pages - 1:
            page_info.current_page = page_info.total_pages - 1

        page_info.items_offset = page_info.current_page * page_info.items_per_page
        self.update_ui(evt_object)

    def enter_on_page(self, evt_object, enter_input):
        page_info = self.get_page_info_evt(evt_object)
        try:
            input = int(enter_input)
        except ValueError:
            self.view.reset_input_ctrl(evt_object)
            self.view.error_message("The input has to be numerical!")
            return
        if input <= 0 or input > page_info.items_size:
            self.view.reset_input_ctrl(evt_object)
            self.view.error_message("The input has to be in bounds of items")
            return

        page_info.items_per_page = input
        page_info.update_total_pages()
        if page_info.current_page > page_info.total_pages - 1:
            page_info.current_page = page_info.total_pages - 1
        page_info.items_offset = page_info.current_page * page_info.items_per_page

        self.view.change_input_ctrl_text(evt_object, input)
        self.update_ui(evt_object)

    def go_first_page(self, evt_object):
        page_info = self.get_page_info_evt(evt_object)

        if page_info.current_page == 0:
            return
        page_info.current_page = 0
        page_info.items_offset = page_info.current_page * page_info.items_per_page
        self.update_ui(evt_object)

    def go_last_page(self, evt_object):
        page_info = self.get_page_info_evt(evt_object)
        if page_info.current_page == page_info.total_pages - 1:
            return
        page_info.current_page = page_info.total_pages - 1
        page_info.items_offset = page_info.current_page * page_info.items_per_page
        self.update_ui(evt_object)

    def go_next_page(self, evt_object):
        page_info = self.get_page_info_evt(evt_object)
        if page_info.current_page + 1 > page_info.total_pages - 1:
            return

        page_info.current_page += 1
        page_info.items_offset = page_info.items_per_page * page_info.current_page
        self.update_ui(evt_object)

    def go_prev_page(self, evt_object):
        page_info = self.get_page_info_evt(evt_object)
        if page_info.current_page - 1 < 0:
            page_info.current_page = 0
            page_info.items_offset = 0
            return
        else:
            page_info.current_page -= 1
            page_info.items_offset = page_info.items_per_page * page_info.current_page

        self.update_ui(evt_object)

    def update_ui(self, evt_object):
        if self.model is None:
            return

        page_info = self.get_page_info_evt(evt_object)
        table = self.make_current_table_request(page_info)

        if table is None:
            return

        self.view.update_table(evt_object, table)
        page_info.on_page = len(table)
        self.view.set_page_text(
            evt_object, page_info.current_page, page_info.total_pages
        )
        self.view.set_on_page_text(evt_object, page_info.on_page)
        self.view.set_per_page(evt_object, page_info.items_per_page)
        self.view.set_amount_text(evt_object, page_info.items_size)
        self.view.set_saved_status(evt_object, self.is_saved)
