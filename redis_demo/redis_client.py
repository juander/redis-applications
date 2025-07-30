import redis

POOL = redis.ConnectionPool(host='redis-demo', port=6379, decode_responses=True)

def get_redis():
    return redis.Redis(connection_pool=POOL)