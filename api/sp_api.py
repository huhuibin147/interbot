# -*- coding: utf-8 -*-
# osu!新人群月度精彩视频集锦



replay_bilibili = [
    {
        'title':'第1集2017.5',
        'url':'https://www.bilibili.com/video/av10959103/'
    },
    {
        'title':'第2集2017.6',
        'url':'https://www.bilibili.com/video/av11800563/'
    },
    {
        'title':'第3集2017.7',
        'url':'https://www.bilibili.com/video/av12957061/'
    },
    {
        'title':'第4集2017.8(第一季完结)',
        'url':'https://www.bilibili.com/video/av14046324/'
    }
]

def get_xinrenqun_replay():
    ship = replay_bilibili
    s_msg = 'osu!新人群月度精彩视频集锦\n'
    for sp in ship:
        s_msg = s_msg + sp['title'] + ' : ' + sp['url'] + '\n'
    return s_msg[0:-1]