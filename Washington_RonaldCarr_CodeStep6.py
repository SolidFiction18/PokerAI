# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 19:04:26 2025

@author: rccarr
"""
import random
import itertools
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
    
def parse_card(card_str):
    """Converts a string like '10H' into a tuple ('10', 'H')"""
    if len(card_str) == 3:
        return (card_str[:2], card_str[2])
    else:
        return (card_str[0], card_str[1])
    
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
 
def rank_all_possible_hands(hole_cards, community_cards):
    """
    Sorts all possible hands by strength from strongest to weakest.
    Returns:
    list: Ranked list of all possible hands.
    """
    possible_hands = generate_possible_hands(hole_cards, community_cards)
    ranked_hands = sorted(possible_hands, key=lambda x:
    HAND_RANKINGS[evaluate_hand(x)], reverse=True)
    return ranked_hands


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
    return wins / num_simulations

# Example usage
hole_cards = [parse_card(c) for c in ["AS", "KS"]]
community_cards = [parse_card(c) for c in ["10S", "QD", "QS", "JS", "QC"]]
#hole_cards = ["AS", "KS"]
#community_cards = ["10S", "QD", "QS", "JS", "QC"]
best_hand, best_rank = find_best_hand(hole_cards, community_cards)
print("Best Hand:", best_hand)
print("Hand Rank:", best_rank)
ranked_hands = rank_all_possible_hands(hole_cards, community_cards)
#for hand in ranked_hands:
    #print(hand, "->", evaluate_hand(hand))
win_probability = monte_carlo_simulation(hole_cards, community_cards)
print(f"Winning Probability: {win_probability:.2%}")