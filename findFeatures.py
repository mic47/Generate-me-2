import sys
from collections import defaultdict
from tools import normalize_type
import json
from bagofwords import getBagOfWordsFeatures
from regexpfeatures import getRegexpFeatures

if len(sys.argv) < 5:
    print ("Not enough arguments")
    exit(0)


memetype_threshold = int(sys.argv[4])
bag_of_words_threshols = int(sys.argv[5])
input_filename = sys.argv[1]
output_data_filename = sys.argv[2]
output_features = sys.argv[3]



    
memes = defaultdict(list)

def extract_line(text, tp):
    if text[:len(tp)] != tp:
        print("ERROR! {0} {1}".format(tp, text))
    l = len(tp)
    while len(text) > l and (text[l] == ' ' or text[l] == '-'):
        l += 1
    return text[l:]

# Load data
f = open(input_filename, "r")
for line in f:
    line = [x.strip() for x in line.split('\t')]
    if len(line) != 4:
        continue
    img = line[0]
    meme_type = normalize_type(line[3])
    text = extract_line(line[1], line[3])
    memes[meme_type].append(text)
    
features = defaultdict(list)

# Filter out data
todel = list()
for (m, t) in memes.iteritems():
    if len(t) < memetype_threshold:
        todel.append(m)
for k in todel:
    del memes[k]

if len(sys.argv) < 7:
    f = open(output_data_filename, "w")
    json.dump(memes, f, indent=1)
    f.close()
    a = list()
    for (m, t) in memes.iteritems():
        a.append((len(t), m))
    a.sort(reverse=True)
    for (_, m) in a:
        print(m)
    exit(0)
else:
    select = sys.argv[6]

# Find features
features = dict()

features['regexp'] = getRegexpFeatures(memes, 10, 10, select)
print("Graphs are written")
features["bag"] = getBagOfWordsFeatures(memes, bag_of_words_threshols)


# Save data
f = open(output_features.format(select), "w")
json.dump(features, f, indent=1)
f.close()

