import random
import time
import itertools
from collections import Counter

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
 
def calculate_hand_strength(hand_rank):
    """
    Converts the hand ranking into a percentage strength value.
    
    Parameters:
    hand_rank (int): The rank of the best hand (1-10, where 10 is the best).
    Returns:
    float: Strength percentage (0-100%).
    """
    return (hand_rank / 10) * 100 # Convert rank to a percentage

def should_bluff(hand_strength):
    """ AI decides if it should bluff. """
    if 30 <= hand_strength <= 50:
        return random.choice([True, False]) # Random 50% bluff chance
    return False

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
        return "Call", 0 # Weak hand → Fold
    elif 10 <= hand_strength < 30:
        return "Call", current_bet # Decent hand → Call
    elif 30<= hand_strength<=50:
        if should_bluff(hand_strength):
            raise_amount = min(ai_stack, current_bet + min_raise)
            print({'raise_amount'})
            return "Raise", raise_amount
        else:
            return "Call", current_bet
    elif 50 < hand_strength <= 90:
        raise_amount = min(ai_stack, current_bet + min_raise) # Raise but within stack limits
        print({'raise_amount'})
        return "Raise", raise_amount
    else:
        return "All-in", ai_stack # Best hand → Go all-in!

def update_best_hand_after_river(hole_cards, community_cards):
    """ Recalculate the AI's best possible hand after the River card is revealed. """
    best_hand, hand_rank = find_best_hand(hole_cards, community_cards)
    hand_strength = calculate_hand_strength(hand_rank)
    print(f"Final Best Hand: {best_hand}")
    print(f"Final Hand Strength: {hand_strength:.2f}%")
    return best_hand, hand_rank

class PokerGame:
    def __init__(self, ai_stack=1000, opponent_stack=1000):
        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.ai_stack = ai_stack
        self.opponent_stack = opponent_stack
        self.pot = 10
        self.hole_cards = []
        self.community_cards = []
        self.current_bet = 10
        self.min_raise = 50
        self.opponent_moves = []
    def create_deck(self):
        """Creates a shuffled deck of 52 cards."""
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["H", "D", "C", "S"]
        return [rank + suit for rank in ranks for suit in suits]
    def deal_hole_cards(self):
        """Deals two hole cards to AI."""
        self.hole_cards = [self.deck.pop(), self.deck.pop()]
        print(f"AI Hole Cards: {self.hole_cards}")
    def deal_flop(self):
        """Deals the Flop (three community cards)."""
        self.community_cards = [self.deck.pop(), self.deck.pop(),
        self.deck.pop()]
        print(f"Flop: {self.community_cards}")
    def deal_turn(self):
        """Deals the Turn (fourth community card)."""
        self.community_cards.append(self.deck.pop())
        print(f"Turn: {self.community_cards}")
    def deal_river(self):
        """Deals the River (fifth community card)."""
        self.community_cards.append(self.deck.pop())
        print(f"River: {self.community_cards}")
    def ai_action(self):
        """AI makes a decision based on hand strength."""
        best_hand, hand_strength = update_best_hand_after_river(self.hole_cards, self.community_cards)
        action, bet_amount = ai_poker_decision(hand_strength, self.current_bet, self.min_raise, self.ai_stack)
        print(f"AI Decision: {action}, Bet: {bet_amount}")
        if action == "Fold":
            return False # AI folds and round ends
        else:
            self.pot += bet_amount
            self.ai_stack -= bet_amount
            return True # AI stays in the round
        
    def opponent_action(self):
        """Simulates an opponent's action."""
        action = random.choice(["Call", "Raise", "Fold"])
        self.opponent_moves.append(action)
        if action == "Call":
            print("Opponent Calls")
            self.pot += self.current_bet
            self.opponent_stack -= self.current_bet
        elif action == "Raise":
            raise_amount = self.current_bet + self.min_raise
            print(f"Opponent Raises to {raise_amount}")
            self.pot += raise_amount
            self.opponent_stack -= raise_amount
            self.current_bet = raise_amount
        else:
            print("Opponent Folds")
            return False # Opponent folds and AI wins pot
        return True # Opponent stays in the round
    def showdown(self):
        """Determines the winner based on final hands."""
        ai_best_hand, ai_hand_rank = update_best_hand_after_river(self.hole_cards, self.community_cards)
        opponent_hand = [random.choice(self.deck[:5]),random.choice(self.deck[:5])] # Simulated opponent hand
        print(f"{opponent_hand}")
        opponent_best_hand, opponent_hand_rank = find_best_hand(opponent_hand, self.community_cards) # Simulated hand ranking
        print(f"AI Final Hand: {ai_best_hand} (Rank: {ai_hand_rank})")
        print(f"Opponent Hand: {opponent_best_hand} (Rank: {opponent_hand_rank})")
        if ai_hand_rank > opponent_hand_rank:
            print("AI Wins the Round!")
            self.ai_stack += self.pot
        else:
            print("Opponent Wins the Round!")
            self.opponent_stack += self.pot
    def play_round(self):
        """Plays a full round of Texas Hold’em."""
        print("\n--- New Poker Round ---")
        self.deal_hole_cards()
        if not self.ai_action():
            print("AI Folded. Round Over.")
            return
        elif not self.opponent_action():
            print("Opponent Folded. Round Over.")
            return
        self.deal_flop()
        if not self.ai_action():
            print("AI Folded. Round Over.")
            return
        elif not self.opponent_action():
            print("Opponent Folded. Round Over.")
            return
        self.deal_turn()
        if not self.ai_action():
            print("AI Folded. Round Over.")
            return
        elif not self.opponent_action():
            print("Opponent Folded. Round Over.")
            return
        self.deal_river()
        if not self.ai_action():
            print("AI Folded. Round Over.")
            return
        elif not self.opponent_action():
            print("Opponent Folded. Round Over.")
            return
        self.showdown()
        
def log_game_data(hole_cards, community_cards, action, hand_strength, result):
    """ Logs poker game data for analysis. """
    with open("poker_game_log.txt", "a") as log_file:
        log_file.write(f"Hole Cards: {hole_cards}\n")
        log_file.write(f"Community Cards: {community_cards}\n")
        log_file.write(f"AI Action: {action}\n")
        log_file.write(f"Hand Strength: {hand_strength:.2f}%\n")
        log_file.write(f"Result: {result}\n")
        log_file.write("-" * 30 + "\n")
 
# Start a game

poker_game = PokerGame()
poker_game.play_round()
log_game_data(["AS", "KH"], ["10H", "8D", "5S", "JD", "3C"], "Raise", 80.0, "AI Wins")
