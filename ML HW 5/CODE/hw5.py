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
np.random.seed(1234)


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
        if (yi * pred) <= 1:
            #mistakes += 1
            for key in list(example.keys()):
                if key == 'label':
                    continue
                else:
                    w[key] = (1-rate)*w[key] + rate*C*yi*example[key]
        else:
            for key in list(example.keys()):
                if key == 'label':
                    continue
                else:
                    w[key] = (1-rate)*w[key]
        b += rate*yi
            
#    print('Total Updates = ' + str(mistakes))
    return w, b, mistakes

def NBayes(data, a, b):
    countp = {}
    countn = {}
    pp = [i['label'] for i in data].count(1)#/len(data)
    pn = [i['label'] for i in data].count(-1)
    for sample in data:
        if sample['label'] == 1:
            for key in sample.keys():
                if key != 'label':
                    if sample[key] == 1:
                        if (key in list(a.keys())):
                            a[key] += 1
                        else:
                            a[key] = 1
        else:
            for key in sample.keys():
               if key != 'label':
                    if sample[key] == 1:
                        if (key in list(b.keys())):
                            b[key] += 1
                        else:
                            b[key] = 1
                        
#    for key in a.keys():
#        a[key] /= [i['label'] for i in data].count(1)
#    for key in b.keys():
#        b[key] /= [i['label'] for i in data].count(-1)
    
    return a, b, pp, pn


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

    optimal = [0,0,-1]
    
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
                print('  Running for rate = ' + str(rate) + ',  C = ' + str(C))
                avgF1 = 0;
                w = {}
                b = np.random.randint(-1e4,1e4) / 1e6
                
                for k in range(epochs):
                    print('   Epoch: ' + str(k + 1) + ' of ' + str(epochs))
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
        
    print('### Cross Validation for SVM ###')
    optimal = [[list(tracker.keys())[list(tracker.values()).index(j)], list(j.keys())[list(j.values()).index(max(j.values()))], max(j.values())] for j in [tracker[i] for i in list(tracker.keys())]]
    print('Optimal Runs: ' + str(optimal))
    print('Maximum Cross-Validation accuracy: F1 = ' + str(max([i[2] for i in optimal])))
    print('')
    return average_acc

def SVM_train(epochs,rate,w,b, C, training_set, dev_set, mistakes, test_set):
    tracker = {}
    for i in range(epochs):
        print('Epoch: ' + str(i + 1) + ' of ' + str(epochs))
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
        
    
    
    plt.plot(np.arange(1,epochs+1,1),[i[0] for i in tracker.values()])
    print('### Test for SVM ###')
    
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
    out = [TP,FP,FN]
    print('  ' + str(out))
    return [TP,FP,FN]

def predictBayes(a,b,pp,pn,lam,data):
    TP = 0
    FP = 0
    FN = 0
    
    
    for example in data:
        yi = 0;
        pred = 0
        predictPlus = 1
        predictMinus = 1
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key]
            else:
                if (key in list(a.keys())):
                    probp = (a[key] + lam)/(pp + 2*lam)
                else:
                    probp = 0
                    
                if (key in list(b.keys())):
                    probn = (b[key] + lam)/(pn + 2*lam)
                else:
                    probn = 0
                
                predictPlus *= probp
                predictMinus *= probn
                
                if pp*predictPlus > pn*predictMinus:
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
                
    return [TP,FP,FN]
    
    
    
def crossValidateBayes(data,a,b,pp,pn,dev_set):
    cvfolds = 5
    training_set = []
    validation_set = []
    F1 = 0;
    
    average_acc = {5:0, 3:0, 2.5:0, 2.25:0, 2:0, 1.5:0, 1:0, 0.5:0, 0:0}
    
    for i in range(cvfolds):
        print('CVFold #' + str(i))
        training_set = []
        for j in range(cvfolds):
            if j == i: 
                validation_set = loadData(CV_DIR + '/training0' + str(i) + '.data')
            else:
                training_set += loadData(CV_DIR + '/training0' + str(j) + '.data')
                
        a,b,pp,pn = NBayes(training_set,{},{})        
#        a,b,pp,pn = NBayes([{'label': 1, '10': 1.0, '12': 1.0, '15': 1.0, '18': 1.0, '31': 1.0, '36': 1.0, '48': 1.0, '59': 1.0, '70': 1.0, '79': 1.0, '90': 1.0, '100': 1.0, '125': 1.0, '140': 1.0, '163': 1.0, '185': 1.0, '200': 1.0}, {'label': 1, '9': 1.0, '11': 1.0, '14': 1.0, '18': 1.0, '29': 1.0, '36': 1.0, '48': 1.0, '59': 1.0, '68': 1.0, '79': 1.0, '89': 1.0, '103': 1.0, '120': 1.0, '143': 1.0, '160': 1.0, '180': 1.0, '200': 1.0}, {'label': -1, '10': 1.0, '11': 1.0, '14': 1.0, '18': 1.0, '29': 1.0, '35': 1.0, '46': 1.0, '57': 1.0, '68': 1.0, '79': 1.0, '90': 1.0, '104': 1.0, '124': 1.0, '143': 1.0, '163': 1.0, '183': 1.0, '203': 1.0}, {'label': 1, '9': 1.0, '11': 1.0, '14': 1.0, '18': 1.0, '30': 1.0, '35': 1.0, '46': 1.0, '57': 1.0, '68': 1.0, '79': 1.0, '90': 1.0, '103': 1.0, '123': 1.0, '143': 1.0, '163': 1.0, '183': 1.0, '204': 1.0}, {'label': -1, '10': 1.0, '12': 1.0, '14': 1.0, '18': 1.0, '33': 1.0, '36': 1.0, '45': 1.0, '56': 1.0, '67': 1.0, '78': 1.0, '89': 1.0, '100': 1.0, '120': 1.0, '140': 1.0, '160': 1.0, '193': 1.0, '203': 1.0}],{},{})
        
        for lam in [5, 3,2.5,2.25, 2,1.5,1,.5,0]:
            print('  Running for lambda = ' + str(lam))
            avgF1 = 0;
                        
            np.random.shuffle(validation_set)
            mistakes = predictBayes(a,b,pp,pn,lam,validation_set)
            
            #mistakes = [TP,FP,FN]
            p = mistakes[0]/(mistakes[0]+mistakes[1])
            r = mistakes[0]/(mistakes[0]+mistakes[2])
            if (p == 0 and r == 0):
                F1 = 0;
            else:
                F1 = 2*(p*r)/(p+r);
            
            average_acc[lam] += (F1) / cvfolds
        
    print('### Cross Validation for Naive Bayes ###')
    a,b,pp,pn = NBayes(data,{},{}) 
    np.random.shuffle(test_set)
    mistakes = predictBayes(a,b,pp,pn,0,test_set)
    
    p = mistakes[0]/(mistakes[0]+mistakes[1])
    r = mistakes[0]/(mistakes[0]+mistakes[2])
    
    if (p == 0 and r == 0):
        F1 = 0;
    else:
        F1 = 2*(p*r)/(p+r);
    
    idx = list(average_acc.keys())[list(average_acc.values()).index(max(list(average_acc.values())))]
    
    print('Optimal lambda: ' + str(idx))
    print('Maximum Cross-Validation accuracy: F1 = ' + str(average_acc[idx]))
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
#tracker = SVM_train(50,.0001,{},0, 1000, data, dev_set, mistakes, test_set)


tracker = crossValidateBayes(data, {}, {}, 0,0,dev_set)
#NBayes(data[0:5],{},{})