
from api import help_api
from api import test_api
from api import user_api
from libs import args_func

def invoke(b):
    if b.message == '!inter':
        return help_api.new_help()
    elif '!test' in b.message:
        uid = args_func.uid_find_or_input(b.message[6:], b.qq)
        if not uid:
            return '你不适合屙屎，删游戏吧(请绑定ID'
        return test_api.test(uid)
    elif '!myinfo' == b.message:
        return user_api.myinfo(b.qq)
    elif '!bbp' in b.message:
        uid = args_func.uid_find_or_input(b.message[5:], b.qq, return_type=1)
        if not uid:
            return '你有能看bp吗???(请绑定ID'
        return user_api.get_bp5info(uid)
    elif '!check' in b.message:
        uid = args_func.uid_find_or_input(b.message[7:], b.qq, return_type=1)
        if not uid:
            return '你太才菜了不想check你(请绑定ID'
        return user_api.check(uid)
    elif '!map' in b.message:
        uid = args_func.uid_find_or_input(b.message[5:], b.qq, return_type=1)
        if not uid:
            return '本bot根本不想给你推荐图QwQ(请绑定ID'
        return user_api.map(uid)
    elif '!helpme' == b.message:
        return 'inter已经去世，请求你群程序猿解救!!!'
    else:
        return 'not define'

