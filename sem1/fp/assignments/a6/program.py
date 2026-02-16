#
# Write the implementation in this file
#
import re


#
# Write below this comment 
# Functions to deal with complex numbers -- dict representation
# -> There should be no print or input statements in this section 
# -> Each function should do one thing only
# -> Functions communicate using input parameters and their return values
#


def create_complex_number(real, imag):
    return {'real': real, 'imag': imag}

def get_real(c):
    return c['real']

def get_imag(c):
    return c['imag']

def set_real(c, value):
    c['real'] = value

def set_imag(c, value):
    c['imag'] = value

def to_string(c):
    return str(get_real(c)) + ("+" if get_imag(c) >= 0 else "") + str(get_imag(c)) + "i"



#
# Write below this comment
# Functions to deal with complex numbers -- list representation
# -> There should be no print or input statements in this section
# -> Each function should do one thing only
# -> Functions communicate using input parameters and their return values
#

# def create_complex_number(real, imag):
#     return [real, imag]
#
# def get_real(c):
#     return c[0]
#
# def get_imag(c):
#     return c[1]
#
# def set_real(c, value):
#     c[0] = value
#
# def set_imag(c, value):
#     c[1] = value
#
# def to_string(c):
#     return str(get_real(c)) + ("+" if get_imag(c) >= 0 else "") + str(get_imag(c)) + "i"


#
# Write below this comment 
# Functions that deal with subarray/subsequence properties
# -> There should be no print or input statements in this section 
# -> Each function should do one thing only
# -> Functions communicate using input parameters and their return values
#


# A7
# The longest subarray of numbers where their real part is in the form of a mountain (first the values increase, then they decrease).
# (e.g. 1-i, 2+6i, 4-67i, 90+3i, 80-7i, 76+i, 43-12i, 3)

def is_mountain(subarray):
    if len(subarray) < 3:
        return False

    real_parts = [get_real(c) for c in subarray]
    i = 0
    n = len(real_parts)

    # go increasing
    while i + 1 < n and real_parts[i] < real_parts[i + 1]:
        i += 1

    if i == 0 or i == n - 1:
        return False

    # go decreasing
    while i + 1 < n and real_parts[i] > real_parts[i + 1]:
        i += 1

    if i == n - 1:
        return True

    else:
        return False


def longest_mountain_subarray(numbers):
    n = len(numbers)
    longest = []
    for start in range(n):
        for end in range(start + 2, n):
            subarray = numbers[start:end+1]
            if is_mountain(subarray):
                if len(subarray) > len(longest):
                    longest = subarray
    return longest, len(longest)


# B5
# The longest alternating subsequence, when considering each number's modulus
# (e.g., given sequence [1, 3, 2, 4, 10, 6, 1], [1, 3, 2, 10, 1] is an alternating subsequence, because 1 < 3 > 2 < 10 > 1).


def get_modulus(c):
    real = get_real(c)
    imag = get_imag(c)
    return real*real + imag*imag

def get_list_of_modulus(numbers):
    modulus_list = []
    for number in numbers:
        modulus = get_modulus(number)
        modulus_list.append(modulus)
    return modulus_list

def longest_alternating_sequence(numbers):
    n = len(numbers)
    if n == 0:
        return [], 0

    mod_list = [get_modulus(c) for c in numbers]

    # dp[i][0] = length of l_a_s ending at i with last difference positive
    # dp[i][1] = length of l_a_s ending at i with last difference negative

    dp = [[1, 1] for _ in range(n)]     # initially, every single element is a subsequence of length 1
    prev = [[-1, -1] for _ in range(n)]  # to reconstruct sequence; -1 means we didn't add an element

    # prev[i][0] = j  =>  to reach dp[i][0], we came from index j with dp[j][1]
    # prev[i][1] = j  =>  to reach dp[i][1], we came from index j with dp[j][0]

    for i in range(1, n):
        for j in range(i):
            if mod_list[i] > mod_list[j] and dp[i][0] < dp[j][1] + 1:  # go up if we went down before
                #extend a sequence that ended at j (with a negative last step)
                dp[i][0] = dp[j][1] + 1
                prev[i][0] = j      # store the position of the number that produced the alternation
            elif mod_list[i] < mod_list[j] and dp[i][1] < dp[j][0] + 1:  # go down if we went up before
                # extend a sequence that ended at j (with a positive last step)
                dp[i][1] = dp[j][0] + 1
                prev[i][1] = j      # store the position of the number that produced the alternation

    # find maximum length
    max_len = 0
    last_index = 0
    last_type = 0
    # search all dp[i][_] to find the biggest length
    # and records where it ends and whether it ends with a pos/neg last step
    for i in range(n):
        if dp[i][0] > max_len:
            max_len = dp[i][0]
            last_index = i
            last_type = 0
        if dp[i][1] > max_len:
            max_len = dp[i][1]
            last_index = i
            last_type = 1

    # reconstruct sequence
    seq = []
    while last_index != -1:     # go in the reverse order
        seq.append(numbers[last_index])
        last_index = prev[last_index][last_type]    # find which element led to the current one
        last_type = 1 - last_type  # alternate type

    seq.reverse()
    return seq, max_len


