
## Redis Demo Prático

Este projeto demonstra 3 funcionalidades do Redis de forma simples e direta:

1. **Leaderboard** (Ranking em tempo real)
2. **Chat em tempo real** (Pub/Sub)
3. **Controle de concorrência** (Locks)

---

### Pré-requisitos

- Docker instalado (para rodar o Redis rapidamente)
- Python 3.7+
- Instalar dependências:
  ```bash
  pip install redis
  ```

---

### Subindo o Redis com Docker

```bash
docker-compose up -d
```

---

## Como executar e testar cada funcionalidade

### 1. Leaderboard (Ranking em tempo real)

**Como executar:**
```bash
python redis_demo/leaderboard.py
```

**Como testar:**
1. Escolha a opção 1 para adicionar/atualizar a pontuação de um jogador.
2. Digite o nome e a pontuação.
3. Escolha a opção 2 para ver o ranking atualizado em tempo real.
4. Repita para vários jogadores e veja o ranking mudar.

---

### 2. Chat em tempo real (Pub/Sub)

**Como executar o subscriber (quem recebe mensagens):**
```bash
python redis_demo/chat/subscriber.py
```
Digite o nome do canal (ex: chat1) e aguarde mensagens.

**Como executar o publisher (quem envia mensagens):**
Abra outro terminal e rode:
```bash
python redis_demo/chat/publisher.py
```
Digite o mesmo nome de canal e envie mensagens. Elas aparecerão instantaneamente nos subscribers conectados ao mesmo canal.

**Como testar:**
1. Abra 2 ou mais terminais rodando o subscriber no mesmo canal.
2. Em outro terminal, rode o publisher e envie mensagens.
3. Veja as mensagens chegando em tempo real nos subscribers.

---

### 3. Controle de concorrência (Locks)

**Como executar:**
```bash
python redis_demo/lock_control.py
```

**Como testar:**
1. Escolha a opção 1 para tentar adquirir o lock (simula acesso exclusivo a um recurso).
2. Em outro terminal, rode o mesmo script e tente adquirir o lock novamente (deve mostrar que está em uso).
3. Libere o lock com a opção 2 e tente novamente.
4. Use a opção 3 para ver o status do lock.

---

## Observações

- Todos os scripts são independentes e podem ser executados separadamente.
- O Redis deve estar rodando localmente na porta padrão (6379).

---

## Aplicações Reais no Mundo

### 🏆 Leaderboard (Sorted Sets)
**Onde é usado (casos reais):**
- **Twitter:** Trending topics em tempo real
- **GitHub:** Repositórios mais populares/starred
- **Stack Overflow:** Ranking de usuários por reputação
- **LinkedIn:** Feed de posts mais engajados
- **Spotify:** Top músicas e artistas

**Por que é essencial:** Precisa ser extremamente rápido para milhões de usuários simultâneos. Bancos de dados tradicionais são lentos para ordenação em tempo real.

### 💬 Pub/Sub (Chat em Tempo Real)
**Onde é usado (casos reais confirmados):**
- **Instagram:** Stories, notificações de curtidas
- **Uber/99:** Localização de motoristas em tempo real
- **Netflix:** Notificações de novos episódios
- **Microsoft Teams:** Chat e presença online
- **Binance:** Atualizações de preços de criptomoedas

**Por que é essencial:** Latência ultra-baixa é crítica. Delay de segundos em chat ou alertas é inaceitável.

### 🔒 Locks Distribuídos
**Onde é usado (casos reais):**
- **PayPal/Stripe:** Evitar cobrança dupla em pagamentos
- **Booking.com:** Reservas simultâneas do mesmo quarto
- **Amazon:** Carrinho de compras e checkout
- **Banco do Brasil/Itaú:** Transferências bancárias
- **Mercado Livre:** Leilões e ofertas relâmpago

**Por que é essencial:** Erros de concorrência causam perda de dinheiro, fraudes e problemas legais graves.

### 🌐 Sistemas Distribuídos (Uso Geral)
**Redis como infraestrutura crítica:**
- **Cache distribuído:** Amazon, Google, Facebook usam Redis para cache de sessões
- **Message Broker:** Substitui RabbitMQ em muitos casos (Airbnb, Pinterest)
- **Session Store:** Compartilhar sessões entre servidores (Netflix, Spotify)
- **Rate Limiting:** Controle de API requests (GitHub, Twitter API)
- **Real-time Analytics:** Contadores em tempo real (Reddit, Medium)
