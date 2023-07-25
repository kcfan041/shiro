import random

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CARDS = [rank + suit for suit in SUITS for rank in RANKS]

ROYAL_FLUSH_WEIGHT = 10
STRAIGHT_FLUSH_WEIGHT = 9
FOUR_OF_A_KIND_WEIGHT = 8
FULL_HOUSE_WEIGHT = 7
FLUSH_WEIGHT = 6
STRAIGHT_WEIGHT = 5
THREE_OF_A_KIND_WEIGHT = 4
TWO_PAIRS_WEIGHT = 3
ONE_PAIR_WEIGHT = 2
HIGH_CARD_WEIGHT = 1

class Player:
    def __init__(self, name, chips):
        self.name = name
        self.hand = []
        self.chips = chips

    def draw_card(self, deck):
        card = random.choice(deck)
        deck.remove(card)
        self.hand.append(card)

    def show_hand(self):
        print(f"{self.name}'s hand: {', '.join(self.hand)}")

    def bet(self, current_bet):
        while True:
            try:
                bet_amount = int(input(f"{self.name}, your current chips: {self.chips}. Enter your bet amount (minimum bet is {current_bet}), or enter 0 to fold: "))
                if bet_amount == 0:
                    print(f"{self.name} folds.")
                    return 0
                elif bet_amount >= current_bet and bet_amount <= self.chips:
                    self.chips -= bet_amount
                    return bet_amount
                else:
                    print("Invalid bet! Try again.")
            except ValueError:
                print("Invalid input! Try again.")

def get_hand_weight(hand):
    rank_values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    hand_values = sorted([rank_values[card[:-1]] for card in hand], reverse=True)
    frequencies = {card: hand_values.count(card) for card in hand_values}

    is_flush = all(card[-1] == hand[0][-1] for card in hand)
    is_straight = len(set(hand_values)) == 5 and (hand_values[0] - hand_values[4] == 4)

    if is_flush and is_straight:
        return ROYAL_FLUSH_WEIGHT if hand_values[0] == 14 else STRAIGHT_FLUSH_WEIGHT
    elif 4 in frequencies.values():
        return FOUR_OF_A_KIND_WEIGHT
    elif 3 in frequencies.values() and 2 in frequencies.values():
        return FULL_HOUSE_WEIGHT
    elif is_flush:
        return FLUSH_WEIGHT
    elif is_straight:
        return STRAIGHT_WEIGHT
    elif 3 in frequencies.values():
        return THREE_OF_A_KIND_WEIGHT
    elif list(frequencies.values()).count(2) == 2:
        return TWO_PAIRS_WEIGHT
    elif 2 in frequencies.values():
        return ONE_PAIR_WEIGHT
    else:
        return HIGH_CARD_WEIGHT

def compare_hands(players_hands, community_cards):
    max_weight = 0
    winners = []

    for player_hand in players_hands:
        total_hand = player_hand + community_cards
        player_weight = get_hand_weight(total_hand)

        if player_weight > max_weight:
            max_weight = player_weight
            winners = [player_hand]
        elif player_weight == max_weight:
            winners.append(player_hand)

    if len(winners) == 1:
        return f"{winners[0]} wins"
    else:
        winner_names = [player.name for player in winners]
        return "Tie between " + ", ".join(winner_names)

def bet_count(players,num_players):
    current_bet = 10  # 起始下注額度
    num_active_players = len([player for player in players if player.chips > 0])
    if num_active_players <= 1:
        # 如果只剩一位玩家參與，那麼這位玩家就是贏家
        for player in players:
            if player.chips > 0:
                print(f"{player.name} wins the pot with {player.chips * num_players} chips!")
                return
    # 進行下注
    for player in players:
        if player.chips > 0:
            player.show_hand()
            bet_amount = player.bet(current_bet)
            if bet_amount == 0:
                num_active_players -= 1
            if bet_amount > current_bet:
                current_bet = bet_amount
    # 檢查是否還有玩家參與比牌
    if num_active_players <= 1:
        # 如果只剩一位玩家參與，那麼這位玩家就是贏家
        for player in players:
            if player.chips > 0:
                print(f"{player.name} wins the pot with {player.chips * num_players} chips!")
                return
def start_game():
    players = []
    num_players = int(input("Enter the number of players: "))
    for i in range(num_players):
        name = input(f"Enter the name of player {i+1}: ")
        chips = int(input(f"Enter the number of chips for player {i+1}: "))
        players.append(Player(name, chips))

    deck = CARDS.copy()
    random.shuffle(deck)

    # 發牌
    for _ in range(2):
        for player in players:
            player.draw_card(deck)

    # 下注
    current_bet = 10  # 起始下注額度
    num_active_players = len(players)  # 記錄剩餘參與比牌的玩家數量
    bet_count(players,num_players)

    # 翻牌
    flop = []
    for _ in range(3):
        card = deck.pop()
        flop.append(card)
    print(f"Flop: {' '.join(flop)}")

    # 下注
    bet_count(players,num_players)

    # 轉牌
    turn = deck.pop()
    print(f"Turn: {turn}")

    # 下注
    bet_count(players,num_players)

    # 河牌
    river = deck.pop()
    print(f"River: {river}")

    # 下注
    bet_count(players,num_players)

    # 展示玩家手牌
    for player in players:
        player.show_hand()

    # 比牌
    players_hands = [player.hand for player in players]
    if num_active_players > 1:
        winner = compare_hands(players_hands, flop + [turn] + [river])
        print(f"{winner} wins the pot with {current_bet * num_active_players} chips!")
    else:
        # 如果只剩一位玩家參與，那麼這位玩家就是贏家
        for player in players:
            if player.chips > 0:
                print(f"{player.name} wins the pot with {player.chips * num_active_players} chips!")
                return

if __name__ == "__main__":
    start_game()

