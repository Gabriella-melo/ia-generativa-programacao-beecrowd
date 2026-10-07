import sys
from collections import deque
from array import array


def solve_case(strs, total_len):
    max_nodes = total_len + 1

    first_child = array('i', [-1]) * max_nodes
    next_sibling = array('i', [-1]) * max_nodes
    edge_char = array('b', [0]) * max_nodes
    next_node = 1

    # Build trie using linked-list style children (no dense 26-array)
    for s in strs:
        cur = 0
        for ch in s:
            c = ch - 97
            child = first_child[cur]
            found = -1
            while child != -1:
                if edge_char[child] == c:
                    found = child
                    break
                child = next_sibling[child]
            if found == -1:
                found = next_node
                next_node += 1
                edge_char[found] = c
                next_sibling[found] = first_child[cur]
                first_child[cur] = found
            cur = found
    total_nodes = next_node

    def find_child(node, c, fc=first_child, ec=edge_char, ns=next_sibling):
        ch = fc[node]
        while ch != -1:
            if ec[ch] == c:
                return ch
            ch = ns[ch]
        return -1

    fail = array('i', [0]) * total_nodes

    q = deque()
    ch0 = first_child[0]
    while ch0 != -1:
        fail[ch0] = 0
        q.append(ch0)
        ch0 = next_sibling[ch0]

    while q:
        u = q.popleft()
        child = first_child[u]
        while child != -1:
            c = edge_char[child]
            v = fail[u]
            while v != 0 and find_child(v, c) == -1:
                v = fail[v]
            t = find_child(v, c)
            if t != -1 and t != child:
                fail[child] = t
            else:
                fail[child] = 0
            q.append(child)
            child = next_sibling[child]

    # Build fail-tree as linked list (avoid list-of-lists)
    fail_first_child = array('i', [-1]) * total_nodes
    fail_next_sibling = array('i', [-1]) * total_nodes
    for v in range(1, total_nodes):
        p = fail[v]
        fail_next_sibling[v] = fail_first_child[p]
        fail_first_child[p] = v

    in_time = array('i', [0]) * total_nodes
    out_time = array('i', [0]) * total_nodes
    cur_child = array('i', fail_first_child)
    stack = array('i', [0]) * total_nodes

    sp = 1
    stack[0] = 0
    timer = 1
    in_time[0] = 0
    while sp > 0:
        node = stack[sp - 1]
        c = cur_child[node]
        if c != -1:
            cur_child[node] = fail_next_sibling[c]
            in_time[c] = timer
            timer += 1
            stack[sp] = c
            sp += 1
        else:
            out_time[node] = timer - 1
            sp -= 1

    size = total_nodes
    lazy = array('h', [0]) * (4 * size)

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

    order = sorted(range(len(strs)), key=lambda i: len(strs[i]))
    answer = 0
    for i in order:
        s = strs[i]
        cur = 0
        best = 0
        for ch in s:
            c = ch - 97
            node = cur
            v = find_child(node, c)
            while v == -1 and node != 0:
                node = fail[node]
                v = find_child(node, c)
            cur = v if v != -1 else 0
            val = query_point(in_time[cur])
            if val > best:
                best = val
        dp = best + 1
        if dp > answer:
            answer = dp
        lo = in_time[cur]
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