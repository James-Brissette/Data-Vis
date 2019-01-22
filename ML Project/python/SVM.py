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

DATA_DIR = '../movie-ratings/data-splits/'
CV_DIR = './data/CVSplits'
DATA_DIM = 19
np.random.seed(9999)


#============================= SVM ======================================

def SVM(data, rate, w, b, C, mistakes):
    counter = 0
    for example in data:
        yi = 0;
        pred = 0
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
            else:
                if (key in list(w.keys())):
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
                    try:
                        w[key] += rate*C*yi*example[key]
                    except:
                        w[key] = rate*C*yi*example[key]
                        
            b += (1-rate)*b + rate*C*yi
        else:
            b += (1-rate)*b# + (1-rate)*C*yi
        counter += 1
        
        if (counter % 250 == 0):
            temp = {}
            for att in w:
                if np.abs(w[att]) > 1e-3:
                    temp[att] = w[att]
            w = temp
            print('        Example ' + str(counter) + ' seen -- weight vector has ' + str(len(w)) + ' elements')
#        print(w)
#        print(b)
#    print('Total Updates = ' + str(mistakes))
    return w, b, mistakes


#========================== SVM CROSS VALIDATION ===========================
def SVM_cross_validate(epochs):
    cvfolds = 1
    training_set = []
    validation_set = []
    avgF1 = 0;
    
    average_acc = {1    : {100000:0, 10000:0, 1000:0, 100:0 ,10:0, 1:0}, \
                   0.1  : {100000:0, 10000:0, 1000:0, 100:0 ,10:0, 1:0}, \
                   .01  : {100000:0, 10000:0, 1000:0, 100:0 ,10:0, 1:0}, \
                   .001 : {100000:0, 10000:0, 1000:0, 100:0 ,10:0, 1:0}, \
                   .0001: {100000:0, 10000:0, 1000:0, 100:0 ,10:0, 1:0}}
    
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
                
        for rate in [0.1]:#,0.01,0.001,0.0001]:
            for C in [10000, 1000, 100, 10]:
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
                
                average_acc[rate][C] += (mistakes) / cvfolds
        
    
    optimal = [[list(average_acc.keys())[list(average_acc.values()).index(j)], list(j.keys())[list(j.values()).index(max(j.values()))], max(j.values())] for j in [average_acc[i] for i in list(average_acc.keys())]]
    print('Optimal Parameters: rate=' + str(max([i[0] for i in optimal])) + ' C=' + str(max([i[1] for i in optimal])))
    print('Cross-Validation accuracy: ' + str(mistakes / len(validation_set)))
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
#        if mistakes[0]+mistakes[1] == 0:
#            p = 1
#        else:
#            p = mistakes[0]/(mistakes[0]+mistakes[1])
#        
#        if mistakes[0]+mistakes[2] == 0:
#            r = 1
#        else:
#            r = mistakes[0]/(mistakes[0]+mistakes[2])
#        
#        if (p == 0 and r == 0):
#            F1 = 0;
#        else:
#            F1 = 2*(p*r)/(p+r);
#            
        tracker[i] = [mistakes/len(dev_set), (w,b)]
        
    
    
#    plt.plot(np.arange(1,epochs+1,1),[i[0] for i in tracker.values()])
    
    
    idx = list(tracker.values()).index(max(tracker.values()))
    print("Max F-score on Dev set: " + str(tracker[idx][0]) + ' at epoch ' + str(idx +1))
    
    np.random.shuffle(test_set)
    mistakes = predict(test_set,tracker[idx][1][0],tracker[idx][1][1])
                
    #mistakes = [TP,FP,FN]
    
    print("Accuracy on Test Set: " + str(mistakes / len(test_set)))
    print('')
    #[i[0] for i in list(tracker.values())].index(min([i[0] for i in tracker.values()]))
    return tracker


def predict(data,w,b):
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
                    w[key] = 0
                    pred += w[key]*example[key]
        #pred += b
        #print(pred)  
        if (yi * pred) <= 0:
            mistakes += 1
            example[1] = yi*-1
        else:
            example[1] = yi
            
        if (counter % 100 == 0):
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

def loadTestData(fpath):
    temp_data = []
    ids = [];
    output = []
    data = {}
    data_file = open(fpath)
    data_id = open(fpath+'.id')
    
    for line in data_file:
        temp_data.append(line)
        
    for line in data_id:
        ids.append(line)
    
    
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
            row[int(parse[0])] = float(parse[1])
        output.append([ids[i].replace('\n',''), 0, row])
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
                    try:
                        pred += w[key]*example[2][key]
                    except:
                        pass 
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


#tracker = SVM_cross_validate(1);
tracker2 = SVM_train(1,.1,{},0, 10000, data, dev_set, mistakes, test_set)            
            
#f = open('test-submissionSVM.txt','w')
#f.write(repr([item[0:2] for item in testData]))
#f.close()
            
  

#to run
#predictAndLabel(test,tracker[0][1][0],tracker[0][1][1])          
            
            