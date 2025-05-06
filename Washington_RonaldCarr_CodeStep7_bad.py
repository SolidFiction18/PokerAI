import random
import itertools
from collections import Counter
'''
def calculate_hand_strength(hand_rank):
    """
    Converts the hand ranking into a percentage strength value.
    
    Parameters:
    hand_rank (int): The rank of the best hand (1-10, where 10 is the best).
    Returns:
    float: Strength percentage (0-100%).
    """
    return (hand_rank / 10) * 100 # Convert rank to a percentage
'''
def monte_carlo_simulation(hole_cards, community_cards, num_simulations=10000):
    """ Simulates poker rounds to estimate the probability of having the
    best hand. """
    wins = 0
    
    for _ in range(num_simulations):
        random_opponent_hand = random.sample(DECK, 2) # Simulate an opponent
        random_opponent_hand_parse = [parse_card(c) for c in random_opponent_hand]
        best_hand_player, rank_player = find_best_hand(hole_cards, community_cards)
        best_hand_opponent, rank_opponent = find_best_hand(random_opponent_hand_parse, community_cards)
        if rank_player > rank_opponent:
            wins += 1
    return wins*100 / num_simulations

def parse_card(card_str):
    """Converts a string like '10H' into a tuple ('10', 'H')"""
    if len(card_str) == 3:
        return (card_str[:2], card_str[2])
    else:
        return (card_str[0], card_str[1])

def ai_poker_decision(hand_strength, current_bet, min_raise, ai_stack, community_cards):
    """
    Determines the AI's action in a poker game based on hand strength.
    Parameters:
    hand_strength (float): The AI's hand strength percentage (0-100%).
    current_bet (int): The current bet required to call.
    min_raise (int): The minimum amount required to raise.
    ai_stack (int): The AI's remaining chips.
    Returns:
    str: The action chosen ("Fold", "Call", "Raise", "All-in").
    int: The amount of chips to bet (if applicable).
    """
    if community_cards == []:
        return "Call", current_bet
    
    if hand_strength < 10:
        return "Fold", 0 # Weak hand → Fold
    elif 10 <= hand_strength < 30:
        return "Call", current_bet # Decent hand → Call
    elif 30<= hand_strength<=50:
        if should_bluff(hand_strength):
            raise_amount = min(ai_stack, current_bet + min_raise)
            return "Raise", raise_amount
        else:
            return "Call", current_bet
    elif 50 < hand_strength <= 90:
        raise_amount = min(ai_stack, current_bet + min_raise) # Raise but within stack limits
        return "Raise", raise_amount
    else:
        return "All-in", ai_stack # Best hand → Go all-in!

def generate_possible_hands(hole_cards, community_cards):
    """
    Generates all possible 5-card hands using the player's hole cards
    and the community cards.
    Parameters:
    hole_cards (list): List of 2 player cards (e.g., ["AS", "KH"]).
    community_cards (list): List of 3-5 community cards (e.g., ["10H",
    "8D", "5S"]).
    Returns:
    list: All possible 5-card hands.
    """
    total_cards = hole_cards + community_cards
    possible_hands = list(itertools.combinations(total_cards, 5)) #Generate all 5-card hands
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
SUITS = ["H", "D", "C", "S"] # Hearts, Diamonds, Clubs, Spades
# Generate all possible cards
DECK = [rank + suit for rank in RANKS for suit in SUITS]

