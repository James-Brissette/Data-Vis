# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 13:36:11 2018

@author: James
"""
import numpy as np

DATA_DIR = 'dataset/'
CV_DIR = 'dataset/CVSplits'
DATA_DIM = 19
INIT_PARAM = np.random.randint(-100,100) / 10000.


def simple_perceptron(data, rate, w, b):
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
            for key in list(example.keys()):
                if key == 'label':
                    continue
                else:
                    w[key-1] += rate*yi*example[key]
            b += rate*yi
            
    print('Mistakes = ' + str(mistakes))
    return w, b

def decaying_perceptron(data, rate, w, b, t):
    decayed_r = rate / (1+t)
    mistakes = 0
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
    print('mistakes = ' + str(mistakes))
    return w, b, t

def margin_perceptron(data, rate, w, b, t, mu):
    decayed_r = rate / (1+t)
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
        
        if (yi * pred) <= mu:
            mistakes += 1
            for key in list(example.keys()):
                if key == 'label':
                    continue
                else:
                    w[key-1] += decayed_r*yi*example[key]
            b += rate*yi
            decayed_r = rate / (1+t)
            print('At t=' + str(t) + ' rate = ' + str(rate) + '/' + str(1+t) + '=' + str(decayed_r))
        
        t += 1
    print('mistakes = ' + str(mistakes))
    return w, b, t

def average_perceptron(data, rate, w, b, avg_w, avg_b):
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
                    print('updating w')
                    w[key-1] += rate*yi*example[key]
                print('updating a')
                avg_w[key-1] += rate*yi*example[key]
                
        if (yi * pred) <= 0:
            b += rate*yi
        avg_b += rate*yi
        print('')
    return w, b, avg_w, avg_b

def aggressive_perceptron():
    
    return


# Need to clarify with the TA exactly how the cross validation is to be run
# before I waste time on trying to set up this function to run it:
    
def cross_validate(algo,epochs,rate,w,b):
    if   algo == 'simple':
#        for i in range(epochs):
#            w, b = simple_perceptron()
        
        return
    elif algo == 'decaying':
        return
    elif algo == 'margin':
        return
    elif algo == 'average':
        return
    elif algo == 'aggressive':
        return
    return

data_file = open(DATA_DIR + 'diabetes.train')

def loadData(fpath):
    temp_data = []
    output = []
    data = {}
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

data = loadData('diabetes.train')

#simple perceptron
rate = .01
w = np.ones(DATA_DIM)*np.random.randint(-10000,10000) / 1000000.
print(str(w))
b = np.random.randint(-10000,10000) / 1000000.

# t for decaying/margin
t = 0

#mu for margin
mu = 0

#a/b for avgerage
avg_w = np.zeros(DATA_DIM)
avg_b = 0

#simple_perceptron(data, rate, w, b)
#decaying_perceptron(data, rate, w, b, t)
#margin_perceptron(data, rate, w, b, t, mu)
x,y,z,aa = average_perceptron(data, rate, w, b, avg_w, avg_b)
