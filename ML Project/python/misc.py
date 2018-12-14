# -*- coding: utf-8 -*-
"""
@author: James Brissette
"""

import numpy as np
import matplotlib.pyplot as plt
np.random.seed(1234)

DATA_DIR = '../movie-ratings/data-splits/'
CV_DIR = './data/CVSplits'
DATA_DIM = 19
np.random.seed(9999)


def logisticRegression(data,w,b,rate,tradeoff):
    counter = 0
    for example in data:
        yi = 0;
        ywTx = 0

        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
            else:
                if (key in list(w.keys())):
                    ywTx += yi*w[key]*example[key]
                else:
                    w[key] = np.random.randint(-10000,10000) / 1000000.
                    ywTx += w[key]*example[key]
                
        
        for key in list(w.keys()):
           if key == 'label':
               continue
           else:
               w[key] = (1-rate)*w[key]
               
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
                b *= (1-rate)
            else:
                w[key] += rate*((example[key]/(1+np.exp(-ywTx)*example[key])))#+(2*w[key]/tradeoff))
        b += rate*(rate*(yi/(1+np.exp(-ywTx))))
        
        counter = counter + 1
        if (counter % 250 == 0):
            print('        Example ' + str(counter) + ' completed')
#        weight=((1-(((rate/(1+i))*2)/margin))*weight)+((((rate/(1+i))*label)/(1+math.exp(label*predict)))*example)
#              bias = ((1-(((rate/(1+i))*2)/margin))*bias)+(((rate/(1+i))*label)/(1+math.exp(label*predict)))
    return w, b, mistakes
        
 
def logisticRegression_cross_validate(epochs):
    cvfolds = 1
    training_set = []
    validation_set = []
    avgF1 = 0;
    
    average_acc = {1     : {10000:0, 1000:0, 100:0, 10:0 ,1:0, 0.1:0}, \
                   0.1   : {10000:0, 1000:0, 100:0, 10:0 ,1:0, 0.1:0}, \
                   .01   : {10000:0, 1000:0, 100:0, 10:0 ,1:0, 0.1:0}, \
                   .001  : {10000:0, 1000:0, 100:0, 10:0 ,1:0, 0.1:0}, \
                   .0001 : {10000:0, 1000:0, 100:0, 10:0 ,1:0, 0.1:0},
                   .00001: {10000:0, 1000:0, 100:0, 10:0 ,1:0, 0.1:0}}

    #optimal = [0,0,-1]
    
    print('### Cross Validation for Logistic Regression ###')
    for i in range(cvfolds):
        print('CVFold #' + str(i))
        start = i * 5000
        stop = (i+1) * 5000
        validation_set = data[start:stop]
        training_set = data[0:start]
        training_set += data[stop:25000]
                
        for rate in [1]:#,0.1,0.01,0.001,0.0001,0.00001]:
            print('  Running for rate = ' + str(rate))
            for tradeoff in [10000]:#, 1000, 100, 10, 1, 0.1]:
                avgF1 = 0;
                w = {}
                b = np.random.randint(-1e4,1e4) / 1e6
                
                for k in range(epochs):
#                    print('   Epoch: ' + str(k + 1) + ' of ' + str(epochs))
                    r = rate / (1 + k)
                    np.random.shuffle(training_set)
                    w,b,_ = logisticRegression(training_set, w, b, r, tradeoff)
                
                np.random.shuffle(validation_set)
                mistakes = predictLogistic(validation_set,w,b)
                
                #mistakes = [TP,FP,FN]
                
#                p = mistakes[0]/(mistakes[0]+mistakes[1])
#                r = mistakes[0]/(mistakes[0]+mistakes[2])
#                if (p == 0 and r == 0):
#                    F1 = 0;
#                else:
#                    F1 = 2*(p*r)/(p+r);
                
                avgF1 += (mistakes / len(training_set)) / epochs;
                
                average_acc[rate][tradeoff] += (avgF1) / cvfolds
        
    
    optimal = [[list(average_acc.keys())[list(average_acc.values()).index(j)], list(j.keys())[list(j.values()).index(max(j.values()))], max(j.values())] for j in [average_acc[i] for i in list(average_acc.keys())]]
    print('Optimal Parameters: rate=' + str(max([i[0] for i in optimal])) + ' tradeoff=' + str(max([i[1] for i in optimal])))
#    print('Precision for optimal: ' + str(pr[max([i[0] for i in optimal])][max([i[1] for i in optimal])][0]) + '; Recall for optimal: ' + str(pr[max([i[0] for i in optimal])][max([i[1] for i in optimal])][1]))
    print('Cross-Validation accuracy: ' + str(max([i[2] for i in optimal])))
    print('')
    return average_acc


