import time
import re
import sys
import random

def getRandomStr(length, reg=False):
    ret = ""
    for i in range(length):
	if reg and random.randint(0,3) == 0:
	    ret += '.'
	elif reg and random.randint(0,4) == 0:
	    ret += '.?'
	else:
	    ret += chr(ord('a') + random.randint(0, 15))
    return ret

strings = [getRandomStr(20) for _ in range(4000)]

cnt = 0;
while True:
    cnt += 1
    reg = [getRandomStr(10, True) for _ in range(500)] 
    now = time.time()
    count = 0
    cc = 0;
    compile_time = 0.0
    search_time = 0.0
    for r in reg:
	re.purge()
	cc += 1
	#if (cc % 50) == 0:
	#    sys.stdout.write('\r{0}/{1} in {2}: {3}'.format(cc, len(reg), time.time() - now, r))
	#    sys.stdout.flush()
	t = time.time()
	c = re.compile(r)
	compile_time += time.time() - t
	t = time.time()
	for s in strings:
	    if c.match(s):
		count += 1
	search_time += time.time() - t
    print('\r{0}        {1}        {2}        {4}        {5}{3}'.format(cnt,time.time() - now, count, ' '*100, compile_time, search_time))
	    
