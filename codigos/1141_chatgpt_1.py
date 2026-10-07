import sys
from array import array


def solve_case(n, inp):
    trans = {}
    fail = array('i', [0])
    info = array('i', [0])
    depth_next = array('i', [-1])
    depth_head = [-1] * 1002

    records = []
    max_depth = 0

    for _ in range(n):
        w = inp.readline().strip()
        p = 0
        depth = 0

        for ch in w:
            c = ch - 97
            depth += 1
            key = (p << 5) | c
            q = trans.get(key, 0)

            if q == 0:
                q = len(fail)
                trans[key] = q
                fail.append(0)
                info.append((p << 5) | c)
                depth_next.append(depth_head[depth])
                depth_head[depth] = q

            p = q

        records.append((len(w), w, p))
        if len(w) > max_depth:
            max_depth = len(w)

    records.sort(key=lambda x: x[0])

    total_nodes = len(fail)

    # Build failure links and the failure tree.
    failure_head = array('i', [-1]) * total_nodes
    failure_sibling = array('i', [0]) * total_nodes

    for depth in range(1, max_depth + 1):
        node = depth_head[depth]

        while node != -1:
            data = info[node]
            parent = data >> 5
            c = data & 31

            if parent == 0:
                f = 0
            else:
                f = fail[parent]
                t = trans.get((f << 5) | c, 0)

                while f and t == 0:
                    f = fail[f]
                    t = trans.get((f << 5) | c, 0)

            fail[node] = t if parent != 0 else 0

            failure_sibling[node] = failure_head[fail[node]]
            failure_head[fail[node]] = node

            node = depth_next[node]

    # Euler tour of the failure tree.
    tin = array('i', [0]) * total_nodes
    subtree_size = array('i', [1]) * total_nodes
    stack = array('i', [0])

    timer = 1

    while stack:
        v = stack[-1]
        child = failure_head[v]

        if child != -1:
            failure_head[v] = failure_sibling[child]
            tin[child] = timer
            timer += 1
            stack.append(child)
        else:
            stack.pop()
            if v != 0:
                subtree_size[fail[v]] += subtree_size[v]

    # Sqrt decomposition for subtree range-chmax + point query.
    block_size = 700
    block_count = (total_nodes + block_size - 1) // block_size

    lazy = array('i', [0]) * block_count
    point = array('i', [0]) * total_nodes

    answer = 0

    for _, word, terminal in records:
        state = 0
        best = 0

        # Find the best DP value among all dictionary strings
        # occurring as substrings of the current string.
        for ch in word:
            c = ch - 97
            t = trans.get((state << 5) | c, 0)

            while state and t == 0:
                state = fail[state]
                t = trans.get((state << 5) | c, 0)

            state = t

            pos = tin[state]
            value = point[pos]
            block_value = lazy[pos // block_size]

            if block_value > value:
                value = block_value

            if value > best:
                best = value

        dp = best + 1

        if dp > answer:
            answer = dp

        # Activating this terminal affects every state in its
        # failure-tree subtree.
        left = tin[terminal]
        right = left + subtree_size[terminal] - 1

        left_block = left // block_size
        right_block = right // block_size

        if left_block == right_block:
            for pos in range(left, right + 1):
                if point[pos] < dp:
                    point[pos] = dp
        else:
            end = (left_block + 1) * block_size
            for pos in range(left, end):
                if point[pos] < dp:
                    point[pos] = dp

            for b in range(left_block + 1, right_block):
                if lazy[b] < dp:
                    lazy[b] = dp

            start = right_block * block_size
            for pos in range(start, right + 1):
                if point[pos] < dp:
                    point[pos] = dp

    return answer


def main():
    inp = sys.stdin.buffer
    out = []

    while True:
        line = inp.readline()
        if not line:
            break

        line = line.strip()
        if not line:
            continue

        n = int(line)
        if n == 0:
            break

        out.append(str(solve_case(n, inp)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()