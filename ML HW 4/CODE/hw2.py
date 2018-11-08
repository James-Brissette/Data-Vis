# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 13:36:11 2018

@author: James
"""
import numpy as np
import matplotlib.pyplot as plt

DATA_DIR = './dataset/'
CV_DIR = './dataset/CVSplits'
DATA_DIM = 19
np.random.seed(1234)

def simple_perceptron(data, rate, w, b, mistakes):
    for example in data:
        yi = 0;
        pred = 0
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
            else:
                pred += w[key-1]*example[key]
        pred += b
        
        if (yi * pred) <= 0:
            mistakes += 1
            for key in list(example.keys()):
                if key == 'label':
                    continue
                else:
                    w[key-1] += rate*yi*example[key]
            b += rate*yi
            
#    print('Total Updates = ' + str(mistakes))
    return w, b, mistakes

def decaying_perceptron(data, rate, w, b, t, mistakes):
    decayed_r = rate / (1+t)
    for example in data:
        yi = 0;
        pred = .01;
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
            else:
                pred += w[key-1]*example[key]
        pred += b
        
        if (yi * pred) <= 0:
            mistakes += 1
            for key in list(example.keys()):
                if key == 'label':
                    continue
                else:
                    w[key-1] += decayed_r*yi*example[key]
            b += rate*yi
            decayed_r = rate / (1+t)
        
        t += 1
#    print('Total Updates = ' + str(mistakes))
    return w, b, t, mistakes

def margin_perceptron(data, rate, w, b, t, mu, mistakes):
    decayed_r = rate / (1+t)
    for example in data:
        yi = 0;
        pred = 0;
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
            else:
                pred += w[key-1]*example[key]
        pred += b
        
        if (yi * pred) <= mu:
            mistakes += 1
            for key in list(example.keys()):
                if key == 'label':
                    continue
                else:
                    w[key-1] += decayed_r*yi*example[key]
            b += rate*yi
            decayed_r = rate / (1+t)
        
        t += 1
#    print('Total Updates = ' + str(mistakes))
    return w, b, t, mistakes

def average_perceptron(data, rate, w, b, avg_w, avg_b, mistakes):
    for example in data:
        yi = 0;
        pred = 0;
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
            else:
                pred += w[key-1]*example[key]
        pred += b
        
#       update w only on error, update a regardless
        for key in list(example.keys()):
            if key == 'label':
                continue
            else:
                if (yi * pred) <= 0:
                    w[key-1] += rate*yi*example[key]
                avg_w[key-1] += w[key-1]
                
                
        if (yi * pred) <= 0:
            mistakes += 1
            b += rate*yi
        avg_b += rate*yi
    
#    print('Total Updates = ' + str(mistakes))
    return w, b, avg_w, avg_b, mistakes

def aggressive_perceptron(data, w, b, mu, mistakes):
    mistakes = 0
    xTx = 0
    
    for example in data:
        yi = 0;
        pred = 0;
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
            else:
                pred += w[key-1]*example[key]
        pred += b
        
#       Calculate xTx for calculating the learning rate
        for key in list(example.keys()):
            if key == 'label':
                continue
            xTx += example[key] * example[key]
        rate = (mu - (yi*pred))/(xTx + 1)
            
        if (yi * pred) <= mu:
            mistakes += 1
            for key in list(example.keys()):
                if key == 'label':
                    continue
                else:
                    w[key-1] += rate*yi*example[key]
                    
            b += rate*yi
        
        xTx = 0
#    print('Total Updates = ' + str(mistakes))
    return w, b, mistakes


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++ SIMPLE PERCEPTRON ++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
def simple_cross_validate(epochs):
    cvfolds = 5
    training_set = []
    validation_set = []
    
    average_acc = {1: 0, .1: 0, .01: 0}
    
    for i in range(cvfolds):
        for j in range(cvfolds):
            if j == i: 
                validation_set = loadData(CV_DIR + '/training0' + str(i) + '.data')
            else:
                training_set += loadData(CV_DIR + '/training0' + str(j) + '.data')
        
        for rate in [1,0.1,0.01]:
            w = np.ones(DATA_DIM)*np.random.randint(-1e4,1e4) / 1e6
            b = np.random.randint(-1e4,1e4) / 1e6
            
            for k in range(epochs):
                np.random.shuffle(training_set)
                w,b,_ = simple_perceptron(training_set, rate, w, b, 0)
            
            np.random.shuffle(validation_set)
            mistakes = predict(validation_set,w,b)
            
            
            average_acc[rate] += (1 - (mistakes / len(validation_set))) / cvfolds
        
    print('### Cross Validation for Simple Perceptron ###')
    print('Optimal Rate: ' + str(list(average_acc.keys())[list(average_acc.values()).index(max(average_acc.values()))]))
    print('Maximum Cross-Validation accuracy: ' + str(max(average_acc.values())))
    print('')
    return average_acc

def simple_train(epochs,rate,w,b,training_set,dev_set,mistakes):
    tracker = {}
    for i in range(epochs):
        np.random.shuffle(training_set)
        w,b, mistakes = simple_perceptron(training_set, rate, w, b, mistakes)
        accuracy = 1 - (predict(dev_set,w,b) / len(dev_set))
        tracker[i] = [accuracy, (w,b)]
    
    
#    plt.plot(np.arange(1,epochs+1,1),[i[0] for i in tracker.values()])
    print('### Test for Simple Perceptron ###')
    print("Total Mistakes across 20 epochs: " + str(mistakes))
    
    idx = list(tracker.values()).index(max(tracker.values()))
    print("Max accuracy on Dev set: " + str(tracker[idx][0]) + ' at epoch ' + str(idx +1))
    print("Accuracy on Test set: " + str((1 - (predict(test_set,tracker[idx][1][0],tracker[idx][1][1]) / len(test_set)))))
    print('')
    return tracker


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++ DECAYING PERCEPTRON ++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def decaying_cross_validate(epochs):
    cvfolds = 5
    training_set = []
    validation_set = []
    
    average_acc = {1: 0, .1: 0, .01: 0}
    
    for i in range(cvfolds):
        for j in range(cvfolds):
            if j == i: 
                validation_set = loadData(CV_DIR + '/training0' + str(i) + '.data')
            else:
                training_set += loadData(CV_DIR + '/training0' + str(j) + '.data')
        
        for rate in [1,0.1,0.01]:
            w = np.ones(DATA_DIM)*np.random.randint(-1e4,1e4) / 1e6
            b = np.random.randint(-1e4,1e4) / 1e6
            t = 0
            
            for k in range(epochs):
                np.random.shuffle(training_set)
                w,b,t,_ = decaying_perceptron(training_set, rate, w, b, t, 0)
                
            np.random.shuffle(validation_set)
            mistakes = predict(validation_set,w,b)
            
            
            average_acc[rate] += (1 - (mistakes / len(validation_set))) / cvfolds
    
    print('### Cross Validation for Decaying Perceptron ###')
    print('Optimal Rate: ' + str(list(average_acc.keys())[list(average_acc.values()).index(max(average_acc.values()))]))
    print('Maximum Cross-Validation accuracy: ' + str(max(average_acc.values())))    
    print('')
    return average_acc

def decaying_train(epochs,rate,w,b,t,training_set,dev_set, mistakes):
    tracker = {}
    for i in range(epochs):
        np.random.shuffle(training_set)
        w,b,t, mistakes = decaying_perceptron(training_set, rate, w, b, t, mistakes)
        accuracy = 1 - (predict(dev_set,w,b) / len(dev_set))
        tracker[i] = [accuracy, (w,b)]
    
    
#    plt.plot(np.arange(1,epochs+1,1),[i[0] for i in tracker.values()])
    print('### Test for Decaying Perceptron ###')
    print("Total Mistakes across 20 epochs: " + str(mistakes))
    
    idx = list(tracker.values()).index(max(tracker.values()))
    print("Max accuracy on Dev set: " + str(tracker[idx][0]) + ' at epoch ' + str(idx +1))
    print("Accuracy on Test set: " + str((1 - (predict(test_set,tracker[idx][1][0],tracker[idx][1][1]) / len(test_set)))))
    print('')
    return tracker


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++ MARGIN PERCEPTRON ++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def margin_cross_validate(epochs):
    cvfolds = 5
    training_set = []
    validation_set = []
    
    average_acc = {1: {1: 0, .1: 0, .01: 0},
                   .1: {1: 0, .1: 0, .01: 0},
                   .01: {1: 0, .1: 0, .01: 0}}
    
#    print('####Crossvalidation for Simple Perceptron####')
    for i in range(cvfolds):
#        print('## Cross Validation on training set ' + str(i))
        for j in range(cvfolds):
            if j == i: 
                validation_set = loadData(CV_DIR + '/training0' + str(i) + '.data')
            else:
                training_set += loadData(CV_DIR + '/training0' + str(j) + '.data')
                
        for margin in [1,0.1,0.01]:
            for rate in [1,0.1,0.01]:
                w = np.ones(DATA_DIM)*np.random.randint(-1e4,1e4) / 1e6
                b = np.random.randint(-1e4,1e4) / 1e6
                t = 0
                
                for k in range(epochs):
                    np.random.shuffle(training_set)
                    w,b,t, _ = margin_perceptron(training_set, rate, w, b, t, margin, 0)
                    
                np.random.shuffle(validation_set)
                mistakes = predict(validation_set,w,b)
                
                average_acc[margin][rate] += (1 - (mistakes / len(validation_set))) / cvfolds
    

    a = [1 , max(average_acc[1].values()) , list(average_acc[1].values()).index(max(average_acc[1].values()))]
    b = [.1 , max(average_acc[.1].values()) , list(average_acc[.1].values()).index(max(average_acc[.1].values()))]
    c = [.01 , max(average_acc[.01].values()) , list(average_acc[.01].values()).index(max(average_acc[.01].values()))]
    
    if a[1] > b[1]:
        if a[1] > c[1]:
            out = a
        else:
            out = c
    elif b[1] > c[1]:
        out = b
    else:
        out = c
        
    print('### Cross Validation for Margin Perceptron ###')    
    print('Optimal Margin: ' + str(out[0]))      
    print('Optimal Rate: ' + str(list(average_acc.keys())[out[2]]))
    print('Maximum Cross-Validation accuracy: ' + str(out[1]))     
    print('')
    return average_acc

def margin_train(epochs,rate,w,b,t,margin,training_set,dev_set, mistakes):
    tracker = {}
    for i in range(epochs):
        np.random.shuffle(training_set)
        w,b,t, mistakes = margin_perceptron(training_set, rate, w, b, t, margin, mistakes)
        accuracy = 1 - (predict(dev_set,w,b) / len(dev_set))
        tracker[i] = [accuracy, (w,b)]
    
    
#    plt.plot(np.arange(1,epochs+1,1),[i[0] for i in tracker.values()])
    print('### Test for Margin Perceptron ###')
    print("Total Mistakes across 20 epochs: " + str(mistakes))
    
    idx = list(tracker.values()).index(max(tracker.values()))
    print("Max accuracy on Dev set: " + str(tracker[idx][0]) + ' at epoch ' + str(idx +1))
    print("Accuracy on Test set: " + str((1 - (predict(test_set,tracker[idx][1][0],tracker[idx][1][1]) / len(test_set)))))
    print('')
    return tracker


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++ AVERAGE PERCEPTRON ++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def average_cross_validate(epochs):
    cvfolds = 5
    training_set = []
    validation_set = []
    
    average_acc = {1: 0, .1: 0, .01: 0}
    
    for i in range(cvfolds):
        for j in range(cvfolds):
            if j == i: 
                validation_set = loadData(CV_DIR + '/training0' + str(i) + '.data')
            else:
                training_set += loadData(CV_DIR + '/training0' + str(j) + '.data')
        
        for rate in [1,0.1,0.01]:
            w = np.ones(DATA_DIM)*np.random.randint(-1e4,1e4) / 1e6
            b = np.random.randint(-1e4,1e4) / 1e6
            avg_w = np.ones(DATA_DIM)*np.random.randint(-1e4,1e4) / 1e6
            avg_b = np.random.randint(-1e4,1e4) / 1e6
            
            for k in range(epochs):
                np.random.shuffle(training_set)
                w,b, avg_w, avg_b, _ = average_perceptron(training_set, rate, w, b, avg_w, avg_b, 0)
            
            np.random.shuffle(validation_set)
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
        np.random.shuffle(training_set)
        w,b, avg_w, avg_b, mistakes = average_perceptron(training_set, rate, w, b, avg_w, avg_b, mistakes)
        accuracy = 1 - (predict(dev_set,avg_w,avg_b) / len(dev_set))
        tracker[i] = [accuracy, (avg_w,avg_b)]
    
#    plt.plot(np.arange(1,epochs+1,1),[i[0] for i in tracker.values()])
    print('### Test for Average Perceptron ###')
    print("Total Mistakes across 20 epochs: " + str(mistakes))
    
    idx = list(tracker.values()).index(max(tracker.values()))
    print("Max accuracy on Dev set: " + str(tracker[idx][0]) + ' at epoch ' + str(idx +1))
    print("Accuracy on Test set: " + str((1 - (predict(test_set,tracker[idx][1][0],tracker[idx][1][1]) / len(test_set)))))
    print('')
    return tracker


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++ AGGRESSIVE PERCEPTRON ++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def aggressive_cross_validate(epochs):
    cvfolds = 5
    training_set = []
    validation_set = []
    
    average_acc = {1: 0, .1: 0, .01: 0}
    
    for i in range(cvfolds):
        for j in range(cvfolds):
            if j == i: 
                validation_set = loadData(CV_DIR + '/training0' + str(i) + '.data')
            else:
                training_set += loadData(CV_DIR + '/training0' + str(j) + '.data')
                
        for margin in [1,0.1,0.01]:
            w = np.ones(DATA_DIM)*np.random.randint(-1e4,1e4) / 1e6
            b = np.random.randint(-1e4,1e4) / 1e6
            
            for k in range(epochs):
                np.random.shuffle(training_set)
                w,b, _ = aggressive_perceptron(training_set, w, b, margin, 0)
                
            np.random.shuffle(validation_set)
            mistakes = predict(validation_set,w,b)
            
            average_acc[margin] += (1 - (mistakes / len(validation_set))) / cvfolds
     
    print('### Cross Validation for Aggressive Perceptron ###')
    print('Optimal Margin: ' + str(list(average_acc.keys())[list(average_acc.values()).index(max(average_acc.values()))]))
    print('Maximum Cross-Validation accuracy: ' + str(max(average_acc.values()))) 
    print('')
    return average_acc

def aggressive_train(epochs,w,b,margin,training_set,dev_set,test_set, mistakes):
    tracker = {}
    for i in range(epochs):
        np.random.shuffle(training_set)
        w,b, mistakes = aggressive_perceptron(training_set, w, b, margin, mistakes)
        accuracy = 1 - (predict(dev_set,w,b) / len(dev_set))
        tracker[i] = [accuracy, (w,b)]
    
    
#    plt.plot(np.arange(1,epochs+1,1),[i[0] for i in tracker.values()])
    
    print('### Test for Aggressive Perceptron ###')
    print("Total Mistakes across 20 epochs: " + str(mistakes))
    idx = list(tracker.values()).index(max(tracker.values()))
    print("Max accuracy on Dev set: " + str(tracker[idx][0]) + ' at epoch ' + str(idx +1))
    print("Accuracy on Test set: " + str((1 - (predict(test_set,tracker[idx][1][0],tracker[idx][1][1]) / len(test_set)))))
    print('')
    return tracker

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def predict(data,w,b):
    mistakes = 0
    for example in data:
        yi = 0;
        pred = 0
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
            else:
                pred += w[key-1]*example[key]
        pred += b
        
        if (yi * pred) <= 0:
            mistakes += 1
    
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
        for j in range(len(data[i])):
            if j == 0:
                continue
            parse = data[i][j].split(':')
            row[int(parse[0])] = float(parse[1])
        output.append(row)
    return output


data = loadData(DATA_DIR + 'diabetes.train')

#simple perceptron
rate = .01
w = np.ones(DATA_DIM)*np.random.randint(-10000,10000) / 1000000.
b = np.random.randint(-10000,10000) / 1000000.
t = 0
mistakes = 0
avg_w = np.zeros(DATA_DIM)
avg_b = 0

dev_set = loadData(DATA_DIR + 'diabetes.dev')
test_set = loadData(DATA_DIR + 'diabetes.test')


#=============================================================================
accuracy = simple_cross_validate(10)
accuracy = decaying_cross_validate(10)
accuracy = margin_cross_validate(10)
accuracy = average_cross_validate(10)
accuracy = aggressive_cross_validate(10)

tracker = simple_train(20,.01,w,b,data,dev_set,mistakes)
tracker = decaying_train(20,1,w,b,t,data,dev_set, mistakes)
tracker = margin_train(20,1,w,b,t,0.01,data,dev_set, mistakes)
tracker = average_train(20,.01,w,b,avg_w, avg_b,data,dev_set, mistakes)
tracker = aggressive_train(20,w,b,0.1,data,dev_set, test_set, mistakes)
#=============================================================================

