"""
3. The sequence a = a1, ..., an with integer elements is given.
Determine all strictly increasing subsequences of sequence a (conserve the order of elements in the original sequence).
"""

"""
# 1 3 7 4 2 6 8 9 10 5

1
1 3 
1 3 7 
1 3 7 8
1 3 7 8 9
1 3 7 8 9 10
1 7
1 7 8
1 7 9
1 7 9 10
1 4
1 4 6....

"""


import random

# this functions checks if we can add elements in the list
def can_add(current_subsequence, candidate):
    #if the sequence is empty, we can add the candidate
    if not current_subsequence:
        return True
    #add the candidate only if it is greater than the last one in the list
    return candidate > current_subsequence[-1]


def iterative_version(sequence):
    n = len(sequence)
    result = []   #the list of "good" subsequences
    #current[i] = value at position i of the subsequence
    current = []        #stores one subsequence at a time
    # indices[i] = index in sequence for next element after current[i-1]
    indices = []

    i = 0  #we start from index 0
    while True:
        #adding elements in the subsequence
        while i < n:
            if can_add(current, sequence[i]):   #if the candidate is ok
                current.append(sequence[i])     #we update the current[] with the new value
                indices.append(i + 1)           #we update the indices[] to keep track of the position where we are currently
                result.append(current.copy())   #record current subsequence
            i += 1      #goes to the next element

        # Backtrack
        if not current:     #we found all the possibilities
            break  # finish the function
        i = indices.pop()   #pop last element and continue from next index
        current.pop()   #pop the last value, to make space for the next one

    return result



def recursive_version(sequence):
    result = []             #the list of "good" subsequences

    def backtrack(start_index, current):
        #if the current subsequence is not empty, we save it in the result[]
        if current:
            result.append(current.copy())

        #check the remaining elements
        for i in range(start_index, len(sequence)):     #pass through the list to search the elements
            if can_add(current, sequence[i]):           #if the candidate is ok
                current.append(sequence[i])             #we update the current[] with the new value
                backtrack(i + 1, current)  #            #go recursively and check for other elements, but on the position starting from the next index
                current.pop()                           #undo the choice, to make room for other possible candidates


    backtrack(0, [])                    #the first call of the function
    return result



def print_menu():
    print("\nMenu:")
    print("1. Enter n (size of the list)")
    print("2. Generate a random list of n numbers from [0,100]")
    print("3. Show strictly increasing subsequences (iterative)")
    print("4. Show strictly increasing subsequences (recursive)")
    print("5. Exit")


def get_int_input(prompt, min_value=None):
    while True:
        try:
            num = int(input(prompt))
            if min_value is not None and num < min_value:
                print(f"Please enter a number >= {min_value}")
                continue
            return num
        except ValueError:
            print("Invalid input! Enter a valid integer.")


def main():
    n = None
    sequence = None
    print_menu()

    while True:
        choice = get_int_input("Choose an option (1-5): ", 1)

        if choice == 1:
            n = get_int_input("Enter n (positive integer): ", 1)
            sequence = None

        elif choice == 2:
            if n is None:
                print("First choose option 1 to set n!")
            else:
                sequence = [random.randint(0, 100) for _ in range(n)]
                print("Generated list:", sequence)

        elif choice == 3:
            if sequence is None:
                print("You must generate a list first (option 2)!")
            else:
                print("\nIterative result:")
                subs = iterative_version(sequence)
                for s in subs:
                    print(s)

        elif choice == 4:
            if sequence is None:
                print("You must generate a list first (option 2)!")
            else:
                print("\nRecursive result:")
                subs = recursive_version(sequence)
                for s in subs:
                    print(s)

        elif choice == 5:
            print("Exiting the program.")
            break

if __name__ == '__main__':
    main()
