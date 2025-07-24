import time

from redis_client import get_redis

def add_score(player, score, key='leaderboard_demo'):
    r = get_redis()
    r.zadd(key, {player: score})
    print(f"✅ Pontuação de {player}: {score} pontos")

def increment_score(player, increment=1.0, key='leaderboard_demo'):
    r = get_redis()
    new_score = r.zincrby(key, increment, player)
    if isinstance(new_score, (int, float)):
        print(f"✅ {player} ganhou {increment} pontos! Total: {new_score}")
        return new_score
    return 0

def get_top_players(limit=10, key='leaderboard_demo'):
    r = get_redis()
    result = r.zrevrange(key, 0, limit-1, withscores=True)
    return result if isinstance(result, list) else []

def get_player_rank(player, key='leaderboard_demo'):
    r = get_redis()
    rank = r.zrevrank(key, player)
    if rank is not None and isinstance(rank, int):
        score = r.zscore(key, player)
        return (rank+1, score)
    return (None, None)

def get_players_around(player, range_size=2, key='leaderboard_demo'):
    r = get_redis()
    rank = r.zrevrank(key, player)
    if rank is None or not isinstance(rank, int):
        return []
    start = max(0, rank-range_size)
    end = rank+range_size
    players = r.zrevrange(key, start, end, withscores=True)
    if isinstance(players, list):
        return [(start+i+1, p, score) for i, (p, score) in enumerate(players)]
    return []

def remove_player(player, key='leaderboard_demo'):
    r = get_redis()
    removed = r.zrem(key, player)
    return isinstance(removed, int) and removed > 0

def clear_leaderboard(key='leaderboard_demo'):
    r = get_redis()
    r.delete(key)
    print("🗑️ Leaderboard limpo!")

def display_leaderboard(title="🏆 LEADERBOARD", key='leaderboard_demo'):
    print(f"\n{title}")
    print("-"*30)
    players = get_top_players(10, key)
    if not players:
        print("(vazio)")
    for i, (player, score) in enumerate(players, 1):
        print(f"{i:2d}. {player:<20} {score:>8.0f} pts")

def run_leaderboard_demo():
    key = 'leaderboard_demo'
    while True:
        print("\n=== Leaderboard Demo ===")
        print("1. Adicionar/Atualizar pontuação")
        print("2. Incrementar pontuação de jogador") 
        print("3. Ver ranking completo")
        print("4. Ver posição de um jogador")
        print("5. Ver jogadores ao redor de alguém")
        print("6. Remover jogador")
        print("7. Limpar leaderboard")
        print("8. Simular jogo rápido")
        print("9. Sair")
        choice = input("Escolha: ").strip()

        if choice == "1":
            player = input("Nome do jogador: ").strip()
            try:
                score = float(input("Pontuação: "))
                add_score(player, score, key)
            except ValueError:
                print("❌ Pontuação inválida!")

        elif choice == "2":
            player = input("Nome do jogador: ").strip()
            if player:
                try:
                    increment = float(input("Incremento (padrão 1): ") or "1")
                    increment_score(player, increment, key)
                except ValueError:
                    print("❌ Incremento inválido!")

        elif choice == "3":
            display_leaderboard(key=key)

        elif choice == "4":
            player = input("Nome do jogador: ").strip()
            if player:
                rank, score = get_player_rank(player, key)
                if rank:
                    print(f"📊 {player}: {rank}º lugar com {score:.0f} pontos")
                else:
                    print(f"❌ Jogador '{player}' não encontrado")

        elif choice == "5":
            player = input("Nome do jogador de referência: ").strip()
            if player:
                try:
                    range_size = int(input("Quantos jogadores acima/abaixo (padrão 2): ") or "2")
                    players_around = get_players_around(player, range_size, key)
                    if players_around:
                        print(f"\n👥 Jogadores ao redor de {player}:")
                        print("-" * 40)
                        for pos, p, score in players_around:
                            marker = "👤" if p == player else "  "
                            print(f"{marker} {pos:2d}. {p:<20} {score:>8.0f} pts")
                    else:
                        print(f"❌ Jogador '{player}' não encontrado")
                except ValueError:
                    print("❌ Valor inválido!")

        elif choice == "6":
            player = input("Nome do jogador a remover: ").strip()
            if player:
                if remove_player(player, key):
                    print(f"✅ Jogador '{player}' removido do leaderboard")
                else:
                    print(f"❌ Jogador '{player}' não encontrado")

        elif choice == "7":
            confirm = input("Tem certeza que deseja limpar o leaderboard? (s/N): ").strip().lower()
            if confirm == 's':
                clear_leaderboard(key)

        elif choice == "8":
            print("\n🎮 Simulando um jogo rápido...")
            game_results = [
                ("Alice", 1250), ("Bob", 980), ("Charlie", 1100),
                ("Diana", 1350), ("Eve", 750), ("Frank", 1180)
            ]
            for player, score in game_results:
                add_score(player, score, key)
                time.sleep(0.1)
            print("✅ Jogo simulado! Veja o ranking:")
            display_leaderboard(key=key)

        elif choice == "9":
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    run_leaderboard_demo()