def evaluate_hand(cards):
    """
    Evaluates a 5-card poker hand and returns its rank as a string.
    
    Parameters:
    cards (list): A list of tuples [(rank, suit), ...] representing a
    poker hand.
    Example: [("A", "♠"), ("K", "♠"), ("Q", "♠"), ("J",
    "♠"), ("10", "♠")]
    Returns:
    str: The name of the poker hand.
    """
    
    def parse_card(card_str):
        if card_str[:-1] == '10':
            return ('10', card_str[-1])
        else:
            return (card_str[0], card_str[1])

    # In evaluate_hand:
    cards = [parse_card(card) if isinstance(card, str) else card for card in cards]
    
    # Sorting ranks from highest to lowest (Ace is highest)
    RANK_ORDER = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    
    # Extract ranks and suits
    ranks = sorted([RANK_ORDER[card[0]] for card in cards], reverse=True)
    suits = [card[1] for card in cards]
    
    # Count occurrences of each rank
    rank_counts = Counter(ranks)
    rank_values = sorted(rank_counts.values(), reverse=True)
    
     # Most common first
    # Check for Flush (all suits same)
    is_flush = len(set(suits)) == 1
    
    # Check for Straight (consecutive numbers)
    is_straight = (max(ranks) - min(ranks) == 4) and (len(set(ranks)) == 5)
    
    # Special case: Ace-low straight (A-2-3-4-5)
    if set(ranks) == {14, 2, 3, 4, 5}:
        is_straight = True
        ranks = [5, 4, 3, 2, 1] # Ace is treated as low
    
    # Identify hand type
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
     """
     Determines the strongest possible hand from all 5-card combinations.
     Parameters:
     hole_cards (list): Player's two hole cards.
     community_cards (list): Community cards on the table.
     Returns:
     tuple: The best hand and its ranking.
     """
     possible_hands = generate_possible_hands(hole_cards, community_cards)
     best_hand = None
     best_rank = 1
     for hand in possible_hands:
         hand_rank = HAND_RANKINGS[evaluate_hand(hand)] # Get ranking value
         if hand_rank > best_rank:
             best_hand = hand
             best_rank = hand_rank
     return best_hand, best_rank

def ai_poker_strategy(hole_cards, community_cards, current_bet, min_raise,ai_stack):
    """
    The AI's complete poker decision-making process.
    Parameters:
    hole_cards (list): Player's two hole cards.
    community_cards (list): Community cards on the table.
    current_bet (int): The current bet required to call.
    min_raise (int): The minimum amount required to raise.
    ai_stack (int): The AI's remaining chips.
    Returns:
    str, int: The action chosen and the bet amount.
    """
    # Find the best hand
    best_hand, hand_rank = find_best_hand(hole_cards, community_cards)
    # Convert hand rank to strength percentage
    hand_strength = monte_carlo_simulation(hole_cards, community_cards)
    #print(hand_strength)
    # Make a decision
    action, bet_amount = ai_poker_decision(hand_strength, current_bet,min_raise, ai_stack, community_cards)
    print(f"AI's Best Hand: {best_hand} (Rank: {hand_rank})")
    print(f"Hand Strength: {hand_strength:.2f}%")
    print(f"AI Decision: {action}, Bet: {bet_amount}")
    return action, bet_amount

def should_bluff(hand_strength):
    """ AI decides if it should bluff. """
    if 30 <= hand_strength <= 50:
        return random.choice([True, False]) # Random 50% bluff chance
    return False

def adjust_strategy(opponent_moves):
    """
    Modifies AI's strategy based on opponent behavior.
    
    opponent_moves (list): History of opponent actions ("Raise", "Call", "Fold").
    """
    aggressive_moves = opponent_moves.count("Raise")
    passive_moves = opponent_moves.count("Fold")
    if aggressive_moves > passive_moves:
        print("Opponent is aggressive → AI plays more cautiously.")
    elif passive_moves > aggressive_moves:
        print("Opponent is passive → AI plays more aggressively.")

def get_hole_cards():
    """
    Prompts the user to manually enter their two hole cards.
    Guarantees the input is valid and returns the selected cards.
    """
    while True:
        # Ask user for input
        user_input = input("Enter your two hole cards (e.g., 'AS KH'):").upper().split()
        # Validate input
        if len(user_input) != 2:
            print("Error: Please enter exactly two cards.")
            continue
        card1, card2 = user_input
        if card1 in DECK and card2 in DECK and card1 != card2:
            print(f"Your hole cards are: {card1}, {card2}")
            return [card1, card2] # Store the hole cards
        else:
            print("Invalid cards! Please enter valid card codes like 'AS KH'.")

