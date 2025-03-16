import random

class Card:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

    def __init__(self, rank_index, suit_index):
        self.value = self.values[rank_index]
        self.suit = self.suits[suit_index]
        self.rank = self.ranks[rank_index]
        self.name = f"{self.ranks[rank_index]} of {self.suits[suit_index]}"

    def printCard(self):
        print(self.value, self.suit, self.name)

class Deck:
    def __init__(self, nPacks):
        self.nInitCards = nPacks * 52
        self.listCards = [Card(i, j) for _ in range(nPacks) for i in range(13) for j in range(4)]

    # Shuffle Method
    def shuffleDeck(self):
        random.shuffle(self.listCards)
    
    def getCardRank(self, i):
        card = self.listCards[i]
        return card.rank
    def getCardSuit(self, i):
        card = self.listCards[i]
        return card.suit
    def getCardRankSuit(self, i):
        data = [self.getCardRank(i), self.getCardSuit(i)]
        return data
