import sys

def matrix_mult(A, B, m):
    return [
        [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % m, (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % m],
        [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % m, (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % m]
    ]

def matrix_pow(A, p, m):
    res = [[1, 0], [0, 1]]
    base = A
    while p > 0:
        if p % 2 == 1:
            res = matrix_mult(res, base, m)
        base = matrix_mult(base, base, m)
        p //= 2
    return res

def solve():
    lines = sys.stdin.read().split()
    if not lines:
        return
    
    idx = 0
    case_num = 1
    while idx < len(lines):
        n = int(lines[idx])
        b = int(lines[idx+1])
        idx += 2
        
        if n == 0 and b == 0:
            break
            
        if n == 0 or n == 1:
            ans = 1 % b
        else:
            # We use the recurrence for total calls: C(n) = 2*fib(n+1) - 1
            # Matrice M = [[1, 1], [1, 0]], M^n = [[fib(n+1), fib(n)], [fib(n), fib(n-1)]]
            M = [[1, 1], [1, 0]]
            M_pow = matrix_pow(M, n, b)
            fib_n_plus_1 = M_pow[0][0]
            ans = (2 * fib_n_plus_1 - 1) % b
            if ans < 0:
                ans += b
                
        print(f"Case {case_num}: {n} {b} {ans}")
        case_num += 1

if __name__ == '__main__':
    solve()