# -*- coding: utf-8 -*-

import re
import random
import traceback
import numpy as np
from cbot import DQN
from comm import Config
from comm import interRedis


key = 'mie_game_win'
key2 = 'mie_game_loss'

def recieve(b):
    try:
        # 启动cmd,权限
        if b.qq == Config.SUPER_QQ:
            if  '!playstart' == b.message:
                init(b, reward=0, autoandtimes=0, playstartflag=1, statelist=[], step=[])
                send(b, '!game_mie 1')

            elif b.message == '!playstop':
                stop(b)

            elif '!auto' in b.message:
                msglist = b.message.split(' ')
                if len(msglist) > 1:
                    autoandtimes = int(msglist[1])
                else:
                    autoandtimes = 1

                trainflag = 1
                if 'play' in b.message:
                    trainflag = 0

                level = 1
                if b.message[5:6] != ' ':
                    level = int(b.message[5:6])

                b.gV_Lock.acquire()
                b.globValue['trainflag'] = trainflag
                b.globValue['autoandtimes'] = autoandtimes
                b.globValue['level'] = level
                b.gV_Lock.release()

                init(b, reward=0, autoandtimes=autoandtimes, playstartflag=1, statelist=[], step=[])
                if trainflag:
                    send(b, '执行%s轮训练测试' % autoandtimes)
                else:
                    send(b, '执行%s轮真实游戏' % autoandtimes)

                send(b, '!game_mie %s' % level)


            elif '!m' in b.message:
                action_n = b.message.split(' ')[1]
                send(b, move(b, action_n))

            elif '!st' == b.message:
                send(b, str(b.globValue.get('statelist')))

            elif '!reward' == b.message:
                send(b, '目前奖赏分数:%s' % b.globValue.get('reward'))

            elif '!win' == b.message:
                rds = interRedis.interRds()
                win = rds.get(key)
                loss = rds.get(key2)
                send(b, 'win:%s\nloss:%s' % (int(win), int(loss)))


        elif b.qq == Config.DALOUBOT_QQ:
            if not b.globValue.get('playstartflag') or '输入错误!' in b.message \
                    or '操作成功' in b.message or '解除成功' in b.message:
                return
            if '[CQ:at,qq=%s]' % Config.LOGGING_QQ in b.message:
                stats = statefilter(b.message)
                b.gV_Lock.acquire()
                b.globValue['statelist'].append(stats)
                b.gV_Lock.release()

                agent = getAgent(b)

                if '胜利' in b.message:
                    if 'bot胜利' in b.message:
                        b.gV_Lock.acquire()
                        b.globValue['reward'] -= 800
                        reward = -800
                        done = 1
                        b.globValue['autoandtimes'] -= 1
                        b.gV_Lock.release()
                        winlosscache(iswin=0)
                    elif '玩家胜利' in b.message:
                        b.gV_Lock.acquire()
                        b.globValue['reward'] += 800
                        b.globValue['autoandtimes'] -= 1
                        reward = 800
                        done = 1
                        b.gV_Lock.release()
                        winlosscache(iswin=1)

                    send(b, '本次得分:%s' % b.globValue.get('reward'))
                    # agent.save()
                    # send(b, '模型已保存！')
                    
                    if b.globValue['autoandtimes']:
                        init(b, reward=0, autoandtimes=b.globValue['autoandtimes'], playstartflag=1, statelist=[], step=[])
                        send(b, '!game_mie %s' % b.globValue['level'])
                    else:
                        init(b, reward=0, autoandtimes=0, playstartflag=0, statelist=[], step=[])

                else:
                    b.gV_Lock.acquire()
                    b.globValue['reward'] += 1
                    reward = 1
                    done = 0
                    b.gV_Lock.release()

                    # 循环跳出-TODO
                    # if len(b.globValue['statelist']) > 50:
                    if checkLoop(b.globValue['statelist']) or len(b.globValue['statelist']) > 150:
                        send(b, '!stop_g')
                        send(b, '检测到死循环!')  
                        send(b, '本次得分:%s' % b.globValue.get('reward'))
                        if b.globValue['autoandtimes']:
                            init(b, reward=0, autoandtimes=b.globValue['autoandtimes'], playstartflag=1, statelist=[], step=[])
                            send(b, '!game_mie %s' % b.globValue['level'])
                            return
                        else:
                            init(b, reward=0, autoandtimes=0, playstartflag=0, statelist=[], step=[])
                            return
                    if b.globValue['autoandtimes']:
                        actcmd = egreedy(b, b.globValue['statelist'][-1])
                        send(b, actcmd)

                if len(b.globValue['step']) > 1:
                    action = int(b.globValue['step'][-1])
                    state = state2array(b.globValue['statelist'][-2])
                    next_state = state2array(b.globValue['statelist'][-1])
                    agent.preceive(state, action, reward, next_state, done)
    except:
        traceback.print_exc()
        stop(b)

