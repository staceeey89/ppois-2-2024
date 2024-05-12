from controller.controller import StudentAttendanceController

if __name__ == "__main__":
    controller = StudentAttendanceController('/Users/wuttang/BSUIR/2 course/PPOIS/sem_4/LW_2/res/student_attendance.db')
    controller.view.mainloop()
