import random
import itertools
from collections import Counter

def monte_carlo_simulation(hole_cards, community_cards, num_simulations=10000):
    wins = 0
    for _ in range(num_simulations):
        random_opponent_hand = random.sample(DECK, 2)
        random_opponent_hand_parse = [parse_card(c) for c in random_opponent_hand]
        best_hand_player, rank_player = find_best_hand(hole_cards, community_cards)
        best_hand_opponent, rank_opponent = find_best_hand(random_opponent_hand_parse, community_cards)
        if rank_player > rank_opponent:
            wins += 1
    return wins * 100 / num_simulations

def parse_card(card_str):
    if len(card_str) == 3:
        return (card_str[:2], card_str[2])
    else:
        return (card_str[0], card_str[1])

def ai_poker_decision(hand_strength, current_bet, min_raise, ai_stack, community_cards):
    if community_cards == []:
        return "Call", current_bet
    if hand_strength < 10:
        return "Fold", 0
    elif 10 <= hand_strength < 30:
        return "Call", current_bet
    elif 30 <= hand_strength <= 50:
        if should_bluff(hand_strength):
            raise_amount = min(ai_stack, current_bet + min_raise)
            return "Raise", raise_amount
        else:
            return "Call", current_bet
    elif 50 < hand_strength <= 90:
        raise_amount = min(ai_stack, current_bet + min_raise)
        return "Raise", raise_amount
    else:
        return "All-in", ai_stack

def generate_possible_hands(hole_cards, community_cards):
    total_cards = hole_cards + community_cards
    possible_hands = list(itertools.combinations(total_cards, 5))
    return possible_hands

HAND_RANKINGS = {
    "High Card": 1,
    "One Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Four of a Kind": 8,
    "Straight Flush": 9,
    "Royal Flush": 10
}

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["H", "D", "C", "S"]
DECK = [rank + suit for rank in RANKS for suit in SUITS]

def evaluate_hand(cards):
    def parse_card(card_str):
        if card_str[:-1] == '10':
            return ('10', card_str[-1])
        else:
            return (card_str[0], card_str[1])
    cards = [parse_card(card) if isinstance(card, str) else card for card in cards]
    RANK_ORDER = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    ranks = sorted([RANK_ORDER[card[0]] for card in cards], reverse=True)
    suits = [card[1] for card in cards]
    rank_counts = Counter(ranks)
    rank_values = sorted(rank_counts.values(), reverse=True)
    is_flush = len(set(suits)) == 1
    is_straight = (max(ranks) - min(ranks) == 4) and (len(set(ranks)) == 5)
    if set(ranks) == {14, 2, 3, 4, 5}:
        is_straight = True
        ranks = [5, 4, 3, 2, 1]
    if is_flush and is_straight:
        return "Royal Flush" if max(ranks) == 14 else "Straight Flush"
    elif rank_values == [4, 1]:
        return "Four of a Kind"
    elif rank_values == [3, 2]:
        return "Full House"
    elif is_flush:
        return "Flush"
    elif is_straight:
        return "Straight"
    elif rank_values == [3, 1, 1]:
        return "Three of a Kind"
    elif rank_values == [2, 2, 1]:
        return "Two Pair"
    elif rank_values == [2, 1, 1, 1]:
        return "One Pair"
    else:
        return "High Card"

def find_best_hand(hole_cards, community_cards):
    possible_hands = generate_possible_hands(hole_cards, community_cards)
    best_hand = None
    best_rank = 1
    for hand in possible_hands:
        hand_rank = HAND_RANKINGS[evaluate_hand(hand)]
        if hand_rank > best_rank:
            best_hand = hand
            best_rank = hand_rank
    return best_hand, best_rank

