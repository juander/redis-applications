"""
Sistema de demonstração das funcionalidades avançadas do Redis.
Menu principal que permite acessar os diferentes módulos demonstrativos.

"""

import sys
import os

try:
    from redis_client import get_redis
    from leaderboard import run_leaderboard_demo
    from lock_control import run_concurrency_demo
    import subprocess
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Certifique-se de que todos os arquivos estão no diretório correto")
    sys.exit(1)


def show_banner():
    """Exibe o banner de boas-vindas."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🚀 REDIS DEMO AVANÇADO                    ║
║                                                              ║
║  Demonstração de funcionalidades poderosas do Redis além     ║
║  do uso tradicional de cache                                 ║
║                                                              ║
║  📊 Leaderboard - Rankings em tempo real (Sorted Sets)       ║
║  💬 Chat - Mensagens em tempo real (Pub/Sub)                 ║
║  🔒 Locks - Controle de concorrência (SET NX EX)             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_redis_connection() -> bool:
    """
    Verifica se a conexão com Redis está funcionando.
    
    Returns:
        True se conectado, False caso contrário
    """
    try:
        r = get_redis()
        r.ping()
        return True
    except Exception as e:
        print(f"Erro ao verificar conexão: {e}")
        return False


def show_redis_info():
    """Exibe informações sobre o Redis conectado."""
    try:
        redis = get_redis()
        info = redis.info()
        
        print("\n📊 INFORMAÇÕES DO REDIS:")
        print("="*50)
        if isinstance(info, dict):
            print(f"Versão: {info.get('redis_version', 'N/A')}")
            print(f"Modo: {info.get('redis_mode', 'standalone')}")
            print(f"Uptime: {info.get('uptime_in_seconds', 0)} segundos")
            print(f"Clientes conectados: {info.get('connected_clients', 0)}")
            print(f"Memória usada: {info.get('used_memory_human', 'N/A')}")
            print(f"Comandos processados: {info.get('total_commands_processed', 0):,}")
            print(f"Banco de dados atual: {redis.connection_pool.connection_kwargs.get('db', 0)}")
            
            # Mostra estatísticas de chaves
            db_info = info.get('db0', {})
            if db_info:
                keys = db_info.get('keys', 0)
                expires = db_info.get('expires', 0)
                print(f"Chaves no DB: {keys} (com TTL: {expires})")
            else:
                print("Chaves no DB: 0")
        else:
            print("Informações não disponíveis")
        print("="*50)
        
    except Exception as e:
        print(f"Erro ao obter informações: {e}")


def run_chat_publisher():
    """Executa o publisher do chat em um processo separado."""
    try:
        chat_path = os.path.join(os.path.dirname(__file__),  "publisher.py")
        
        print("🚀 Iniciando Chat Publisher...")
        print("💡 Dica: Execute este comando em outro terminal para o Subscriber:")
        print(f"   python {os.path.join(os.path.dirname(__file__), 'chat', 'subscriber.py')}")
        print("-" * 60)
        
        # Executa o publisher
        subprocess.run([sys.executable, chat_path])
        
    except FileNotFoundError:
        print("Arquivo publisher.py não encontrado")
    except Exception as e:
        print(f"Erro ao executar publisher: {e}")


def run_chat_subscriber():
    """Executa o subscriber do chat em um processo separado."""
    try:
        chat_path = os.path.join(os.path.dirname(__file__), "subscriber.py")
        
        print("🚀 Iniciando Chat Subscriber...")
        print("💡 Dica: Execute este comando em outro terminal para o Publisher:")
        print(f"   python {os.path.join(os.path.dirname(__file__), 'chat', 'publisher.py')}")
        print("-" * 60)
        
        # Executa o subscriber
        subprocess.run([sys.executable, chat_path])
        
    except FileNotFoundError:
        print("Arquivo subscriber.py não encontrado")
    except Exception as e:
        print(f"Erro ao executar subscriber: {e}")


def show_help():
    """Exibe ajuda sobre o sistema."""
    help_text = """
📖 AJUDA - Redis Demo Avançado

🏆 LEADERBOARD (Sorted Sets):
   • Rankings em tempo real com pontuações
   • Adicionar/atualizar scores de jogadores
   • Buscar posição e pontuação de jogadores específicos
   • Ver top jogadores e rankings ao redor de um jogador
   • Demonstra operações: ZADD, ZREVRANGE, ZRANK, ZSCORE

💬 CHAT (Pub/Sub):
   • Sistema de mensagens em tempo real
   • Publisher: envia mensagens para canais
   • Subscriber: recebe mensagens instantaneamente
   • Suporte a múltiplos canais simultâneos
   • Demonstra operações: PUBLISH, SUBSCRIBE, PUBSUB

