from deckgen import Deck
from sidebet_counter import DeckMap
import numpy as np
import matplotlib.pyplot as plt

def sim():
    n = 8
    N_sim = 1000
    n_pasi = 250

    #ev21_3 = np.zeros((N_sim,n_pasi))
    #evpp = np.zeros((N_sim,n_pasi))
    tcount = np.zeros((N_sim, n_pasi))

    deck = Deck(n)
    for i in range(N_sim):
        deck.shuffleDeck()
        deckmap = DeckMap(n)  # Shuffle for each simulation
        for j in range(n_pasi):
            card = deck.getCardRankSuit(j)
            deckmap.popCard(card[0], card[1])
            #ev21_3[i, j] = deckmap.get21_3ExpectedPayout()
            #evpp[i, j] = deckmap.getPPExpectedPayout()
            tcount[i,j] = deckmap.getTrueCount()

    plt.figure(figsize=(10,6))
    for i in range(N_sim):  # Plot only 10 trajectories
        plt.plot(tcount[i, :], linewidth=1)
    plt.axhline(y=0.00, color='black', linestyle='dotted', linewidth=1)
    plt.grid(True)
    plt.show()

def callmet():
    n=8
    deckmap = DeckMap(n)
    #print(deckmap.getCountsByRankSuit('Ace', 'Clubs'))
    #print(deckmap.get21_3ExpectedPayout())
    #print(deckmap.getCountsByRankSuit('Ace', 'Diamonds'))

def main():
    sim()
if __name__ == '__main__':
    main()