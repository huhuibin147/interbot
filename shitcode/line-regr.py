# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:51:06 2018

@author: huhb
"""

import numpy as np
import pandas as pd

data = pd.read_csv('ex1data1.txt', names=['population','profit'])
data.info()

ones = pd.DataFrame({'ones': np.ones(len(data))})
cc_data = pd.concat([ones, data], axis=1)
X = cc_data.iloc[:,:-1].as_matrix()
y = cc_data.iloc[:,-1].as_matrix()

def normalize_featrue(data):
    return data.apply(lambda column: (column - column.mean()) / column.std())

data = normalize_featrue(data)

theta = np.zeros(X.shape[1])
m = X.shape[0]
def lr_cost(theta, X, y):
    inner = X @ theta - y
    cost = inner.T @ inner / (2 * m)
    return cost

def gradient(theta, X, y):
    return X.T @ (X @ theta - y) / m

def batch_gradient_decent(theta, X, y, epoch, alpha=0.01):
    cost_data = [lr_cost(theta, X, y)]
    _theta = theta.copy()
    
    for i in range(epoch):
        _theta = _theta - alpha * gradient(_theta, X, y)
        cost_data.append(lr_cost(_theta, X, y))
    
    return _theta, cost_data

f_theta, cost_data = batch_gradient_decent(theta, X, y, epoch=500, alpha=0.01)
