# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 17:41:04 2018

@author: huhb
"""

import pandas as pd
import numpy as np
import tensorflow as tf    
import json
with open('us.txt', 'r') as f:
    datas = json.loads(f.readlines()[0])

for r in datas:
    r['pc'] = float(r['pc'])
    r['tth'] = float(r['tth'])

def normalize_feature(df):
    return df.apply(lambda column: (column - column.mean()) / column.std())


def descre(df):
    return df.apply(lambda c: 1 / c)

df = pd.DataFrame(datas)

pp_m = df['pp_raw'].mean()
pp_s = df['pp_raw'].std()
acc_m = df['acc'].mean()
acc_s = df['acc'].std()
bpacc_m = df['bpacc'].mean()
bpacc_s = df['bpacc'].std()
bppp_m = df['bppp'].mean()
bppp_s = df['bppp'].std()
pc_m = df['pc'].mean()
pc_s = df['pc'].std()
tth_m = df['tth'].mean()
tth_s = df['tth'].std()

#df = descre(df)
df = normalize_feature(df)


ys = df['pp_raw']
del df['pp_raw']

#df = normalize_feature(df)
#df = descre(df)


#xs = df.as_matrix()
ys = ys.as_matrix()
xs = np.float32(df.T)

b = tf.Variable(tf.zeros([1]))
w = tf.Variable(tf.random_uniform([1, 5], 0, 1.0))
y = tf.matmul(w, xs) + b


loss =  tf.reduce_mean(tf.square(y - ys))
optimizer = tf.train.GradientDescentOptimizer(0.1)
train = optimizer.minimize(loss)

init = tf.global_variables_initializer()
sess =  tf.Session()
sess.run(init)

w1 = None
b1 = None
for step in range(5):
    sess.run(train)
    if step % 1 == 0:
        w1 = sess.run(w)
        b1 = sess.run(b)
        print(step, w1, b1)


def xx(acc, bpacc, bppp, pc, tth):
    global w1
    w2 = w1[0]
    print(w2,b1)
    pp = (acc-acc_m)/acc_s*(w2[0]) + (bpacc-bpacc_m)/(bpacc_s)*(w2[1]) + \
    (bppp-bppp_m)/bppp_s*(w2[2]) + (pc-pc_m)/pc_s*(w2[3]) + (tth-tth_m) \
    /tth_s*(w2[4]) + (b1[0])
    return pp*pp_s+pp_m

xx(93.79, 934.8300, 1139.0, 13222.0, 2012278.0)
xx(93.17, 943.7400, 1832.0, 12345.0, 3395347.0)
