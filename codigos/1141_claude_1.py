import sys
from collections import deque
from array import array


def solve_case(strs, total_len):
    n = len(strs)
    max_nodes = total_len + 1
    children = array('i', [-1]) * (max_nodes * 26)
    fail = array('i', [0]) * max_nodes
    next_node = 1  # 0 is root

    # insert all strings into the trie
    for s in strs:
        cur = 0
        for ch in s:
            c = ch - 97
            pos = cur * 26 + c
            nxt = children[pos]
            if nxt == -1:
                nxt = next_node
                children[pos] = nxt
                next_node += 1
            cur = nxt
    total_nodes = next_node

    # BFS to build fail links and complete goto table (Aho-Corasick)
    q = deque()
    root = 0
    for c in range(26):
        v = children[c]
        if v == -1:
            children[c] = root
        else:
            fail[v] = root
            q.append(v)

    while q:
        u = q.popleft()
        ubase = u * 26
        fu = fail[u]
        fubase = fu * 26
        for c in range(26):
            pos = ubase + c
            v = children[pos]
            if v == -1:
                children[pos] = children[fubase + c]
            else:
                fail[v] = children[fubase + c]
                q.append(v)

    # build fail-tree children lists for Euler tour
    failtree_children = [[] for _ in range(total_nodes)]
    for v in range(1, total_nodes):
        failtree_children[fail[v]].append(v)

    in_time = array('i', [0]) * total_nodes
    out_time = array('i', [0]) * total_nodes
    child_ptr = [0] * total_nodes
    stack = [root]
    timer = 0
    in_time[root] = timer
    timer += 1
    while stack:
        node = stack[-1]
        clist = failtree_children[node]
        cp = child_ptr[node]
        if cp < len(clist):
            child_ptr[node] += 1
            child = clist[cp]
            in_time[child] = timer
            timer += 1
            stack.append(child)
        else:
            out_time[node] = timer - 1
            stack.pop()

    size = total_nodes
    lazy = [0] * (4 * size)

    def update(node_idx, l, r, ql, qr, val):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            if val > lazy[node_idx]:
                lazy[node_idx] = val
            return
        mid = (l + r) // 2
        update(2 * node_idx, l, mid, ql, qr, val)
        update(2 * node_idx + 1, mid + 1, r, ql, qr, val)

    def query_point(pos):
        node_idx = 1
        l, r = 0, size - 1
        res = 0
        while True:
            if lazy[node_idx] > res:
                res = lazy[node_idx]
            if l == r:
                break
            mid = (l + r) // 2
            if pos <= mid:
                node_idx = 2 * node_idx
                r = mid
            else:
                node_idx = 2 * node_idx + 1
                l = mid + 1
        return res

    order = sorted(range(n), key=lambda i: len(strs[i]))
    answer = 0
    for i in order:
        s = strs[i]
        cur = 0
        best = 0
        for ch in s:
            c = ch - 97
            cur = children[cur * 26 + c]
            val = query_point(in_time[cur])
            if val > best:
                best = val
        dp = best + 1
        if dp > answer:
            answer = dp
        lo, hi = in_time[cur], out_time[cur]
        update(1, 0, size - 1, lo, hi, dp)

    return answer


def main():
    sys.setrecursionlimit(10000)
    data = sys.stdin.buffer.read().split()
    idx = 0
    out_lines = []
    m = len(data)
    while idx < m:
        n = int(data[idx])
        idx += 1
        if n == 0:
            break
        strs = []
        total_len = 0
        for _ in range(n):
            s = data[idx]
            idx += 1
            strs.append(s)
            total_len += len(s)
        out_lines.append(str(solve_case(strs, total_len)))
    sys.stdout.write('\n'.join(out_lines) + ('\n' if out_lines else ''))


if __name__ == '__main__':
    main()