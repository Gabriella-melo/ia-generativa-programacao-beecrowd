import sys
from collections import deque
from array import array


def solve(strings):
    first = array('i', [-1])
    to = array('i')
    nxt = array('i')
    chars = array('b')

    node_of = array('i')

    def new_node():
        first.append(-1)
        return len(first) - 1

    def add_edge(v, c):
        u = new_node()
        to.append(u)
        chars.append(c)
        nxt.append(first[v])
        first[v] = len(to) - 1
        return u

    # Build trie.
    for s in strings:
        v = 0
        for b in s:
            c = b - 97
            e = first[v]
            u = -1

            while e != -1:
                if chars[e] == c:
                    u = to[e]
                    break
                e = nxt[e]

            if u == -1:
                u = add_edge(v, c)

            v = u

        node_of.append(v)

    m = len(first)

    # For nodes having only one child, direct lookup avoids traversing
    # the linked list. This is important because most trie nodes have
    # a single child.
    only_char = array('b', [-1]) * m
    only_child = array('i', [-1]) * m

    for v in range(m):
        e = first[v]
        if e != -1 and nxt[e] == -1:
            only_char[v] = chars[e]
            only_child[v] = to[e]

    def child(v, c):
        oc = only_char[v]
        if oc == c:
            return only_child[v]

        e = first[v]
        while e != -1:
            if chars[e] == c:
                return to[e]
            e = nxt[e]
        return -1

    # Aho-Corasick failure links.
    fail = array('i', [0]) * m
    q = deque()

    e = first[0]
    while e != -1:
        q.append(to[e])
        e = nxt[e]

    while q:
        v = q.popleft()
        e = first[v]

        while e != -1:
            u = to[e]
            c = chars[e]

            f = fail[v]
            w = child(f, c)

            while w == -1 and f != 0:
                f = fail[f]
                w = child(f, c)

            if w == -1:
                fail[u] = 0
            else:
                fail[u] = w

            q.append(u)
            e = nxt[e]

    # Failure tree.
    ffirst = array('i', [-1]) * m
    fnxt = array('i', [-1]) * m

    for v in range(1, m):
        p = fail[v]
        fnxt[v] = ffirst[p]
        ffirst[p] = v

    # Euler tour of failure tree.
    tin = array('i', [0]) * m
    tout = array('i', [0]) * m

    timer = 0
    stack = [(0, False)]

    while stack:
        v, exit_node = stack.pop()

        if not exit_node:
            tin[v] = timer
            timer += 1

            stack.append((v, True))

            u = ffirst[v]
            while u != -1:
                stack.append((u, False))
                u = fnxt[u]
        else:
            tout[v] = timer - 1

    # Segment tree:
    # range chmax update + point maximum query.
    size = 1
    while size < m:
        size <<= 1

    seg = array('i', [0]) * (size << 1)

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
        ans = 0

        while p:
            x = seg[p]
            if x > ans:
                ans = x
            p >>= 1

        return ans

    # Strings must be processed by increasing length.
    order = list(range(len(strings)))
    order.sort(key=lambda i: len(strings[i]))

    dp = array('i', [0]) * len(strings)
    answer = 1

    pos = 0
    n = len(strings)

    while pos < n:
        end = pos + 1
        length = len(strings[order[pos]])

        while end < n and len(strings[order[end]]) == length:
            end += 1

        # Calculate DP for this entire length before inserting them.
        for k in range(pos, end):
            idx = order[k]
            s = strings[idx]

            v = 0
            best = 0

            for b in s:
                c = b - 97
                u = child(v, c)

                while u == -1 and v != 0:
                    v = fail[v]
                    u = child(v, c)

                if u == -1:
                    v = 0
                else:
                    v = u

                x = query(tin[v])
                if x > best:
                    best = x

            cur = best + 1
            dp[idx] = cur

            if cur > answer:
                answer = cur

        # Activate all strings of this length.
        for k in range(pos, end):
            idx = order[k]
            v = node_of[idx]
            update(tin[v], tout[v], dp[idx])

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