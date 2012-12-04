import data

def knn(trainD, trainC, testD):
    return range(len(testD)) 

def rf(trainD, trainC, testD):
    return range(len(testD)) 

def bayes(trainD, trainC, testD):
    return range(len(testD)) 


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





    
data = [range(10)]*99
razred = [1]*99

print crossVal(data, razred,  knn, 7)






