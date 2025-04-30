import random
import itertools
from collections import Counter

def calculate_hand_strength(hand_rank):
    """
    Converts the hand ranking into a percentage strength value.
    
    Parameters:
    hand_rank (int): The rank of the best hand (1-10, where 10 is the best).
    Returns:
    float: Strength percentage (0-100%).
    """
    return (hand_rank / 10) * 100 # Convert rank to a percentage

def ai_poker_decision(hand_strength, current_bet, min_raise, ai_stack):
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
     best_rank = 0
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
    hand_strength = calculate_hand_strength(hand_rank)
    # Make a decision
    action, bet_amount = ai_poker_decision(hand_strength, current_bet,min_raise, ai_stack)
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

# Example Usage
hole_cards = ["AS", "KH"]
community_cards = ["QH", "8D", "8S","8D", "3C"]
current_bet = 100
min_raise = 50
ai_stack = 1000
ai_poker_strategy(hole_cards, community_cards, current_bet, min_raise, ai_stack)
