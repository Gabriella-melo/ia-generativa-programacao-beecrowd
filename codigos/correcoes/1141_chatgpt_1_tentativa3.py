import sys
from collections import deque


def solve(strings):
    # Trie / Aho-Corasick
    nxt = [{}]
    fail = [0]
    parent = [-1]
    pchar = [-1]
    terminal = [-1]

    terminals = []

    for idx, s in enumerate(strings):
        v = 0
        for ch in s:
            c = ord(ch) - 97
            u = nxt[v].get(c)
            if u is None:
                u = len(nxt)
                nxt[v][c] = u
                nxt.append({})
                fail.append(0)
                parent.append(v)
                pchar.append(c)
                terminal.append(-1)
            v = u
        terminal[v] = idx
        terminals.append(v)

    m = len(nxt)

    # Build failure links.
    q = deque()

    for c, u in nxt[0].items():
        fail[u] = 0
        q.append(u)

    while q:
        v = q.popleft()

        for c, u in nxt[v].items():
            f = fail[v]

            while f and c not in nxt[f]:
                f = fail[f]

            w = nxt[f].get(c)
            if w is None:
                w = 0

            fail[u] = w
            q.append(u)

    # Failure tree, then Euler tour.
    children = [[] for _ in range(m)]
    for v in range(1, m):
        children[fail[v]].append(v)

    tin = [0] * m
    tout = [0] * m

    timer = 0
    stack = [(0, 0)]

    while stack:
        v, state = stack.pop()

        if state == 0:
            tin[v] = timer
            timer += 1
            stack.append((v, 1))

            for u in reversed(children[v]):
                stack.append((u, 0))
        else:
            tout[v] = timer - 1

    # Range chmax + point query using sqrt decomposition.
    B = 1024
    nb = (m + B - 1) // B
    lazy = [0] * nb
    point = [0] * m

    def update(l, r, value):
        bl = l // B
        br = r // B

        if bl == br:
            end = r + 1
            for i in range(l, end):
                if point[i] < value:
                    point[i] = value
            return

        end = (bl + 1) * B
        for i in range(l, end):
            if point[i] < value:
                point[i] = value

        for b in range(bl + 1, br):
            if lazy[b] < value:
                lazy[b] = value

        start = br * B
        for i in range(start, r + 1):
            if point[i] < value:
                point[i] = value

    def query(pos):
        v = point[pos]
        z = lazy[pos // B]
        return z if z > v else v

    # Process strictly by increasing length.
    # Equal-length different strings can never contain one another.
    order = sorted(range(len(strings)), key=lambda i: len(strings[i]))

    dp = [0] * len(strings)
    answer = 1

    i = 0
    n = len(strings)

    while i < n:
        j = i
        length = len(strings[order[i]])

        while j < n and len(strings[order[j]]) == length:
            j += 1

        # Calculate all DP values of this length before updating
        # the structure, preventing equal-length strings from chaining.
        for k in range(i, j):
            idx = order[k]
            s = strings[idx]

            v = 0
            best = 0

            for ch in s:
                c = ord(ch) - 97

                while v and c not in nxt[v]:
                    v = fail[v]

                u = nxt[v].get(c)
                if u is None:
                    v = 0
                else:
                    v = u

                x = query(tin[v])
                if x > best:
                    best = x

            dp[idx] = best + 1
            if dp[idx] > answer:
                answer = dp[idx]

        # Now activate all strings of this length.
        for k in range(i, j):
            idx = order[k]
            v = terminals[idx]
            update(tin[v], tout[v], dp[idx])

        i = j

    return answer


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    out = []

    while pos < len(data):
        n = int(data[pos])
        pos += 1

        if n == 0:
            break

        strings = data[pos:pos + n]
        pos += n

        out.append(str(solve(strings)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()