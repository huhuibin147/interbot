import redis

def interRds(host='127.0.0.1', port=6379):
    return redis.Redis(host, port)
    