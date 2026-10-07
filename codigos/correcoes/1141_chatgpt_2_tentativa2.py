import sys
from array import array
from collections import deque


def solve(strings):
    n = len(strings)

    # Trie / Aho-Corasick represented with compact integer arrays.
    first = array('i', [-1])
    to = array('i')
    nxt = array('i')
    char = array('b')

    terminal = array('i', [-1])

    def new_node():
        first.append(-1)
        terminal.append(-1)
        return len(first) - 1

    def find_child(v, c):
        e = first[v]
        while e != -1:
            if char[e] == c:
                return to[e]
            e = nxt[e]
        return -1

    def add_child(v, c):
        u = new_node()
        to.append(u)
        char.append(c)
        nxt.append(first[v])
        first[v] = len(to) - 1
        return u

    # Build trie.
    for i, s in enumerate(strings):
        v = 0
        for ch in s:
            c = ch - 97
            u = find_child(v, c)
            if u == -1:
                u = add_child(v, c)
            v = u
        terminal[v] = i

    nodes = len(first)

    # Failure links.
    fail = array('i', [0]) * nodes

    # Failure-tree adjacency.
    ffirst = array('i', [-1]) * nodes
    fnxt = array('i', [-1]) * nodes

    q = deque()

    e = first[0]
    while e != -1:
        u = to[e]
        q.append(u)
        e = nxt[e]

    while q:
        v = q.popleft()

        e = first[v]
        while e != -1:
            u = to[e]
            c = char[e]

            f = fail[v]
            w = find_child(f, c)

            while f != 0 and w == -1:
                f = fail[f]
                w = find_child(f, c)

            if w != -1:
                fail[u] = w
            else:
                fail[u] = 0

            q.append(u)
            e = nxt[e]

    # Build failure tree.
    for v in range(1, nodes):
        p = fail[v]
        fnxt[v] = ffirst[p]
        ffirst[p] = v

    # Euler intervals of the failure tree.
    tin = array('i', [0]) * nodes
    tout = array('i', [0]) * nodes

    timer = 0
    stack = [(0, ffirst[0], False)]

    while stack:
        v, child, exiting = stack.pop()

        if not exiting:
            tin[v] = timer
            timer += 1

            stack.append((v, -1, True))

            children = []
            u = child
            while u != -1:
                children.append(u)
                u = fnxt[u]

            for u in reversed(children):
                stack.append((u, ffirst[u], False))
        else:
            tout[v] = timer - 1

    # Segment tree for range maximum updates and point queries.
    size = 1
    while size < nodes:
        size <<= 1

    seg = array('i', [0]) * (size * 2)

    def update(l, r, value):
        l += size
        r += size

        while l <= r:
            if l & 1:
                if value > seg[l]:
                    seg[l] = value
                l += 1

            if not (r & 1):
                if value > seg[r]:
                    seg[r] = value
                r -= 1

            l >>= 1
            r >>= 1

    def query(p):
        p += size
        result = 0

        while p:
            if seg[p] > result:
                result = seg[p]
            p >>= 1

        return result

    # Process by increasing length.
    order = sorted(range(n), key=lambda i: len(strings[i]))
    dp = array('i', [0]) * n

    answer = 1
    pos = 0

    while pos < n:
        end = pos + 1
        current_len = len(strings[order[pos]])

        while end < n and len(strings[order[end]]) == current_len:
            end += 1

        # Calculate DP first, without activating this length.
        for k in range(pos, end):
            idx = order[k]
            s = strings[idx]

            v = 0
            best = 0

            for ch in s:
                c = ch - 97

                u = find_child(v, c)

                while u == -1 and v != 0:
                    v = fail[v]
                    u = find_child(v, c)

                if u == -1:
                    v = 0
                else:
                    v = u

                value = query(tin[v])
                if value > best:
                    best = value

            cur = best + 1
            dp[idx] = cur

            if cur > answer:
                answer = cur

        # Activate strings of this length.
        for k in range(pos, end):
            idx = order[k]
            node = -1

            # Find the terminal node again.
            v = 0
            for ch in strings[idx]:
                u = find_child(v, ch - 97)
                v = u
            node = v

            update(tin[node], tout[node], dp[idx])

        pos = end

    return answer


def main():
    input_data = sys.stdin.buffer
    output = []

    while True:
        line = input_data.readline()
        if not line:
            break

        n = int(line)
        if n == 0:
            break

        strings = []
        for _ in range(n):
            strings.append(input_data.readline().strip())

        output.append(str(solve(strings)))

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()