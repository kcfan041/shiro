import random

# 定义扑克牌
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CARDS = [rank + suit for suit in SUITS for rank in RANKS]

# 定义玩家类
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_card(self, deck):
        card = random.choice(deck)
        deck.remove(card)
        self.hand.append(card)

    def show_hand(self):
        print(f"{self.name}'s hand: {', '.join(self.hand)}")

# 初始化游戏
def start_game():
    players = []
    num_players = int(input("Enter the number of players: "))
    for i in range(num_players):
        name = input(f"Enter the name of player {i+1}: ")
        players.append(Player(name))

    deck = CARDS.copy()
    random.shuffle(deck)

    # 发牌
    for _ in range(2):
        for player in players:
            player.draw_card(deck)

    # 展示玩家手牌
    for player in players:
        player.show_hand()

    

# 运行游戏
start_game()
