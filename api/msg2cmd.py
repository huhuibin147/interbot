
from api import help_api
from api import test_api

def invoke(b):
    if b.message == '!inter':
        return help_api.new_help()
    elif '!test' in b.message:
        uid = b.message[6:]
        if not uid:
            return test_api.new_test()
        return test_api.test(uid)
    else:
        return 'not define'

