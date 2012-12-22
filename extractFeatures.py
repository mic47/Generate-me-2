import sys
from tools import normalize_word, writecsv
import json

if len(sys.argv) < 4:
    print ("Not enough arguments")
    exit(0)

feature_def_filename = sys.argv[1]
input_data_filename = sys.argv[2]
output_features_filename = sys.argv[3]

features = json.load(open(feature_def_filename, "r"))
memes = json.load(open(input_data_filename, "r"))

output = list()
output.append(features['bag'] + ['MemeType'])
for (meme_type, texts) in memes.iteritems():
    for text in texts:
        words = [normalize_word(word) for word in text.split(' ')]
        out = list()
        for feature in features['bag']:
            if feature in words:
                out.append(1)
            else:
                out.append(0)
        out.append(meme_type)
        output.append(out)

f = open(output_features_filename, "w")                
writecsv(f, output)
f.close()