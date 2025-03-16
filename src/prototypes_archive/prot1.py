import random
from collections import Counter

class Card:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.card = f"{rank[0]}{suit[0]}"  # Example: "10C" for 10 of Clubs

    def __repr__(self):
        return self.card  # For easy printing


class Deck:
    def __init__(self, nPacks=1):
        self.listCards = [Card(rank, suit) for _ in range(nPacks) 
                          for rank in Card.ranks for suit in Card.suits]

    def shuffleDeck(self):
        random.shuffle(self.listCards)

    def countUniqueCards(self):
        return Counter(card.card for card in self.listCards)

    def getCardProbability(self, card_name):
        card_counts = self.countUniqueCards()
        return card_counts[card_name] / len(self.listCards) if card_name in card_counts else 0

    def printDeck(self):
        print(self.listCards)

def main():
    # Example Usage
    deck = Deck(2)  # Creates a deck with 2 standard 52-card decks (104 cards total)
    deck.shuffleDeck()  # Shuffle the deck
    deck.printDeck()  # Print shuffled deck

    card_counts = deck.countUniqueCards()
    print(card_counts)  # Output: {'10C': 2, 'KH': 2, ...}

    print(deck.getCardProbability('10C'))  # Probability of drawing '10C'

if __name__ == '__main__':
    main()