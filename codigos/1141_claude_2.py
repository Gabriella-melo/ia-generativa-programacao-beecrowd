import sys
from collections import deque


def getF(u, F, fail, bestDp):
    if F[u] != -1:
        return F[u]
    path = []
    v = u
    while F[v] == -1:
        path.append(v)
        v = fail[v]
    val = F[v]
    for node in reversed(path):
        if bestDp[node] > val:
            val = bestDp[node]
        F[node] = val
    return F[u]


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    out = []
    L = len(data)
    while idx < L:
        n = int(data[idx]); idx += 1
        if n == 0:
            break
        strings = []
        for _ in range(n):
            strings.append(data[idx].decode()); idx += 1

        # Build trie
        children = [[-1] * 26]  # root = node 0
        node_count = 1

        for s in strings:
            cur = 0
            for ch in s:
                c = ord(ch) - 97
                nxt = children[cur][c]
                if nxt == -1:
                    children.append([-1] * 26)
                    nxt = node_count
                    node_count += 1
                    children[cur][c] = nxt
                cur = nxt

        # Build fail links and full goto table (BFS), reusing 'children' as goto
        fail = [0] * node_count
        goto = children
        q = deque()
        for c in range(26):
            v = goto[0][c]
            if v == -1:
                goto[0][c] = 0
            else:
                fail[v] = 0
                q.append(v)

        while q:
            u = q.popleft()
            fu = fail[u]
            gu = goto[u]
            gfu = goto[fu]
            for c in range(26):
                v = gu[c]
                if v == -1:
                    gu[c] = gfu[c]
                else:
                    fail[v] = gfu[c]
                    q.append(v)

        # dp computation
        F = [-1] * node_count
        F[0] = 0
        bestDp = [0] * node_count

        order = sorted(range(n), key=lambda i: len(strings[i]))

        ans = 0
        for i in order:
            s = strings[i]
            node = 0
            maxPrev = 0
            for ch in s:
                c = ord(ch) - 97
                node = goto[node][c]
                v = getF(node, F, fail, bestDp)
                if v > maxPrev:
                    maxPrev = v
            dp_i = 1 + maxPrev

            node_i = node
            fv = getF(node_i, F, fail, bestDp)
            if dp_i > fv:
                F[node_i] = dp_i
            bestDp[node_i] = dp_i

            if dp_i > ans:
                ans = dp_i

        out.append(str(ans))

    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == "__main__":
    main()