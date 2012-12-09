import data
import funkcije
import Orange
reload(data)
reload(funkcije)



def linReg(trainD, trainC, testD ):
    orangeData = funkcije.listToOrangeContinuous(trainD+testD, trainC+[0]*len(testD))
    ind = [1]*len(trainD)+[0]*len(testD)
    orangeTrainD = orangeData.select_ref(ind,1)
    orangeTestD = orangeData.select_ref(ind,0)
    learner = Orange.regression.linear.LinearRegressionLearner()
    classifier = learner(orangeTrainD)
    return [classifier(ins).value for ins in orangeTestD]


def lasso(trainD, trainC, testD ):
    orangeData = funkcije.listToOrangeContinuous(trainD+testD, trainC+[0]*len(testD))
    ind = [1]*len(trainD)+[0]*len(testD)
    orangeTrainD = orangeData.select_ref(ind,1)
    orangeTestD = orangeData.select_ref(ind,0)
    learner = Orange.regression.lasso.LassoRegressionLearner(lasso_lambda=1, n_boot=100, n_perm=100)
    classifier = learner(orangeTrainD)
    return [classifier(ins).value for ins in orangeTestD]



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
       



tekme = data.vrniTekme()
testTekme = data.vrniTestData()

trainD = []
trainC = []

for tekmovanja in tekme.values():
    for tekma in tekmovanja:
        D, R = data.urediTekmo(tekma)
        trainD.append(D)
        trainC.append(R[1])

testD = [data.urediTekmo(tekma)[0] for tekma in testTekme]
testC = [data.urediTekmo(tekma)[1][1] for tekma in testTekme]


lr = crossVal(trainD, trainC, linReg, 10)

for i,r in enumerate(trainC):
    print "%4d   %3.3f  %3.3f  %3.3f" % (i,r,lr[i],r-lr[i])


povprecnaNapaka  = sum([ abs(r-lr[i]) for i,r in enumerate(trainC) ])/len(trainC)

print povprecnaNapaka






