import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    while True:
        try:
            n_str = next(iterator)
        except StopIteration:
            break
        
        N = int(n_str)
        points = []
        for _ in range(N):
            x = int(next(iterator))
            y = int(next(iterator))
            points.append((x, y))
        
        # Sort points by x-coordinate
        points.sort(key=lambda p: p[0])
        
        # Find all candidate values for y_base (which corresponds to a - 1)
        # Since y = a - 1 or a + 1, the two allowed y levels are a - 1 and a + 1.
        # Their difference is 2, so y_upper - y_lower = 2.
        # Any valid point must have its y equal to y_lower or y_lower + 2.
        y_bases = set()
        for x, y in points:
            y_bases.add(y)
            y_bases.add(y - 2)
            
        max_points = 0
        
        for y_base in y_bases:
            y_low = y_base
            y_high = y_base + 2
            
            # dp0: max points ending with y_low
            # dp1: max points ending with y_high
            dp0 = 0
            dp1 = 0
            
            last_x = None
            
            # Process points grouped by x coordinate
            i = 0
            while i < len(points):
                x = points[i][0]
                has_low = False
                has_high = False
                
                while i < len(points) and points[i][0] == x:
                    y = points[i][1]
                    if y == y_low:
                        has_low = True
                    elif y == y_high:
                        has_high = True
                    i += 1
                
                if not has_low and not has_high:
                    continue
                
                new_dp0 = dp0
                new_dp1 = dp1
                
                if has_low:
                    new_dp0 = max(dp0, dp1 + 1)
                if has_high:
                    new_dp1 = max(dp1, dp0 + 1)
                
                dp0 = new_dp0
                dp1 = new_dp1
            
            max_points = max(max_points, dp0, dp1)
            
        print(max_points)

if __name__ == '__main__':
    solve()
