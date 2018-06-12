# -*- coding: utf-8 -*-
import re
import random

def one_plus_one_check(list_g, content, diff):
    check_input = re.match(r'^[123456789] [123456789]$', content)
    msg2 = ''
    gg = 0
    if check_input:
        user_x = int(content[0])
        user_y = int(content[2])
        # print('输入:',user_x,user_y)
        if user_x != list_g[1][0] and user_x != list_g[1][1]:
            msg1 = '输入错误,你需要使用自己的其中一只手的数字而不是%s\nbot目前数字: %s %s\n玩家目前数字: %s %s' % (user_x,
                    list_g[0][0], list_g[0][1], list_g[1][0], list_g[1][1])
        elif user_y != list_g[0][0] and user_y != list_g[0][1]:
            msg1 = '输入错误,你需要指定bot的其中一只手的数字而不是%s\nbot目前数字: %s %s\n玩家目前数字: %s %s' % (user_y,
                    list_g[0][0], list_g[0][1], list_g[1][0], list_g[1][1])
        else:
            for i in range(0, 2):
                if user_x == list_g[1][i]:
                    for j in range(0, 2):
                        if user_y == list_g[0][j]:
                            list_g[1][i] = (list_g[1][i] + user_y) % 10
                            break
                    break
            msg1 = '操作成功!\nbot目前数字: %s %s\n玩家目前数字: %s %s' % (list_g[0][0], list_g[0][1], list_g[1][0], list_g[1][1])
            did = ai(list_g, 0, 0, diff)

            if list_g[0][did // 2] == 0 or list_g[1][did % 2] == 0:
                msg2 = '咩羊发现自己算错了,他放弃了!'
                gg = 2
            else:
                msg2 = 'bot经过一番计算，决定使用它的数字%s碰你的数字%s\n' % (list_g[0][did // 2], list_g[1][did % 2])
                list_g[0][did // 2] = (list_g[0][did // 2] + list_g[1][did % 2]) % 10
                msg2 = msg2 + 'bot目前数字: %s %s\n玩家目前数字: %s %s' % (list_g[0][0], list_g[0][1], list_g[1][0], list_g[1][1])
            if list_g[0][0] == 0 and list_g[0][1] == 0:
                msg2 = msg2 + '\nbot胜利!'
                gg = 1
            elif list_g[1][0] == 0 and list_g[1][1] == 0:
                msg2 = msg2 + '\n玩家胜利!'
                gg = 2
    else:
        msg1 = '输入错误!\n正确输入格式为:x y\n其中x是你的其中一只手的数字,y是bot其中一只手的数字,且均取值1~9之间\n' \
               'bot目前数字: %s %s\n玩家目前数字: %s %s' % (list_g[0][0], list_g[0][1], list_g[1][0], list_g[1][1])
    # print(msg1, msg2)
    return msg1, msg2, gg, list_g


def ai(finger, lvl, zero, diff):
    level = lvl
    level = level + 1
    if level == 1:
        for i in range(0, 2):
            for j in range(0, 2):
                if finger[i][j] == 0:
                    zero = zero + 1
    zero_ = 0  # 每次都判断的0的数量
    for i in range(0, 2):
        for j in range(0, 2):
            if finger[i][j] == 0:
                zero_ = zero_ + 1
    if zero_ == 2 and lvl:  # 最终结局计算
        fig1 = finger[0][0] + finger[0][1]
        fig2 = finger[1][0] + finger[1][1]
        score = ender(fig1, fig2)
        if level % 2 == 0:
            if score == 0:
                score = 90
            return score
        else:
            if score == 0:
                score = -90
            return score
    score_list = [[-200, -200], [-200, -200]]  # 0左1右，AI在前
    if zero == 1:
        level_max = diff * 2
    else:
        level_max = diff
    if level < level_max:
        if finger[0][0] == finger[0][1]:
            i_max = 1
        else:
            i_max = 2
        if finger[1][0] == finger[1][1]:
            j_max = 1
        else:
            j_max = 2
        for i in range(0, i_max):
            if finger[0][i]:
                for j in range(0, j_max):
                    if finger[1][j]:
                        ai_new = [[finger[0][0], finger[0][1]], [finger[1][0], finger[1][1]]]
                        ai_new[0][i] = (ai_new[0][i] + finger[1][j]) % 10
                        score_list[i][j] = estimation(ai_new, level)
                        if score_list[i][j] == 100:
                            if level > 1:
                                return 100
                            else:
                                return 2 * i + j
                        else:
                            for k in range(0, 2):
                                temp = ai_new[0][k]
                                ai_new[0][k] = ai_new[1][k]
                                ai_new[1][k] = temp
                            score_list[i][j] = -ai(ai_new, level, zero, diff)
                            if score_list[i][j] == 100:
                                if level > 1:
                                    return 100
                                else:
                                    return 2 * i + j
    else:
        return estimation(finger)
    trap = 0  # 陷阱加分
    if lvl % 2 == 1:
        for i in range(0, 2):
            for j in range(0, 2):
                if finger[0][i] * finger[1][j] > 0 and finger[0][i] + finger[1][j] == 10:
                    trap = trap - 1
    max_score = score_list[0][0]
    for i in range(0, 2):
        for j in range(0, 2):
            if score_list[i][j] > max_score:
                max_score = score_list[i][j]
    if level > 1:
        return max_score + trap
    able = [[0, 0], [0, 0]]
    for i in range(0, 2):
        for j in range(0, 2):
            if score_list[i][j] == max_score:
                able[i][j] = 1
    things_can_be_done = 0
    for i in range(0, 2):
        for j in range(0, 2):
            things_can_be_done = things_can_be_done + able[i][j]
    will_do = yran(things_can_be_done)
    for i in range(0, 2):
        for j in range(0, 2):
            if able[i][j]:
                if will_do == 0:
                    return 2 * i + j
                else:
                    will_do = will_do - 1


def estimation(fig, level=0):
    a = 0
    b = 0
    if level != 0:
        if level % 2 == 1:
            a = 1
        else:
            b = 1
    score = 0
    for i in range(0, 2):
        if fig[0][i] == 0:
            score = score + 30 + b * 5
        if fig[1][i] == 0:
            score = score - 30 - a * 5
    if fig[0][0] == fig[0][1]:
        score = score - 10
    if fig[1][0] == fig[1][1]:
        score = score + 10
    if fig[0][0] == 0 and fig[0][1] == 0:
        score = 100
    if fig[1][0] == 0 and fig[1][1] == 0:
        score = -100
    if (fig[0][0] + fig[0][1] + fig[1][0] + fig[1][1]) == 0:
        score = 0
    return score


def ender(figin1, figin2):
    fig = [figin1, figin2]
    for i in range(0, 3):
        if fig[0] != 0 and fig[1] != 0:
            fig[0] = (fig[0] + fig[1]) % 10
            fig[1] = (fig[1] + fig[0]) % 10
    draw = [fig[0], fig[1]]
    while fig[0] and fig[1]:
        fig[0] = (fig[0] + fig[1]) % 10
        fig[1] = (fig[1] + fig[0]) % 10
        if draw[0] == fig[0] and draw[1] == fig[1]:
            break
    if fig[0] == 0:
        return 100
    elif fig[1] == 0:
        return -100
    else:
        return 0


def yran(a):
    return random.randint(0, a-1)






import tensorflow as tf
import numpy as np
import random
from collections import deque

GAMMA = 0.9
INITIAL_EPSILON = 0.5
EPSILON_DECAY = 0.00001
FINAL_EPSILON = 0.01
REPLAY_SIZE = 10000
BATCH_SIZE = 32



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
        checkpoint = tf.train.get_checkpoint_state("model")
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
            # print('egreedy-随机探索')
            return random.randint(0,self.action_dim-1)
            # return 'random'
        else:
            action = np.argmax(Q_value)
            # print('egreedy-选择action:%s' % str(action))
            return action
        
    
    def action(self,state):
        Q_value = self.Q_value.eval(feed_dict={self.state_input:[state]},session=self.session)[0]
        return np.argmax(Q_value)
    
    def save(self):
        self.saver.save(self.session, 'model/net_dqn')
        # print('模型自动保存')
        


class Env():

    def __init__(self, level=4):
        self.statels = [[[1, 1], [1, 1]]]
        self.level = level

    def step(self, state, inputs, level):
        """
        state当前数字[[x1,x2],[x3,x4]]
        input 1 1 执行数字
        """
        inputstr = '%s %s' % (inputs[0], inputs[1])
        _, _, gg, next_state = one_plus_one_check(state, inputstr, level)
        done = 1
        if gg == 0:
            done = 0
            reward = 1
        elif gg == 1:
            reward = -800
        elif gg == 2:
            reward = 800
        self.statels.append(next_state)
        return next_state, reward, done, gg

    def reset(self):
        self.statels = [[[1, 1], [1, 1]]]
        return [[1, 1], [1, 1]]
            
    def actionref(self, action_n, state):
        """
        动作(0/1/2/3)映射指定操作数字
        """
        botleft = state[0][0]
        botright = state[0][1]
        myleft = state[1][0]
        myright = state[1][1]
        action_n = int(action_n)
        if action_n == 0:
            ret = [myleft, botleft]
        elif action_n == 1:
            ret = [myleft, botright]
        elif action_n == 2:
            ret = [myright, botleft]
        elif action_n == 3:
            ret = [myright, botright]
        return ret

    def checkmove_and_choice(self, state, action):
        action = int(action)
        randflag = 0
        if state[0][0] == 0:
            if 0 == action or 2 == action:
                randflag = 1
        if state[0][1] == 0:
            if 1 == action or 3 == action:
                randflag = 1
        if state[1][0] == 0:
            if 0 == action or 1 == action:
                randflag = 1
        if state[1][1] == 0:
            if 2 == action or 3 == action:
                randflag = 1
        if randflag:
            action = self.randomAction(state)
        return action

    def randomAction(self, state):
        action = [0,1,2,3]
        if state[0][0] == 0:
            if 0 in action:
                action.remove(0)
            if 2 in action:
                action.remove(2)
        if state[0][1] == 0:
            if 1 in action:
                action.remove(1)
            if 3 in action:
                action.remove(3)
        if state[1][0] == 0:
            if 0 in action:
                action.remove(0)
            if 1 in action:
                action.remove(1)
        if state[1][1] == 0:
            if 2 in action:
                action.remove(2)
            if 3 in action:
                action.remove(3)
        action_n = random.choice(action)
        return action_n

    def checkLoop(self, ls):
        ls = [[r[0][0],r[0][1],r[1][0],r[1][1]] for r in ls]
        lst = ls[-1]
        diff = 0
        for i,n in enumerate(ls[-2::-1]):
            if lst == n:
                diff = i
                break
        clen = diff + 1
        if ls[-clen:] == ls[-2*clen:-1*clen] and ls[-2*clen:-1*clen] == ls[-3*clen:-2*clen]:
            print('检测到死循环')
            return True
        return False

    def state2array(self, state):
        statarr = np.zeros([40])
        state = state[0]+state[1]
        for i,s in enumerate(state):
            statarr[(i-1)*10+int(s)] = 1
        return statarr


import sys

EPSILON = 1000000
STEP = 200
            

def main(play):
    env = Env()
    agent = DQN()
    
    if play == '1':
        print('[%s]play mode' % play)
    else:
        print('[%s]train mode' % play)
    win = 0
    lose = 0
    for episode in range(EPSILON):
        print('EPSILON',episode)
        state = env.reset()
        if agent.epsilon % 10000 == 0:
            pirnt('自动重置epsilon')
            agent.epsilon = INITIAL_EPSILON
        # train
        for s in range(STEP):
            if play == '1':
                action = agent.action(env.state2array(state))
            else:
                action = agent.egreedy_action(env.state2array(state))
            action = env.checkmove_and_choice(state, action)
            next_state, reward, done, gg = env.step(state, env.actionref(action, state), env.level)
            agent.preceive(env.state2array(state), action, reward, env.state2array(next_state), done)
            state = next_state

            if done:
                if gg == 1:
                    lose += 1
                elif gg == 2:
                    win += 1
                agent.save()
                break
        if (episode+1) % 10 == 0:
            print('[%s]轮情况,执行次数[%s],胜[%s],负[%s]' % (episode, EPSILON, win, lose))


if __name__ == '__main__':
    # gg 1-lose  2-win
    print('start..')
    # game_content = [[1, 1], [1, 1]]
    # content = '1 1'
    # diff = 2
    # m1,m2,gg,list_g = one_plus_one_check(game_content, content, diff)
    # print('gg',gg)
    # print('num',list_g)
    main(sys.argv[1])


