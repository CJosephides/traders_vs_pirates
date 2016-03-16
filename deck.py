"""
deck.py

The Deck class.
"""

import numpy as np

class Deck:
    """
    A deck of cards. Initialization creates a new deck.
    """

    def __init__(self):
        self.deck = []
        for t in ('i', 's', 'p'):
            for i in range(1, 11):
                self.deck.append(t + str(i))

    def deal_card(self):
        # Pick card.
        card = np.random.choice(self.deck, replace=False)
        # Remove from deck.
        self.deck.remove(card)
        # Return.
        return card




        