def ai_poker_strategy(hole_cards, community_cards, current_bet, min_raise, ai_stack, last_raise):
    best_hand, hand_rank = find_best_hand(hole_cards, community_cards)
    hand_strength = monte_carlo_simulation(hole_cards, community_cards)
    action, bet_amount = ai_poker_decision(hand_strength, current_bet, min_raise, ai_stack, community_cards)
    
    # If the action is "Call", ensure the AI calls the correct amount
    if action == "Call":
        bet_amount = last_raise  # Set bet_amount to the last raise amount

    print(f"AI's Best Hand: {best_hand} (Rank: {hand_rank})")
    print(f"Hand Strength: {hand_strength:.2f}%")
    print(f"AI Decision: {action}, Bet: {bet_amount}")
    
    return action, bet_amount


def should_bluff(hand_strength):
    if 30 <= hand_strength <= 50:
        return random.choice([True, False])
    return False

def adjust_strategy(opponent_moves):
    aggressive_moves = opponent_moves.count("Raise")
    passive_moves = opponent_moves.count("Fold")
    if aggressive_moves > passive_moves:
        print("Opponent is aggressive → AI plays more cautiously.")
    elif passive_moves > aggressive_moves:
        print("Opponent is passive → AI plays more aggressively.")

def get_hole_cards():
    while True:
        user_input = input("Enter your two hole cards (e.g., 'AS KH'): ").upper().split()
        if len(user_input) != 2:
            print("Error: Please enter exactly two cards.")
            continue
        card1, card2 = user_input
        if card1 in DECK and card2 in DECK and card1 != card2:
            print(f"Your hole cards are: {card1}, {card2}")
            return [card1, card2]
        else:
            print("Invalid cards! Please enter valid card codes like 'AS KH'.")

def get_flop():
    while True:
        user_input = input("Enter your three flop cards (e.g., '10H 8D 5S'): ").upper().split()
        if len(user_input) != 3:
            print("Error: Please enter exactly three cards.")
            continue
        card1, card2, card3 = user_input
        print(f"Flop cards are: {card1}, {card2}, {card3}")
        if card1 in DECK and card2 in DECK and card3 in DECK and card1 != card2 and card1 != card3 and card3 != card2:
            return [card1, card2, card3]
        else:
            print("Invalid cards! Please enter valid card codes like '10H 8D 5S'.")

def get_turn():
    while True:
        user_input = input("Enter your one turn card (e.g., '7C'): ").upper().split()
        if len(user_input) != 1:
            print("Error: Please enter exactly one card.")
            continue
        card4 = user_input[0]
        if card4 in DECK:
            return [card4]
        else:
            print("Invalid card! Please enter valid card codes like '7C'.")

def get_river():
    while True:
        user_input = input("Enter your one river card (e.g., 'JD'): ").upper().split()
        if len(user_input) != 1:
            print("Error: Please enter exactly one card.")
            continue
        card5 = user_input[0]
        if card5 in DECK:
            return [card5]
        else:
            print("Invalid card! Please enter valid card codes like 'JD'.")

def get_players_and_turn():
    while True:
        try:
            total_players = int(input("Enter number of players (2 to 10): "))
            if 2 <= total_players <= 10:
                break
            else:
                print("Player count must be between 2 and 10.")
        except ValueError:
            print("Invalid number.")

    while True:
        try:
            ai_position = int(input(f"Enter AI's player number (1 to {total_players}, where the dealer is player {total_players}): "))
            if 1 <= ai_position <= total_players:
                break
            else:
                print("Invalid player number.")
        except ValueError:
            print("Invalid input.")

    print(f"AI is Player {ai_position} out of {total_players} players.")
    return total_players, ai_position

