from sklearn.ensemble import RandomForestClassifier
from tools import writecsv, readcsv
import sys
import sklearn.ensemble
import matplotlib.pyplot as pyplot


sklearn.ensemble.RandomForestClassifier()


#read in the training file
features_filename = sys.argv[1]
traincount = int(sys.argv[2])
(data, head) = readcsv(open(features_filename, "r"))
attr = len(data[0])

T = dict()
rT = dict()
Tc = 0

for i in range(len(data)):
    key = data[i][attr - 1]
    if key not in T:
        T[key] = Tc
        rT[Tc] = key
        Tc += 1
    data[i][attr - 1] = T[key]
    

train = data[1:traincount]
test = data[traincount:]
trainX = [x[0 : attr - 1] for x in train]
trainY = [x[attr - 1] for x in train]
testX = [x[0 : attr - 1] for x in test]
testY = [x[attr - 1] for x in test]


# random forest code
rf = RandomForestClassifier(n_estimators=150, min_samples_split=2, n_jobs=1, verbose=True)

print('fitting the model')
rf.fit(trainX, trainY)

# run model against test data
print('testing data')
print(rf.classes_)
predicted_probs = rf.predict_proba(testX)
predicted_probs = [["%f" % xx for xx in x] for x in predicted_probs]
#predicted_probs = predicted_probs[0:3]
#print(predicted_probs)
success_rate = [0 for _ in range(Tc)]

fig = pyplot.figure()
ax = fig.add_subplot(111)
ax.grid(True)

for tp in range(Tc):
    print(rT[tp])
    success_rate = [0 for _ in range(Tc)]
    cnt = 0
    for i in range(len(predicted_probs)):
        if tp != testY[i]: continue
        cnt += 1
    #    if i<2: continue
        l = list(reversed(sorted([(predicted_probs[i][ii], ii) for ii in range(Tc)])))
    #    print(testY[i], l)
        add = 0
        for ii in range(Tc):
            if l[ii][1] == testY[i]:
                add = 1
            success_rate[ii] += add
    #    print(success_rate)
    for i in range(len(success_rate)):
        success_rate[i] = float(success_rate[i]) / float(cnt)
    print(success_rate)
    ax.plot(range(Tc), success_rate, '-', label=rT[tp])
pyplot.legend(loc=5)
pyplot.show()
