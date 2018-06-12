# -*- coding: utf-8 -*-
"""
Created on Tue May 22 20:28:42 2018

@author: hb
"""

import tensorflow as tf
import numpy as np
import random
from collections import deque

GAMMA = 0.9
INITIAL_EPSILON = 0.5
EPSILON_DECAY = 0.01
FINAL_EPSILON = 0.01
REPLAY_SIZE = 10000
BATCH_SIZE = 5

# 对话环境下控制频率
# 测试次数1
EPSILON = 1
STEP = 300
            

class DQN():
    def __init__(self):
        self.replay_buffer=deque()
        self.time_step=0
        self.epsilon=INITIAL_EPSILON
        self.state_dim=40
        self.action_dim=4
        
        self.create_Q_network()
        self.create_training_method()
        
        self.session=tf.InteractiveSession()
        self.session.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver()
        checkpoint = tf.train.get_checkpoint_state("cbot/model")
        if checkpoint and checkpoint.model_checkpoint_path:
            self.saver.restore(self.session, checkpoint.model_checkpoint_path)
            print('模型载入成功')
        else:
            print('模型不存在')
        
    
    def create_Q_network(self):
        w1 = self.weight_variable([self.state_dim,20])
        b1 = self.bias_variable([20])
        w2 = self.weight_variable([20,self.action_dim])
        b2 = self.bias_variable([self.action_dim])
        self.state_input=tf.placeholder("float",[None,self.state_dim])
        h_layer = tf.nn.relu(tf.matmul(self.state_input,w1)+b1)
        self.Q_value = tf.matmul(h_layer,w2)+b2
    
    def weight_variable(self,shape):
        return tf.Variable(tf.truncated_normal(shape))
    
    def bias_variable(self,shape):
        return tf.Variable(tf.constant(0.01, shape=shape))
    
    def preceive(self,state,action,reward,next_state,done):
        one_hot_action = np.zeros(self.action_dim)
        one_hot_action[action] = 1
        self.replay_buffer.append((state,one_hot_action,reward,next_state,done))
        if len(self.replay_buffer) > REPLAY_SIZE:
            self.replay_buffer.popleft()
        if len(self.replay_buffer) > BATCH_SIZE:
            self.train_Q_network()
    
    def create_training_method(self):
        self.action_input=tf.placeholder("float",[None,self.action_dim])
        self.y_input=tf.placeholder("float",[None])
        Q_action=tf.reduce_sum(tf.multiply(self.Q_value,self.action_input),reduction_indices=1)
        self.cost=tf.reduce_mean(tf.square(self.y_input-Q_action))
        self.optimizer=tf.train.AdamOptimizer(0.00001).minimize(self.cost)
        
    
    def train_Q_network(self):
        self.time_step += 1
        minibatch = random.sample(self.replay_buffer,BATCH_SIZE)
        state_batch = [data[0] for data in minibatch]
        action_batch = [data[1] for data in minibatch]
        reward_batch = [data[2] for data in minibatch]
        next_state_batch = [data[3] for data in minibatch]
        
        y_batch = []
        Q_value_batch=self.Q_value.eval(feed_dict={self.state_input:next_state_batch},session=self.session)
        for i in range(0, BATCH_SIZE):
            done = minibatch[i][4]
            if done:
                y_batch.append(reward_batch[i])
            else:
                y_batch.append(reward_batch[i]+GAMMA*np.max(Q_value_batch[i]))
                
        self.optimizer.run(feed_dict={
                self.y_input:y_batch,
                self.action_input:action_batch,
                self.state_input:state_batch
                },session=self.session)

    def egreedy_action(self,state):
        Q_value = self.Q_value.eval(feed_dict={self.state_input:[state]},session=self.session)[0]
        # 衰减
        if self.epsilon > FINAL_EPSILON:
            self.epsilon -= EPSILON_DECAY
        # 是否探索
        if random.random() <= self.epsilon:
            print('egreedy-随机探索')
            # return radom.randint(0,self.action_dim-1)
            return 'random'
        else:
            action = np.argmax(Q_value)
            print('egreedy-选择action:%s' % str(action))
            return action
        
    
    def action(self,state):
        Q_value = self.Q_value.eval(feed_dict={self.state_input:[state]},session=self.session)[0]
        return np.argmax(Q_value)
    
    def save(self):
        self.saver.save(self.session, 'cbot/model/net_dqn')


def main():
    env = Env()
    agent = DQN()
    

    for episode in range(EPSILON):
        state = env.reset()
        # train
        for step in range(STEP):
            action = agent.egreedy_action(state)
            next_state, reward, done = env.step(action)
            agent.preceive(state,action,reward,next_state,done)
            state = next_state
            if done:
                break
    
    

            