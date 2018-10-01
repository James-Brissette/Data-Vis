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
INIT_PARAM = np.random.randint(-100,100) / 10000.


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
            
    print('Total Updates = ' + str(mistakes))
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
#            print('At t=' + str(t) + ' rate = ' + str(rate) + '/' + str(1+t) + '=' + str(decayed_r))
        
        t += 1
    print('Total Updates = ' + str(mistakes))
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
#            print('At t=' + str(t) + ' rate = ' + str(rate) + '/' + str(1+t) + '=' + str(decayed_r))
        
        t += 1
    print('Total Updates = ' + str(mistakes))
    return w, b, t, mistakes

def average_perceptron(data, rate, w, b, avg_w, avg_b):
    mistakes = 0
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
#                    print('updating w')
                    w[key-1] += rate*yi*example[key]
#                print('updating a')
                avg_w[key-1] += rate*yi*example[key]
                
        if (yi * pred) <= 0:
            mistakes += 1
            b += rate*yi
        avg_b += rate*yi
    
    print('mistakes = ' + str(mistakes))
    return w, b, avg_w, avg_b

def aggressive_perceptron(data, rate, w, b, t, mu):
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
        print(str(example))
        for key in list(example.keys()):
            if key == 'label':
                continue
            xTx += example[key] * example[key]
        print(str(xTx))
        rate = (mu - (yi*pred))/(xTx + 1)
            
        if (yi * pred) <= mu:
            mistakes += 1
            for key in list(example.keys()):
                if key == 'label':
                    continue
                else:
                    w[key-1] += rate*yi*example[key]
                    
            b += rate*yi
#            print('At t=' + str(t) + ' rate = ' + str(rate) + '/' + str(1+t) + '=' + str(decayed_r))
        
        xTx = 0
        t += 1
    print('mistakes = ' + str(mistakes))
    return w, b, t


# Need to clarify with the TA exactly how the cross validation is to be run
# before I waste time on trying to set up this function to run it:
    
def simple_cross_validate(epochs):
    cvfolds = 5
    training_set = []
    validation_set = []
    
    average_acc = {1: 0, .1: 0, .01: 0}
    
#    print('####Crossvalidation for Simple Perceptron####')
    for i in range(cvfolds):
#        print('## Cross Validation on training set ' + str(i))
        for j in range(cvfolds):
            if j == i: 
                validation_set = loadData(CV_DIR + '/training0' + str(i) + '.data')
            else:
                training_set += loadData(CV_DIR + '/training0' + str(j) + '.data')
        
        for rate in [1,0.1,0.01]:
            w = np.ones(DATA_DIM)*np.random.randint(-1e4,1e4) / 1e6
            b = np.random.randint(-1e4,1e4) / 1e6
#            print('    Hyperparameter "rate" = ' + str(rate))
            for k in range(epochs):
                np.random.shuffle(training_set)
                w,b = simple_perceptron(training_set, rate, w, b)
            
#            print('  -- Trained for ' + str(epochs)+ ' Epochs --')
            #predict and report accuracy
            np.random.shuffle(validation_set)
            mistakes = predict(validation_set,w,b)
#            print('    Prediction Accuracy of Learner on Validation Set:' )
#            print('      Mistakes = ' + str(mistakes))
#            print('      Accuracy = ' + str(1 - (mistakes / len(validation_set))))
            
            
            average_acc[rate] += (1 - (mistakes / len(validation_set))) / cvfolds
            
    return average_acc

def simple_train(epochs,rate,w,b,training_set,dev_set,mistakes):
    tracker = {}
    for i in range(epochs):
        np.random.shuffle(training_set)
        w,b, mistakes = simple_perceptron(training_set, rate, w, b, mistakes)
        accuracy = 1 - (predict(dev_set,w,b) / len(dev_set))
        tracker[i] = [accuracy, (w,b)]
    
    
    plt.plot(np.arange(1,epochs+1,1),[i[0] for i in tracker.values()])
    print("Total Mistakes across 20 epochs: " + str(mistakes))
    return tracker







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
            
    return average_acc

def decaying_train(epochs,rate,w,b,t,training_set,dev_set, mistakes):
    tracker = {}
    for i in range(epochs):
        np.random.shuffle(training_set)
        w,b,t, mistakes = decaying_perceptron(training_set, rate, w, b, t, mistakes)
        accuracy = 1 - (predict(dev_set,w,b) / len(dev_set))
        tracker[i] = [accuracy, (w,b)]
    
    
    plt.plot(np.arange(1,epochs+1,1),[i[0] for i in tracker.values()])
    print("Total Mistakes across 20 epochs: " + str(mistakes))
    return tracker







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
            
    return average_acc

def margin_train(epochs,rate,w,b,t,margin,training_set,dev_set, mistakes):
    tracker = {}
    for i in range(epochs):
        np.random.shuffle(training_set)
        w,b,t, mistakes = margin_perceptron(training_set, rate, w, b, t, margin, mistakes)
        accuracy = 1 - (predict(dev_set,w,b) / len(dev_set))
        tracker[i] = [accuracy, (w,b)]
    
    
    plt.plot(np.arange(1,epochs+1,1),[i[0] for i in tracker.values()])
    print("Total Mistakes across 20 epochs: " + str(mistakes))
    return tracker









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


#data_file = open(DATA_DIR + 'diabetes.train')

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

# t for decaying/margin
t = 0
mistakes = 0

#mu for margin
#mu = 0

#a/b for avgerage
#avg_w = np.zeros(DATA_DIM)
#avg_b = 0

dev_set = loadData(DATA_DIR + 'diabetes.dev')
test_set = loadData(DATA_DIR + 'diabetes.test')

#command to run simple perceptron
#accuracy = decaying_cross_validate(10)
#accuracy = margin_cross_validate(10)
#tracker = simple_train(20,.01,w,b,data,dev_set,mistakes)
#tracker = decaying_train(20,1,w,b,t,data,dev_set, mistakes)
tracker = margin_train(20,1,w,b,t,0.01,data,dev_set, mistakes)
#command to run decaying perceptron

#tracker = decaying_train(20,1,w,b,t,data,dev_set, mistakes)
#simple_mistakes_test = predict(test_set,w,b)


#decaying_perceptron(data, rate, w, b, t)
#margin_perceptron(data, rate, w, b, t, mu)
#aggressive_perceptron(data, rate, w, b, t, mu)
#x,y,z,aa = average_perceptron(data, rate, w, b, avg_w, avg_b)
#b = [0,0,0]
#for i in range(5):
#    a = decaying_cross_validate(10)
#    b[0] += a[1]   / 5
#    b[1] += a[.1]  / 5
#    b[2] += a[.01] / 5
#    print(str(a))