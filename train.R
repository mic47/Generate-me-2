library('randomForest')
X = read.csv("features_shuffled.csv", sep="\t")
N = length(X)
train = 39473
Y = X[1:train, N]
X = X[1:train, 1:N-1]
r = randomForest(X, Y, importance=TRUE)
r