# coding: utf-8

import requests
import logging
import json
import socket
import re
import traceback
from draws import drawRank
from api import rank_tab
from libs import osu_user
from libs import score
from comm import Config

class IRCBot(object):
    def __init__(self):
        self.irc_host = "irc.ppy.sh"
        self.irc_port = 6667
        self.irc_chan = "#announce"
        self.bot_name = "-interesting-"
        self.usr_name = "-interesting-"
        self.ral_name = "-interesting-"
        self.password = "f19cccc9"
        self.irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_sock.connect((self.irc_host, self.irc_port))

        self.irc_sock.send(("PASS " + self.password + "\r\n").encode())
        self.irc_sock.send(("NICK " + self.bot_name + "\r\n").encode())
        self.irc_sock.send(("USER " + self.bot_name + " " + self.bot_name + " " + self.bot_name + " :" + self.bot_name + "\r\n").encode())
        # self.irc_sock.send(("JOIN " + self.irc_chan + "\r\n").encode())


def get_data(data):
    get_url_rgex = r"https://osu.ppy.sh/./\d*"
    ptn = re.compile(get_url_rgex)

    url = re.search(ptn,data).group(0)

    content = data[len(url):]

    get_id_rgex = r"/\d*\s"
    ptn2 = re.compile(get_id_rgex)

    id = url = re.search(ptn2,data).group(0)[1:]
    return url,content,id

def start(cbot):
    get_url_rgex = r"(?<=\[).+(?=\])"
    ptn = re.compile(get_url_rgex)

    get_name_rgex = r"(?<=:).+(?=\!cho)"
    ptn2 = re.compile(get_name_rgex)

    bot = IRCBot()

    while True:
        try:
            data = bot.irc_sock.makefile(encoding='utf-8')
        except:
            bot.irc_sock.connect((bot.irc_host, bot.irc_port))
        for line in data:
            if line.startswith("PING"):
                print('***********IRC PRING***********')
                # cbot.send_private_msg(user_id=Config.SUPER_QQ, message='PING')
                bot.irc_sock.send(line.replace("PING", "PONG").encode('utf-8'))
                continue
            elif "QUIT" in line or "JOIN" in line or "PART" in line:
                continue
            elif "PRIVMSG #announce" in line:
                continue
                print(line.encode('utf-8').decode().split("PRIVMSG #announce :")[1])
                buzhidao = "藕酥动态！！！\n" + line.encode('utf-8').decode().split("PRIVMSG #announce :")[1]
            elif "ACTION is listening to" in line or "ACTION is watching" in line or "ACTION is playing" in line:
                mch = re.search(ptn,line.encode('utf-8').decode()).group(0)
                name = re.search(ptn2, line.encode('utf-8').decode()).group(0)
                url,content,bid = get_data(mch)

                # sid = (json.loads(requests.get("https://osu.ppy.sh/api/get_beatmaps?k=3ed2b75576b7ff7ca932d9e5d4fd880894ace722&b=" + bid).text))[0]["beatmapset_id"]
                # m = name + " np了一首 " + content + "\nMap: " + url
                n = name.strip()
                # osuname绑定群id
                gid = score.get_ircbind(n)
                if gid == -1:
                    # 向客户端反馈
                    continue 
                # upload rec
                try:
                    rank_tab.upload_rec(n, gid, limit=10)
                except:
                    traceback.print_exc()
                m,f = send2qq(bid, gid, n)
                if f == 1:
                    m =  m + '\nosu.ppy.sh/b/' + bid
                cbot.send_group_msg(group_id=gid, message=m)
            elif "PRIVMSG" in line:
                m = line.encode('utf-8').decode()
                print(m)
                cbot.send_private_msg(user_id=Config.SUPER_QQ, message=m)




def send2qq(bid, groupid, name, hid=1, mods=-1):
    o = osu_user.Osuer()
    ret = o.get_user_from_db2(name)
    uid = ret['osuid'] if ret else -1
    try:
        drawRank.start(bid, groupid, hid, mods, uid)
    except:
        traceback.print_exc()
        return '打了就是你的top\nosu.ppy.sh/b/%s'%bid,-1
    return '[CQ:image,file=file://%s\%s]' % (Config.IMAGE_PATH, 'rank.png'),1
