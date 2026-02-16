from random import randint
from texttable import Texttable
import timeit

# This function prints the menu of our console driven application
def print_menu():
    print("1. Generate a list of n natural numbers.")
    print("2. Search for an item in the list using Interpolation Search.")
    print("3. Sort this list using Permutation Sort.")
    print("4. Sort this list using Comb Sort.")
    print("5. Display on a table how the algorithm behaves during the Best Case.")
    print("6. Display on a table how the algorithm behaves during the Average Case.")
    print("7. Display on a table how the algorithm behaves during the Worst Case.")
    print("8. Exit the program.")


def get_int_input(prompt, min_value=None, max_value=None):
    while True:
        user_input = input(prompt)
        try:
            num = int(user_input)
            if min_value is not None and num < min_value:
                print("Please enter a number greater than or equal to" ,min_value)
                continue
            if max_value is not None and num > max_value:
                print("Please enter a number less than or equal to", max_value)
                continue
            return num
        except ValueError:
            print("Invalid input! Please enter a valid integer.")

# This function generates n natural numbers in the interval (0, 1000)
def generate_number_list(n):
    number_list = []
    for i in range(0, n, 1):
        number_list.append(randint(0,1000))
    return number_list

def generate_sorted_list(n):
    number_list = generate_number_list(n)
    number_list.sort()
    return number_list

def generate_reversed_sorted_list(n):
    number_list = generate_number_list(n)
    number_list.sort(reverse=True)
    return number_list

def generate_best_case_list(n):
    return list(range(n))

def generate_worst_case_list(n):
    return [2 ** i for i in range(n)]

