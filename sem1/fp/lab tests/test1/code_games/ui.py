from functions import *


def print_ui():
    cn = generate_number()
    while True:
        hn = int(input("Enter your guess: "))
        if not valid(hn):
            print("Game over!")
            break
        else:
            if hn == 8086:
                print("The number you're looking for is", cn)
            elif hn == cn:
                print("Congratulations! You guessed the secret number!")
                break
            else:
                print("Sorry, the number you entered is not correct!")
                codes = codes_count(cn, hn)
                runners = runners_count(cn, hn)
                print("The number of codes reported is", codes)
                print("The number of runners reported is", runners)