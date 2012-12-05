import data
import funkcije
import Orange
from random import random

def knn(trainD, trainC, testD):
    orangeData = funkcije.listToOrangeSingleClass(trainD+testD, trainC+[0]*len(testD))
    ind = [1]*len(trainD)+[0]*len(testD)
    orangeTrainD = orangeData.select_ref(ind,1)
    orangeTestD = orangeData.select_ref(ind,0)

    knnLearner = Orange.classification.knn.kNNLearner(name="knn")
    cl = knnLearner(orangeTrainD)
    return [cl(i,  Orange.classification.Classifier.GetProbabilities)[True] for i in orangeTestD]

def rf(trainD, trainC, testD):
    orangeData = funkcije.listToOrangeSingleClass(trainD+testD, trainC+[0]*len(testD))
    ind = [1]*len(trainD)+[0]*len(testD)
    orangeTrainD = orangeData.select_ref(ind,1)
    orangeTestD = orangeData.select_ref(ind,0)

    rfLearner = Orange.ensemble.forest.RandomForestLearner(trees = 100, name = "forest" )
    cl = rfLearner(orangeTrainD)
    return [cl(i, Orange.classification.Classifier.GetProbabilities)[True] for i in orangeTestD]


def bayes(trainD, trainC, testD):
    orangeData = funkcije.listToOrangeSingleClass(trainD+testD, trainC+[0]*len(testD))
    ind = [1]*len(trainD)+[0]*len(testD)
    orangeTrainD = orangeData.select_ref(ind,1)
    orangeTestD = orangeData.select_ref(ind,0)
    
    bayesLearner = Orange.classification.bayes.NaiveLearner(name="naiveBayes")
    cl = bayesLearner(orangeTrainD)
    return [cl(i,  Orange.classification.Classifier.GetProbabilities)[True] for i in orangeTestD]


def crossVal(data, razred, predictor, k = 10):
    n = len(data)
    testC = []
    for i in range(k):
        od, do = n*i/k, n*(i+1)/k
        trainD = data[:od]+data[do:]
        trainC = razred[:od]+razred[do:]
        testD = data[od:do]
        testC += predictor(trainD, trainC, testD)
        
    return testC


def tocnost(napovedi, razred):
    return  sum([napovedi[i]==razred[i] for i in range(len(razred))])*1.0/len(razred)
 
def probToClass(trainC, testC):
    procentEnk = 1.*sum(trainC)/len(trainC)
    mejaZaPoz = sorted(testC)[int((1-procentEnk)*len(trainC))]
    return [int(i > mejaZaPoz) for i in testC]
       
    
data = [[int(random()*6) for j in range(100)] for i in range(2000)]
razred = [int(random()*(i[0]+i[1]) > 7 or i[5]==2 or i[7]*2 < i[4]) for i in data]

#for i in range(len(data)):
#    print data[i],razred[i]

rfRes = crossVal(data, razred,  rf, 10)

napovedi = probToClass(razred, rfRes)

print tocnost(napovedi, razred)

#bayesRes = crossVal(data, razred,  bayes, 10)
#knnRes = crossVal(data, razred,  rf, 10)
#
#crossValRes = [knnRes[i]*0.5+bayesRes[i]*0.5 for i in range(len(knnRes))]
#
#
#for i,res in enumerate(crossValRes):
#    print "tocno/napoved: %4d/%d    %.5f" % (razred[i],napovedi[i],res)
#
#print tocnost(napovedi, razred)
#
#dataOrange = funkcije.listToOrangeSingleClass(data, razred)




