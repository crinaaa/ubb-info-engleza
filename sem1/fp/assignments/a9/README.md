💻 Assignment 09 - Layered Architecture I
## Requirements common to all problem statements
1. Implement layered architecture using classes. Provide a menu-driven console-based user interface. Implementation details are up to you
2. Have at least 20 procedurally generated items **for each domain class** in your application at startup (e.g., at least 20 students, 20 disciplines and 20 grades). Hint - the **[faker](https://faker.readthedocs.io/en/master/#)** library can generate many of the required class fields.
3. Provide specifications and **[PyUnit test cases](https://realpython.com/python-testing/)** for all non-UI classes and methods for the first functionality. You may skip simple getter/setter functions or properties.
4. Implement and use your own exception classes.
5. Implement in-memory, as well as file-based repositories for all entities. For each entity, implement a text-file repository and a binary-file repository (using [Pickle](https://docs.python.org/3/library/pickle.html)). The program must work the same way using in-memory repositories, text-file repositories and binary file repositories. You may use inheritance to reuse repository source code.
6. Allow configuring the application using a `settings.properties` file. The decision of which repositories are employed, as well as the location of the repository input files will be made in the program’s `settings.properties` file. An example is below:

    a. `settings.properties` for working with repositories that store entities in memory (in this case there are no input files):
    ```
    repository = inmemory
    cars = “”
    clients = “”
    rentals = “”
    ```
    b. `settings.properties` for working with repositories that store entities to binary files:
    ```
    repository = binaryfiles
    cars = “cars.pickle”
    clients = “clients.pickle”
    rentals = “rentals.pickle”
    ```

## Problem Statements

### 2. Student Lab Assignment
Write an application that manages student lab assignments for a discipline. The application will store:
- **Student**: `student_id`, `name`, `group`
- **Assignment**: `assignment_id`, `description`, `deadline`
- **Grade**: `assignment_id`, `student_id`, `grade_value`

Create an application that allows to:
1. Manage students and assignments. The user can add, remove, update, and list both students and assignments.
2. Give assignments to a student or a group of students. In case an assignment is given to a group of students, every student in the group will receive it. In case there are students who were previously given that assignment, it will not be assigned again.
3. Grade student for a given assignment. When grading, the program must allow the user to select the assignment that is graded, from the student’s list of ungraded assignments. A student’s grade for a given assignment cannot be changed. Deleting a student removes their assignments. Deleting an assignment also removes all grades at that assignment.


Deadline for maximum grade is **week 11**