import sys
from collections import deque

def solve(strings):
    n = len(strings)

    # Trie using sparse linked edges.
    head = [-1]
    edge_to = []
    edge_next = []
    edge_char = []

    def new_node():
        head.append(-1)
        return len(head) - 1

    def get_child(v, c):
        e = head[v]
        while e != -1:
            if edge_char[e] == c:
                return edge_to[e]
            e = edge_next[e]
        return -1

    def add_child(v, c):
        u = new_node()
        edge_to.append(u)
        edge_char.append(c)
        edge_next.append(head[v])
        head[v] = len(edge_to) - 1
        return u

    terminal = [0] * n
    node_of = [0] * n

    for i, s in enumerate(strings):
        v = 0
        for ch in s:
            c = ord(ch) - 97
            u = get_child(v, c)
            if u == -1:
                u = add_child(v, c)
            v = u
        terminal[i] = v
        node_of[i] = v

    m = len(head)

    fail = [0] * m

    # Build failure links.
    q = deque()
    e = head[0]
    while e != -1:
        u = edge_to[e]
        fail[u] = 0
        q.append(u)
        e = edge_next[e]

    while q:
        v = q.popleft()
        e = head[v]
        while e != -1:
            c = edge_char[e]
            u = edge_to[e]

            f = fail[v]
            w = get_child(f, c)
            while f and w == -1:
                f = fail[f]
                w = get_child(f, c)

            if w != -1 and w != u:
                fail[u] = w
            else:
                fail[u] = 0

            q.append(u)
            e = edge_next[e]

    # Failure tree, for Euler intervals.
    fhead = [-1] * m
    fnext = [-1] * m
    for v in range(1, m):
        p = fail[v]
        fnext[v] = fhead[p]
        fhead[p] = v

    # Iterative Euler tour of failure tree.
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
            u = fhead[v]
            while u != -1:
                stack.append((u, 0))
                u = fnext[u]
        else:
            tout[v] = timer - 1

    # Segment tree supporting:
    # range chmax update + point max query.
    size = 1
    while size < m:
        size <<= 1
    seg = [0] * (size << 1)

    def range_update(l, r, value):
        l += size
        r += size
        while l <= r:
            if l & 1:
                if seg[l] < value:
                    seg[l] = value
                l += 1
            if not (r & 1):
                if seg[r] < value:
                    seg[r] = value
                r -= 1
            l >>= 1
            r >>= 1

    def point_query(p):
        p += size
        ans = 0
        while p:
            if seg[p] > ans:
                ans = seg[p]
            p >>= 1
        return ans

    order = sorted(range(n), key=lambda i: len(strings[i]))

    dp = [1] * n
    answer = 1

    pos = 0
    while pos < n:
        end = pos + 1
        length = len(strings[order[pos]])
        while end < n and len(strings[order[end]]) == length:
            end += 1

        # Compute all strings of this length before inserting them,
        # so a string cannot use another string of the same length.
        for k in range(pos, end):
            idx = order[k]
            s = strings[idx]
            v = 0
            best = 0

            for ch in s:
                c = ord(ch) - 97
                u = get_child(v, c)

                while u == -1 and v:
                    v = fail[v]
                    u = get_child(v, c)

                if u == -1:
                    v = 0
                else:
                    v = u

                x = point_query(tin[v])
                if x > best:
                    best = x

            dp[idx] = best + 1
            if dp[idx] > answer:
                answer = dp[idx]

        # Activate all strings of this length.
        for k in range(pos, end):
            idx = order[k]
            v = node_of[idx]
            range_update(tin[v], tout[v], dp[idx])

        pos = end

    return answer


def main():
    data = sys.stdin.buffer
    out = []

    while True:
        line = data.readline()
        if not line:
            break

        n = int(line)
        if n == 0:
            break

        strings = [data.readline().strip() for _ in range(n)]
        out.append(str(solve(strings)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()