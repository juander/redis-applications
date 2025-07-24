import time

from redis_client import get_redis

def acquire_lock(r, lock_key, expire=15):
    return r.set(lock_key, 'locked', nx=True, ex=expire)

def release_lock(r, lock_key):
    r.delete(lock_key)

def run_concurrency_demo():
    r = get_redis()
    lock_key = 'demo_lock'
    
    while True:
        print('\n=== Controle de Concorrência Demo ===')
        print('1. Tentar adquirir lock')
        print('2. Liberar lock')
        print('3. Ver status do lock')
        print('4. Simular concorrência com timeout')
        print('5. Sair')
        op = input('Escolha: ')
        
        if op == '1':
            if acquire_lock(r, lock_key):
                print('✅ Lock adquirido com sucesso!')
                print('💡 O lock expira automaticamente em 15 segundos')
            else:
                print('❌ Lock já está em uso por outro processo.')
                
        elif op == '2':
            release_lock(r, lock_key)
            print('🔓 Lock liberado.')
            
        elif op == '3':
            if r.get(lock_key):
                ttl = r.ttl(lock_key)
                if isinstance(ttl, int) and ttl > 0:
                    print(f'🔒 Lock está em uso. Expira em {ttl} segundos.')
                else:
                    print('🔒 Lock está em uso (sem expiração).')
            else:
                print('🟢 Lock está livre.')
                
        elif op == '4':
            print('\n🎯 Simulando tentativas de adquirir lock...')
            for i in range(3):
                print(f'Tentativa {i+1}:', end=' ')
                if acquire_lock(r, lock_key, expire=2):
                    print('✅ Sucesso!')
                    time.sleep(1)
                    release_lock(r, lock_key)
                    print('🔓 Lock liberado')
                else:
                    print('❌ Falhou - lock em uso')
                time.sleep(0.5)
                
        elif op == '5':
            break
        else:
            print('❌ Opção inválida!')

if __name__ == '__main__':
    run_concurrency_demo()
