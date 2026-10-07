import sys
import math

input = sys.stdin.readline

c = int(input())

for _ in range(c):
    n, m = map(int, input().split())
    
    if n == 1:
        print(1)
    else:
        digits = int(m * math.log10(n)) + 1
        print(digits)