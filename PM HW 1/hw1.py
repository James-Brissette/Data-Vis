# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 12:34:50 2019

@author: James
"""

import numpy as np
from scipy.stats import t, norm, beta
from scipy.optimize import minimize
import matplotlib.pyplot as plt

##### Question 1 #####
#for d in [0.1, 1, 10, 100, 1000000]:
#    rv = t(df=d, loc=0, scale=1)
#    mean, var, skew, kurt = rv.stats(moments='mvsk')
#    
#    x = np.linspace(rv.ppf(0.0001), rv.ppf(0.9999), 1000000)
#    y = rv.pdf(x)
#
#    plt.xlim(-3,3)
#    plt.plot(x,y, label='T, df=' + str(d))
#    
#gauss = norm()
#x = np.linspace(norm.ppf(0.0001), norm.ppf(0.9999), 100)
#y = gauss.pdf(x)
######################


##### Question 2a #####
#for d in [1, 5, 10]:
#    a = d
#    b = a
#    rv = beta(a,b)
#    mean, var, skew, kurt = beta.stats(a, b, moments='mvsk')
#    
#    x = np.linspace(beta.ppf(0.00001, a, b), beta.ppf(0.99999, a, b), 100)
#    y = beta.pdf(x,a,b)
#
#    plt.xlim(0,1)
#    plt.plot(x,y, label='a=' + str(a) + ',b=' + str(b))
#    
#plt.legend()
#######################

##### Question 2b #####
#for d in [1, 5, 10]:
#    a = d
#    b = a + 1
#    rv = beta(a,b)
#    mean, var, skew, kurt = beta.stats(a, b, moments='mvsk')
#    
#    x = np.linspace(beta.ppf(0.00001, a, b), beta.ppf(0.99999, a, b), 100)
#    y = beta.pdf(x,a,b)
#
#    plt.xlim(0,1)
#    plt.plot(x,y, label='a=' + str(a) + ',b=' + str(b))
#    
#plt.legend()
#######################

x = norm.rvs(loc=0, scale=2, size=30)
y = norm.pdf(x)
plt.xlim(-3,3)


def model(params):
    mean, var = params[0], params[1]
    log_lik = -np.sum(norm.logpdf(x,loc=mean,scale=var))
    
    return log_lik

start = np.array([5,5])
model = minimize(model, start, method="L-BFGS-B", options={'disp': True})


xs = np.linspace(norm.ppf(0.01),norm.ppf(0.99),100)
ys = norm.pdf(xs,loc=model.x[0],scale=model.x[1])

plt.plot(xs,ys)
plt.scatter(x,y)