# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 11:27:36 2018

@author: James
"""

import numpy as np
import matplotlib.pyplot as plt

DATA_DIR = '../movie-ratings/data-splits/'
np.random.seed(1234)

def average_perceptron(data, rate, w, b, avg_w, avg_b, mistakes):
    counter = 0
    for example in data:
        yi = 0;
        pred = 0;
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
            else:
                if (key in list(w.keys())):
                    pred += w[key]*example[key]
                else:
                    w[key] = np.random.randint(-10000,10000) / 1000000.
                    pred += w[key]*example[key]
#                print('key: ' + str(key) + ' -- w[key]: ' + str(w[key]))
        pred += b
        
#       update w only on error, update a regardless
        for key in list(example.keys()):
            if key == 'label':
                continue
            else:
                if (yi * pred) <= 0:
                    w[key] += rate*yi*example[key]
#                    print('  prediction incorrect. Updating w')
                
                if (key in list(avg_w.keys())):
                    avg_w[key] += w[key]
                else:
                    avg_w[key] = w[key]
                
        if (yi * pred) <= 0:
            mistakes += 1
            b += rate*yi
        avg_b += rate*yi
#    print('Total Updates = ' + str(mistakes))
        counter = counter + 1
        if (counter % 250 == 0):
            print('        Example ' + str(counter) + ' completed')
            
    return w, b, avg_w, avg_b, mistakes

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++ AVERAGE PERCEPTRON ++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def average_cross_validate(epochs):
    cvfolds = len(CVFolds);
    training_set = []
    validation_set = []
    
    average_acc = {1: 0, .1: 0, .01: 0}
    
    print('Entering Cross Validation for ' + str(epochs) + ' epochs using ' + str(cvfolds) + '-Fold Cross Validation')
    for i in range(cvfolds):
        training_set = []
        for j in range(cvfolds):
            if j == i: 
                validation_set = CVFolds[j][0][0:20]
            else:
                training_set += CVFolds[j][0][0:20]
        
        for rate in [1,0.1,0.01]:
            print('    Initializing CV with rate = ' + str(rate))
#            w = np.ones(DATA_DIM)*np.random.randint(-1e4,1e4) / 1e6
            w = {}
            b = np.random.randint(-1e4,1e4) / 1e6
#            avg_w = np.ones(DATA_DIM)*np.random.randint(-1e4,1e4) / 1e6
            avg_w = {}
            avg_b = np.random.randint(-1e4,1e4) / 1e6
            
            for k in range(epochs):
                print('    Starting epoch ' + str(k))
                np.random.shuffle(training_set)
                w,b, avg_w, avg_b, _ = average_perceptron(training_set, rate, w, b, avg_w, avg_b, 0)
            
            np.random.shuffle(validation_set)
            print('     Beginning Prediction...')
            mistakes = predict(validation_set,avg_w,avg_b)
            
            average_acc[rate] += (1 - (mistakes / len(validation_set))) / cvfolds
        
    print('### Cross Validation for Average Perceptron ###')
    print('Optimal Rate: ' + str(list(average_acc.keys())[list(average_acc.values()).index(max(average_acc.values()))]))
    print('Maximum Cross-Validation accuracy: ' + str(max(average_acc.values()))) 
    print('')
    return average_acc

def average_train(epochs,rate,w,b, avg_w, avg_b, training_set, dev_set, mistakes):
    tracker = {}
    for i in range(epochs):
        print('Starting epoch ' + str(i))
        np.random.shuffle(training_set)
        w,b, avg_w, avg_b, mistakes = average_perceptron(training_set, rate, w, b, avg_w, avg_b, mistakes)
        accuracy = 1 - (predict(dev_set,avg_w,avg_b) / len(dev_set))
        tracker[i] = [accuracy]
    
#    plt.plot(np.arange(1,epochs+1,1),[i[0] for i in tracker.values()])
    print('### Test for Average Perceptron ###')
    print("Total Mistakes across 20 epochs: " + str(mistakes))
    
    idx = list(tracker.values()).index(max(tracker.values()))
    print("Max accuracy on Dev set: " + str(tracker[idx][0]) + ' at epoch ' + str(idx +1))
#    print("Accuracy on Test set: " + str((1 - (predict(test_set,tracker[idx][1][0],tracker[idx][1][1]) / len(test_set)))))
    print('')
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
                    w[key] = np.random.randint(-10000,10000) / 1000000.
                    pred += w[key]*example[key]
        pred += b
        
        if (yi * pred) <= 0:
            mistakes += 1
        
        counter = counter + 1
        if (counter % 250 == 0):
            print('        Prediction ' + str(counter) + ' completed')
            
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
            row[int(parse[0])] = float(parse[1])
        output.append(row)
    return output

def generateCVFolds(data, numFolds):
    np.random.shuffle(data)
    n = len(data)
    batch = int(n/numFolds)
    for i in range(numFolds):
        idx = int(i*batch);
        print('idx of fold ' + str(i+1) + ' = ' + str(idx))
        CVFolds.append([data[idx:idx+batch]])
    return
    
    
test = []
CVFolds = []
data = loadData(DATA_DIR + 'data.train')
generateCVFolds(data,5)


w = {}
b = np.random.randint(-10000,10000) / 1000000.
t = 0
mistakes = 0
avg_w = {}
avg_b = 0


#accuracy = average_cross_validate(5)
tracker = average_train(20,1,w,b,avg_w, avg_b,data[5000:5100],CVFolds[0][0][100:300], mistakes)