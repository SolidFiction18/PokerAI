# Define a standard deck of 52 cards
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["H", "D", "C", "S"] # Hearts, Diamonds, Clubs, Spades
# Generate all possible cards
DECK = [rank + suit for rank in RANKS for suit in SUITS]
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
# Run the function
hole_cards = get_hole_cards()
