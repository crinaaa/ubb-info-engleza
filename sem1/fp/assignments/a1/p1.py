# Solve the problem from the first set here

# number_digits(n) returns a list of n’s digits.
def number_digits(n):
    digits = []
    while n > 0:
        digits.append(n % 10)
        n = n // 10
    return digits


# sort_digits(n) sorts the list of digits in ascending order
def sort_digits(digits):
    n=len(digits)
    for i in range(0,n-1,1):
        for j in range(i+1,n,1):
            if digits[i]>digits[j]:
                digits[i],digits[j] = digits[j],digits[i]
    return digits


# calculate_number(n) reconstructs the number from a list of digits
def calculate_number(digits):
    nr=0
    for i in digits:
        nr=nr*10+i
    return nr


# new_number(n) creates the smallest number possible from the digits of n (without leading zeros)
def new_number(n):
    digits=number_digits(n)
    digits=sort_digits(digits)

    if digits[0]==0:
        for i in range(1, len(digits)):
            if digits[i]!=0:
                digits[0], digits[i] = digits[i], digits[0]
                break

    return calculate_number(digits)

def main():
    n=int(input("Enter a natural number n: "))
    m=new_number(n)
    print("The minimal natural number written with the same digits as",n, "is", m)

if __name__=='__main__':
    main()