def logisticRegression_train(epochs,rate,w,b, tradeoff, training_set, dev_set, mistakes, test_set):
    print('### Test for Logistic Regression ###')
    tracker = {}
    for i in range(epochs):
#        print('Epoch: ' + str(i + 1) + ' of ' + str(epochs))
        np.random.shuffle(training_set)
        r = rate / (1 + i)
        w,b, mistakes = logisticRegression(training_set, w, b, r, tradeoff)
        
        np.random.shuffle(dev_set)
        mistakes = predict(dev_set,w,b)
                
        #mistakes = [TP,FP,FN]
        p = mistakes[0]/(mistakes[0]+mistakes[1])
        r = mistakes[0]/(mistakes[0]+mistakes[2])
        if (p == 0 and r == 0):
            F1 = 0;
        else:
            F1 = 2*(p*r)/(p+r);
            
        tracker[i] = [F1, (w,b)]
        
    
    
#    plt.plot(np.arange(1,epochs+1,1),[i[0] for i in tracker.values()])
    
    
    idx = list(tracker.values()).index(max(tracker.values()))
    print("Max F-score on Dev set: " + str(tracker[idx][0]) + ' at epoch ' + str(idx +1))
    
    np.random.shuffle(test_set)
    mistakes = predict(test_set,tracker[idx][1][0],tracker[idx][1][1])
                
    #mistakes = [TP,FP,FN]
    p = mistakes[0]/(mistakes[0]+mistakes[1])
    r = mistakes[0]/(mistakes[0]+mistakes[2])
    if (p == 0 and r == 0):
        F1 = 0;
    else:
        F1 = 2*(p*r)/(p+r);
            
    print("Precision on Test Set: " + str(p) + "; Recall on Test Set; " + str(r))
    print("F-Score on Test set: " + str(F1))
    print('')
    #[i[0] for i in list(tracker.values())].index(min([i[0] for i in tracker.values()]))
    return tracker

    
def predictLogistic(data,w,b):
    counter = 0
    mistakes = 0
    
    for example in data:
        yi = 0;
        pred = 0
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
            else:
                if (key in list(w.keys())):
                    pred += w[key]*example[key]
                else:
                    w[key] = np.random.randint(-10000,10000) / 1000000.
                    pred += w[key]*example[key]
        
        if (1 / (1 + np.exp(-pred))) > 0.5:
            pred = 1
        else:
            pred = -1
        
        if (yi * pred) <= 0:
            mistakes += 1
            example[1] = 0
        else:
            example[1] = 1
            
            
        if (counter % 250 == 0):
            print('        Prediction ' + str(counter) + ' completed')
        counter = counter + 1
        
    return mistakes
    

    
def loadData(fpath):
    temp_data = []
    output = []
    data = {}
    data_file = open(fpath)
    for line in data_file:
        temp_data.append(line)
    
    for i in range(len(temp_data)):
        data[i] = temp_data[i].replace('\n','').split(' ')
        
    for i in range(len(data)):
        row = {}
        row['label'] = int(data[i][0])
        if (row['label'] == 0):
            row['label'] = -1;
            
        for j in range(len(data[i])):
            if j == 0:
                continue
            parse = data[i][j].split(':')
            row[str(int(parse[0]))] = float(parse[1])
        output.append(row)
    return output

test = loadTestData(DATA_DIR + 'data.eval.anon')
testData = loadData(DATA_DIR + 'data.test')
np.random.shuffle(testData)

test_set = testData[0:10000]
dev_set = testData[10000:12500]
#
CVFolds = []
data = loadData(DATA_DIR + 'data.train')
mistakes = 0
numFeatures = 74481;

#tracker = SVM_cross_validate(1);
#tracker = SVM_train(30,1.5,{},0, 10000, data, dev_set, mistakes, test_set)
tracker = logisticRegression_cross_validate(1)
#tracker = logisticRegression_train(10,.1,{},0, 10000, data, dev_set, mistakes, test_set)

#=================== PREDICT AND LABEL ===================================

def predictAndLabel(data,w,b):
    counter = 1
    mistakes = 0
    for example in data:
        yi = 0;
        pred = 0
        for key in list(example[2].keys()):
            if key == 'label':
                yi = example[2][key];
            else:
                if (key in list(w.keys())):
                    pred += w[key]*example[2][key]
                else:
                    w[key] = np.random.randint(-10000,10000) / 1000000.
                    pred += w[key]*example[2][key]
        pred += b
        
        if (yi * pred) <= 0:
            mistakes += 1
            example[1] = yi*-1
        else:
            example[1] = yi
        
        
        if (counter % 250 == 0):
            print('        Prediction ' + str(counter) + ' completed')
        counter = counter + 1
    return mistakes

