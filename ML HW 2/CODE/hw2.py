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
    for example in data:
        yi = 0;
        pred = .01;
        for key in list(example.keys()):
            if key == 'label':
                yi = example[key];
            else:
                pred += w[key-1]*example[key]
        pred += b
        
        if (yi * pred) < 0:
#            print('Incorrect prediction at epoch=' + str(epoch))
            #update weights and bias
            for key in list(example.keys()):
                if key == 'label':
                    continue
                else:
                    w[key-1] += rate*yi*example[key]
            b += rate*yi
        else:
            continue
#            print('Correct prediction at epoch=' + str(epoch))
    return w, b

def decaying_perceptron():
    
    return

def margin_perceptron():
    
    return

def average_perceptron():
    
    return

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

w = np.ones(DATA_DIM)*np.random.randint(-100,100) / 10000.
b = np.random.randint(-100,100) / 10000.
simple_perceptron(data, .01, w, b)
