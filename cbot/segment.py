# -*- coding:utf-8 -*-
# 切词模块
import jieba
import logging


def run():

    stopwords = set()
    with open('cbot\stopwords.txt','r',encoding='utf-8') as sw:
        for line in sw:
            stopwords.add(line.strip('\n'))

    output = open('cbot\chat_seg.txt','w',encoding='utf-8')

    texts_num = 0

    with open('cbot\chat.txt','r',encoding='utf-8') as content:
        for line in content:
            words = jieba.cut(line, cut_all=False)
            for word in words:
                if word not in stopwords:
                    output.write(word+' ')
            texts_num+=1
            if texts_num % 50000 == 0:
                logging.info('已完成前 %s 行的断词' % texts_num)
    output.close()

# if __name__ == '__main__':
#     run()
