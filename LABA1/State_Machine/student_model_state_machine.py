from statemachine import State
from statemachine import StateMachine

from Student_Model.group import Group
from Student_Model.student import Student
from Student_Model.exam import Exam
from Student_Model.subject_progress import Subject_Progress

from Student_Model.check_correct_input_classes import ValidNumber, ValidDate, ValidInitials, ValidSubjectName

from Student_File.file import File

from Exceptions.exceptions import File_Exception, Delete_Exception


class Student_Model_State_Machine(StateMachine):
    view_groups = State(initial=True)
    add_group = State()
    view_group = State()
    view_student = State()
    add_student = State()
    expel_student = State()
    view_exams = State()
    add_exam = State()
    choice = State()
    in_library = State()
    view_subjects_progress = State()
    in_university = State()
    prepare_for_exams = State()
    exit_ = State(final=True)

    next_state = (
            exit_.from_(view_groups, cond="navigating_backwards")

            | view_groups.from_(view_group, cond="navigating_backwards")
            | view_groups.to(view_group, cond="navigating_by_index")

            | view_groups.from_(add_group)
            | view_groups.to(add_group, cond="navigating_add")

            | view_group.to(add_student, cond="navigating_add")
            | view_group.from_(add_student)

            | view_group.from_(view_exams, cond="navigating_backwards")
            | view_group.to(view_exams, cond="navigating_exams")

            | view_group.to(expel_student, cond="navigating_expel")
            | view_group.from_(expel_student)

            | view_exams.to(add_exam, cond="navigating_add")
            | view_exams.from_(add_exam)

            | view_group.from_(view_student, cond="navigating_backwards")
            | view_group.to(view_student, cond="navigating_by_index")

            | view_student.to(choice, cond="navigating_prepare")
            | choice.to(in_library, cond="navigating_yes")
            | choice.to(prepare_for_exams, cond="navigating_no")
            | view_student.from_(choice, cond="navigating_backwards")
            | choice.from_(prepare_for_exams)
            | choice.from_(in_library)


            | view_student.to(view_subjects_progress, cond="navigating_subjects_progress")
            | view_student.from_(view_subjects_progress, cond="navigating_backwards")

            | view_student.to(in_university, cond="navigating_go_to_university")
            | view_student.from_(in_university)

            # in case user enters invalid index
            | choice.to.itself(internal=True)
            | in_library.to.itself(internal=True)
            | view_subjects_progress.to.itself(internal=True)
            | view_groups.to.itself(internal=True)
            | view_group.to.itself(internal=True)
            | view_student.to.itself(internal=True)
            | view_exams.to.itself(internal=True)
    )

    def __init__(self, file: File):
        self.file: File = file
        self.selected_index: int
        self.selected_group: Group
        self.selected_student: Student

        try:
            print("Loading state...")
            self.groups: list[Group] = file.load()

        except File_Exception:

            self.groups: list[Group] = []


        super().__init__()  # call the constructor of the parent class (StateMachine)

    def navigating_backwards(self, input_: str) -> bool:
        return input_ == 'q'

    def navigating_yes(self, input_: str) -> bool:
        return input_ == 'y'

    def navigating_no(self, input_: str) -> bool:
        return input_ == 'n'

    def navigating_add(self, input_: str) -> bool:
        return input_ == 'a'

    def navigating_expel(self, input_: str) -> bool:
        return input_ == 'ex'

    def navigating_exams(self, input_: str) -> bool:
        return input_ == 'e'

    def navigating_prepare(self, input_: str) -> bool:
        return input_ == 'p'

    def navigating_go_to_library(self, input_: str) -> bool:
        return input_ == 'l'

    def navigating_go_to_university(self, input_: str) -> bool:
        return input_ == 'u'

    def navigating_subjects_progress(self, input_: str) -> bool:
        return input_ == 's'

    def navigating_by_index(self, input_: str) -> bool:

        if input_.isnumeric():
            self.selected_index = int(input_)
            return True
        else:
            return False

    def on_enter_view_groups(self) -> None:
        self.selected_group = None
        print("\nList of all groups:")
        for i in range(len(self.groups)):
            print(f"{i} - {self.groups[i].get_name()}")

    def on_enter_add_group(self) -> None:
        new_group = Group(ValidNumber().input_number("group name"))  # check correct input
        self.groups.append(new_group)
        print(f"Group {new_group.get_name()} was added")
        self.next_state()

    def on_enter_view_group(self) -> None:
        self.selected_student = None
        try:
            if self.selected_group is None:
                self.selected_group = self.groups[self.selected_index]

            print(f"\nGroup {self.selected_group.get_name()} information:")
            students = self.selected_group.get_list_of_students()

            for i in range(len(students)):
                print(f"{i} - {students[i].get_name()}")
        except IndexError:

            print("Invalid index")
            self.next_state('q')

    def on_enter_expel_student(self) -> None:
        try:
            students: list[Student] = self.selected_group.get_list_of_students()

            if not students:
                raise Delete_Exception

            print(f"\nStudents:")
            for i in range(len(students)):
                print(f"{i} - {students[i].get_name()}")

            index = ValidNumber().input_index("student index you want to expel", len(students))

            group: Group = self.selected_group
            group.expel_student(index)

        except Delete_Exception:
            print("Noone to delete")
        finally:
            self.next_state()

    def on_enter_add_student(self) -> None:
        student_name = ValidInitials().input_initials("full name (Surname Firstname Patronymic)")

        try:
            new_student = Student(student_name)
            self.selected_group.add_student(new_student)
            print(f"Student {student_name} was added to the group {self.selected_group.get_name()}")
        except ValueError as e:
            print(str(e))
        finally:
            self.next_state()

    def on_enter_view_student(self) -> None:
        try:

            self.selected_student = self.selected_group.get_list_of_students()[self.selected_index]

            if not self.selected_student.get_subjects_progress():
                for i in range(len(self.selected_group.get_list_of_exams())):
                    name = self.selected_group.get_list_of_exams()[i].get_name()
                    self.selected_student.get_subjects_progress().append(Subject_Progress(name))

            else:
                i = len(self.selected_student.get_subjects_progress())
                while i < len(self.selected_group.get_list_of_exams()):
                    name = self.selected_group.get_list_of_exams()[i].get_name()
                    self.selected_student.get_subjects_progress().append(Subject_Progress(name))
                    i += 1

            print(f"Selected student: {self.selected_student.get_name()}  group: {self.selected_group.get_name()}")
        except IndexError:
            print("Invalid index")
            self.next_state('q')

    def on_enter_view_exams(self) -> None:
        print("\nList of all exams:")
        group: Group = self.selected_group

        for i in range(len(group.get_list_of_exams())):
            print(f"{i} - {group.get_list_of_exams()[i].get_name()} "
                  f"{group.get_list_of_exams()[i].get_schedule().get_date()} "
                  f"{group.get_list_of_exams()[i].get_schedule().get_time()}")

    def on_enter_add_exam(self) -> None:
        exam_name = ValidSubjectName().input_subject_name("exam name")
        exam_date = ValidDate().input_date("date")
        exam_time = ValidDate().input_time("time")

        new_exam = Exam(exam_name, exam_date, exam_time)
        self.selected_group.add_exam(new_exam)
        print("Exam was added")

        self.next_state()

    def on_enter_view_subjects_progress(self) -> None:
        print("Progress of all subjects:")

        subj = self.selected_student.get_subjects_progress()
        for i in range(len(subj)):
            print(f"{subj[i].get_name()} - {subj[i].get_progress()}%")

    def on_enter_prepare_for_exams(self) -> None:
        print("List of exams:")
        exams = self.selected_group.get_list_of_exams()
        for i in range(len(exams)):
            print(f"{i} - {exams[i].get_name()}")

        index = ValidNumber().input_index("exam index", len(exams))
        ours = ValidDate().input_ours("ours you want to spend")

        stud: Student = self.selected_student

        prog = stud.get_subjects_progress()[index].get_progress()
        prog += 3*ours
        stud.get_subjects_progress()[index].set_progress(prog)

        if (stud.get_subjects_progress()[index].get_progress() > 100):
            self.selected_student.get_subjects_progress()[index].set_progress(100)

        self.next_state('q')

    def on_enter_in_library(self) -> None:
        print("List of exams:")
        exams = self.selected_group.get_list_of_exams()
        for i in range(len(exams)):
            print(f"{i} - {exams[i].get_name()}")

        index = ValidNumber().input_index("exam index", len(exams))
        ours = ValidDate().input_ours("ours you want to spend")

        stud: Student = self.selected_student

        prog = stud.get_subjects_progress()[index].get_progress()
        prog += 5*ours
        stud.get_subjects_progress()[index].set_progress(prog)

        if (stud.get_subjects_progress()[index].get_progress() > 100):
            stud.get_subjects_progress()[index].set_progress(100)

        self.next_state('q')

    def on_enter_choice(self) -> None:
        print("Would you like to go to the library? (y/n)")

    def on_enter_in_university(self) -> None:
        classes = ValidNumber().input_number_of_classes("number of classes you want to attend")
        subjects = self.selected_student.get_subjects_progress()

        stud: Student = self.selected_student

        for i in range(len(subjects)):

            prog = stud.get_subjects_progress()[i].get_progress()
            prog += 5 * classes
            stud.get_subjects_progress()[i].set_progress(prog)
            if(stud.get_subjects_progress()[i].get_progress() > 100):
                stud.get_subjects_progress()[i].set_progress(100)

        self.next_state('q')

    def before_move_next(self):
        print()

    def on_enter_exit_(self):
        print("Saving state...")
        self.file.save(self.groups)
        exit()