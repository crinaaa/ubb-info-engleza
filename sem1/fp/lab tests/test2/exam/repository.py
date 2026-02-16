from domain import Student
from exceptions import RepositoryException


class TextFileRepo:
    def __init__(self, filename = "students.txt"):
        self._students = {}
        self._filename = filename
        self._load_file()

    def add_student(self, new_student: Student):
        if new_student.id in self._students:
            raise RepositoryException("Student with the given ID already exists!")
        self._students[new_student.id] = new_student
        self._save_file()

    def get_all(self):
        return list(self._students.values())

    def _save_file(self):
        try:
            with open(self._filename, "w") as fout:     #open the file for writing
                for student in self.get_all():
                    fout.write(f"{student.id}, {student.name}, {student.attendances}, {student.grade}\n")

        except EOFError:
            pass

    def save(self):
        self._save_file()

    def _load_file(self):
        try:
            with open(self._filename, "r") as fin:   # open the file for parsing
                for line in fin:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        if len(parts)!=4:
                            continue   #skip bad lines

                        #otherwise
                        student_id = int(parts[0].strip())
                        name = parts[1].strip()
                        attendances = int(parts[2].strip())
                        grade = int(parts[3].strip())

                        student = Student(student_id, name, attendances, grade)
                        self.add_student(student)

        except EOFError:
            pass
