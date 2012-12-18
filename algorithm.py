import math
from collections import defaultdict

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

def entropy(E):
    ret = 0.0
    all = float(sum(E))
    for e in E:
	if e > 0:
	    ee = float(e)/ all
	    ret -= ee * math.log(ee)
    return ret

def informationGain(split):
    all = defaultdict(float)
    total = 0.0
    ret = 0.0
    for s in split:
	a = sum(s)
	total += a
	ret -= entropy(s) * a
	for i in range(len(s)):
	    all[i] += s[i]
    ret /= float(total)
    ret += entropy([x for (_, x) in all.iteritems()])
    return ret

def argmax(l):
    if type(l) == list:
        iter = ((i, l[i]) for i in range(len(l)))
    elif type(l) == dict:
        iter = range.iteritems()
    else:
        raise "Bad type";
    mx = None
    it = -1
    for (i, val) in iter:
        if val >= mx:
            mx = val
            it = i
    return it
