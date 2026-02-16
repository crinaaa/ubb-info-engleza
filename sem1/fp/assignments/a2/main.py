from random import randint

# This function prints the menu of our console driven application
def print_menu():
    print("1. Generate a list of n natural numbers.")
    print("2. Search for an item in the list using Interpolation Search.")
    print("3. Sort this list using Permutation Sort.")
    print("4. Sort this list using Comb Sort.")
    print("5. Exit the program.")

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

# This function check if the list is sorted
def is_sorted(number_list):
    for i in range(0, len(number_list)-1):
        if number_list[i] > number_list[i + 1]:
            return False
    return True


"""
The next functions are used for implementing Comb Sort.
"""

# We print the list in its actual state for every iteration until the [step] value
def print_step_comb_sort(number_list, step):
    print("Step", step, ":", number_list)

# This function computes successively the gap we use in Comb Sort implementation
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
        if pos < left or pos > right:  # left and right indices change, so the pos value my not be in the right range(infinite loop!)
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


# user interface
def main():
    print_menu()
    example_list = []
    generated_list = False
    sorted_list=False
    while True:
        option = get_int_input("Select an option: ", 1, 5)

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
            sorted_list=True

        elif option == 4:
            if not generated_list:
                print("The list must be generated before sorting!")
                continue
            step = get_int_input("Choose a value for step: ", 1)
            comb_sort(example_list, step)
            sorted_list = True

        elif option == 5:
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()

