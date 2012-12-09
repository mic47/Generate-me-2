from tools import normalize_word
from collections import defaultdict

def getBagOfWordsFeatures(dct, number_of_words):
    cnt = defaultdict(lambda *_: defaultdict(int))
    words = set()
    num = dict()
    for (meme_type, v) in dct.iteritems():
        num[meme_type] = float(len(v))
    for (meme_type, v) in dct.iteritems():
        for txt in v:
            was = set()
            for word in txt.split(' '):
                nw = normalize_word(word)
                
                if len(nw) <= 0:
                    continue
                if nw in was:
                    continue
                was.add(nw)
                cnt[meme_type][nw] += 1
                words.add(nw)
    for tp in cnt:
        for word in cnt[tp]:
            cnt[tp][word] = float(cnt[tp][word]) / num[tp] 
    types = [t for t in dct]
    select = list()
    for word in words:
        strength = 0.0
        for t1 in types:
            for t2 in types:
                if t1 == t2:
                    continue
                strength += abs(cnt[t1][word] - cnt[t2][word])
        select.append((strength, word)) 
    select = list(reversed(sorted(select)))
    ret = list()
    for i in range(min(number_of_words, len(select))):
        ret.append(select[i][1])
        print (select[i])
    return ret