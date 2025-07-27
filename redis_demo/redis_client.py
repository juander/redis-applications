import redis

def get_redis():
    return redis.Redis(host='redis-demo', port=6379, decode_responses=True)
