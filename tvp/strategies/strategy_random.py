"""
strategy_random.py

author: Christos
date: 17/03/2016
description: always play a random card
"""

import random

class Strategy_Random:

    def __init__(self):
        self.name = 'random'

    def play(self, states, active_player):
        r = random.randint(0, len(active_player.hand)-1)  # includes both ends
        action = active_player.hand[r]
        return action
