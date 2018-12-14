# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 13:13:02 2018

@author: James
"""

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
    
    
    
    return ap, an, bp, bn


def predictBayes(data, ap, an, bp, bn, p, n):
    mistakes = 0
    counter = 0
    
    pred = 0
    for example in data:
        yi = 0;
#        predictPlus =p
#        predictMinus =n
        predictPlus = np.log(p)
        predictMinus = np.log(n)
        
        yi = example['label']
        for key in list(example.keys()):
            if key == 'label':
                continue
            else:
                if key == '1':
                    predictPlus += np.log(ap[int(key)-1])
                    predictMinus += np.log(an[int(key)-1])
                else:
                    predictPlus += np.log(bp[int(key)-1])
                    predictMinus += np.log(bn[int(key)-1])
#                if key == '1':
#                    predictPlus *= ap[int(key)-1]
#                    predictMinus *= an[int(key)-1]
#                else:
#                    predictPlus *= bp[int(key)-1]
#                    predictMinus *= bn[int(key)-1]
                    
        if  predictPlus >= predictMinus :
            pred = 1
        else:
            pred = -1
        
        
        if (yi * pred) <= 0:
            mistakes += 1
        
        counter = counter + 1
#        if (counter % 250 == 0):
#            print('        Prediction ' + str(counter) + ' completed')
                
    return mistakes
    
    
def crossValidateBayes(data,dev_set,numFeatures):
    cvfolds = 5
    training_set = []
    validation_set = []
    
    np.random.shuffle(data)
    
    average_acc = {5:0, 3:0, 2.5:0, 2.25:0, 2:0, 1.5:0, 1:0, 0.5:0, 0.1:0}
    
    print('### Cross Validation for Naive Bayes ###')
    for i in range(cvfolds):
        print('CVFold #' + str(i))
        start = i * 5000
        stop = (i+1) * 5000
        validation_set = data[start:stop]
        training_set = data[0:start]
        training_set += data[stop:25000]
        
        ap, an, bp, bn = NBayes(training_set,numFeatures)        
#        a,b,pp,pn = NBayes([{'label': 1, '10': 1.0, '12': 1.0, '15': 1.0, '18': 1.0, '31': 1.0, '36': 1.0, '48': 1.0, '59': 1.0, '70': 1.0, '79': 1.0, '90': 1.0, '100': 1.0, '125': 1.0, '140': 1.0, '163': 1.0, '185': 1.0, '200': 1.0}, {'label': 1, '9': 1.0, '11': 1.0, '14': 1.0, '18': 1.0, '29': 1.0, '36': 1.0, '48': 1.0, '59': 1.0, '68': 1.0, '79': 1.0, '89': 1.0, '103': 1.0, '120': 1.0, '143': 1.0, '160': 1.0, '180': 1.0, '200': 1.0}, {'label': -1, '10': 1.0, '11': 1.0, '14': 1.0, '18': 1.0, '29': 1.0, '35': 1.0, '46': 1.0, '57': 1.0, '68': 1.0, '79': 1.0, '90': 1.0, '104': 1.0, '124': 1.0, '143': 1.0, '163': 1.0, '183': 1.0, '203': 1.0}, {'label': 1, '9': 1.0, '11': 1.0, '14': 1.0, '18': 1.0, '30': 1.0, '35': 1.0, '46': 1.0, '57': 1.0, '68': 1.0, '79': 1.0, '90': 1.0, '103': 1.0, '123': 1.0, '143': 1.0, '163': 1.0, '183': 1.0, '204': 1.0}, {'label': -1, '10': 1.0, '12': 1.0, '14': 1.0, '18': 1.0, '33': 1.0, '36': 1.0, '45': 1.0, '56': 1.0, '67': 1.0, '78': 1.0, '89': 1.0, '100': 1.0, '120': 1.0, '140': 1.0, '160': 1.0, '193': 1.0, '203': 1.0}],{},{})
        
        for lam in [5,3,2.5,2.25, 2,1.5,1,.5,0.1]:
            print('  Running for lambda = ' + str(lam))                       
            
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
            
            
            average_acc[lam] += (mistakes / len(training_set)) / cvfolds
            
        
    idx = list(average_acc.keys())[list(average_acc.values()).index(max(list(average_acc.values())))]
    ap, an, bp, bn =  NBayes(data,numFeatures)
    lam = idx
    
    p = [i['label'] for i in data].count(1)
    n = [i['label'] for i in data].count(-1)
    
    ap = (ap + lam) / (p + 2*lam)
    an = (an + lam) / (n + 2*lam)
    bp = (bp + lam) / (p + 2*lam)
    bn = (bn + lam) / (n + 2*lam)
    
    pn = p+n
    p = p / (pn)
    n = n / (pn)
    
    
    np.random.shuffle(test_set)
    mistakes = predictBayes(testData, ap, an, bp, bn, p, n)
    
    
    idx = list(average_acc.keys())[list(average_acc.values()).index(max(list(average_acc.values())))]
    
    print('Optimal lambda: ' + str(idx))
    print('Maximum Cross-Validation accuracy: ' + str(average_acc[idx]))
    print('')
    print('### Test for Naive Bayes ###')
    print('Accuracy on Test Set: ' + str((mistakes / len(training_set))))
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
#tracker = logisticRegression_cross_validate(1)
#tracker = logisticRegression_train(10,.1,{},0, 10000, data, dev_set, mistakes, test_set)
#tracker = crossValidateBayes(data,dev_set,numFeatures)

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


#=================== PREDICT AND LABEL ===================================

def predictAndLabel(data,ap, an, bp, bn, p, n):
    counter = 1
    mistakes = 0
    for example in data:
        yi = 0;
        predictPlus = np.log(p)
        predictMinus = np.log(n)
        
        for key in list(example[2].keys()):
            if key == 'label':
                yi = example[2][key];
            else:
                if key == '1':
                    predictPlus += np.log(ap[int(key)-1])
                    predictMinus += np.log(an[int(key)-1])
                else:
                    predictPlus += np.log(bp[int(key)-1])
                    predictMinus += np.log(bn[int(key)-1])
#        pred += b
        
        if  predictPlus >= predictMinus :
            pred = 1
        else:
            pred = -1
        
        if (yi * pred) <= 0:
            mistakes += 1
            
        example[1] = pred
       
        if (counter % 250 == 0):
            print('        Prediction ' + str(counter) + ' completed')
        counter = counter + 1
    return mistakes



#ap, an, bp, bn = NBayes(data,numFeatures)

#lam = 0.1
#data = [{'label':-1},{'label':-1,'2':1},{'label':-1,'1':1},{'label':1,'1':1,'2':1}]

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
#mistakes = predictBayes(dev_set, ap, an, bp, bn, p, n)
#p = mistakes[0]/(mistakes[0]+mistakes[1])
#r = mistakes[0]/(mistakes[0]+mistakes[2])
#
#if (p == 0 and r == 0):
#    F1 = 0;
#else:
#    F1 = 2*(p*r)/(p+r);
            
#print('Accuracy =' + str(mistakes / len(dev_set)))

entropy = np.zeros(numFeatures)



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
            
#===================================================          
ap, an, bp, bn = NBayes(data,numFeatures)
a = ap + an
b = bp + bn
omega = 1e-20
pap = ap / a
pan = an / a
hsa = -pan*np.log2((pan+omega))-pap*np.log2((pap+omega))

pbp = bp / b
pbn = bn / b
hsb = -pbn*np.log2((pbn+omega))-pbp*np.log2((pbp+omega))

hs = -.5*np.log2(.5)-.5*np.log2(.5)
IG = 1 - (a/len(data))*hsa - (b/len(data))*hsb
IG_dict = {i:IG[i] for i in range(0,len(IG))}

minimum = min(IG_dict.values())
maximum = max(IG_dict.values())
normalizedIG = {}

for cutoff in [.001,.002,.003,.004,.005,.006,.007,.008,.009,.01]:
    normalizedIG = {}
    for att in test:
        if (test[att] - minimum)/(maximum - minimum) >= cutoff:
            normalizedIG[att] = (test[att] - minimum)/(maximum - minimum)
    print('At cutoff =',str(cutoff),'len = ',str(len(normalizedIG)))

trimmedData = []
for example in data:
    entry = {}
    for key in example:
        if key == 'label':
            entry[key] = example[key]
        else:
            if key in normalizedIG.keys():
                entry[key] = example[key]
    trimmedData.append(entry)
    
            
            
            