def egreedy(b, state):
    agent = getAgent(b)
    if not b.globValue['trainflag']:
        action = agent.action(state2array(state))
        print('正式行动:%s' % action)
    else:
        action = agent.egreedy_action(state2array(state))
    if action == 'random':
        return randomAction(b)
    return move(b, action)

def getAgent(b):
    if not b.globValue.get('agent'):
        print('进行DQN实例化')
        agent = DQN.DQN()
        b.gV_Lock.acquire()
        b.globValue['agent'] = agent
        b.gV_Lock.release()
    else:
        agent = b.globValue.get('agent')
    return agent

def state2array(state):
    statarr = np.zeros([40])
    for i,s in enumerate(state):
        statarr[(i-1)*10+int(s)] = 1
    return statarr

def action2array(action):
    actionarr = np.zeros([4])
    actionarr[int(action)] = 1
    return actionarr


def init(b, **kw):
    b.gV_Lock.acquire()
    b.globValue['reward'] = kw.get('reward') if kw.get('reward') else 0
    b.globValue['autoandtimes'] = kw.get('autoandtimes') if kw.get('autoandtimes') else 0
    b.globValue['playstartflag'] = kw.get('playstartflag') if kw.get('playstartflag') else 0
    b.globValue['statelist'] = kw.get('statelist') if kw.get('statelist') else []
    b.globValue['step'] = kw.get('step') if kw.get('step') else []
    b.gV_Lock.release()
    agent = getAgent(b)
    agent.epsilon = 0.5

def randomAction(b):
    action = ['0','1','2','3']
    laststate = b.globValue['statelist'][-1]
    if laststate[0] == '0':
        if '0' in action:
            action.remove('0')
        if '2' in action:
            action.remove('2')
    if laststate[1] == '0':
        if '1' in action:
            action.remove('1')
        if '3' in action:
            action.remove('3')
    if laststate[2] == '0':
        if '0' in action:
            action.remove('0')
        if '1' in action:
            action.remove('1')
    if laststate[3] == '0':
        if '2' in action:
            action.remove('2')
        if '3' in action:
            action.remove('3')
    action_n = random.choice(action)
    return move(b, action_n)

def move(b, action_n):
    laststate = b.globValue['statelist'][-1]
    if not checkmove(laststate, action_n):
        print('行动选择错误,执行随机探索')
        return randomAction(b)
    actionlist = actionref(action_n, laststate)
    b.gV_Lock.acquire()
    b.globValue['step'].append(action_n)
    b.gV_Lock.release()
    return ' '.join(actionlist)

def statefilter(content):
    p = re.compile('\d+')
    r = p.findall(content)
    r = r[-4:]
    return r

def send(b, msg):
    b.bot.send_group_msg(group_id=b.group_id, message=msg)

def actionref(action_n, laststate):
    botleft = laststate[0]
    botright = laststate[1]
    myleft = laststate[2]
    myright = laststate[3]
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

def checkmove(state, action):
    action = int(action)
    if state[0] == '0':
        if 0 == action or 2 == action:
            return False
    if state[1] == '0':
        if 1 == action or 3 == action:
            return False
    if state[2] == '0':
        if 0 == action or 1 == action:
            return False
    if state[3] == '0':
        if 2 == action or 3 == action:
            return False
    return True

def stop(b):
    send(b, '!stop_g')
    send(b, '本次得分:%s' % b.globValue.get('reward'))
    init(b, reward=0, autoandtimes=0, playstartflag=0, statelist=[])


def winlosscache(iswin=1):
    rds = interRedis.interRds()
    if iswin:
        rds.incr(key, 1)
    else:
        rds.incr(key2, 1)


def checkLoop(ls):
    lst = ls[-1]
    diff = 0
    for i,n in enumerate(ls[-2::-1]):
        if lst == n:
            diff = i
            break
    clen = diff + 1
    if ls[-clen:] == ls[-2*clen:-1*clen] and ls[-2*clen:-1*clen] == ls[-3*clen:-2*clen]:
        return True
    return False