def generate_worst_case_comb(n):
    low = list(range(1, n // 2 + 1))
    high = list(range(1000000, 1000000 - (n // 2), -1))
    result = []
    for i in range(n // 2):
        result.append(low[i])
        result.append(high[i])
    if n % 2 != 0:
        result.append(low[-1])
    return result


# This function check if the list is sorted
def is_sorted(number_list):
    for i in range(0, len(number_list)-1):
        if number_list[i] > number_list[i + 1]:
            return False
    return True



"""
The next functions are used for implementing Comb Sort.
"""


# This function computes successively the gap we use in Comb Sort implementation
def print_step_comb_sort(number_list, step):
    print("Step", step, ":", number_list)

def next_gap(gap):
    # the shrink factor was found to be 1.3
    gap=(gap*10)//13
    if gap<1:   # we are applying the algorithm as long as the gap is >=1
        return 1
    return gap

def comb_sort(number_list, step):
    n = len(number_list)
    gap = n
    swap = True
    step_counter = 0
    last_printed = 0  # track last multiple printed
    while swap or gap > 1:
        gap = next_gap(gap)
        swap = False
        for i in range(0, n - gap):
            if number_list[i] > number_list[i + gap]:
                number_list[i], number_list[i + gap] = number_list[i + gap], number_list[i]
                swap = True
        step_counter += 1
        if step_counter % step == 0 and step_counter != last_printed:
            print_step_comb_sort(number_list, step_counter)
            last_printed = step_counter
        if is_sorted(number_list):
            break
    if step_counter != last_printed:
        print_step_comb_sort(number_list, step_counter)
    print(f"Comb Sort completed in {step_counter} actual steps.")
    return number_list

def comb_sort_without_step(number_list):
    n = len(number_list)
    gap = n
    swap = True
    while swap or gap > 1:
        gap = next_gap(gap)
        swap = False
        for i in range(0, n - gap):
            if number_list[i] > number_list[i + gap]:
                number_list[i], number_list[i + gap] = number_list[i + gap], number_list[i]
                swap = True
    return number_list

"""
The next functions are for implementing Interpolation Search, using linear interpolation, on a sorted list.
"""

def interpolation_search(number_list, x):
    n = len(number_list)
    if n == 0:
        return -1  # empty list
    left = 0
    right = n - 1
    while left <= right and number_list[left] != number_list[right]:
        pos = left + (x - number_list[left]) * (right - left) // (number_list[right] - number_list[left])
        if pos < left or pos > right:  # left and right indexes change, so the pos value my not be in the right range(infinite loop!)
            return -1
        if number_list[pos] == x:
            return pos
        elif number_list[pos] < x:
            left = pos + 1
        else:
            right = pos - 1
    if left == right and number_list[left] == x:
        return left
    return -1


"""
The next functions are for implementing Permutation Sort
"""
def print_step_permutation_sort(number_list, step):
    print("Step", step, ":", number_list)

def permutation_sort(number_list, step, current_step=0, start=0):
    if start == len(number_list):
        current_step += 1
        if current_step % step == 0:
            print_step_permutation_sort(number_list, current_step)
            last_printed = current_step
        else:
            last_printed = None
        if is_sorted(number_list):
            if last_printed != current_step:
                print_step_permutation_sort(number_list, current_step)
            print(f"Permutation Sort completed in {current_step} actual steps.")
            return -1
        return current_step

    for i in range(start, len(number_list)):
        number_list[start], number_list[i] = number_list[i], number_list[start]
        current_step = permutation_sort(number_list, step, current_step, start + 1)
        if current_step == -1:
            return -1
        number_list[start], number_list[i] = number_list[i], number_list[start]

    return current_step

def permutation_sort_without_step(number_list, start=0):
    if start == len(number_list):
        if is_sorted(number_list):
            return number_list
        return None

    for i in range(start, len(number_list)):
        number_list[start], number_list[i] = number_list[i], number_list[start]
        result=permutation_sort_without_step(number_list, start+1)
        if result is not None:
            return result
        number_list[start], number_list[i] = number_list[i], number_list[start]

    return None



"""
The next functions are for timing the algorithms and creating the table.
"""

def build_table(case_name, perm_gen, comb_gen, search_gen):
    n = get_int_input(f"Enter starting list length for {case_name.lower()}: ", 1)
    perm_n = n  #separate counter for permutation sort
    table = Texttable()
    table.set_cols_dtype(["t", "t", "t", "t", "t"])
    table.set_cols_align(["c", "c", "c", "c", "c"])
    table.header([
        "Permutation n (+1)",
        "Comb/Search n (x2)",
        "Permutation Sort (s)",
        "Comb Sort (s)",
        "Interpolation Search (s)"
    ])

    for _ in range(5):
        lst_perm = perm_gen(perm_n)
        lst_comb = comb_gen(n)
        lst_search = search_gen(n)

        # Permutation Sort
        if perm_n <= 10:
            start_ps = timeit.default_timer()
            permutation_sort_without_step(lst_perm)
            end_ps = timeit.default_timer()
            ps_time = end_ps - start_ps
            ps_time_str = f"{ps_time:.7f}"
        else:
            ps_time_str = "Too Slow"

        # Comb Sort
        start_cs = timeit.default_timer()
        comb_sort_without_step(lst_comb)
        end_cs = timeit.default_timer()
        cs_time = end_cs - start_cs
        cs_time_str = f"{cs_time:.7f}"

        # Interpolation Search
        if case_name == "Best Case":
            target = lst_search[randint(0, n - 1)]
        elif case_name == "Average Case":
            target = lst_search[randint(0, n - 1)]
        else:  # Worst Case
            target = lst_search[-1]+10

        start_s = timeit.default_timer()
        interpolation_search(lst_search, target)
        end_s = timeit.default_timer()
        s_time = end_s - start_s
        s_time_str = f"{s_time:.7f}"

        table.add_row([str(perm_n), str(n), ps_time_str, cs_time_str, s_time_str])

        perm_n += 1  # +1 for permutation sort
        n *= 2       # double for comb&interpolation

    print(f"\n{case_name} Table:")
    print(table.draw(), "\n")




# user interface
def main():
    print_menu()
    example_list = []
    generated_list = False
    sorted_list=False
    while True:
        option = get_int_input("Select an option: ", 1, 8)

        if option == 1:
            n = get_int_input("Choose a value for n: ", 1)
            example_list = generate_number_list(n)
            print(example_list)
            generated_list = True

        elif option == 2:
            if not generated_list:
                print("The list must be generated before searching!")
                continue
            if not sorted_list:
                print("The list must be sorted before searching!")
                continue
            x = get_int_input("Choose a value for the number searched in the list: ")
            res = interpolation_search(example_list, x)
            if res == -1:
                print("The number", x, "is not in the list!")
            else:
                print("The given number was found at index", res)

        elif option == 3:
            if not generated_list:
                print("The list must be generated before sorting!")
                continue
            step = get_int_input("Choose a value for step: ", 1)
            permutation_sort(example_list, step)
            sorted_list = True

        elif option == 4:
            if not generated_list:
                print("The list must be generated before sorting!")
                continue
            step = get_int_input("Choose a value for step: ", 1)
            comb_sort(example_list, step)
            sorted_list = True

        #table(permutation, comb, search)

        elif option == 5:

            build_table("Best Case", generate_sorted_list, generate_sorted_list, generate_best_case_list)

        elif option == 6:

            build_table("Average Case", generate_number_list, generate_number_list, generate_number_list)

        elif option == 7:

            build_table("Worst Case", generate_reversed_sorted_list, generate_worst_case_comb, generate_worst_case_list)
        else:
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()