def get_flop():
    """
    Prompts the user to manually enter their two hole cards.
    Guarantees the input is valid and returns the selected cards.
    """
    while True:
        # Ask user for input
        user_input = input("Enter your three flop cards (e.g., 'AS KH'):").upper().split()
        # Validate input
        if len(user_input) != 3:
            print("Error: Please enter exactly three cards.")
            continue
        card1, card2, card3 = user_input
        print(f"Flop cards are: {card1}, {card2}, {card3}")
        if card1 in DECK and card2 in DECK and card3 in DECK and card1 != card2 and card1 != card3 and card3 != card2:
            return [card1, card2, card3] # Store the hole cards
        else:
            print("Invalid cards! Please enter valid card codes like 'AS KH'.")
def get_turn():
    """
    Prompts the user to manually enter their two hole cards.
    Guarantees the input is valid and returns the selected cards.
    """
    while True:
        # Ask user for input
        user_input = input("Enter your one turn card (e.g., 'AS KH'):").upper().split()
        # Validate input
        if len(user_input) != 1:
            print("Error: Please enter exactly one card.")
            continue
        card4 = user_input[0]
        if card4 in DECK:
            return [card4] # Store the hole cards
        else:
            print("Invalid card! Please enter valid card codes like 'AS KH'.")
def get_river():
    """
    Prompts the user to manually enter their two hole cards.
    Guarantees the input is valid and returns the selected cards.
    """
    while True:
        # Ask user for input
        user_input = input("Enter your one river card (e.g., 'AS KH'):").upper().split()
        # Validate input
        if len(user_input) != 1:
            print("Error: Please enter exactly one card.")
            continue
        card5 = user_input[0]
        if card5 in DECK:
            return [card5] # Store the hole cards
        else:
            print("Invalid card! Please enter valid card codes like 'AS KH'.")
            
def betting_round(hole_cards, community_cards, current_bet, min_raise, ai_stack):
    all_call = False
    while not all_call:
        action, bet = ai_poker_strategy(hole_cards, community_cards, current_bet, min_raise, ai_stack)
        if action != "Fold":
            ai_stack -= bet
        else:
            print("AI folded. Ending hand.")
            return ai_stack, True  # True means game is over
        try:
            current_bet = int(input("Enter current bet this round: "))
        except ValueError:
            print("Invalid input. Using previous bet value.")
        user_response = input("Has everyone called or folded? (yes/no): ").strip().lower()
        if user_response == 'yes':
            all_call = True
    print(ai_stack)
    return ai_stack, False  # False means continue game

def play_poker_hand(ai_stack, min_raise):
    current_bet = 0
    community_cards = []
    hole_cards = get_hole_cards()

    # Pre-flop
    ai_stack, game_over = betting_round(hole_cards, community_cards, current_bet, min_raise, ai_stack)
    if game_over:
        return ai_stack

    # Flop
    community_cards = get_flop()
    ai_stack, game_over = betting_round(hole_cards, community_cards, current_bet, min_raise, ai_stack)
    if game_over:
        return ai_stack

    # Turn
    community_cards += get_turn()
    ai_stack, game_over = betting_round(hole_cards, community_cards, current_bet, min_raise, ai_stack)
    if game_over:
        return ai_stack

    # River
    community_cards += get_river()
    ai_stack, game_over = betting_round(hole_cards, community_cards, current_bet, min_raise, ai_stack)
    if game_over:
        return ai_stack

    # End of hand — ask for result and update stack
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

def main():
    ai_stack = 1000
    min_raise = 50
    
    while ai_stack > 0:
        print(f"\n--- New Poker Hand ---")
        ai_stack = play_poker_hand(ai_stack, min_raise)
        
        cont = input("Play another hand? (yes/no): ").strip().lower()
        if cont != 'yes':
            break
    
    print("Game over. Thanks for playing!")

if __name__ == "__main__":
    main()