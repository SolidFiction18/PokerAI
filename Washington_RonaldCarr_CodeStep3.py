from collections import Counter

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
    
    # Sorting ranks from highest to lowest (Ace is highest)
    RANK_ORDER = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    
    # Extract ranks and suits
    ranks = sorted([RANK_ORDER[card[0]] for card in cards],
    reverse=True)
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
    
# Test Cases
hand1 = [("A", "♠"), ("K", "♠"), ("Q", "♠"), ("J", "♠"), ("10", "♠")]
# Royal Flush
hand2 = [("9", "♦"), ("8", "♦"), ("7", "♦"), ("6", "♦"), ("5", "♦")]
# Straight Flush
hand3 = [("4", "♠"), ("4", "♦"), ("4", "♣"), ("9", "♥"), ("9", "♠")]
# Four of a Kind
hand4 = [("10", "♠"), ("10", "♦"), ("10", "♣"), ("8", "♠"), ("8", "♦")]
# Full House
    
print(evaluate_hand(hand1)) # Royal Flush
print(evaluate_hand(hand2)) # Straight Flush
print(evaluate_hand(hand3)) # Four of a Kind
print(evaluate_hand(hand4)) # Full House