"""
Função utilitária para obter o cliente Redis.
"""

import redis

def get_redis():
    return redis.Redis(host='localhost', port=6379, decode_responses=True)
