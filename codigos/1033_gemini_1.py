import sys

def matrix_mult(A, B, mod):
    return [
        [(A[0][0]*B[0][0] + A[0][1]*B[1][0] + A[0][2]*B[2][0]) % mod,
         (A[0][0]*B[0][1] + A[0][1]*B[1][1] + A[0][2]*B[2][1]) % mod,
         (A[0][0]*B[0][2] + A[0][1]*B[1][2] + A[0][2]*B[2][2]) % mod],
        [(A[1][0]*B[0][0] + A[1][1]*B[1][0] + A[1][2]*B[2][0]) % mod,
         (A[1][0]*B[0][1] + A[1][1]*B[1][1] + A[1][2]*B[2][1]) % mod,
         (A[1][0]*B[0][2] + A[1][1]*B[1][2] + A[1][2]*B[2][2]) % mod],
        [(A[2][0]*B[0][0] + A[2][1]*B[1][0] + A[2][2]*B[2][0]) % mod,
         (A[2][0]*B[0][1] + A[2][1]*B[1][1] + A[2][2]*B[2][1]) % mod,
         (A[2][0]*B[0][2] + A[2][1]*B[1][2] + A[2][2]*B[2][2]) % mod]
    ]

def matrix_pow(M, p, mod):
    result = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
    base = M
    while p > 0:
        if p & 1:
            result = matrix_mult(result, base, mod)
        base = matrix_mult(base, base, mod)
        p >>= 1
    return result

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    case_num = 1
    idx = 0
    while idx < len(input_data):
        n = int(input_data[idx])
        b = int(input_data[idx+1])
        idx += 2
        
        if n == 0 and b == 0:
            break
            
        if n == 0:
            ans = 1 % b
        elif n == 1:
            ans = 1 % b
        else:
            # Transition matrix T for [calls(n), calls(n-1), 1]^T
            # T * [calls(k), calls(k-1), 1]^T = [calls(k+1), calls(k), 1]^T
            # where T = [[1, 1, 1], [1, 0, 0], [0, 0, 1]]
            # We want calls(n) starting from [calls(1), calls(0), 1]^T = [1, 1, 1]^T
            # So [calls(n), calls(n-1), 1]^T = T^(n-1) * [1, 1, 1]^T
            T = [
                [1, 1, 1],
                [1, 0, 0],
                [0, 0, 1]
            ]
            Tn = matrix_pow(T, n - 1, b)
            ans = (Tn[0][0] + Tn[0][1] + Tn[0][2]) % b
            
        print(f"Case {case_num}: {n} {b} {ans}")
        case_num += 1

if __name__ == '__main__':
    solve()
