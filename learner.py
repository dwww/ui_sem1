import data
import funkcije
import Orange
import numpy as np
from random import random
reload(data)
reload(funkcije)

def reliefFilter(trainD, trainC):
    orangeData = funkcije.listToOrangeSingleClass(trainD, trainC)
    meas = Orange.feature.scoring.Relief()
    mr = [ (a.name, meas(a, orangeData)) for a in orangeData.domain.attributes]
    mr.sort(key=lambda x: -x[1]) #sort decreasingly by the score
    return [i[0] for i in mr]


def getProb(trainD, trainC, testD , lrn):
    orangeData = funkcije.listToOrangeSingleClass(trainD+testD, trainC+[0]*len(testD))
    ind = [1]*len(trainD)+[0]*len(testD)
    orangeTrainD = orangeData.select_ref(ind,1)
    orangeTestD = orangeData.select_ref(ind,0)

    cl = lrn(orangeTrainD)
    return [cl(i,  Orange.classification.Classifier.GetProbabilities)[True] for i in orangeTestD]


def knn(trainD, trainC, testD):
    knnLearner = Orange.classification.knn.kNNLearner(name="knn")
    return getProb(trainD, trainC, testD, knnLearner)

def rf(trainD, trainC, testD):
    rfLearner = Orange.ensemble.forest.RandomForestLearner(trees = 50, name = "forest" )
    return getProb(trainD, trainC, testD, rfLearner)

def bayes(trainD, trainC, testD):
    bayesLearner = Orange.classification.bayes.NaiveLearner(name="naiveBayes")
    return getProb(trainD, trainC, testD, bayesLearner)

def filterArr(a,ind):
    a = np.array(a)
    return list(a.T[ind].T)

def svm(trainD, trainC, testD):
    ind = reliefFilter(trainD, trainC)[:50]
    trainD = filterArr(trainD, ind)
    testD = filterArr(testD, ind)
    bayesLearner = Orange.classification.svm.SVMLearner(name="svm")
    return getProb(trainD, trainC, testD, bayesLearner)

def tree(trainD, trainC, testD):
    bayesLearner = Orange.classification.tree.TreeLearner(name="tree")
    return getProb(trainD, trainC, testD, bayesLearner)

def logReg(trainD, trainC, testD):
    bayesLearner = Orange.classification.logreg.LogRegLearner(remove_singular=1, name="logreg")
    return getProb(trainD, trainC, testD, bayesLearner)


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
    mejaZaPoz = sorted(testC)[int((1-procentEnk)*len(testC))]
    return [int(i > mejaZaPoz) for i in testC]
       



tekme = data.vrniTekme()
testTekme = data.vrniTestData()

trainD = []
trainC = []

for tekmovanja in tekme.values():
    for tekma in tekmovanja:
        D, R = data.urediTekmo(tekma)
        trainD.append(D)
        trainC.append(R[0])


testD = [data.urediTekmo(tekma)[0] for tekma in testTekme]
testC = [data.urediTekmo(tekma)[1][0] for tekma in testTekme]

napovedi = []
tocnosti = []
for f in [rf, bayes, knn, tree, svm]:
    rfRes = crossVal(trainD, trainC,  f, 4)
    
    napovedi.append(rfRes)
    
    tocnosti.append(tocnost(probToClass(trainC, rfRes), trainC))
    print tocnosti[-1]
    
tocnosti = np.array(tocnosti)**3
tocnosti = tocnosti / tocnosti.sum()
napovedi = np.array(napovedi)
utezenaNapoved = list(napovedi.T.dot(tocnosti))

print tocnost(probToClass(trainC, utezenaNapoved), trainC)


napovedi = []
for f in [rf, bayes, knn, tree, svm]:
    rfRes = f(trainD, trainC, testD)
    
    napovedi.append(rfRes)

napovedi = np.array(napovedi)
utezenaNapoved = list(napovedi.T.dot(tocnosti))

print tocnost(probToClass(trainC, utezenaNapoved), testC)


