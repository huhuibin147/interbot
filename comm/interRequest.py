# -*- coding: utf-8 -*-
import requests
import json
import logging

class interReq():
    def __init__(self, url=None, params=None, timeout=5):
        self.headers = {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, br',
            'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection' : 'keep-alive',
            'Cookie' : '__cfduid=d0f839d6873527f32fe3b9dc8426362481508213944; XSRF-TOKEN=DMTtpVyEN1VvSFglE9tFYui1BkrkcuHMxh9bB1IH; osu_session=eyJpdiI6IktyNWxtVFJVNmwwcGdoS05FK21yYVE9PSIsInZhbHVlIjoiZ0t3Z0pzYUoxbXJcL1J6Mm10UmM0WG51c1Y0RTg3R0ZrNVRtcVJCSWV0bytwZjQ2OFwvaTI1MFI5Z2x5bkx3b0RrbWlyclV4U1wvQmtxQU5EY01VN2FcL0NnPT0iLCJtYWMiOiJlZWJhZTU0NzgzNzM4MGQxMmJlYTY0NjA2NTE0NDQyYmJkNzg1MDQyNWE3YjU0OTUyMGZmOGQwOGE5ZTM5YjQ0In0%3D; _ga=GA1.2.987670012.1508213952; __utma=226001156.987670012.1508213952.1508238423.1509076921.2; __utmz=226001156.1508238423.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); cf_clearance=ffcabb88813877be171e47f35a2c99cbb8c1146a-1509076917-31536000; __utmb=226001156.3.10.1509076921; _gid=GA1.2.38718716.1509076975',
            'Host'  :  'osu.ppy.sh',
            'Upgrade-Insecure-Requests' :  '1',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        } 
        self.url = url
        self.params = params
        self.timeout = timeout


    def post(self, url=None, params=None):
        url = url if url else self.url
        params = params if params else self.params
        res = requests.post(url=url, data=params, headers=self.headers, timeout=self.timeout)
        try:
            ret = json.loads(res.text)
        except:
            ret = res.text
        return ret

    def get(self, url=None):
        url = url if url else self.url
        res = requests.get(url=url, headers=self.headers, timeout=self.timeout)
        try:
            ret = json.loads(res.text)
        except:
            ret = res.text
        return ret

    def down_image(self, iname, url=None, path=None):
        url = url if url else self.url
        if not url:
            return 0
        ir = requests.get(url=url)
        path = path+iname+'.jpg' if path else 'static/image/osuimg/%s.png' % iname
        if ir.status_code == 200:
            with open(path, 'wb') as f:
                f.write(ir.content)
            return 1
        else:
            return 0


