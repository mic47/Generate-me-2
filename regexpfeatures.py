from tools import normalize_word
from collections import defaultdict
import random
import sys
import time
from graph import Graph
import re
from multiprocessing import Pool

def dist(c1, c2):
    if c1 == c2:
        return 1
    else:
        return -1   


def make_regexp(string):
    # TODO: optimize: replace .?.?.? chains with .{0,3}, replace long chains with *, replace slow reg expressions
    ret = ""
    clen = 0
    for c in string:
	if ord(c) == 29:
	    clen += 1
	else:
	    if clen > 0:
		ret += '.{{0,{0}}}'.format(clen)
		clen = 0
	    if ord(c) == 28:
		ret += '.'
	    else:
		ret += re.escape(c)
    if clen > 0:
	ret += '.{{0,{0}}}'.format(clen)
    return ret
            


def editDistanceString(w1, w2):
    if w1 == "" or w2 == "": return (0, "")
    l1 = len(w1)
    l2 = len(w2)
    D = [[0 for _ in range(l2)] for _ in range(l1)]
    P = [[(0, 0) for _ in range(l2)] for _ in range(l1)]
    for i in range(l1):
        D[i][0] = max(0, dist(w1[i], w2[0])) 
    for i in range(l2):
        D[0][i] = max(0, dist(w1[0], w2[i]))
    
    ret = 0
    retp = (0, 0)
    for i in range(l1):
        if i==0: continue
        for j in range(l2):
            if j==0: continue
            be = 0
            pr = (0, 0)
            new = D[i - 1][j] - 1
            if new > be:
                be = new
                pr = (-1, 0)
            new = D[i][j - 1] - 1
            if new > be:
                be = new
                pr = (0, -1)
            new = D[i - 1][j - 1] + dist(w1[i], w2[j])
            if new > be:
                be = new
                pr = (-1, -1) 
            D[i][j] = be
            P[i][j] = pr
            if be > ret:
                ret = be
                retp = (i, j)
    rets = ""
    x, y = retp
    while P[x][y] != (0, 0):
        if P[x][y] == (-1, -1):
            if w1[x] == w2[y]:
                rets += w1[x]
            else:
                rets += chr(28) #'*'
        else:
            rets += chr(29) #'+' 
        dx, dy = P[x][y]
        x += dx
        y += dy
    if (x == 0 or y == 0) and w1[x] == w2[y]:
        rets += w1[x] 
    return (ret, rets[::-1])

def cluster(sentences, name):
    G = Graph(sentences)
    pool = G.getIDs()
    bestpat = ""
    prevl = 0
    n = len(pool)
    start = time.time()
    outofpool = set()
    while len(pool) > 1:
        sys.stdout.write(
            "\r[{2}] (iterations: {0}), progress: {1}/{3} ({4} seconds)".format(
                prevl, len(pool), name, n, round(time.time() - start)))
        sys.stdout.flush()
        prevl = 0
        best = 0;
        bestpair = (-1, -1)
        notchanged = 0
        while notchanged < 1000:
            prevl += 1
            i = random.randint(0, len(pool) - 1)
            j = random.randint(0, len(pool) - 1)
            if i == j:
                continue
            ui = pool[i]
            vi = pool[j]
            u = G.getVertex(ui)
            v = G.getVertex(vi)
            dp = u[0]
            vp = v[0]
            if ui == vi:
                continue
            notchanged += 1
            (dist, pattern) = editDistanceString(dp, vp)
            if dist > best:
                notchanged = 0
                best = dist
                bestpair  = (i, j)
                bestpat = pattern
        if best <= 0:
            break
        newID = G.getVertexId(bestpat)
        i, j = bestpair
        ui = pool[i]
        vi = pool[j]
        if newID not in outofpool and newID != ui and newID != vi:
            pool.append(newID)
        
        if newID != ui:
            # add edge ui -> newID
            G.addEdge(ui, newID, best)
            # remove ui from pool
            outofpool.add(ui)
            if i < len(pool):
                pool[i] = pool[len(pool) - 1]
                pool.pop()
            if j == len(pool):
                j = i
            
        if newID != vi:
            # add edge vi -> newID
            G.addEdge(vi, newID, best)
            # remove vi from pool
            outofpool.add(vi)
            if j < len(pool):
                pool[j] = pool[len(pool) - 1]
                pool.pop()
    print("\r[{0}] {1} sequences clustered in {2} seconds.".format(
        name, len(sentences), time.time() - start))
    f = open(name + "_graph.dot", "w")
    G.write(f)
    f.close()
    return [make_regexp(x) for x in G.getAllInternalNodes()]
                    

def getRegexpFeatures(dct, number_of_words_per_type, number_of_words):
    it = list()
    for (mt, sen) in dct.iteritems():
        it.append((len(sen), mt, sen))
    it.sort(reverse=True)
    regexps = dict()
    glob = list()
    ret = list()
    for (_, meme_type, sentences) in it:
        regexps[meme_type] = cluster(sentences, meme_type)
        N = len(regexps[meme_type])
        n = 0
        start = time.time()
        loc = list()
        for regexp in regexps[meme_type]:
            n += 1
            sys.stdout.write(
                "\r[{0}] {1}/{2} RE in {3} s. ({4})".format(
                    meme_type, n, N, round(time.time() - start), regexp))
            sys.stdout.flush()
            compiled = re.compile(regexp)
            cnt = dict()
            for (meme, sentences) in dct.iteritems():
                count = 0
                for sent in sentences:
                    if compiled.search(sent.lower()) != None:
                        count += 1
                cnt[meme] = float(count) / float(len(sentences))
            localweight = 0
            mine = cnt[meme_type]
            for (meme, val) in cnt.iteritems():
                localweight += mine - val
            loc.append((localweight, regexp))
            globalweight = 0
            for (_, v) in cnt.iteritems():
                for (_, vv) in cnt.iteritems():
                    globalweight += abs(v - vv)
            glob.append((globalweight, regexp))
        loc.sort(reverse=True)
        for i in range(min(number_of_words_per_type, len(loc))):
            ret.append(loc[i][1])
        print("\r[{0}] Regular expressions selected in {1} seconds. (best: {2})".format(meme_type, time.time() - start, loc[0][1]))
    glob.sort(reverse=True)
    for i in range(min(number_of_words)):
        ret.append(glob[i][1])
    return ret
            
            
            