#
# Write below this comment 
# UI section
# Write all functions that have input or print statements here
# Ideally, this section should not contain any calculations relevant to program functionalities
#


def read_complex_number_ui(numbers):
    while True:
        try:
            n = int(input("Enter the list length: "))
            if n <= 0:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input! Enter an integer number.")
    for i in range(n):
        while True:
            number = input("Enter number in form 'a + bi' or 'a - bi': ").replace(" ", "")
            if not number.endswith("i"):
                print("Must end with 'i'. Example: 3+4i or -2-5i")
                continue
            number = number[:-1]
            parts = re.split(r'(?<!^)(?=[+-])', number)
            if len(parts) != 2:
                print("Invalid format! Example: 3+4i or -2-5i")
                continue
            try:
                real = int(parts[0])
                imag = int(parts[1])
                c = create_complex_number(0, 0)  # start with zero
                set_real(c, real)
                set_imag(c, imag)
                numbers.append(c)
                break
            except ValueError:
                print("Invalid numbers! Please use integers only.")
                continue


def display_complex_numbers(numbers):
    for c in numbers:
        print(to_string(c))


def print_menu():
    print("1. Read a list of complex numbers (in z = a + bi form) from the console: ")
    print("2. Display the entire list of numbers on the console.")

    print("3. Display the longest subarray of numbers where their real part is in the form of a mountain.")
    #(e.g., given sequence [1, 3, 2, 4, 10, 6, 1], [1, 3, 2, 10] is an alternating subsequence,
    # because 1 < 3 > 2 < 10).

    print("4. Display the longest alternating subsequence, when considering each number's modulus.")
    #(e.g., given sequence [1, 3, 2, 4, 10, 6, 1], [1, 3, 2, 10, 1] is an alternating subsequence,
    # because 1 < 3 > 2 < 10 > 1).

    print("5. Exit the program.")


def main():
    # start with an empty list
    numbers = []

    # default numbers list (will only be used if user hasn't added any)
    default_numbers = [
        create_complex_number(1, 2),
        create_complex_number(3, -1),
        create_complex_number(4, 4),
        create_complex_number(-2, 5),
        create_complex_number(0, -3),
        create_complex_number(6, 1),
        create_complex_number(2, -2),
        create_complex_number(-1, 0),
        create_complex_number(5, 5),
        create_complex_number(3, -3)
    ]

    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            numbers.clear()
            read_complex_number_ui(numbers)
        elif choice == "2":
            # if numbers list is empty, use the default numbers
            if not numbers:
                numbers = default_numbers.copy()
            print("List of complex numbers:")
            display_complex_numbers(numbers)
        elif choice == "3":
            if not numbers:
                numbers = default_numbers.copy()
            mountain, length = longest_mountain_subarray(numbers)
            if length == 0:
                print("No subarray found.")
            else:
                print("Length of mountain subarray:", length)
                print("Longest mountain subarray:")
                display_complex_numbers(mountain)
        elif choice == "4":
            if not numbers:
                numbers = default_numbers.copy()
            alt_seq, length = longest_alternating_sequence(numbers)
            print("Length of alternating sequence:", length)
            print("Longest alternating subsequence:")
            display_complex_numbers(alt_seq)
            print("The modulus of the numbers in the alternating sequence:")
            for no in alt_seq:
                print(get_modulus(no))
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()




# def main():
#     # initial 10 numbers for testing
#     numbers = [
#         create_complex_number(1, 2),
#         create_complex_number(3, -1),
#         create_complex_number(4, 4),
#         create_complex_number(-2, 5),
#         create_complex_number(0, -3),
#         create_complex_number(6, 1),
#         create_complex_number(2, -2),
#         create_complex_number(-1, 0),
#         create_complex_number(5, 5),
#         create_complex_number(3, -3)
#     ]
#     while True:
#         print_menu()
#         choice = input("Enter your choice: ")
#         if choice == "1":
#             read_complex_number_ui(numbers)
#         elif choice == "2":
#             print("List of complex numbers:")
#             display_complex_numbers(numbers)
#         elif choice == "3":
#             mountain, length = longest_mountain_subarray(numbers)
#             print("Length of mountain subarray:", length)
#             print("Longest mountain subarray:")
#             display_complex_numbers(mountain)
#         elif choice == "4":
#             alt_seq, length = longest_alternating_sequence(numbers)
#             print("Length of alternating sequence:", length)
#             print("Longest alternating subsequence:")
#             display_complex_numbers(alt_seq)
#             print("The modulus of the numbers in the alternating sequence:")
#             for no in alt_seq:
#                 print(get_modulus(no))
#         elif choice == "5":
#             print("Exiting the program.")
#             break
#         else:
#             print("Invalid choice. Please enter a valid option.")