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


# Load data
f = open(input_filename, "r")
for line in f:
    line = [x.strip() for x in line.split('\t')]
    if len(line) != 3:
        continue
    img = line[0]
    meme_type = normalize_type(line[1])
    text = line[2]
    memes[meme_type].append(text)
    
features = defaultdict(list)

# Filter out data
todel = list()
for (m, t) in memes.iteritems():
    if len(t) < memetype_threshold:
        todel.append(m)
for k in todel:
    del memes[k]

# Find features
features = dict()

features['regexp'] = getRegexpFeatures(memes, 10, 100)
print("Graphs are written")
features["bag"] = getBagOfWordsFeatures(memes, bag_of_words_threshols)


# Save data
f = open(output_features, "w")
json.dump(features, f, indent=1)
f.close()

f = open(output_data_filename, "w")
json.dump(memes, f, indent=1)
f.close()