def track_opponent_actions(total_players, ai_position, last_raise):
    actions = {}
    for i in range(1, total_players + 1):
        if i == ai_position:

            continue
        while True:
            move = input(f"Enter action for Player {i} (fold/call/raise amount): ").strip().lower()
            if move.startswith("raise"):
                try:
                    amount = int(move.split()[1])
                    actions[f"Player {i}"] = ("Raise", amount)
                    last_raise = max(last_raise, amount)  # Update last raise to the highest
                    break
                except:
                    print("Invalid raise amount. Please enter again.")
            elif move == "call":
                actions[f"Player {i}"] = ("Call", last_raise)  # Match last raise
                break
            elif move == "fold":
                actions[f"Player {i}"] = ("Fold", 0)
                break
            else:
                print("Invalid action. Please enter 'fold', 'call', or 'raise <amount>'.")
    return actions, last_raise

def play_poker_hand(ai_stack, min_raise):
    total_players, ai_position = get_players_and_turn()
    current_bet = 0
    community_cards = []
    hole_cards = get_hole_cards()

    print("-- Pre-Flop Actions --")
    
    last_raise = current_bet  # Initialize last_raise here
    # AI makes its move first
    #ai_action, ai_bet = ai_poker_strategy(hole_cards, community_cards, current_bet, min_raise, ai_stack, last_raise)
    
    # Track actions of opponents, passing the last raise
    opponent_moves, last_raise = track_opponent_actions(total_players, ai_position, last_raise)

    #game_over is wrong in line 255
    ai_stack, game_over, last_raise = betting_round(hole_cards, community_cards, current_bet, min_raise, ai_stack, ai_position, total_players, last_raise)
    if game_over:
        return ai_stack

    community_cards = get_flop()
    print("-- Flop Actions --")
    ai_stack, game_over, last_raise = betting_round(hole_cards, community_cards, current_bet, min_raise, ai_stack, ai_position, total_players, last_raise)
    if game_over:
        return ai_stack

    community_cards += get_turn()
    print("-- Turn Actions --")
    ai_stack, game_over, last_raise = betting_round(hole_cards, community_cards, current_bet, min_raise, ai_stack, ai_position, total_players, last_raise)
    if game_over:
        return ai_stack

    community_cards += get_river()
    print("-- River Actions --")
    ai_stack, game_over, last_raise = betting_round(hole_cards, community_cards, current_bet, min_raise, ai_stack, ai_position, total_players, last_raise)
    if game_over:
        return ai_stack

    while True:
        try:
            pot = int(input("What was the total pot size? "))
            break
        except ValueError:
            print("Please enter a valid number.")

    result = input("Did the AI win the pot? (yes/no): ").strip().lower()
    if result == 'yes':
        ai_stack += pot
        print(f"AI won the pot! New stack: {ai_stack}")
    else:
        print(f"AI lost the pot. Current stack: {ai_stack}")

    return ai_stack



def betting_round(hole_cards, community_cards, current_bet, min_raise, ai_stack, ai_position, total_players, last_raise):
    all_call = False
    game_over = False
    while not all_call:
        # AI makes its action first
        ai_action, ai_bet = ai_poker_strategy(hole_cards, community_cards, current_bet, min_raise, ai_stack, last_raise)
        print(f"AI's Action: {ai_action} with bet {ai_bet}")
        ai_stack -= ai_bet
        current_bet = ai_bet

        # Now, track the actions of other players
        actions, last_raise = track_opponent_actions(total_players, ai_position, current_bet)
        all_call = all(player_action[0] == "Call" for player_action in actions.values())

        if not all_call:
            user_response = input("Is the betting phase over? (yes/no): ").strip().lower()
            if user_response == 'yes':
                all_call = True
            else:
                print("Betting continues to the next player.")
        #ask if game over if yes, gameover = true, else false
    
    return ai_stack, game_over, last_raise


def main():
    ai_stack = 1000
    min_raise = 50
    while ai_stack > 0:
        print(f"\n--- New Poker Hand --- {ai_stack}")
        ai_stack = play_poker_hand(ai_stack, min_raise)
        cont = input("Play another hand? (yes/no): ").strip().lower()
        if cont != 'yes':
            break
    print("Game over. Thanks for playing!")

if __name__ == "__main__":
    main()
