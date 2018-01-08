
from api import help_api

def invoke(b):
    if b.message == '!inter':
        return help_api.new_help()
    else:
        return 'not define'

