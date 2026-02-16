# Solve the problem from the third set here

# sum_of_divisors(n) calculates the sum of n's divisors (without n), in an efficient way, going as far as the square root of n
def sum_of_divisors(n):
    s=1
    for i in range(2,int(n**0.5)+1,1):
        if n%i==0:
            s+=i
            if i*i!=n:
                s+=n//i
    return s


# perfect_number(n) checks if n is a perfect number, using the function above
def perfect_number(n):
    if n==sum_of_divisors(n) and n!=1:
        return True
    else:
        return False


# largest_number(n) finds the largest perfect number smaller than n.
# it starts from n-1 and checks downward until it finds one or reaches 0.

def largest_number(n):
    start=n-1
    while start>0:
        if perfect_number(start):
            return start
        start=start-1
    return None


def main():
    n=int(input("Enter a natural number n: "))
    m=largest_number(n)
    if m is not None:
        print("The largest parfect number smaller than", n, "is", m)
    else:
        print("A perfect smaller number than", n, "DOES NOT exist.")

if __name__ == '__main__':
    main()