import Orange

def listToOrangeSingleClass(X,y):
    features = [Orange.feature.Continuous("%d" % i) for i in range(len(X[0]))]
    class_var = Orange.feature.Discrete("class", values=["0","1"])
    domain = Orange.data.Domain(features + [class_var])
    data = Orange.data.Table(domain)
    [data.append(Orange.data.Instance(domain, list(map(lambda x: 1 if x=='True' else (0 if x=='False' else x), X[i]))+[["0", "1"][y[i]]])) for i in range(len(X))]
    return data


def listToOrangeContinuous(X,y):
    features = [Orange.feature.Continuous("%d" % i) for i in range(len(X[0]))]
    class_var = Orange.feature.Continuous("class")
    domain = Orange.data.Domain(features + [class_var])
    data = Orange.data.Table(domain)
    [data.append(Orange.data.Instance(domain, list(X[i])+[y[i]])) for i in range(len(X))]
    return data