"""
Dynamic Programming solution for:
Maximize A[m] - A[n] + A[p] - A[q], where m > n > p > q.

For A = [30, 5, 15, 18, 30, 40],
the maximum value is 32 (40 - 18 + 15 - 5).
"""

import math
from pprint import pprint

# rewrite the expression : - A[q] + A[p] - A[n] + A[m], q<p<n<m


# naive version
def brute_force_max_expr(a):
    n = len(a)
    best_val = -math.inf
    best_tuple = None  # stores indexes (m, n, p, q)

    for q in range(0, n - 3):
        for p in range(q + 1, n - 2):
            for n_idx in range(p + 1, n - 1):
                for m in range(n_idx + 1, n):
                    val = a[m] - a[n_idx] + a[p] - a[q]
                    if val > best_val:
                        best_val = val
                        best_tuple = (m, n_idx, p, q)
    return best_val, best_tuple

def dp_max_expr(a):
    n = len(a)

    stages = 4  # we need to find 4 values
    sign = [-1, +1, -1, +1]

    # DP table: 4 rows (stages) × n columns
    # dp[k][i] = the maximum value achievable up to index i,having completed k stages.
    dp = [[-math.inf] * n for _ in range(stages)]


    # store values used to get the best value, in order to reconstruct the expression at the end
    values = [[[] for _ in range(n)] for _ in range(stages)]

    # base case for stage 0
    dp[0][0] = -a[0]      # for stage 0 (just -A[q]), at index 0, best value is -a[0]
    values[0][0] = [a[0]]       # store a[0] as the chosen value


    print("Iteration: 1")
    pprint(dp)
    print()


    for i in range(1, n):
        for k in range(stages):

            if k == 0:
                # the formula for the base stage
                dp[k][i] = max(dp[k][i - 1], -a[i])

                # keep track of which value was chosen
                if dp[k][i] == -a[i]:
                    values[k][i] = [a[i]]           # if we use current element, add it to the sequence
                else:
                    values[k][i] = values[k][i - 1]     #  copy previous sequence

            else:
                # general formula for all other stages
                dp[k][i] = max(dp[k][i - 1], dp[k - 1][i - 1] + sign[k] * a[i])

                # keep track of which value was chosen
                if dp[k][i] == dp[k - 1][i - 1] + sign[k] * a[i]:
                    values[k][i] = values[k - 1][i - 1] + [a[i]]       # if we use current element, add it to the sequence
                else:
                    values[k][i] = values[k][i - 1]             #  copy previous sequence

        print("Iteration:", i + 1)
        pprint(dp)
        print()



    # final answer
    max_val = dp[3][-1]     # the maximum is in the last cell of the data structure
    seq = values[3][-1]

    q, p, n_, m = seq
    expr = f"{m} - {n_} + {p} - {q}"


    print(f"Maximum value: {max_val}")
    print(f"Expression: {expr}")





def main():
    a = [30, 5, 15, 18, 30, 40]
    print("Array A:", a)
    print()

    # naive version
    print("Solution obtained using the NAIVE VERSION:")
    bf_val, bf_tuple = brute_force_max_expr(a)
    bf_expr = f"{a[bf_tuple[0]]} - {a[bf_tuple[1]]} + {a[bf_tuple[2]]} - {a[bf_tuple[3]]}"
    print(f"Expression: {bf_expr}","=",bf_val)
    print()

    # DP version
    print("Solution obtained using DYNAMIC PROGRAMMING:")
    dp_max_expr(a)



if __name__ == "__main__":
    main()