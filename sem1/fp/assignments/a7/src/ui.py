#
# This is the program's UI module. The user interface and all interaction with the user (print and input statements)
# are found here
#


from functions import *
from texttable import Texttable


def command_add(rest, numbers, history):
    try:
        rest = rest.strip()
        # check if this is an "insert" with "at"
        if " at " in rest:
            parts = re.split(r"\s*at\s*", rest, maxsplit=1)
            if len(parts) != 2:
                raise ValueError("Invalid insert syntax. Use: insert <number> at <position>")

            num_part = parts[0].replace(" ", "")
            pos_part = parts[1].strip()

            pos = int(pos_part)
            save_state(numbers, history)
            insert_number(num_part, numbers, pos)

        else:  # simple "add"
            num_part = rest.replace(" ", "")
            if num_part == "":
                raise ValueError("Missing number for add.")
            save_state(numbers, history)
            add_number(num_part, numbers)

    except ValueError as ve:
        print(ve)


def command_remove(rest, numbers, history):
    try:
        save_state(numbers, history)

        rest = rest.strip()
        if not rest:   # no position was entered
            print("No position provided!")
            return

        if " to " in rest:
            range_parts = re.split(r"\s*to\s*", rest, maxsplit=1)
            if len(range_parts) != 2:
                print("Invalid range format! Use: remove <start> to <end>")
                return
            start_str, end_str = range_parts
            try:
                start = int(start_str.strip())
                end = int(end_str.strip())
                remove_start_end(start, end, numbers)
            except ValueError:
                print("Start and end must be integers!")
        else:
            # Check if rest is a single number
            tokens = rest.split()
            if len(tokens) != 1:
                print("Invalid command! Use a single index or a range with 'to'.")
                return
            try:
                pos = int(tokens[0])
                remove_position(pos, numbers)
            except ValueError:
                print("Position must be an integer!")

    except ValueError as ve:
        print(ve)

def command_replace(rest, numbers, history):
    try:
        parts = re.split(r"\s*with\s*", rest, maxsplit=1)
        if len(parts) != 2:
            raise ValueError("Invalid replace syntax. Use: replace <old> with <new>")

        old_num = parts[0].replace(" ", "")
        new_num = parts[1].replace(" ", "")

        save_state(numbers, history)
        replace_x_y(old_num, new_num, numbers)

    except ValueError as ve:
        print(ve)


def command_list(rest, numbers):
    try:
        rest = rest.strip()

        # list
        if rest == "":
            print(build_numbers_table(numbers).draw())
            return

        # list real A to B
        m_real = re.match(r"^real\s*(\d+)\s*to\s*(\d+)$", rest)
        if m_real:
            start = int(m_real.group(1))
            end = int(m_real.group(2))
            real_numbers = list_real_number(numbers, start, end)
            table = build_numbers_table(real_numbers)
            print(table.draw())
            return

        # list modulo <|=|> number
        m_mod = re.match(r"^modulo\s*(<|=|>)\s*(\d+)$", rest)
        if m_mod:
            symbol = m_mod.group(1)
            number = int(m_mod.group(2))
            filtered = list_modulo(numbers, symbol, number)
            table = build_numbers_table(filtered)
            print(table.draw())
            return

        print("Invalid list command.")

    except ValueError as ve:
        print(ve)


def command_filter(rest, numbers, history):
    try:
        rest = rest.strip()

        save_state(numbers, history)

        # filter real
        if rest == "real":
            filter_real(numbers)
            return

        # filter modulo <|=|> number
        m_mod = re.match(r"^modulo\s+(<|=|>)\s*(\d+)$", rest)
        if m_mod:
            symbol = m_mod.group(1)
            number = int(m_mod.group(2))
            filter_modulo(numbers, symbol, number)
            return

        print("Invalid filter command.")

    except ValueError as ve:
        print(ve)



def command_undo(numbers, history):
    try:
        undo_state(numbers, history)
    except ValueError as ve:
        print(ve)



def process_command(raw, numbers, history):
    raw = raw.strip()
    if raw == "":
        print("Unknown command.")
        return

    parts = raw.split(maxsplit=1)   #split after the first space, so we can get the command
    cmd = parts[0].lower()
    if len(parts) > 1:
        rest = parts[1]
    else:
        rest = ""

    if cmd == "add" or cmd == "insert":
        command_add(rest, numbers, history)
    elif cmd == "remove":
        command_remove(rest, numbers, history)
    elif cmd == "replace":
        command_replace(rest, numbers, history)
    elif cmd == "list":
        command_list(rest, numbers)
    elif cmd == "filter":
        command_filter(rest, numbers, history)
    elif cmd == "undo":
        command_undo(numbers, history)
    else:
        print("Unknown command.")


def print_ui():
    numbers = generate_random_number()
    history = []

    print("Welcome! Type 'exit' to quit.")

    while True:
        raw = input("Enter command: ")
        if raw.strip().lower() == "exit":
            break
        process_command(raw, numbers, history)