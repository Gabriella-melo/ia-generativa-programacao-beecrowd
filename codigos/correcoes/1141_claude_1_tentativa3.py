import sys
from collections import deque
from array import array


def solve_case(strs, total_len):
    # Node numbering starts at 1 (root = 1). Index 0 is a sentinel meaning
    # "no explicit child" so we can zero-initialize arrays cheaply
    # (no giant python list is created, avoiding the earlier MLE).
    max_nodes = total_len + 2  # upper bound on number of trie nodes (+ sentinel)

    children = array('i', bytes(4 * max_nodes * 26))  # zero-filled
    next_node = 2  # 1 is root

    root = 1

    # Build trie
    for s in strs:
        cur = root
        for ch in s:
            c = ch - 97
            idx = cur * 26 + c
            nxt = children[idx]
            if nxt == 0:
                nxt = next_node
                next_node += 1
                children[idx] = nxt
            cur = nxt
    total_nodes = next_node  # nodes 1 .. total_nodes-1 are valid

    fail = array('i', bytes(4 * total_nodes))
    fail[root] = root

    # Initialize root's missing edges as self-loops
    rbase = root * 26
    for c in range(26):
        idx = rbase + c
        if children[idx] == 0:
            children[idx] = root

    q = deque()
    for c in range(26):
        v = children[rbase + c]
        if v != root:
            fail[v] = root
            q.append(v)

    while q:
        u = q.popleft()
        ubase = u * 26
        fbase = fail[u] * 26
        for c in range(26):
            idx = ubase + c
            ch = children[idx]
            if ch:
                fail[ch] = children[fbase + c]
                q.append(ch)
            else:
                children[idx] = children[fbase + c]

    # Build fail-tree as linked list (avoid list-of-lists) for Euler tour
    fail_first_child = array('i', bytes(4 * total_nodes))
    fail_next_sibling = array('i', bytes(4 * total_nodes))
    for v in range(root + 1, total_nodes):
        p = fail[v]
        fail_next_sibling[v] = fail_first_child[p]
        fail_first_child[p] = v

    in_time = array('i', bytes(4 * total_nodes))
    out_time = array('i', bytes(4 * total_nodes))
    cur_child = array('i', fail_first_child)
    stack = array('i', bytes(4 * total_nodes))

    sp = 1
    stack[0] = root
    timer = 0
    in_time[root] = timer
    timer += 1
    while sp > 0:
        node = stack[sp - 1]
        c = cur_child[node]
        if c != 0:
            cur_child[node] = fail_next_sibling[c]
            in_time[c] = timer
            timer += 1
            stack[sp] = c
            sp += 1
        else:
            out_time[node] = timer - 1
            sp -= 1

    size = timer  # number of nodes actually placed in euler order (== total_nodes-1)
    lazy = array('i', bytes(4 * 4 * (size + 1)))

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
        l = 0
        r = size - 1
        res = 0
        lz = lazy
        while True:
            v = lz[node_idx]
            if v > res:
                res = v
            if l == r:
                break
            mid = (l + r) >> 1
            if pos <= mid:
                node_idx <<= 1
                r = mid
            else:
                node_idx = (node_idx << 1) | 1
                l = mid + 1
        return res

    order = sorted(range(len(strs)), key=lambda i: len(strs[i]))
    answer = 0
    ch_arr = children
    it = in_time
    for i in order:
        s = strs[i]
        cur = root
        best = 0
        for ch in s:
            c = ch - 97
            cur = ch_arr[cur * 26 + c]
            val = query_point(it[cur])
            if val > best:
                best = val
        dp = best + 1
        if dp > answer:
            answer = dp
        lo = it[cur]
        hi = out_time[cur]
        update(1, 0, size - 1, lo, hi, dp)

    return answer


def main():
    sys.setrecursionlimit(10000)
    data = sys.stdin.buffer.read().split()
    idx = 0
    m = len(data)
    out_lines = []
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