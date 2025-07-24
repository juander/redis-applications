from redis_client import get_redis

def main():
    r = get_redis()
    canal = input('Canal para publicar: ')
    usuario = input('Seu nome: ')
    print('Digite mensagens para enviar. Ctrl+C para sair.')
    try:
        while True:
            msg = input('Mensagem: ')
            if msg.strip():
                subscribers = r.publish(canal, f'{usuario}: {msg}')
                if isinstance(subscribers, int):
                    print(f'📤 Enviado para {subscribers} subscriber(s)')
                else:
                    print('📤 Mensagem enviada')
    except KeyboardInterrupt:
        print('\nSaindo do publisher.')

if __name__ == '__main__':
    main()
