
from domain import Student
from exceptions import ValidationException

class StudentService:
    def __init__(self, repo):
        self._repo = repo

    def add_student(self, student_id:int, name:str, attendances:int, grade:int):
        try:
            if student_id < 0:
                raise ValidationException("Student ID must be a positive integer!")

            if attendances < 0:
                raise ValidationException("The number of attendances must be a positive integer!")

            if grade < 0 or grade > 10:
                raise  ValidationException("The grade must be an integer between 0 and 10!")

            if not name or len(name.strip()) == 0:
                raise  ValidationException("Name cannot be empty!")

            parts = name.strip().split(" ")
            if len(parts)<2:
                raise ValidationException("Name must contain at least 2 words!")
            for w in parts:
                if len(w)<3:
                    raise ValidationException("Each name part must have at least 3 characters!")

            new_student = Student(student_id, name, attendances, grade)
            self._repo.add_student(new_student)

        except ValidationException as ve:
            print(ve)


    def get_students_sorted(self):
        students = self._repo.get_all()
        return sorted(students, key = lambda s: (-s.grade, s.name.lower()))

    def bonuses(self, student: Student, p:int, b:int):
        if student.attendances >= p:
            student.set_grade(student.grade + b)
            if student.grade > 10:
                student.set_grade(10)
        self._repo.save()

    def sort_by_name(self, word:str):
        students = self._repo.get_all()
        new_list = []
        for ss in students:
            if word.lower() in ss.name.lower():
                new_list.append(ss)

        new_list.sort(key=lambda s: s.name.lower())
        return new_list