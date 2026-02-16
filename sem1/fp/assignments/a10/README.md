💻 Assignment 10 - Layered Architecture II
## Requirements
There are some new requirements for the program you've implemented for the previous assignment. The undo/redo requirement is common across all problem statements. Additionally, for each problem statement you will have to create the statistics detailed in the text below.

### Common requirement for all problem statements
Implement unlimited undo/redo functionality using the [Command design pattern](https://refactoring.guru/design-patterns/command), which ensures a memory-efficient implementation of undo/redo operations. Each step will undo/redo the previous operation performed by the user. Undo/redo operations must cascade (e.g., deleting a student must also delete their grades; undoing the deletion must restore all deleted objects).


### 2. Student Lab Assignment
4. Create statistics:
    - All students who received a given assignment, ordered descending by grade.
    - All students who are late in handing in at least one assignment. These are all the students who have an ungraded assignment for which the deadline has passed.
    - Students with the best school situation, sorted in descending order of the average grade received for all graded assignments.
  

deadline for maximum grade is **week 12**.
