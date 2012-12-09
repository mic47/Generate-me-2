def find(L, c):
    if L[c] < 0:
        return c
    L[c] = find(L, L[c])
    return L[c]


def union(L, c1, c2):
    p1 = find(L, c1)
    p2 = find(L, c2)
    if p1 == p2:
        return False
    if L[p1] < L[p2]:
        L[p1] += L[p2]
        L[p2] = p1
    else:
        L[p2] += L[p1]
        L[p1] = p2
    return True