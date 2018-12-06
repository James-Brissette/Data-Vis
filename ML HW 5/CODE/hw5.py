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
np.random.shuffle(test)

test_set = testData[0:7999]
dev_set = testData[8000:9999]

CVFolds = []
data = loadData(DATA_DIR + 'train.liblinear')
mistakes = 0

#tracker = SVM_cross_validate(1);
tracker = SVM_train(50,.0001,{},0, 1000, data, dev_set, mistakes, test_set)