#numFeatures = 2;
#
#ap, an, bp, bn = NBayes([{'label':-1},{'label':-1,'2':1},{'label':-1,'1':1},{'label':1,'1':1,'2':1}],2)
#
#lam = 0.1
#data = [{'label':-1},{'label':-1,'2':1},{'label':-1,'1':1},{'label':1,'1':1,'2':1}]
#
#p = [i['label'] for i in data].count(1) 
#n = [i['label'] for i in data].count(-1)
#
#ap = (ap + lam) / (p + 2*lam)
#an = (an + lam) / (n + 2*lam)
#bp = (bp + lam) / (p + 2*lam)
#bn = (bn + lam) / (n + 2*lam)
#
#
#p = (p + lam) / (len(data) + 2*lam)
#n = (n + lam) / (len(data) + 2*lam)
#
#mistakes = predictBayes([{'label':1,'1':1,'2':1}], ap, an, bp, bn, p, n)
#p = mistakes[0]/(mistakes[0]+mistakes[1])
#r = mistakes[0]/(mistakes[0]+mistakes[2])
#
#if (p == 0 and r == 0):
#    F1 = 0;
#else:
#    F1 = 2*(p*r)/(p+r);
#            
#print('@lam=' + str(lam) + ' F1 = ' + str(F1))





#[{'label':0,'x1':0,'x2':0, 'x3':0},{'label':0,'x1':0,'x2':0, 'x3':1},{'label':0,'x1':0,'x2':1, 'x3':0},{'label':0,'x1':0,'x2':1, 'x3':1},  {'label':0,'x1':1,'x2':0, 'x3':0},{'label':0,'x1':1,'x2':0, 'x3':1},{'label':0,'x1':1,'x2':1, 'x3':0},{'label':0,'x1':1,'x2':1, 'x3':1}]
#ap, an, bp, bn, p, n = NBayes([{'label':-1},{'label':-1,'2':1},{'label':-1,'1':1},{'label':1,'1':1,'2':1}],2,0.1)

#NBayes([{'label':1},{'label':0,'3':1},{'label':1,'2':1},{'label':1,'2':1, '3':1},  {'label':1,'1':1},{'label':0,'1':1,'3':1},{'label':0,'1':1,'2':1},{'label':0,'1':1,'2':1, '3':1}],3)
#ap, an, bp, bn, p, n = NBayes(data,numFeatures,10)
#tracker = crossValidateBayes(data, dev_set, numFeatures)
#mistakes = predictBayes(testData, ap, an, bp, bn, p, n)
#    
#p = mistakes[0]/(mistakes[0]+mistakes[1])
#r = mistakes[0]/(mistakes[0]+mistakes[2])
#
#if (p == 0 and r == 0):
#    F1 = 0;
#else:
#    F1 = 2*(p*r)/(p+r);
    
#att = {}
#for e in data:
#    for key in e.keys():
#        if key in att.keys() or key == 'label' or key == 'b':
#            continue
#        else:
#            att[key]=0
#            
#for e in testData:
#    for key in e.keys():
#        if key in att.keys() or key == 'label' or key == 'b':
#            continue
#        else:
#            att[key]=0
#numFeatures = max([int(i) for i in list(att.keys())])
   
####################################################         
#ap, an, bp, bn =  NBayes(data,numFeatures)
#lam = 2
#
#p = [i['label'] for i in data].count(1) 
#n = [i['label'] for i in data].count(-1)
#
#
#ap = (ap + lam) / (p + numFeatures*lam)
#an = (an + lam) / (n + numFeatures*lam)
#bp = (bp + lam) / (p + numFeatures*lam)
#bn = (bn + lam) / (n + numFeatures*lam)
#
#pn = p+n
#p = p / (pn)
#n = n / (pn)
#
#
#np.random.shuffle(test_set)
#mistakes = predictBayes(test_set, ap, an, bp, bn, p, n)

#p = mistakes[0]/(mistakes[0]+mistakes[1])
#r = mistakes[0]/(mistakes[0]+mistakes[2])
#
#if (p == 0 and r == 0):
#    F1 = 0;
#else:
#    F1 = 2*(p*r)/(p+r);
#            
#print('@lam=' + str(lam) + ' F1 = ' + str(F1))
            
            
            
            
            
            
            
            
            
            