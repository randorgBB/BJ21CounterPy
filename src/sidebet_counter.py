import numpy as np
import math

class DeckMap:

    # Useful global data
    #global suits, ranks, values, colour
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    colour = ['Red', 'Red', 'Black', 'Black']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    values = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11])
    # Combination Lambda Methods for easy access and use
    #global comb_vec2, comb_vec3
    comb_vec2 = np.vectorize(lambda x: math.comb(x, 2) if x >= 2 else 0)
    comb_vec3 = np.vectorize(lambda x: math.comb(x, 3) if x >= 3 else 0)
    # Constructor and initialising variables
    def __init__(self, nPacks):
        self.initPacks = nPacks
        self.initCards = nPacks * 52
        self.marray = np.empty((len(self.ranks), len(self.suits), 5), dtype=object)
        for i, rank in enumerate(self.ranks):
            for j, suit in enumerate(self.suits):
                self.marray[i, j] = [rank, suit, int(self.values[i]), nPacks, self.colour[j]]  # Initialize
        self.initMean = self.getMeanValue()
        self.nCards = self.getTotalNCards()
        self.nPacks = self.getTotalNDecks()

    # Deck/Shoe statistics Methods
    def getTotalNCards(self):
        return np.sum(self.marray[:,:,3])
    def getTotalNDecks(self):
        return np.sum(self.marray[:,:,3])/52
    def getMeanValue(self):
        # Calculate weighted mean value considering marray[:,:,3] as the number of cards
        total_value = np.sum(self.marray[:,:,2] * self.marray[:,:,3])  # Sum of value * count
        total_cards = np.sum(self.marray[:,:,3])  # Total number of cards
        return total_value / total_cards if total_cards > 0 else 0
    def getRunningCount(self):
        highCards_mask = self.marray[:, :, 2] >= 10  # Compare rank (marray[:, :, 0] corresponds to ranks)
        lowCards_mask = self.marray[:, :, 2] <= 6
        sum = np.sum(self.marray[highCards_mask,3]) - np.sum(self.marray[lowCards_mask,3])
        return sum
    def getTrueCount(self):
        return self.getRunningCount()/self.getTotalNDecks()
    def getNTotalCombinations(self, a):
        return math.comb(self.getTotalNCards(),a)

    # Utility Methods 0
    def printDeckMap(self):
        print(self.marray)
        #print('Initial Mean Value(', self.nCards * 52 ,'cards):', self.initMean)

    def popCard(self,a,b, prnt = False):
        rank_mask = self.marray[:, :, 0] == a  # Compare rank (marray[:, :, 0] corresponds to ranks)
        suit_mask = self.marray[:, :, 1] == b  # Compare suit (marray[:, :, 1] corresponds to suits)
        combined_mask = rank_mask & suit_mask
        if(self.marray[combined_mask, 3] > 0):
            self.marray[combined_mask, 3] -= 1
        else:
            raise Exception("Count cannot be lower than 0")
        if(prnt == True):
            print(self.marray[combined_mask])
    
    # Utility Methods 1:
    # Colour Methods: 
    def getCountsByRankColour(self, a, b):
        rank_mask = self.marray[:, :, 0] == a  # Compare rank (marray[:, :, 0] corresponds to ranks)
        colour_mask = self.marray[:, :, 4] == b
        combined_mask = rank_mask & colour_mask
        return self.marray[combined_mask]
    def getCountsByColours(self, b):
        sums = []
        for a in self.ranks:
            arr = self.getCountsByRankColour(a,b)
            sums.append(np.sum(arr[:,3]))
        return sums
    
    # Rank Methods:
    def getCountsByRanks(self):
        sums = []
        for a in self.ranks:
            rank_mask = self.marray[:, :, 0] == a
            sums.append(np.sum(self.marray[rank_mask,3]))
        return sums
    def getCountByRank(self, a):
        rank_mask = self.marray[:, :, 0] == a
        return np.sum(self.marray[rank_mask,3])
    
    # Suits Methods:
    def getCountsByRankSuit(self, a, b):
        rank_mask = self.marray[:, :, 0] == a  # Compare rank (marray[:, :, 0] corresponds to ranks)
        suit_mask = self.marray[:, :, 1] == b
        combined_mask = rank_mask & suit_mask
        return self.marray[combined_mask,3][0]

    def getCountsBySuits(self):
        sums = []
        for b in self.suits:
            suit_mask = self.marray[:,:,1] == b
            sums.append(np.sum(self.marray[suit_mask,3]))
        return sums

    # Calcul No. SideBet Perfect Pairs (x25, x12, x6)
    def getNPerfectPair(self):
        return np.sum(self.comb_vec2(self.marray[:,:,3]))
    def getNColouredPair(self):
        reds_arr = self.getCountsByColours('Red')
        blacks_arr = self.getCountsByColours('Black')
        return np.sum(self.comb_vec2(reds_arr)) + np.sum(self.comb_vec2(blacks_arr)) - self.getNPerfectPair()
    def getNMixedPair(self):
        sums = self.getCountsByRanks()
        return np.sum(self.comb_vec2(sums)) - self.getNColouredPair() - self.getNPerfectPair()
    def getNonPairLoser(self):
        return self.getNTotalCombinations(2) - (self.getNPerfectPair() + self.getNColouredPair() + self.getNMixedPair())
    def getPPExpectedPayout(self):
        payouts = [25,12,6,-1]
        return (self.getNPerfectPair() * payouts[0] + self.getNColouredPair() * payouts[1] + self.getNMixedPair() * payouts[2] + self.getNonPairLoser() * payouts[3])/self.getNTotalCombinations(2)

    # Calcul No. SideBet 21+3 (x100, x40, x25, x10, x5)
    def getNSuited3Kind(self):
        return np.sum(self.comb_vec3(self.marray[:,:,3]))
    def getNStraightFlush(self):
        sumval = 0
        for b in self.suits:
            sumval+= self.getCountsByRankSuit('Ace',b) * self.getCountsByRankSuit('2',b) * self.getCountsByRankSuit('3',b)
            for a in range(len(self.ranks)-2):
                sumval+= self.getCountsByRankSuit(self.ranks[a],b) * self.getCountsByRankSuit(self.ranks[a+1],b) * self.getCountsByRankSuit(self.ranks[a+2],b)
        return sumval
    def getNMixed3Kind(self):
        sums = self.getCountsByRanks()
        return np.sum(self.comb_vec3(sums)) - self.getNSuited3Kind()
    def getNStraight(self):
        sumval = self.getCountByRank('Ace') * self.getCountByRank('2') * self.getCountByRank('3')
        for a in range(len(self.ranks)-2):
            sumval+= self.getCountByRank(self.ranks[a]) * self.getCountByRank(self.ranks[a+1]) * self.getCountByRank(self.ranks[a+2])
        return sumval - self.getNStraightFlush()
    def getNFlush(self):
        sums = self.getCountsBySuits()
        return np.sum(self.comb_vec3(sums)) - self.getNSuited3Kind() - self.getNStraightFlush()
    def getNon21_3Loser(self):
        return self.getNTotalCombinations(3) - (self.getNSuited3Kind() + self.getNStraightFlush() + self.getNMixed3Kind() + self.getNStraight() + self.getNFlush())
    def get21_3ExpectedPayout(self):
        payouts = [100,40,25,10,5,-1]
        return (self.getNSuited3Kind()*payouts[0] + self.getNStraightFlush()*payouts[1] + self.getNMixed3Kind()*payouts[2] + self.getNStraight()*payouts[3] + self.getNFlush()*payouts[4] + self.getNon21_3Loser() * payouts[5])/self.getNTotalCombinations(3)

    def printAllCals(self):
        #print(20*'-')
        #print("Cards: ",self.getTotalNCards())
        #print('Decks: ', self.getTotalNDecks())
        #print("Mean Value: ", self.getMeanValue())
        #print("Running Count: ",self.getRunningCount())
        #print('True Count: ', self.getTrueCount())
        #print(20*'-')
        # PP Sidebet payout calculations
        #print('Perfect Pair: ', self.getNPerfectPair())#/deckmap.getNTotalCombinations(2))
        #print('Coloured Pair: ', self.getNColouredPair())#/deckmap.getNTotalCombinations(2))
        #print('Mixed Pair: ', self.getNMixedPair())#/deckmap.getNTotalCombinations(2))
        #print('No Pair(Loser hand): ', self.getNonPairLoser())
        print('Expected PP payout: ', self.getPPExpectedPayout())

        print(20*'-')
        # 21+3 Sidebet payout calculations
        #print('Suited three of a kind: ', self.getNSuited3Kind())#/deckmap.getNTotalCombinations(3))
        #print('Straight flush: ', self.getNStraightFlush())#/deckmap.getNTotalCombinations(3))
        #print('Three of a kind: ', self.getNMixed3Kind())#/deckmap.getNTotalCombinations(3))
        #print('Straight: ' , self.getNStraight())#/deckmap.getNTotalCombinations(3))
        #print('Flush: ', self.getNFlush())#/deckmap.getNTotalCombinations(3))
        #print('No 21+3(Loser hand): ', self.getNon21_3Loser())
        print('Expected 21+3 payout: ', self.get21_3ExpectedPayout())
        print("\n")
        #print("Cards: ",self.getTotalNCards())

# Real Time manual counter
def outputStats():
    n = 8
    deckmap = DeckMap(n)
    while True:
        deckmap.printAllCalcs()
        rank = input("Enter card rank (or 'exit' to stop): ")
        if rank.lower() == 'exit':
            break
        suit = input("Enter card suit: ")
        
        card = deckmap.popCard(rank, suit)  # Calling the method with input values
        print(f"Popped card: {card}")

