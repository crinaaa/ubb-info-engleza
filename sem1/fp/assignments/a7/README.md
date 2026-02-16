💻 Assignment 07 - Modular programming

## Requirements
- You will be given one of the problems below to solve
- In addition to **procedural programming**, also use **modular programming** by having a **UI** module, a **Functions** module and a **Start** module
- The **UI** module provides a command-based console user interface that accepts given commands **exactly** as stated
- Handle the case of incorrect user input by displaying error messages. The program must not crash regardless of user input.
- Use the built-in `list` or `dict` compound types to represent entities in the problem domain and access/modify them using *getter* and *setter* functions
- Use Python's [exception mechanism](https://docs.python.org/3/tutorial/errors.html) so that functions can signal that an exceptional situation, or error, has happened.
- Provide **specifications** for all non-UI functions (except getters and setters), and tests for all non-UI functions related to functionalities **(A)** and **(B)**
- Use the [texttable package](https://github.com/foutaise/texttable) to display the (filtered) list of program entities, such as required at point **(C)**. Each entity (e.g., complex number, expense) will be represented on one line, and in the case of entities having more elements (e.g., day, amount of money etc.) each of them will be displayed on its own column. The table must have a header. You can use the Texttable's `set_deco()` method to customize how the table is drawn, as shown in its documentation. 
- Have at least 10 randomly generated items in your application at program startup
- Deadline for maximum grade is **week 8**.

## Bonus (0.1p)
- Use the [pdoc](https://pdoc.dev/) Python package to generate documentation for the **Functions** module of your solution in HTML format. The bonus will be awarded if the documentation is complete, meaning that functions use type hints and all declared functions are fully documented (what each function does, input parameters and return values, as well as potential errors that might be raised).

## Problem Statements
### 1. Numerical List
A math teacher needs a program to help students test different properties of complex numbers, provided in the `a+bi` form (assume `a` and `b` are integers, for simplicity). Write a program that implements the functionalities exemplified below:

**(A) Add a number**\
`add <number>`\
`insert <number> at <position>`\
e.g.\
`add 4+2i` – appends `4+2i` to the list\
`insert 1+1i at 1` – insert number `1+i` at position `1` in the list (positions are numbered starting from `0`)

**(B) Modify numbers**\
`remove <position>`\
`remove <start position> to <end position>`\
`replace <old number> with <new number>`\
e.g.\
`remove 1` – removes the number at position `1`\
`remove 1 to 3` – removes the numbers at positions `1`,`2`, and `3`\
`replace 1+3i with 5-3i` – replaces all occurrences of number `1+3i` with the number `5-3i`

**(C) Display numbers having different properties**\
`list`\
`list real <start position> to <end position>`\
`list modulo [ < | = | > ] <number>`\
e.g.\
`list` – display all numbers\
`list real 1 to 5` – display the real numbers (imaginary part `=0`) between positions `1` and `5`\
`list modulo < 10` – display all numbers with modulo `<10`\
`list modulo = 5` – display all numbers with modulo `=5`

**(D) Filter the list**\
`filter real`\
`filter modulo [ < | = | > ] <number>`\
e.g.\
`filter real` – keep only numbers having imaginary part `=0`\
`filter modulo < 10` – keep only numbers having modulo `<10`\
`filter modulo > 6` – keep only those numbers having modulo `>6`

**(E) Undo**\
`undo` – the last operation that modified program data is reversed. The user can undo all operations performed since program start by repeatedly calling this function.

