def normalize_type(val):
    ret = ""
    for c in val:
        if not c.isalnum():
            continue
        ret += c
    return ret.lower()

def normalize_word(val):
    return normalize_type(val)

def writecsv(fp, data, sep="\t"):
    fp.writelines([sep.join([str(X) for X in line]) + "\n" for line in data])
    
def readcsv(fp, sep="\t"):
    output = list()
    first = True
    for line in fp:
        l = [x.strip() for x in line.split(sep)]
        if first:
            head = l
            first = False
            continue
        output.append(l)
    return (output, head)
        