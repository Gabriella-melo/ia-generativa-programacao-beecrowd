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
        
        if N == 0:
            print(0)
            continue

        points = []
        for _ in range(N):
            x = int(input_data[idx])
            y = int(input_data[idx+1])
            idx += 2
            points.append((x, y))
        
        by_y = {}
        for x, y in points:
            if y not in by_y:
                by_y[y] = []
            by_y[y].append(x)
            
        for y in by_y:
            by_y[y].sort()
        
        max_points = 1
        
        for y1 in by_y:
            y2 = y1 + 2
            if y2 not in by_y:
                continue
            
            x_list1 = by_y[y1]
            x_list2 = by_y[y2]
            
            len1 = len(x_list1)
            len2 = len(x_list2)
            
            p1, p2 = 0, 0
            count1 = 0
            last_x = -float('inf')
            while True:
                while p1 < len1 and x_list1[p1] <= last_x:
                    p1 += 1
                if p1 < len1:
                    count1 += 1
                    last_x = x_list1[p1]
                    p1 += 1
                else:
                    break
                
                while p2 < len2 and x_list2[p2] <= last_x:
                    p2 += 1
                if p2 < len2:
                    count1 += 1
                    last_x = x_list2[p2]
                    p2 += 1
                else:
                    break
            
            p1, p2 = 0, 0
            count2 = 0
            last_x = -float('inf')
            while True:
                while p2 < len2 and x_list2[p2] <= last_x:
                    p2 += 1
                if p2 < len2:
                    count2 += 1
                    last_x = x_list2[p2]
                    p2 += 1
                else:
                    break

                while p1 < len1 and x_list1[p1] <= last_x:
                    p1 += 1
                if p1 < len1:
                    count2 += 1
                    last_x = x_list1[p1]
                    p1 += 1
                else:
                    break
                        
            if count1 > max_points:
                max_points = count1
            if count2 > max_points:
                max_points = count2

        print(max_points)

if __name__ == '__main__':
    solve()