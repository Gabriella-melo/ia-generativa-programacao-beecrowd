import sys

def main():
    data = sys.stdin.read().split()
    i = 0
    output = []

    while i < len(data):
        n = int(data[i])
        i += 1

        max_speed = -1

        for day in range(1, n + 1):
            t = int(data[i])
            d = int(data[i + 1])
            i += 2

            # Compare d/t without using floating point.
            if day == 1 or d * max_time > max_distance * t:
                output.append(str(day))
                max_distance = d
                max_time = t

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    main()
