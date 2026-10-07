import sys
from array import array

def solve(n, data, pos):
    trans = {}
    parent = array('i', [0])
    fail = array('i', [0])
    score = array('i', [0])
    terminal = bytearray(1)

    for _ in range(n):
        s = data[pos]
        pos += 1

        v = 0
        for c in s:
            x = c - 97
            key = (v << 5) | x
            u = trans.get(key)

            if u is None:
                u = len(parent)
                trans[key] = u
                parent.append(v)
                fail.append(0)
                score.append(0)
                terminal.append(0)

            v = u

        terminal[v] = 1

    ans = 0
    total = len(parent)

    for v in range(1, total):
        p = parent[v]
        c = v

        # Recover the character of this trie edge.
        # It is stored in the transition key.
        # Searching the parent's outgoing edge is unnecessary:
        # use the fact that the child id itself is the transition value.
        # We find the character through the small alphabet.
        base = p << 5
        ch = 0
        while trans.get(base | ch) != v:
            ch += 1

        f = fail[p]

        while f:
            u = trans.get((f << 5) | ch)
            if u is not None:
                f = u
                break
            f = fail[f]
        else:
            f = trans.get(ch, 0)

        fail[v] = f

        a = score[p]
        b = score[f]
        if b > a:
            a = b

        a += terminal[v]
        score[v] = a

        if a > ans:
            ans = a

    return ans, pos


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    out = []

    while pos < len(data):
        n = int(data[pos])
        pos += 1

        if n == 0:
            break

        trans = {}
        parent = array('i', [0])
        fail = array('i', [0])
        score = array('i', [0])
        terminal = bytearray(1)

        for _ in range(n):
            s = data[pos]
            pos += 1

            v = 0
            for c in s:
                x = c - 97
                key = (v << 5) | x
                u = trans.get(key)

                if u is None:
                    u = len(parent)
                    trans[key] = u
                    parent.append(v)
                    fail.append(0)
                    score.append(0)
                    terminal.append(0)

                v = u

            terminal[v] = 1

        total = len(parent)
        ans = 0

        for v in range(1, total):
            p = parent[v]

            # Store the character of each node temporarily in the
            # high unused bits of a separate compact array.
            # Reconstruct it by checking at most 26 transitions.
            base = p << 5
            ch = 0
            while trans.get(base | ch) != v:
                ch += 1

            f = fail[p]

            while f:
                u = trans.get((f << 5) | ch)
                if u is not None:
                    f = u
                    break
                f = fail[f]
            else:
                f = trans.get(ch, 0)

            fail[v] = f

            best = score[p]
            if score[f] > best:
                best = score[f]

            best += terminal[v]
            score[v] = best

            if best > ans:
                ans = best

        out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()