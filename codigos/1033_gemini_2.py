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
            
        if n == 0:
            ans = 1 % b
        elif n == 1:
            ans = 1 % b
        else:
            T = [[1, 1], [1, 0]]
            T_pow = matrix_pow(T, n - 1, b)
            # C(n) = (2 * T_pow[0][0] - 1) % b
            ans = (2 * T_pow[0][0] - 1) % b
            if ans < 0:
                ans += b
                
        print(f"Case {case_num}: {n} {b} {ans}")
        case_num += 1

if __name__ == '__main__':
    solve()
