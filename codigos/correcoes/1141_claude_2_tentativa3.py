import sys
from collections import deque


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
            strings.append(data[idx]); idx += 1

        # ---- Build trie (only real edges, as dicts) ----
        trans = [{}]          # trans[node] = {char: child}  (later augmented with fallback links)
        node_count = 1        # root = 0

        for s in strings:
            cur = 0
            for ch in s:                 # iterating bytes gives ints directly
                d = trans[cur]
                nxt = d.get(ch)
                if nxt is None:
                    nxt = node_count
                    node_count += 1
                    trans.append({})
                    d[ch] = nxt
                cur = nxt

        fail = [0] * node_count

        # iterative goto with path compression
        def go(u, c):
            d = trans[u]
            v = d.get(c)
            if v is not None:
                return v
            path = [u]
            cur = fail[u]
            while True:
                dcur = trans[cur]
                v = dcur.get(c)
                if v is not None:
                    break
                if cur == 0:
                    v = 0
                    break
                path.append(cur)
                cur = fail[cur]
            for node in path:
                trans[node][c] = v
            return v

        # ---- BFS to compute fail links (only over real trie edges) ----
        q = deque()
        for c, v in trans[0].items():
            fail[v] = 0
            q.append(v)

        while q:
            u = q.popleft()
            fu = fail[u]
            for c, v in list(trans[u].items()):
                fail[v] = go(fu, c)
                q.append(v)

        # ---- DP with suffix-link max propagation ----
        F = [-1] * node_count
        F[0] = 0
        bestDp = [0] * node_count

        def get_val(u):
            if F[u] != -1:
                return F[u]
            path = []
            v = u
            while F[v] == -1:
                path.append(v)
                v = fail[v]
            val = F[v]
            for pn in path:
                bd = bestDp[pn]
                if bd > val:
                    val = bd
                F[pn] = val
            return val

        order = sorted(range(n), key=lambda i: len(strings[i]))

        ans = 0
        for i in order:
            s = strings[i]
            node = 0
            maxPrev = 0
            for ch in s:
                node = go(node, ch)
                v = get_val(node)
                if v > maxPrev:
                    maxPrev = v
            dp_i = 1 + maxPrev

            fv = get_val(node)
            if dp_i > fv:
                F[node] = dp_i
            bestDp[node] = dp_i

            if dp_i > ans:
                ans = dp_i

        out.append(str(ans))

    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == "__main__":
    main()