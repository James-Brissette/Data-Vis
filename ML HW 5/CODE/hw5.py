# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 01:36:42 2018

@author: jtbri
"""

# -*- coding: utf-8 -*-
"""
@author: James Brissette
"""

import numpy as np
import matplotlib.pyplot as plt
np.random.seed(1234)

DATA_DIR = './data/'
CV_DIR = './data/CVSplits'
DATA_DIM = 19
np.random.seed(9999)


def SVM(data, rate, w, b, C, mistakes):
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
        pred += b
        #print('prediction: ' + str(pred) + '; yi: ' + str(yi))
        
        for key in list(w.keys()):
           if key == 'label':
               continue
           else:
               w[key] = (1-rate)*w[key]
            
        if (yi * pred) <= 1:
            #mistakes += 1
            for key in list(example.keys()):
                if key == 'label':
                    continue
                else:
                    w[key] += rate*C*yi*example[key]

        b += rate*yi
            
#    print('Total Updates = ' + str(mistakes))
    return w, b, mistakes

def NBayes(data, numFeatures):

    ap = np.zeros(numFeatures,int)
    an = np.zeros(numFeatures,int)
    bp = np.zeros(numFeatures,int)
    bn = np.zeros(numFeatures,int)
    
    for sample in data:
        if sample['label'] == 1:
            bp += 1
            for key in sample.keys():
                if key != 'label' and key != 'b':
                    if sample[key] == 1:
                        bp[int(key)-1] -= 1
                        ap[int(key)-1] += 1
        else:
            bn += 1
            for key in sample.keys():
               if key != 'label' and key != 'b':
                    if sample[key] == 1:
                        bn[int(key)-1] -= 1
                        an[int(key)-1] += 1
                        
#    for key in a.keys():
#        a[key] /= [i['label'] for i in data].count(1)
#    for key in b.keys():
#        b[key] /= [i['label'] for i in data].count(-1)
    
    
    
    return ap, an, bp, bn, p, n

def logisticRegression(data,w,b,rate,tradeoff):
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
                
                
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
                b += rate*yi
            else:
                w[key] = rate*((-yi*example[key]*np.exp(-ywTx))/(1+np.exp(-ywTx))+(2*w[key]/tradeoff))
        
    return w, b, mistakes

def SVM_cross_validate(epochs):
    cvfolds = 5
    training_set = []
    validation_set = []
    avgF1 = 0;
    
    average_acc = {1    : {100000:0, 10000:0, 1000:0, 100:0 ,10:0, 1:0}, \
                   0.1  : {100000:0, 10000:0, 1000:0, 100:0 ,10:0, 1:0}, \
                   .01  : {100000:0, 10000:0, 1000:0, 100:0 ,10:0, 1:0}, \
                   .001 : {100000:0, 10000:0, 1000:0, 100:0 ,10:0, 1:0}, \
                   .0001: {100000:0, 10000:0, 1000:0, 100:0 ,10:0, 1:0}}

    pr = {1    : {100000:[0,0], 10000:[0,0], 1000:[0,0], 100:[0,0] ,10:[0,0], 1:[0,0]}, \
                   0.1  : {100000:[0,0], 10000:[0,0], 1000:[0,0], 100:[0,0] ,10:[0,0], 1:[0,0]}, \
                   .01  : {100000:[0,0], 10000:[0,0], 1000:[0,0], 100:[0,0] ,10:[0,0], 1:[0,0]}, \
                   .001 : {100000:[0,0], 10000:[0,0], 1000:[0,0], 100:[0,0] ,10:[0,0], 1:[0,0]}, \
                   .0001: {100000:[0,0], 10000:[0,0], 1000:[0,0], 100:[0,0] ,10:[0,0], 1:[0,0]}}
    
    optimal = [0,0,-1]
    
    print('### Cross Validation for SVM ###')
    for i in range(cvfolds):
        print('CVFold #' + str(i))
        training_set = []
        for j in range(cvfolds):
            if j == i: 
                validation_set = loadData(CV_DIR + '/training0' + str(i) + '.data')
            else:
                training_set += loadData(CV_DIR + '/training0' + str(j) + '.data')
                
        for rate in [1,0.1,0.01,0.001,0.0001]:
            for C in [100000, 10000, 1000, 100, 10, 1]:
#                print('  Running for rate = ' + str(rate) + ',  C = ' + str(C))
                avgF1 = 0;
                w = {}
                b = np.random.randint(-1e4,1e4) / 1e6
                
                for k in range(epochs):
#                    print('   Epoch: ' + str(k + 1) + ' of ' + str(epochs))
                    r = rate / (1 + k)
                    np.random.shuffle(training_set)
                    w,b,_ = SVM(training_set, r, w, b, C, 0)
                
                np.random.shuffle(validation_set)
                mistakes = predict(validation_set,w,b)
                
                #mistakes = [TP,FP,FN]
                p = mistakes[0]/(mistakes[0]+mistakes[1])
                r = mistakes[0]/(mistakes[0]+mistakes[2])
                if (p == 0 and r == 0):
                    F1 = 0;
                else:
                    F1 = 2*(p*r)/(p+r);
                
                avgF1 += F1 / epochs;
                
                average_acc[rate][C] += (avgF1) / cvfolds
                pr[rate][C][0] += p / cvfolds
                pr[rate][C][1] += r / cvfolds
        
    
    optimal = [[list(average_acc.keys())[list(average_acc.values()).index(j)], list(j.keys())[list(j.values()).index(max(j.values()))], max(j.values())] for j in [average_acc[i] for i in list(average_acc.keys())]]
    print('Optimal Parameters: rate=' + str(max([i[0] for i in optimal])) + ' C=' + str(max([i[1] for i in optimal])))
    print('Optimal: ' + str(optimal))
    print('Precision for optimal: ' + str(pr[max([i[0] for i in optimal])][max([i[1] for i in optimal])][0]) + '; Recall for optimal: ' + str(pr[max([i[0] for i in optimal])][max([i[1] for i in optimal])][1]))
    print('Cross-Validation accuracy: F1 = ' + str(max([i[2] for i in optimal])))
    print('')
    return average_acc

def SVM_train(epochs,rate,w,b, C, training_set, dev_set, mistakes, test_set):
    print('### Test for SVM ###')
    tracker = {}
    for i in range(epochs):
#        print('Epoch: ' + str(i + 1) + ' of ' + str(epochs))
        np.random.shuffle(training_set)
        r = rate / (1 + i)
        w,b, mistakes = SVM(training_set, r, w, b, C, mistakes)
        
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

def logisticRegression_cross_validate(epochs):
    cvfolds = 5
    training_set = []
    validation_set = []
    avgF1 = 0;
    
    average_acc = {1     : {10000:0, 1000:0, 100:0, 10:0 ,1:0, 0.1:0}, \
                   0.1   : {10000:0, 1000:0, 100:0, 10:0 ,1:0, 0.1:0}, \
                   .01   : {10000:0, 1000:0, 100:0, 10:0 ,1:0, 0.1:0}, \
                   .001  : {10000:0, 1000:0, 100:0, 10:0 ,1:0, 0.1:0}, \
                   .0001 : {10000:0, 1000:0, 100:0, 10:0 ,1:0, 0.1:0},
                   .00001: {10000:0, 1000:0, 100:0, 10:0 ,1:0, 0.1:0}}
    
    pr = {1     : {10000:[0,0], 1000:[0,0], 100:[0,0], 10:[0,0] ,1:[0,0], 0.1:[0,0]}, \
                   0.1   : {10000:[0,0], 1000:[0,0], 100:[0,0], 10:[0,0] ,1:[0,0], 0.1:[0,0]}, \
                   .01   : {10000:[0,0], 1000:[0,0], 100:[0,0], 10:[0,0] ,1:[0,0], 0.1:[0,0]}, \
                   .001  : {10000:[0,0], 1000:[0,0], 100:[0,0], 10:[0,0] ,1:[0,0], 0.1:[0,0]}, \
                   .0001 : {10000:[0,0], 1000:[0,0], 100:[0,0], 10:[0,0] ,1:[0,0], 0.1:[0,0]},
                   .00001: {10000:[0,0], 1000:[0,0], 100:[0,0], 10:[0,0] ,1:[0,0], 0.1:[0,0]}}

    #optimal = [0,0,-1]
    
    print('### Cross Validation for Logistic Regression ###')
    for i in range(cvfolds):
        print('CVFold #' + str(i))
        training_set = []
        for j in range(cvfolds):
            if j == i: 
                validation_set = loadData(CV_DIR + '/training0' + str(i) + '.data')
            else:
                training_set += loadData(CV_DIR + '/training0' + str(j) + '.data')
                
        for rate in [1,0.1,0.01,0.001,0.0001,0.00001]:
            print('  Running for rate = ' + str(rate))
            for tradeoff in [10000, 1000, 100, 10, 1, 0.1]:
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
                
                p = mistakes[0]/(mistakes[0]+mistakes[1])
                r = mistakes[0]/(mistakes[0]+mistakes[2])
                if (p == 0 and r == 0):
                    F1 = 0;
                else:
                    F1 = 2*(p*r)/(p+r);
                
                avgF1 += F1 / epochs;
                
                average_acc[rate][tradeoff] += (avgF1) / cvfolds
                pr[rate][tradeoff][0] += p / cvfolds
                pr[rate][tradeoff][1] += r / cvfolds
        
    
    optimal = [[list(average_acc.keys())[list(average_acc.values()).index(j)], list(j.keys())[list(j.values()).index(max(j.values()))], max(j.values())] for j in [average_acc[i] for i in list(average_acc.keys())]]
    print('Optimal Parameters: rate=' + str(max([i[0] for i in optimal])) + ' tradeoff=' + str(max([i[1] for i in optimal])))
    print('Precision for optimal: ' + str(pr[max([i[0] for i in optimal])][max([i[1] for i in optimal])][0]) + '; Recall for optimal: ' + str(pr[max([i[0] for i in optimal])][max([i[1] for i in optimal])][1]))
    print('Cross-Validation accuracy: F1 = ' + str(max([i[2] for i in optimal])))
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


def predict(data,w,b):
    counter = 0
    mistakes = 0
    TP = 0
    FP = 0
    FN = 0
    
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
        pred += b
        
        if (yi * pred) > 0:
            TP = TP + 1
        elif (yi * pred) <= 0:
            if (yi == -1):
                FP = FP + 1
            else:
                FN = FN + 1  
                
    return [TP,FP,FN]

def predictBayes(data, ap, an, bp, bn, p, n):
    TP = 0
    FP = 0
    FN = 0
    
    pred = 0
    for example in data:
        yi = 0;
        predictPlus = p
        predictMinus = n
        
        yi = example['label']
        for key in list(example.keys()):
            if key == 'label':
                continue
            else:
                if key == '1':
                    predictPlus *= ap[int(key)-1]
                    predictMinus *= an[int(key)-1]
                else:
                    predictPlus *= bp[int(key)-1]
                    predictMinus *= bn[int(key)-1]
                    
        if  predictPlus >= predictMinus :
            pred = 1
        else:
            pred = -1
        
        if (yi * pred) > 0:
            TP += 1
        elif (yi * pred) <= 0:
            if (yi == -1):
                FP += 1
            else:
                FN += 1
                
#    for example in data:
#        yi = 0;
#        pred = 0
#        predictPlus = 1
#        predictMinus = 1
#        for key in list(example.keys()):
#            if key == 'label':
#                yi = example[key]
#            else:
#                if (key in list(a.keys())):
#                    probp = (a[key] + lam)/(pp + 2*lam)
#                else:
#                    probp = 0
#                    
#                if (key in list(b.keys())):
#                    probn = (b[key] + lam)/(pn + 2*lam)
#                else:
#                    probn = 0
#                
#                predictPlus *= probp
#                predictMinus *= probn
#                
#                if pp*predictPlus > pn*predictMinus:
#                    pred = 1
#                else:
#                    pred = -1
#        
#        if (yi * pred) > 0:
#            TP += 1
#        elif (yi * pred) <= 0:
#            if (yi == -1):
#                FP += 1
#            else:
#                FN += 1  
                
    return [TP,FP,FN]
    
def predictLogistic(data,w,b):
    counter = 0
    mistakes = 0
    TP = 0
    FP = 0
    FN = 0
    
    
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
        
        if (yi * pred) > 0:
            TP += 1
        elif (yi * pred) <= 0:
            if (yi == -1):
                FP += 1
            else:
                FN += 1  
                
    out = [TP,FP,FN]
    return [TP,FP,FN]
    
def crossValidateBayes(data,dev_set,numFeatures):
    cvfolds = 5
    training_set = []
    validation_set = []
    F1 = 0;
    
    average_acc = {5:0, 3:0, 2.5:0, 2.25:0, 2:0, 1.5:0, 1:0, 0.5:0, 0.1:0}
    pr = {5:[0,0], 3:[0,0], 2.5:[0,0], 2.25:[0,0], 2:[0,0], 1.5:[0,0], 1:[0,0], 0.5:[0,0], 0.1:[0,0]}
    
    print('### Cross Validation for Naive Bayes ###')
    for i in range(cvfolds):
        print('CVFold #' + str(i))
        training_set = []
        for j in range(cvfolds):
            if j == i: 
                validation_set = loadData(CV_DIR + '/training0' + str(i) + '.data')
            else:
                training_set += loadData(CV_DIR + '/training0' + str(j) + '.data')
                
        ap, an, bp, bn, p, n = NBayes(training_set,numFeatures)        
#        a,b,pp,pn = NBayes([{'label': 1, '10': 1.0, '12': 1.0, '15': 1.0, '18': 1.0, '31': 1.0, '36': 1.0, '48': 1.0, '59': 1.0, '70': 1.0, '79': 1.0, '90': 1.0, '100': 1.0, '125': 1.0, '140': 1.0, '163': 1.0, '185': 1.0, '200': 1.0}, {'label': 1, '9': 1.0, '11': 1.0, '14': 1.0, '18': 1.0, '29': 1.0, '36': 1.0, '48': 1.0, '59': 1.0, '68': 1.0, '79': 1.0, '89': 1.0, '103': 1.0, '120': 1.0, '143': 1.0, '160': 1.0, '180': 1.0, '200': 1.0}, {'label': -1, '10': 1.0, '11': 1.0, '14': 1.0, '18': 1.0, '29': 1.0, '35': 1.0, '46': 1.0, '57': 1.0, '68': 1.0, '79': 1.0, '90': 1.0, '104': 1.0, '124': 1.0, '143': 1.0, '163': 1.0, '183': 1.0, '203': 1.0}, {'label': 1, '9': 1.0, '11': 1.0, '14': 1.0, '18': 1.0, '30': 1.0, '35': 1.0, '46': 1.0, '57': 1.0, '68': 1.0, '79': 1.0, '90': 1.0, '103': 1.0, '123': 1.0, '143': 1.0, '163': 1.0, '183': 1.0, '204': 1.0}, {'label': -1, '10': 1.0, '12': 1.0, '14': 1.0, '18': 1.0, '33': 1.0, '36': 1.0, '45': 1.0, '56': 1.0, '67': 1.0, '78': 1.0, '89': 1.0, '100': 1.0, '120': 1.0, '140': 1.0, '160': 1.0, '193': 1.0, '203': 1.0}],{},{})
        
        for lam in [5,3,2.5,2.25, 2,1.5,1,.5,0.1]:
#            print('  Running for lambda = ' + str(lam))
            avgF1 = 0;
                       
            
            p = [i['label'] for i in training_set].count(1) + numFeatures*lam
            n = [i['label'] for i in training_set].count(-1) + numFeatures*lam
            
            ap = (ap + lam) / p
            an = (an + lam) / n
            bp = (bp + lam) / p
            bn = (bn + lam) / n
            
            pn = p+n
            p = p / (pn)
            n = n / (pn)
    
            np.random.shuffle(validation_set)
            mistakes = predictBayes(validation_set, ap, an, bp, bn, p, n)
            
            #mistakes = [TP,FP,FN]
            p = mistakes[0]/(mistakes[0]+mistakes[1])
            r = mistakes[0]/(mistakes[0]+mistakes[2])
            if (p == 0 and r == 0):
                F1 = 0;
            else:
                F1 = 2*(p*r)/(p+r);
            
            average_acc[lam] += (F1) / cvfolds
            pr[lam][0] = p / cvfolds
            pr[lam][1] = r / cvfolds
        
    
    ap, an, bp, bn, p, n =  NBayes(data,numFeatures)
    lam = 5
    
    p = [i['label'] for i in data].count(1) + numFeatures*lam
    n = [i['label'] for i in data].count(-1) + numFeatures*lam
    
    ap = (ap + lam) / p
    an = (an + lam) / n
    bp = (bp + lam) / p
    bn = (bn + lam) / n
    
    pn = p+n
    p = p / (pn)
    n = n / (pn)
    
    
    np.random.shuffle(test_set)
    mistakes = predictBayes(test_set, ap, an, bp, bn, p, n)
    
    p = mistakes[0]/(mistakes[0]+mistakes[1])
    r = mistakes[0]/(mistakes[0]+mistakes[2])
    
    if (p == 0 and r == 0):
        F1 = 0;
    else:
        F1 = 2*(p*r)/(p+r);
    
    idx = list(average_acc.keys())[list(average_acc.values()).index(max(list(average_acc.values())))]
    
    print('Optimal lambda: ' + str(idx))
    print('Precision for optimal: ' + str(pr[idx][0]) + '; Recall for optimal: ' + str(pr[idx][1]))
    print('Maximum Cross-Validation accuracy: F1 = ' + str(average_acc[idx]))
    print('')
    print('### Test for Naive Bayes ###')
    print("Precision on Test Set: " + str(p) + "; Recall on Test Set; " + str(r))
    print('F1 Score on Test Set: ' + str(F1))
    return average_acc

    
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

testData = loadData(DATA_DIR + 'test.liblinear')
np.random.shuffle(testData)

test_set = testData[0:7999]
dev_set = testData[8000:9999]

CVFolds = []
data = loadData(DATA_DIR + 'train.liblinear')
mistakes = 0

#tracker = SVM_cross_validate(1);
#tracker = SVM_train(30,.0001,{},0, 100, data, dev_set, mistakes, test_set)
#tracker = logisticRegression_cross_validate(1)
#tracker = logisticRegression_train(10,1,{},0, 10000, data, dev_set, mistakes, test_set)


numFeatures = 219;

#NBayes([{'label':0,'x1':0,'x2':0},{'label':0,'x1':0,'x2':1},{'label':0,'x1':1,'x2':0},{'label':1,'x1':1,'x2':1}])
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
            
for lam in range(0,100,2):        
    ap, an, bp, bn, p, n =  NBayes(data,numFeatures)
    lam = lam / 10;
    
    p = [i['label'] for i in data].count(1) + numFeatures*lam
    n = [i['label'] for i in data].count(-1) + numFeatures*lam
    
    ap = (ap + lam) / p
    an = (an + lam) / n
    bp = (bp + lam) / p
    bn = (bn + lam) / n
    
    pn = p+n
    p = p / (pn)
    n = n / (pn)
    
    
    np.random.shuffle(test_set)
    mistakes = predictBayes(test_set, ap, an, bp, bn, p, n)
    
    p = mistakes[0]/(mistakes[0]+mistakes[1])
    r = mistakes[0]/(mistakes[0]+mistakes[2])
    
    if (p == 0 and r == 0):
        F1 = 0;
    else:
        F1 = 2*(p*r)/(p+r);
                
    print('@lam=' + str(lam) + ' F1 = ' + str(F1))
            
            
            
            
            
            
            
            
            
            