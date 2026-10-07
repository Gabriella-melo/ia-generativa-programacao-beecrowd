import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    num_tokens = len(input_data)
    
    while idx < num_tokens:
        N = int(input_data[idx])
        idx += 1
        
        points = []
        for _ in range(N):
            x = int(input_data[idx])
            y = int(input_data[idx+1])
            idx += 2
            points.append((x, y))
        
        # Sort points by x-coordinate ascending
        points.sort(key=lambda p: p[0])
        
        max_points = 0
        
        # Group points by y-coordinate
        by_y = {}
        for x, y in points:
            if y not in by_y:
                by_y[y] = []
            by_y[y].append(x)
        
        for y1 in by_y:
            y2 = y1 + 2
            if y2 not in by_y:
                continue
            
            x_list1 = by_y[y1]
            x_list2 = by_y[y2]
            
            len1 = len(x_list1)
            len2 = len(x_list2)
            
            # Case 1: Sequence starts with y1
            p1, p2 = 0, 0
            count1 = 0
            curr_y = y1
            while True:
                if curr_y == y1:
                    # Find first point in x_list1 with x > previous x (if any)
                    # Since x_list1 is sorted, we just advance p1 until x_list1[p1] > last_x
                    if count1 > 0:
                        last_x = x_list2[p2 - 1]
                        while p1 < len1 and x_list1[p1] <= last_x:
                            p1 += 1
                    if p1 < len1:
                        count1 += 1
                        p1 += 1
                        curr_y = y2
                    else:
                        break
                else:
                    last_x = x_list1[p1 - 1]
                    while p2 < len2 and x_list2[p2] <= last_x:
                        p2 += 1
                    if p2 < len2:
                        count1 += 1
                        p2 += 1
                        curr_y = y1
                    else:
                        break
            
            # Case 2: Sequence starts with y2
            p1, p2 = 0, 0
            count2 = 0
            curr_y = y2
            while True:
                if curr_y == y2:
                    if count2 > 0:
                        last_x = x_list1[p1 - 1]
                        while p2 < len2 and x_list2[p2] <= last_x:
                            p2 += 1
                    if p2 < len2:
                        count2 += 1
                        p2 += 1
                        curr_y = y1
                    else:
                        break
                else:
                    last_x = x_list2[p2 - 1]
                    while p1 < len1 and x_list1[p1] <= last_x:
                        p1 += 1
                    if p1 < len1:
                        count2 += 1
                        p1 += 1
                        curr_y = y2
                    else:
                        break
                        
            if count1 > max_points:
                max_points = count1
            if count2 > max_points:
                max_points = count2

        print(max_points)

if __name__ == '__main__':
    solve()
