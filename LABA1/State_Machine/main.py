# this module runs all the project

from student_model_state_machine import Student_Model_State_Machine
from Student_File.student_file import Student_File, File

file: File = Student_File("file.pickle")

state = Student_Model_State_Machine(file)

while True:
    state.next_state(input())
