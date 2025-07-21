import redis

def main():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    canal = input('Canal para assinar: ')
    pubsub = r.pubsub()
    pubsub.subscribe(canal)
    print(f'👂 Aguardando mensagens no canal "{canal}"... Ctrl+C para sair.')
    try:
        while True:
            msg = pubsub.get_message(timeout=1.0)
            if msg and isinstance(msg, dict) and msg.get('type') == 'message':
                data = msg.get('data')
                if data:
                    print(f'📨 {data}')
    except KeyboardInterrupt:
        print('\nSaindo do subscriber.')
    finally:
        pubsub.close()

if __name__ == '__main__':
    main()