🔒 CONTROLE DE CONCORRÊNCIA (Locks):
   • Locks distribuídos para operações críticas
   • Previne condições de corrida em aplicações distribuídas
   • Demos de transferências bancárias e controle de estoque
   • Timeout automático e liberação segura
   • Demonstra operações: SET NX EX, Scripts Lua

💾 PRÉ-REQUISITOS:
   • Redis Server rodando em localhost:6379
   • Python 3.7+ com biblioteca redis-py
   • Para instalar: pip install redis

🚀 COMO USAR:
   1. Certifique-se que o Redis está rodando
   2. Execute: python main.py
   3. Escolha a funcionalidade no menu
   4. Para chat, abra múltiplos terminais

📁 ESTRUTURA DOS ARQUIVOS:
   main.py           - Menu principal (este arquivo)
   redis_client.py   - Cliente Redis compartilhado
   leaderboard.py    - Sistema de ranking
   chat/publisher.py - Envia mensagens de chat
   chat/subscriber.py- Recebe mensagens de chat
   lock_control.py   - Controle de concorrência
    """
    print(help_text)


def clean_redis_demo_data():
    """Limpa dados de demonstração do Redis."""
    try:
        redis = get_redis()
        
        patterns = [
            "demo_leaderboard",
            "game_leaderboard", 
            "account:*",
            "inventory:*",
            "lock:*"
        ]
        
        total_deleted = 0
        for pattern in patterns:
            keys = redis.keys(pattern)
            if keys and isinstance(keys, list):
                deleted = redis.delete(*keys)
                if isinstance(deleted, int):
                    total_deleted += deleted
                    print(f"🗑️ Removidas {deleted} chaves do padrão: {pattern}")
                else:
                    print(f"🗑️ Removidas chaves do padrão: {pattern}")
        
        if total_deleted > 0:
            print(f"✅ Total de {total_deleted} chaves removidas")
        else:
            print("ℹ️ Nenhuma chave de demo encontrada")
            
    except Exception as e:
        print(f"Erro ao limpar dados: {e}")


def main():
    """Função principal do programa."""
    show_banner()
    
    # Verifica conexão com Redis
    if not check_redis_connection():
        print("\n💡 SOLUÇÕES:")
        print("  • Verifique se o Redis está instalado")
        print("  • Inicie o Redis Server:")
        print("    - Windows: redis-server.exe")
        print("    - Linux/Mac: redis-server")
        print("    - Docker: docker run -p 6379:6379 redis")
        print("  • Verifique se a porta 6379 está disponível")
        
        input("\nPressione Enter para tentar novamente ou Ctrl+C para sair...")
        return main()  # Tenta novamente
    
    while True:
        print("\n" + "="*60)
        print("🎯 MENU PRINCIPAL - ESCOLHA UMA DEMONSTRAÇÃO:")
        print("="*60)
        print("1. 🏆 Leaderboard - Rankings em tempo real (Sorted Sets)")
        print("2. 💬 Chat Publisher - Enviar mensagens (Pub/Sub)")
        print("3. 👂 Chat Subscriber - Receber mensagens (Pub/Sub)")
        print("4. 🔒 Controle de Concorrência - Locks distribuídos")
        print()
        print("📊 INFORMAÇÕES:")
        print("5. 📈 Ver informações do Redis")
        print("6. 🗑️ Limpar dados de demonstração")
        print("7. 📖 Ajuda e documentação")
        print()
        print("9. 🚪 Sair")
        print("="*60)
        
        try:
            choice = input("\n🎮 Digite sua escolha (1-9): ").strip()
            
            if choice == "1":
                print("\n🏆 Iniciando demo do Leaderboard...")
                run_leaderboard_demo()
                
            elif choice == "2":
                print("\n💬 Iniciando Chat Publisher...")
                run_chat_publisher()
                
            elif choice == "3":
                print("\n👂 Iniciando Chat Subscriber...")
                run_chat_subscriber()
                
            elif choice == "4":
                print("\n🔒 Iniciando demo de Controle de Concorrência...")
                run_concurrency_demo()
                
            elif choice == "5":
                show_redis_info()
                
            elif choice == "6":
                confirm = input("\n⚠️ Tem certeza que deseja limpar os dados de demo? (s/N): ").strip().lower()
                if confirm == 's':
                    clean_redis_demo_data()
                    
            elif choice == "7":
                show_help()
                
            elif choice == "9":
                print("\n👋 Obrigado por usar o Redis Demo!")
                print("🚀 Continue explorando o poder do Redis!")
                break
                
            else:
                print("❌ Opção inválida! Digite um número de 1 a 9.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo encerrado pelo usuário")
            break
        except Exception as e:
            print(f"\nErro inesperado: {e}")
            print("Retornando ao menu principal...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Programa encerrado")
    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)
