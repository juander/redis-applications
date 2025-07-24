import redis

try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.ping()
    print('Conexão com Redis funcionando!')
    r.set('teste', '123')
    print('Valor salvo:', r.get('teste'))
    info = r.info()
    print('Versão do Redis:', info.get('redis_version', 'N/A') if isinstance(info, dict) else 'N/A')
except Exception as e:
    print('Erro ao conectar no Redis:', e)
