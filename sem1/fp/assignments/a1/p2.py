# Solve the problem from the second set here


# prime_number(n) checks if n is a prime number
def prime_number(n):
    if n<2:
        return False
    elif n==2:
        return True
    elif n%2==0:
        return False
    else:
        d=3
        while d*d<=n:
            if n%d==0:
                return False
            d=d+2
        return True


# twin_primes(n) finds the first pair of twin prime numbers (p1, p2). p1 starts from n+1, the function checks if both p1 and
# p2 (p1+2) are prime, in which case it stops; otherwise the process continues
def twin_primes(n):
    p1=n+1
    while True:
        p2=p1+2
        if prime_number(p1) and prime_number(p2):
            return p1, p2
        p1=p1+1

def main():
    n=int(input("Enter a natural number n: "))
    p1, p2 = twin_primes(n)
    print("The twin prime numbers immediately larger than",n,"are",p1,"and",p2)

if __name__=='__main__':
    main()