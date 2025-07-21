import redis
import time

class Leaderboard:
    def __init__(self, key='leaderboard_demo'):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.key = key

    def add_score(self, player, score):
        self.redis.zadd(self.key, {player: score})
        print(f"✅ Pontuação de {player}: {score} pontos")

    def increment_score(self, player, increment=1.0):
        new_score = self.redis.zincrby(self.key, increment, player)
        if isinstance(new_score, (int, float)):
            print(f"✅ {player} ganhou {increment} pontos! Total: {new_score}")
            return new_score
        return 0

    def get_top_players(self, limit=10):
        result = self.redis.zrevrange(self.key, 0, limit-1, withscores=True)
        return result if isinstance(result, list) else []

    def get_player_rank(self, player):
        rank = self.redis.zrevrank(self.key, player)
        if rank is not None and isinstance(rank, int):
            score = self.redis.zscore(self.key, player)
            return (rank+1, score)
        return (None, None)

    def get_players_around(self, player, range_size=2):
        rank = self.redis.zrevrank(self.key, player)
        if rank is None or not isinstance(rank, int):
            return []
        start = max(0, rank-range_size)
        end = rank+range_size
        players = self.redis.zrevrange(self.key, start, end, withscores=True)
        if isinstance(players, list):
            return [(start+i+1, p, score) for i, (p, score) in enumerate(players)]
        return []

    def remove_player(self, player):
        removed = self.redis.zrem(self.key, player)
        return isinstance(removed, int) and removed > 0

    def clear_leaderboard(self):
        self.redis.delete(self.key)
        print("🗑️ Leaderboard limpo!")

def display_leaderboard(leaderboard, title="🏆 LEADERBOARD"):
    print(f"\n{title}")
    print("-"*30)
    players = leaderboard.get_top_players(10)
    if not players:
        print("(vazio)")
    for i, (player, score) in enumerate(players, 1):
        print(f"{i:2d}. {player:<20} {score:>8.0f} pts")

def run_leaderboard_demo():
    leaderboard = Leaderboard()
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
                leaderboard.add_score(player, score)
            except ValueError:
                print("❌ Pontuação inválida!")

        elif choice == "2":
            player = input("Nome do jogador: ").strip()
            if player:
                try:
                    increment = float(input("Incremento (padrão 1): ") or "1")
                    leaderboard.increment_score(player, increment)
                except ValueError:
                    print("❌ Incremento inválido!")

        elif choice == "3":
            display_leaderboard(leaderboard)

        elif choice == "4":
            player = input("Nome do jogador: ").strip()
            if player:
                rank, score = leaderboard.get_player_rank(player)
                if rank:
                    print(f"📊 {player}: {rank}º lugar com {score:.0f} pontos")
                else:
                    print(f"❌ Jogador '{player}' não encontrado")

        elif choice == "5":
            player = input("Nome do jogador de referência: ").strip()
            if player:
                try:
                    range_size = int(input("Quantos jogadores acima/abaixo (padrão 2): ") or "2")
                    players_around = leaderboard.get_players_around(player, range_size)
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
                if leaderboard.remove_player(player):
                    print(f"✅ Jogador '{player}' removido do leaderboard")
                else:
                    print(f"❌ Jogador '{player}' não encontrado")

        elif choice == "7":
            confirm = input("Tem certeza que deseja limpar o leaderboard? (s/N): ").strip().lower()
            if confirm == 's':
                leaderboard.clear_leaderboard()

        elif choice == "8":
            print("\n🎮 Simulando um jogo rápido...")
            game_results = [
                ("Alice", 1250),
                ("Bob", 980),
                ("Charlie", 1100),
                ("Diana", 1350),
                ("Eve", 750),
                ("Frank", 1180),
                ("Grace", 920),
                ("Henry", 1050)
            ]
            for player, score in game_results:
                leaderboard.add_score(player, score)
                time.sleep(0.1)
            print("✅ Jogo simulado! Veja o ranking:")
            display_leaderboard(leaderboard)

        elif choice == "9":
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    run_leaderboard_demo()
